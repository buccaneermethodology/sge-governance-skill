#!/usr/bin/env python3
"""Build the retained Semx-specific TCO compatibility view.

Deprecated for new generic KYM/TCO authoring. Use the independent kym-tco
project for new products. This module remains authoritative for existing Semx
RCP/SAG compatibility outputs until a separately approved removal migration.

TCO means Testing Coverage Outline here: a feature coverage outline for
Business Rules. Each implementable module (M) is modeled with TSP:
Topic, Scope, Purpose. Source notes, current implementation status, claim
ceilings, and repo-state observations stay in Ref Info.
"""

from __future__ import annotations

import argparse
import html
import importlib.util
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_SOURCE = Path("semx-kb/bm-doc/KYM/4. RCP+SAG KYM.md")
DEFAULT_MODEL = Path(__file__).resolve().with_name("kym_business_rules_tco_model.json")
DEFAULT_COVERAGE_MODEL = Path(__file__).resolve().with_name("kym_business_rules_tco_coverage_model.json")
DEFAULT_OUTPUT_DIR = Path(".semx/latest/visualization")
SECTION_TITLE = "Business Rules"
BULLET_RE = re.compile(r"^(?P<indent>\s*)-\s+(?P<text>.*\S)?\s*$")
COVERAGE_STATES = (
    "unknown",
    "not_started",
    "design_only",
    "schema_validator",
    "test_bound",
    "bounded_runtime",
    "integrated_runtime",
)
DEFAULT_CAPABILITY_TARGET_STATE = "bounded_runtime"
DEFAULT_POLICY_TARGET_STATE = "test_bound"
NODE_KINDS = {"group", "capability", "policy"}
NODE_KIND_LABELS = {
    "group": "功能域",
    "capability": "能力",
    "policy": "规则",
}
COVERAGE_STATE_LABELS = {
    "unknown": "未知",
    "not_started": "未开始",
    "design_only": "设计/合同",
    "schema_validator": "Schema/Validator",
    "test_bound": "测试边界",
    "bounded_runtime": "有界 Runtime",
    "integrated_runtime": "集成 Runtime",
}
EVIDENCE_KINDS = {
    "code",
    "schema",
    "test",
    "bdd",
    "dashboard",
    "kb",
    "command",
    "candidate_evidence",
}
PATH_EVIDENCE_KINDS = {"code", "schema", "test", "bdd", "dashboard", "kb"}
COUNTED_EVIDENCE_KINDS = EVIDENCE_KINDS - {"candidate_evidence"}
VERIFICATION_TIMEOUT_SECONDS = 300
FORBIDDEN_TSP_STATUS_PHRASES = {
    "当前 Repo",
    "当前 repo",
    "当前已经",
    "当前可通过",
    "当前没有",
    "尚无",
    "不代表",
    "claim ceiling",
    "Claim ceiling",
    "不能冒充",
    "不能据此断言",
    "不是已获批准",
}
FORBIDDEN_GENERATED_PHRASES = {
    "作为父节点范围内的聚合节点",
    "补足该层级的可查看内容",
    "未显式给出 Scope",
    "包含子节点：",
}


@dataclass
class BulletNode:
    title: str
    line: int
    indent: int
    children: list["BulletNode"] = field(default_factory=list)


@dataclass
class RefInfo:
    line: int
    text: str

    def to_dict(self) -> dict[str, Any]:
        return {"line": self.line, "text": self.text}


@dataclass
class TcoNode:
    node_id: str
    node_kind: str
    title: str
    topic: str
    scope: list[str]
    purpose: str
    ref_info: list[RefInfo]
    children: list["TcoNode"] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.node_id,
            "node_kind": self.node_kind,
            "title": self.title,
            "topic": self.topic,
            "ref_info": [ref.to_dict() for ref in self.ref_info],
            "scope": self.scope,
            "purpose": self.purpose,
            "children": [child.to_dict() for child in self.children],
        }


@dataclass
class CoverageBuild:
    root: dict[str, Any]
    nodes: list[dict[str, Any]]
    warnings: list[str]
    verification_results: dict[str, Any]
    target_profiles: list[dict[str, Any]]
    verify_requested: bool
    model_path: Path


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalized_key(value: str) -> str:
    return normalize_text(value).casefold()


def extract_section_lines(markdown: str, section_title: str) -> tuple[int, list[tuple[int, str]]]:
    lines = markdown.splitlines()
    start_index: int | None = None
    start_indent: int | None = None

    for index, line in enumerate(lines):
        match = BULLET_RE.match(line)
        if not match:
            continue
        if normalize_text(match.group("text") or "") == section_title:
            start_index = index
            start_indent = len(match.group("indent"))
            break

    if start_index is None or start_indent is None:
        raise ValueError(f"未找到 section: {section_title}")

    selected: list[tuple[int, str]] = []
    for index in range(start_index, len(lines)):
        line = lines[index]
        match = BULLET_RE.match(line)
        if index > start_index and match and len(match.group("indent")) <= start_indent:
            break
        selected.append((index + 1, line))
    return start_index + 1, selected


def parse_bullets(section_lines: list[tuple[int, str]]) -> BulletNode:
    root: BulletNode | None = None
    stack: list[BulletNode] = []

    for line_no, line in section_lines:
        match = BULLET_RE.match(line)
        if not match:
            continue
        title = normalize_text(match.group("text") or "")
        if not title:
            continue
        node = BulletNode(title=title, line=line_no, indent=len(match.group("indent")))
        while stack and stack[-1].indent >= node.indent:
            stack.pop()
        if stack:
            stack[-1].children.append(node)
        else:
            root = node
        stack.append(node)

    if root is None:
        raise ValueError("section 中没有可解析的 bullet")
    return root


def flatten_text(node: BulletNode, max_depth: int = 3, depth: int = 0) -> list[str]:
    parts = [node.title]
    if depth >= max_depth:
        return parts
    for child in node.children:
        parts.extend(flatten_text(child, max_depth=max_depth, depth=depth + 1))
    return parts


def index_bullets(root: BulletNode) -> dict[str, list[BulletNode]]:
    index: dict[str, list[BulletNode]] = {}

    def visit(node: BulletNode) -> None:
        index.setdefault(normalized_key(node.title), []).append(node)
        for child in node.children:
            visit(child)

    visit(root)
    return index


def load_model(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "semx.visualization.tco_model.v1":
        raise ValueError(f"不支持的 TCO model schema: {data.get('schema')}")
    errors: list[str] = []
    seen_ids: set[str] = set()
    for index, node in enumerate(data.get("nodes", []), start=1):
        node_id = node.get("id")
        if not node_id:
            errors.append(f"nodes[{index}] 缺少 id")
            continue
        if node_id in seen_ids:
            errors.append(f"TCO model 重复定义 node id: {node_id}")
        seen_ids.add(node_id)
        node_kind = node.get("node_kind")
        if node_kind not in NODE_KINDS:
            errors.append(f"{node_id} 缺少或使用了非法 node_kind: {node_kind}")
    root_id = data.get("root")
    if root_id not in seen_ids:
        errors.append(f"root 指向不存在的 node id: {root_id}")
    for node in data.get("nodes", []):
        for child_id in node.get("children", []):
            if child_id not in seen_ids:
                errors.append(f"{node.get('id', '<missing-id>')} 引用了不存在的 child id: {child_id}")
    seen_profile_ids: set[str] = set()
    for profile in data.get("target_profiles", []):
        profile_id = profile.get("id")
        if not profile_id or profile_id in seen_profile_ids:
            errors.append(f"target profile 缺少或重复 id: {profile_id}")
            continue
        seen_profile_ids.add(profile_id)
        for root_id in profile.get("root_ids", []):
            if root_id not in seen_ids:
                errors.append(f"target profile {profile_id} 引用了不存在的 root id: {root_id}")
        for requirement in profile.get("requirements", []):
            requirement_id = requirement.get("id", "<missing-id>")
            for node_id in requirement.get("node_ids", []):
                if node_id not in seen_ids:
                    errors.append(
                        f"target profile {profile_id}/{requirement_id} 引用了不存在的 node id: {node_id}"
                    )
            target_state = requirement.get("target_coverage_state")
            if target_state not in COVERAGE_STATES:
                errors.append(
                    f"target profile {profile_id}/{requirement_id} 使用非法 target state: {target_state}"
                )
    if errors:
        raise ValueError("TCO model 校验失败:\n- " + "\n- ".join(errors))
    return data


def collect_ref_info(
    node_spec: dict[str, Any],
    bullet_index: dict[str, list[BulletNode]],
) -> tuple[list[RefInfo], list[str]]:
    refs: list[RefInfo] = []
    missing: list[str] = []
    seen: set[tuple[int, str]] = set()

    for raw_title in node_spec.get("ref_titles", []):
        key = normalized_key(raw_title)
        matches = bullet_index.get(key, [])
        if not matches:
            matches = [
                node
                for indexed_key, nodes in bullet_index.items()
                if key in indexed_key
                for node in nodes
            ]
        if not matches:
            missing.append(raw_title)
            continue
        for match in matches:
            depth = int(node_spec.get("ref_depth", 3))
            text = "；".join(flatten_text(match, max_depth=depth))
            text = normalize_text(text)
            identity = (match.line, text)
            if identity in seen:
                continue
            seen.add(identity)
            refs.append(RefInfo(line=match.line, text=text))

    return compact_ref_info(refs), missing


def compact_ref_info(refs: list[RefInfo]) -> list[RefInfo]:
    compacted: list[RefInfo] = []
    for ref in sorted(refs, key=lambda item: (item.line, len(item.text))):
        if any(ref.text == existing.text and ref.line == existing.line for existing in compacted):
            continue
        if any(ref.text in existing.text for existing in compacted):
            continue
        compacted = [existing for existing in compacted if existing.text not in ref.text]
        compacted.append(ref)
    return sorted(compacted, key=lambda item: item.line)


def build_tco_tree(model: dict[str, Any], bullet_root: BulletNode) -> tuple[TcoNode, list[str]]:
    node_specs = {node["id"]: node for node in model["nodes"]}
    bullet_index = index_bullets(bullet_root)
    missing_refs: list[str] = []

    def build_node(node_id: str) -> TcoNode:
        if node_id not in node_specs:
            raise ValueError(f"TCO model 引用了不存在的 node id: {node_id}")
        spec = node_specs[node_id]
        ref_info, missing = collect_ref_info(spec, bullet_index)
        missing_refs.extend(f"{node_id}: {title}" for title in missing)
        children = [build_node(child_id) for child_id in spec.get("children", [])]
        scope = spec.get("scope", [])
        if isinstance(scope, str):
            scope = [scope]
        node = TcoNode(
            node_id=node_id,
            node_kind=spec["node_kind"],
            title=spec["title"],
            topic=normalize_text(spec["topic"]),
            scope=[normalize_text(item) for item in scope],
            purpose=normalize_text(spec["purpose"]),
            ref_info=ref_info,
            children=children,
        )
        validate_node(node)
        return node

    return build_node(model["root"]), missing_refs


def validate_node(node: TcoNode) -> None:
    if node.node_kind not in NODE_KINDS:
        raise ValueError(f"{node.node_id} 使用了非法 node_kind: {node.node_kind}")
    if not node.topic:
        raise ValueError(f"{node.node_id} 缺少 Topic")
    if not node.scope:
        raise ValueError(f"{node.node_id} 缺少 Scope")
    if not node.purpose:
        raise ValueError(f"{node.node_id} 缺少 Purpose")
    generated_text = " ".join([node.topic, node.purpose, *node.scope])
    for phrase in FORBIDDEN_GENERATED_PHRASES:
        if phrase in generated_text:
            raise ValueError(f"{node.node_id} 含机械 fallback 文案: {phrase}")
    for phrase in FORBIDDEN_TSP_STATUS_PHRASES:
        if phrase in generated_text:
            raise ValueError(f"{node.node_id} 的 TSP 含实现状态/claim 信息，应移到 Ref Info: {phrase}")
    for child in node.children:
        validate_node(child)


def walk_tco_nodes(node: TcoNode, depth: int = 0) -> list[tuple[TcoNode, int]]:
    nodes = [(node, depth)]
    for child in node.children:
        nodes.extend(walk_tco_nodes(child, depth + 1))
    return nodes


def coverage_rank(state: str) -> int:
    return COVERAGE_STATES.index(state)


def state_from_rank(rank: int) -> str:
    return COVERAGE_STATES[max(0, min(rank, len(COVERAGE_STATES) - 1))]


def default_target_state(node_kind: str) -> str | None:
    if node_kind == "capability":
        return DEFAULT_CAPABILITY_TARGET_STATE
    if node_kind == "policy":
        return DEFAULT_POLICY_TARGET_STATE
    return None


def coverage_gap_items(
    scope_rows: list[dict[str, Any]],
    target_state: str | None,
) -> list[dict[str, Any]]:
    if target_state is None:
        return []
    target_rank = coverage_rank(target_state)
    gaps = []
    for row in scope_rows:
        state = row.get("coverage_state", "unknown")
        if state not in COVERAGE_STATES or coverage_rank(state) >= target_rank:
            continue
        gaps.append(
            {
                "scope": row.get("scope", ""),
                "coverage_state": state,
                "target_coverage_state": target_state,
                "source": row.get("source", ""),
                "notes": (
                    "该 Scope 的当前证据低于本节点目标；"
                    "目标来自 node target，而不是全局 Runtime 阈值。"
                ),
            }
        )
    return gaps


def coverage_label(state: str) -> str:
    return COVERAGE_STATE_LABELS.get(state, state)


def load_coverage_model(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "semx.visualization.tco_coverage_model.v1":
        raise ValueError(f"不支持的 TCO coverage model schema: {data.get('schema')}")
    return data


def load_maintained_gates(repo_root: Path) -> dict[str, Any]:
    gate_path = repo_root / "tests/contract/run_maintained_validation.py"
    if not gate_path.exists():
        raise ValueError(f"未找到 maintained gate registry: {gate_path}")
    spec = importlib.util.spec_from_file_location("semx_maintained_validation", gate_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"无法加载 maintained gate registry: {gate_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return {gate.name: gate for gate in module.GATES}


def resolve_repo_path(repo_root: Path, raw_ref: str) -> Path:
    ref = raw_ref.split(":", 1)[0] if ":" in raw_ref and not raw_ref.startswith("/") else raw_ref
    path = Path(ref)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def tail_text(value: str, max_chars: int = 2000) -> str:
    value = value.strip()
    if len(value) <= max_chars:
        return value
    return value[-max_chars:]


def validate_coverage_model(
    model: dict[str, Any],
    tco_node_ids: set[str],
    tco_node_kinds: dict[str, str],
    tco_node_scopes: dict[str, list[str]],
    repo_root: Path,
    maintained_gates: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    records: dict[str, dict[str, Any]] = {}
    warnings: list[str] = []
    errors: list[str] = []

    for index, raw_record in enumerate(model.get("coverage", []), start=1):
        node_id = raw_record.get("tco_node_id")
        if not node_id:
            errors.append(f"coverage[{index}] 缺少 tco_node_id")
            continue
        if node_id not in tco_node_ids:
            errors.append(f"coverage[{index}] 引用了不存在的 TCO node: {node_id}")
            continue
        if node_id in records:
            errors.append(f"coverage 重复定义 TCO node: {node_id}")
            continue

        state = raw_record.get("coverage_state", "unknown")
        if state not in COVERAGE_STATES:
            errors.append(f"{node_id} 使用了非法 coverage_state: {state}")
        node_kind = tco_node_kinds[node_id]
        if node_kind == "group" and state not in {"unknown", "not_started"}:
            errors.append(
                f"{node_id} 是 group，不能配置直接完成状态 {state}；group Coverage 必须由 Scope/Sub M 派生"
            )

        counted_evidence = 0
        candidate_evidence = 0
        for evidence_index, evidence in enumerate(raw_record.get("evidence", []), start=1):
            kind = evidence.get("kind")
            if kind not in EVIDENCE_KINDS:
                errors.append(f"{node_id}.evidence[{evidence_index}] 使用了非法 kind: {kind}")
                continue
            if kind in COUNTED_EVIDENCE_KINDS:
                counted_evidence += 1
            if kind == "candidate_evidence":
                candidate_evidence += 1
            if kind in PATH_EVIDENCE_KINDS:
                ref = evidence.get("ref")
                if not ref:
                    errors.append(f"{node_id}.evidence[{evidence_index}] 缺少 ref")
                    continue
                ref_path = resolve_repo_path(repo_root, str(ref))
                if not ref_path.exists():
                    errors.append(f"{node_id}.evidence[{evidence_index}] 路径不存在: {ref}")
            if kind == "command":
                gate = evidence.get("gate") or evidence.get("ref")
                if not gate:
                    errors.append(f"{node_id}.evidence[{evidence_index}] command 缺少 gate/ref")
                elif gate not in maintained_gates:
                    errors.append(f"{node_id}.evidence[{evidence_index}] maintained gate 未注册: {gate}")

        if state not in {"unknown", "not_started"} and counted_evidence == 0:
            warnings.append(f"{node_id} 标记为 {state}，但没有 declared evidence；candidate_evidence 不计入覆盖")

        declared_scope_keys = {normalized_key(item): item for item in tco_node_scopes[node_id]}
        seen_scope_keys: set[str] = set()
        for scope_index, scope in enumerate(raw_record.get("scope_coverage", []), start=1):
            scope_state = scope.get("coverage_state", "unknown")
            if scope_state not in COVERAGE_STATES:
                errors.append(f"{node_id}.scope_coverage[{scope_index}] 使用了非法 coverage_state: {scope_state}")
            if not scope.get("scope"):
                errors.append(f"{node_id}.scope_coverage[{scope_index}] 缺少 scope")
                continue
            scope_key = normalized_key(str(scope["scope"]))
            if scope_key in seen_scope_keys:
                errors.append(f"{node_id}.scope_coverage 重复定义 Scope: {scope['scope']}")
            seen_scope_keys.add(scope_key)
            if scope_key not in declared_scope_keys:
                errors.append(f"{node_id}.scope_coverage 引用了 TCO model 中不存在的 Scope: {scope['scope']}")

        if node_kind != "group" and state not in {"unknown", "not_started"}:
            missing_scope_keys = set(declared_scope_keys) - seen_scope_keys
            if missing_scope_keys:
                missing_scopes = ", ".join(declared_scope_keys[key] for key in sorted(missing_scope_keys))
                errors.append(
                    f"{node_id} 标记为 {state}，但未逐项覆盖全部 Scope: {missing_scopes}"
                )

        record = dict(raw_record)
        record["_counted_evidence_count"] = counted_evidence
        record["_candidate_evidence_count"] = candidate_evidence
        records[node_id] = record

    if errors:
        raise ValueError("Coverage model 校验失败:\n- " + "\n- ".join(errors))
    return records, warnings


def collect_gate_names(records: dict[str, dict[str, Any]], verify_node_ids: set[str] | None) -> set[str]:
    gate_names: set[str] = set()
    for node_id, record in records.items():
        if verify_node_ids is not None and node_id not in verify_node_ids:
            continue
        for evidence in record.get("evidence", []):
            if evidence.get("kind") == "command":
                gate = evidence.get("gate") or evidence.get("ref")
                if gate:
                    gate_names.add(str(gate))
    return gate_names


def run_gate_verification(
    gate_names: set[str],
    maintained_gates: dict[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for gate_name in sorted(gate_names):
        gate = maintained_gates[gate_name]
        try:
            completed = subprocess.run(
                gate.command,
                cwd=repo_root,
                text=True,
                capture_output=True,
                timeout=VERIFICATION_TIMEOUT_SECONDS,
                check=False,
            )
            results[gate_name] = {
                "status": "pass" if completed.returncode == 0 else "fail",
                "exit_code": completed.returncode,
                "command": gate.display_command,
                "stdout_tail": tail_text(completed.stdout),
                "stderr_tail": tail_text(completed.stderr),
            }
        except subprocess.TimeoutExpired as exc:
            results[gate_name] = {
                "status": "timeout",
                "exit_code": None,
                "command": gate.display_command,
                "stdout_tail": tail_text(exc.stdout or ""),
                "stderr_tail": tail_text(exc.stderr or ""),
            }
    return results


def scope_coverage_for_node(
    node: TcoNode,
    record: dict[str, Any],
    child_payloads: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    modeled = {
        normalized_key(item.get("scope", "")): item
        for item in record.get("scope_coverage", [])
        if item.get("scope")
    }
    child_by_key: dict[str, dict[str, Any]] = {}
    for child in child_payloads:
        child_by_key[normalized_key(child["title"])] = child
        child_by_key[normalized_key(child["id"])] = child

    scope_rows: list[dict[str, Any]] = []
    for scope_item in node.scope:
        key = normalized_key(scope_item)
        if key in modeled:
            modeled_row = dict(modeled[key])
            modeled_row.setdefault("source", "coverage_model")
            scope_rows.append(modeled_row)
            continue
        if key in child_by_key:
            child = child_by_key[key]
            scope_rows.append(
                {
                    "scope": scope_item,
                    "coverage_state": child["coverage_state"],
                    "source": "sub_m_rollup",
                    "notes": f"由 Sub M {child['id']} 的 Coverage 汇总得到。",
                }
            )
            continue
        scope_rows.append(
            {
                "scope": scope_item,
                "coverage_state": "unknown",
                "source": "default_unknown",
                "notes": "coverage model 尚未为该 Scope 项提供 repo evidence。",
            }
        )
    return scope_rows


def state_counts(rows: list[dict[str, Any]], key: str = "coverage_state") -> dict[str, int]:
    counts = {state: 0 for state in COVERAGE_STATES}
    for row in rows:
        state = row.get(key, "unknown")
        counts[state] = counts.get(state, 0) + 1
    return {state: count for state, count in counts.items() if count}


def build_coverage_tree(
    node: TcoNode,
    records: dict[str, dict[str, Any]],
    verification_results: dict[str, Any],
    target_state_overrides: dict[str, str] | None = None,
    depth: int = 0,
) -> dict[str, Any]:
    target_state_overrides = target_state_overrides or {}
    child_payloads = [
        build_coverage_tree(child, records, verification_results, target_state_overrides, depth + 1)
        for child in node.children
    ]
    record = records.get(node.node_id, {})
    direct_state = record.get("coverage_state", "unknown")
    evidence = []
    for raw_evidence in record.get("evidence", []):
        item = {key: value for key, value in raw_evidence.items() if key not in {"verification"}}
        if item.get("kind") == "command":
            gate = item.get("gate") or item.get("ref")
            if gate in verification_results:
                item["verification"] = verification_results[gate]
        evidence.append(item)

    scope_rows = scope_coverage_for_node(node, record, child_payloads)
    target_state = target_state_overrides.get(node.node_id, default_target_state(node.node_kind))
    for row in scope_rows:
        if row.get("source") == "sub_m_rollup":
            child = next(
                (item for item in child_payloads if normalized_key(item["title"]) == normalized_key(row["scope"])),
                None,
            )
            row_target = child.get("target_coverage_state") if child else target_state
        else:
            row_target = target_state
        row["target_coverage_state"] = row_target
        row["target_met"] = (
            row_target is not None
            and coverage_rank(row["coverage_state"]) >= coverage_rank(row_target)
        )
    coverage_gaps = coverage_gap_items(scope_rows, target_state)
    child_ranks = [coverage_rank(child["coverage_state"]) for child in child_payloads]
    scope_ranks = [coverage_rank(row["coverage_state"]) for row in scope_rows]
    structural_ranks = [*child_ranks, *scope_ranks]
    if structural_ranks:
        # Effective Coverage intentionally follows the weakest declared child/scope.
        # A direct record is evidence metadata, not permission to hide an uncovered branch.
        effective_rank = min(structural_ranks)
    else:
        effective_rank = coverage_rank(direct_state)
    effective_state = state_from_rank(effective_rank)

    target_met = (
        target_state is not None
        and coverage_rank(effective_state) >= coverage_rank(target_state)
    )
    aggregate_members = [*child_payloads, *scope_rows]
    aggregate_covered = sum(
        item.get("coverage_state") not in {"unknown", "not_started"} for item in aggregate_members
    )
    aggregate_target_met = sum(item.get("target_met") is True for item in aggregate_members)
    if node.node_kind == "group":
        if aggregate_covered == 0:
            aggregate_status = "not_started"
        elif aggregate_members and aggregate_target_met == len(aggregate_members):
            aggregate_status = "covered"
        else:
            aggregate_status = "partial"
    else:
        aggregate_status = "not_applicable"

    modeled_missing = [normalize_text(item) for item in record.get("missing_scope_items", [])]
    auto_missing = [
        row["scope"]
        for row in scope_rows
        if row["coverage_state"] in {"unknown", "not_started"} and row["scope"] not in modeled_missing
    ]
    covered_scope_count = sum(
        row["coverage_state"] not in {"unknown", "not_started"} for row in scope_rows
    )
    covered_child_count = sum(
        child["coverage_state"] not in {"unknown", "not_started"} for child in child_payloads
    )
    unknown_scope_items = [row["scope"] for row in scope_rows if row["coverage_state"] == "unknown"]
    not_started_scope_items = [row["scope"] for row in scope_rows if row["coverage_state"] == "not_started"]
    verified_evidence_count = sum(
        item.get("kind") == "command" and item.get("verification", {}).get("status") == "pass"
        for item in evidence
    )

    return {
        "id": node.node_id,
        "node_kind": node.node_kind,
        "node_kind_label": NODE_KIND_LABELS[node.node_kind],
        "title": node.title,
        "depth": depth,
        "coverage_state": effective_state,
        "coverage_state_label": coverage_label(effective_state),
        "target_coverage_state": target_state,
        "target_coverage_state_label": coverage_label(target_state) if target_state else "不适用",
        "target_met": target_met if node.node_kind != "group" else None,
        "coverage_gap_kind": "none" if target_met else ("below_node_target" if target_state else "aggregate_only"),
        "aggregate_status": aggregate_status,
        "aggregate_covered": aggregate_covered,
        "aggregate_total": len(aggregate_members),
        "aggregate_target_met": aggregate_target_met,
        "direct_coverage_state": direct_state,
        "direct_coverage_state_label": coverage_label(direct_state),
        "claim_ceiling": record.get(
            "claim_ceiling",
            "暂无人工确认的 repo coverage evidence；不得据此声明该 M 已实现。",
        ),
        "evidence": evidence,
        "declared_evidence_count": record.get("_counted_evidence_count", 0),
        "verified_evidence_count": verified_evidence_count,
        "candidate_evidence_count": record.get("_candidate_evidence_count", 0),
        "scope_coverage": scope_rows,
        "coverage_gap_items": coverage_gaps,
        "missing_scope_items": modeled_missing + auto_missing,
        "unknown_scope_items": unknown_scope_items,
        "not_started_scope_items": not_started_scope_items,
        "notes": record.get("notes", []),
        "child_state_counts": state_counts(child_payloads),
        "scope_state_counts": state_counts(scope_rows),
        "scope_completeness": {
            "covered": covered_scope_count,
            "total": len(scope_rows),
            "complete": covered_scope_count == len(scope_rows),
        },
        "child_completeness": {
            "covered": covered_child_count,
            "total": len(child_payloads),
            "complete": covered_child_count == len(child_payloads),
        },
        "rollup_rule": (
            "coverage_state 取所有声明的 Sub M 与 Scope 中最低覆盖层级；"
            "direct_coverage_state 只保留证据元数据，不能掩盖 unknown/not_started 分支。"
        ),
        "children": child_payloads,
    }


def flatten_coverage_nodes(node: dict[str, Any]) -> list[dict[str, Any]]:
    current = {
        key: node[key]
        for key in [
            "id",
            "node_kind",
            "node_kind_label",
            "title",
            "depth",
            "coverage_state",
            "coverage_state_label",
            "target_coverage_state",
            "target_coverage_state_label",
            "target_met",
            "coverage_gap_kind",
            "aggregate_status",
            "aggregate_covered",
            "aggregate_total",
            "aggregate_target_met",
            "direct_coverage_state",
            "direct_coverage_state_label",
            "claim_ceiling",
            "evidence",
            "declared_evidence_count",
            "verified_evidence_count",
            "candidate_evidence_count",
            "scope_coverage",
            "coverage_gap_items",
            "missing_scope_items",
            "unknown_scope_items",
            "not_started_scope_items",
            "notes",
            "child_state_counts",
            "scope_state_counts",
            "scope_completeness",
            "child_completeness",
        ]
    }
    rows = [current]
    for child in node.get("children", []):
        rows.extend(flatten_coverage_nodes(child))
    return rows


def find_coverage_node(root: dict[str, Any], node_id: str) -> dict[str, Any] | None:
    if root["id"] == node_id:
        return root
    for child in root.get("children", []):
        found = find_coverage_node(child, node_id)
        if found is not None:
            return found
    return None


def profile_requirement(
    requirement_id: str,
    title: str,
    node_ids: list[str],
    target_state: str,
    node_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    states = [node_by_id[node_id]["coverage_state"] for node_id in node_ids]
    current_state = state_from_rank(min(coverage_rank(state) for state in states))
    met = all(coverage_rank(state) >= coverage_rank(target_state) for state in states)
    return {
        "id": requirement_id,
        "title": title,
        "node_ids": node_ids,
        "current_coverage_state": current_state,
        "target_coverage_state": target_state,
        "met": met,
    }


def build_target_profiles(
    profile_specs: list[dict[str, Any]],
    root_payload: dict[str, Any],
) -> list[dict[str, Any]]:
    flat_nodes = flatten_coverage_nodes(root_payload)
    node_by_id = {node["id"]: node for node in flat_nodes}
    profiles: list[dict[str, Any]] = []
    for spec in profile_specs:
        requirements: list[dict[str, Any]] = []
        if spec.get("requirements"):
            for raw in spec["requirements"]:
                requirements.append(
                    profile_requirement(
                        str(raw["id"]),
                        str(raw["title"]),
                        [str(node_id) for node_id in raw["node_ids"]],
                        str(raw["target_coverage_state"]),
                        node_by_id,
                    )
                )
        else:
            selected: dict[str, dict[str, Any]] = {}
            for root_id in spec.get("root_ids", []):
                profile_root = find_coverage_node(root_payload, str(root_id))
                if profile_root is None:
                    raise ValueError(f"target profile {spec.get('id')} 引用了不存在的 root id: {root_id}")
                for node in flatten_coverage_nodes(profile_root):
                    if node["node_kind"] != "group":
                        selected[node["id"]] = node
            for node_id, node in selected.items():
                target_state = node.get("target_coverage_state")
                if target_state is None:
                    continue
                requirements.append(
                    profile_requirement(node_id, node["title"], [node_id], target_state, node_by_id)
                )
        met_count = sum(item["met"] for item in requirements)
        profiles.append(
            {
                "id": spec["id"],
                "label": spec["label"],
                "description": spec.get("description", ""),
                "claim_ceiling": spec.get("claim_ceiling", ""),
                "requirement_count": len(requirements),
                "met_count": met_count,
                "gap_count": len(requirements) - met_count,
                "met": bool(requirements) and met_count == len(requirements),
                "requirements": requirements,
            }
        )
    return profiles


def build_coverage(
    tree: TcoNode,
    coverage_model_path: Path,
    repo_root: Path,
    verify: bool,
    strict_coverage: bool,
    verify_nodes: list[str],
    target_profiles: list[dict[str, Any]],
) -> CoverageBuild:
    coverage_model_path = coverage_model_path.resolve()
    coverage_model = load_coverage_model(coverage_model_path)
    tco_nodes = walk_tco_nodes(tree)
    tco_node_ids = {node.node_id for node, _depth in tco_nodes}
    tco_node_kinds = {node.node_id: node.node_kind for node, _depth in tco_nodes}
    tco_node_scopes = {node.node_id: node.scope for node, _depth in tco_nodes}
    maintained_gates = load_maintained_gates(repo_root)
    records, warnings = validate_coverage_model(
        coverage_model,
        tco_node_ids,
        tco_node_kinds,
        tco_node_scopes,
        repo_root,
        maintained_gates,
    )

    target_state_overrides = coverage_model.get("target_state_overrides", {})
    invalid_target_ids = sorted(set(target_state_overrides) - tco_node_ids)
    invalid_target_states = sorted(
        f"{node_id}={state}"
        for node_id, state in target_state_overrides.items()
        if state not in COVERAGE_STATES
    )
    if invalid_target_ids or invalid_target_states:
        parts = []
        if invalid_target_ids:
            parts.append("不存在的 node: " + ", ".join(invalid_target_ids))
        if invalid_target_states:
            parts.append("非法 target state: " + ", ".join(invalid_target_states))
        raise ValueError("Coverage target override 校验失败: " + "; ".join(parts))

    missing_model_nodes = sorted(tco_node_ids - set(records))
    missing_leaf_nodes = [node_id for node_id in missing_model_nodes if tco_node_kinds[node_id] != "group"]
    if missing_leaf_nodes:
        raise ValueError(
            "Coverage model 缺少 capability/policy 节点:\n- " + "\n- ".join(missing_leaf_nodes)
        )
    # Missing group records are intentional: group Coverage is always derived from
    # declared Scope/Sub M and must never become a manually asserted capability.

    verify_node_set = set(verify_nodes)
    unknown_verify_nodes = verify_node_set - tco_node_ids
    if unknown_verify_nodes:
        raise ValueError(f"--verify-node 引用了不存在的 TCO node: {', '.join(sorted(unknown_verify_nodes))}")
    verification_results: dict[str, Any] = {}
    if verify:
        verification_scope = verify_node_set or None
        gate_names = collect_gate_names(records, verification_scope)
        verification_results = run_gate_verification(gate_names, maintained_gates, repo_root)

    root_payload = build_coverage_tree(tree, records, verification_results, target_state_overrides)
    flat_nodes = flatten_coverage_nodes(root_payload)
    profile_results = build_target_profiles(target_profiles, root_payload)
    if strict_coverage:
        strict_errors = [
            warning
            for warning in warnings
            if "declared evidence" in warning
        ]
        if strict_errors:
            raise ValueError("Strict coverage 校验失败:\n- " + "\n- ".join(strict_errors))

    return CoverageBuild(
        root=root_payload,
        nodes=flat_nodes,
        warnings=warnings,
        verification_results=verification_results,
        target_profiles=profile_results,
        verify_requested=verify,
        model_path=coverage_model_path,
    )


def count_nodes(node: TcoNode) -> int:
    return 1 + sum(count_nodes(child) for child in node.children)


def count_ref_info_nodes(node: TcoNode) -> int:
    current = 1 if node.ref_info else 0
    return current + sum(count_ref_info_nodes(child) for child in node.children)


def render_list(items: list[str]) -> str:
    return "<ol>" + "".join(f"<li>{html.escape(item)}</li>" for item in items) + "</ol>"


def render_ref_info(refs: list[RefInfo]) -> str:
    if not refs:
        return ""
    return "<ul>" + "".join(
        f'<li><span class="line">line {ref.line}</span><span>{html.escape(ref.text)}</span></li>' for ref in refs
    ) + "</ul>"


def render_coverage_badge(state: str, label: str | None = None) -> str:
    display = label or coverage_label(state)
    return f'<span class="coverage-badge state-{html.escape(state)}">{html.escape(display)}</span>'


def render_node_kind_badge(node_kind: str) -> str:
    return (
        f'<span class="node-kind kind-{html.escape(node_kind)}">'
        f'{html.escape(NODE_KIND_LABELS[node_kind])}</span>'
    )


def render_key_value(label: str, value: str) -> str:
    return f"<dt>{html.escape(label)}</dt><dd>{html.escape(value)}</dd>"


def render_coverage_counts(counts: dict[str, int]) -> str:
    if not counts:
        return '<span class="muted">无</span>'
    return " ".join(
        f'{render_coverage_badge(state)}<span class="count">{count}</span>'
        for state, count in counts.items()
    )


def render_evidence_list(evidence: list[dict[str, Any]]) -> str:
    if not evidence:
        return '<p class="empty">暂无人工确认的 repo evidence。</p>'
    rows = []
    for item in evidence:
        kind = item.get("kind", "")
        ref = item.get("ref") or ""
        gate = item.get("gate") or ""
        if item.get("label"):
            label = item["label"]
        elif gate:
            label = gate
        elif ref:
            label = Path(str(ref)).name
        else:
            label = kind
        verification = item.get("verification")
        verification_html = ""
        if verification:
            verification_html = (
                f' <span class="verify-result verify-{html.escape(verification["status"])}">'
                f'{html.escape(verification["status"])}</span>'
            )
        elif kind == "command":
            verification_html = ' <span class="verify-result verify-not-run">未运行</span>'
        rows.append(
            "<li>"
            f'<span class="evidence-kind">{html.escape(kind)}</span>'
            f'<span class="evidence-label">{html.escape(str(label))}</span>'
            f'<span class="evidence-ref">{html.escape(str(ref))}</span>'
            f"{verification_html}"
            "</li>"
        )
    return "<ul class=\"evidence-list\">" + "".join(rows) + "</ul>"


def render_scope_coverage(scope_rows: list[dict[str, Any]]) -> str:
    if not scope_rows:
        return '<p class="empty">暂无 Scope 覆盖项。</p>'
    rows = []
    for item in scope_rows:
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(item.get('scope', '')))}</td>"
            f"<td>{render_coverage_badge(str(item.get('coverage_state', 'unknown')))}</td>"
            f"<td>{html.escape(str(item.get('source', '')))}</td>"
            f"<td>{html.escape(str(item.get('notes', '')))}</td>"
            "</tr>"
        )
    return (
        '<table class="coverage-table">'
        "<thead><tr><th>Scope item</th><th>State</th><th>Source</th><th>说明</th></tr></thead>"
        "<tbody>"
        + "".join(rows)
        + "</tbody></table>"
    )


def render_coverage_gap(gap_rows: list[dict[str, Any]]) -> str:
    if not gap_rows:
        return '<p class="empty">无低于本节点目标的 Coverage gap。</p>'
    rows = []
    for item in gap_rows:
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(item.get('scope', '')))}</td>"
            f"<td>{render_coverage_badge(str(item.get('coverage_state', 'unknown')))}</td>"
            f"<td>{render_coverage_badge(str(item.get('target_coverage_state', DEFAULT_CAPABILITY_TARGET_STATE)))}</td>"
            f"<td>{html.escape(str(item.get('notes', '')))}</td>"
            "</tr>"
        )
    return (
        '<table class="coverage-table">'
        "<thead><tr><th>Scope item</th><th>Current</th><th>Node target</th><th>说明</th></tr></thead>"
        "<tbody>"
        + "".join(rows)
        + "</tbody></table>"
    )


def render_coverage_info(coverage: dict[str, Any]) -> str:
    notes = coverage.get("notes", [])
    unknown = coverage.get("unknown_scope_items", [])
    not_started = coverage.get("not_started_scope_items", [])
    notes_html = ""
    if notes:
        notes_html = "<ul>" + "".join(f"<li>{html.escape(str(note))}</li>" for note in notes) + "</ul>"
    unknown_html = "<ol>" + "".join(f"<li>{html.escape(str(item))}</li>" for item in unknown) + "</ol>" if unknown else ""
    not_started_html = "<ol>" + "".join(f"<li>{html.escape(str(item))}</li>" for item in not_started) + "</ol>" if not_started else ""
    scope_completeness = coverage.get("scope_completeness", {})
    child_completeness = coverage.get("child_completeness", {})
    if coverage["node_kind"] == "group":
        effective_value = {
            "covered": "聚合目标已覆盖",
            "partial": "聚合部分覆盖",
            "not_started": "聚合未开始",
        }.get(coverage.get("aggregate_status"), "聚合状态未知")
        direct_value = "不适用（功能域不拥有直接实现状态）"
        target_value = "不适用（按子 M 各自目标汇总）"
    else:
        effective_value = coverage_label(coverage["coverage_state"])
        direct_value = coverage_label(coverage["direct_coverage_state"])
        target_value = coverage.get("target_coverage_state_label", "不适用")
    return f"""
      <div class="coverage-panel">
        <dl class="coverage-kv">
          {render_key_value("Node kind", coverage["node_kind_label"])}
          {render_key_value("Effective", effective_value)}
          {render_key_value("Direct", direct_value)}
          {render_key_value("Node target", target_value)}
          {render_key_value("Scope completeness", f'{scope_completeness.get("covered", 0)}/{scope_completeness.get("total", 0)}')}
          {render_key_value("Sub M completeness", f'{child_completeness.get("covered", 0)}/{child_completeness.get("total", 0)}')}
          {render_key_value("Declared evidence", str(coverage["declared_evidence_count"]))}
          {render_key_value("Verified gates", str(coverage["verified_evidence_count"]))}
          {render_key_value("Candidate evidence", str(coverage["candidate_evidence_count"]))}
        </dl>
        <p class="claim-ceiling"><strong>Claim ceiling：</strong>{html.escape(coverage["claim_ceiling"])}</p>
        <div class="coverage-counts"><strong>Sub M：</strong>{render_coverage_counts(coverage.get("child_state_counts", {}))}</div>
        <div class="coverage-counts"><strong>Scope：</strong>{render_coverage_counts(coverage.get("scope_state_counts", {}))}</div>
        <h3>Evidence</h3>
        {render_evidence_list(coverage.get("evidence", []))}
        <h3>Scope Coverage</h3>
        {render_scope_coverage(coverage.get("scope_coverage", []))}
        <h3>Coverage Gap（未达本节点目标）</h3>
        {render_coverage_gap(coverage.get("coverage_gap_items", []))}
        <h3>Unknown Scope（尚未确认）</h3>
        {unknown_html or '<p class="empty">无 unknown Scope。</p>'}
        <h3>Not-started Scope（已确认未开始）</h3>
        {not_started_html or '<p class="empty">无 not-started Scope。</p>'}
        <h3>Notes</h3>
        {notes_html or '<p class="empty">无备注。</p>'}
      </div>
    """


def render_tsp_branch(label: str, body: str, open_by_default: bool = True) -> str:
    open_attr = " open" if open_by_default else ""
    return f"""
      <details class="tsp-branch"{open_attr}>
        <summary>{html.escape(label)}</summary>
        <div class="branch-body">{body}</div>
      </details>
    """


def scope_completeness_filter_value(scope_completeness: dict[str, Any]) -> str:
    covered = int(scope_completeness.get("covered", 0))
    total = int(scope_completeness.get("total", 0))
    if total == 0:
        return "empty"
    if covered == 0:
        return "none"
    if covered == total:
        return "complete"
    return "partial"


def render_tco_node(node: TcoNode, coverage_by_id: dict[str, dict[str, Any]], depth: int = 0) -> str:
    coverage = coverage_by_id[node.node_id]
    scope_completeness_filter = scope_completeness_filter_value(coverage.get("scope_completeness", {}))
    children_html = ""
    if node.children:
        children_html = "\n".join(render_tco_node(child, coverage_by_id, depth + 1) for child in node.children)
        children_html = f"""
          <details class="subfeatures" open>
            <summary>Sub M</summary>
            <div class="children">{children_html}</div>
          </details>
        """
    if node.node_kind == "group":
        aggregate_label = {
            "covered": "聚合：目标已覆盖",
            "partial": "聚合：部分覆盖",
            "not_started": "聚合：未开始",
        }.get(coverage.get("aggregate_status"), "聚合：未知")
        status_badge = render_coverage_badge(coverage["coverage_state"], aggregate_label)
    else:
        status_badge = render_coverage_badge(coverage["coverage_state"])
    return f"""
      <details class="tco-node" data-depth="{depth}" data-node-kind="{html.escape(node.node_kind)}" data-coverage-state="{html.escape(coverage["coverage_state"])}" data-scope-completeness="{html.escape(scope_completeness_filter)}" open>
        <summary>
          <span class="node-title">{html.escape(node.title)}</span>
          <span class="summary-meta">{render_node_kind_badge(node.node_kind)}{status_badge}<span class="node-id">{html.escape(node.node_id)}</span></span>
        </summary>
        <div class="tsp-grid">
          {render_tsp_branch("Topic", f"<p>{html.escape(node.topic)}</p>")}
          {render_tsp_branch("Ref Info", render_ref_info(node.ref_info), open_by_default=False)}
          {render_tsp_branch("Scope", render_list(node.scope))}
          {render_tsp_branch("Purpose", f"<p>{html.escape(node.purpose)}</p>")}
          {render_tsp_branch("Coverage", render_coverage_info(coverage), open_by_default=False)}
        </div>
        {children_html}
      </details>
    """


def render_coverage_summary(coverage_build: CoverageBuild) -> str:
    leaf_nodes = [node for node in coverage_build.nodes if node.get("node_kind") != "group"]
    counts = state_counts(leaf_nodes)
    kind_counts = {
        kind: sum(node.get("node_kind") == kind for node in coverage_build.nodes)
        for kind in sorted(NODE_KINDS)
    }
    cards = "".join(
        f'<div class="summary-card">{render_coverage_badge(state)}<strong>{count}</strong></div>'
        for state, count in counts.items()
    )
    warning_html = ""
    if coverage_build.warnings:
        warning_html = (
            '<div class="coverage-warnings">'
            + "".join(f"<p>{html.escape(warning)}</p>" for warning in coverage_build.warnings)
            + "</div>"
        )
    profile_rows = "".join(
        "<tr>"
        f"<td>{html.escape(profile['label'])}</td>"
        f"<td>{profile['met_count']}/{profile['requirement_count']}</td>"
        f"<td>{'达到当前 profile' if profile['met'] else '仍有缺口'}</td>"
        f"<td>{html.escape(profile['claim_ceiling'])}</td>"
        "</tr>"
        for profile in coverage_build.target_profiles
    )
    verification_status = (
        f"已请求验证；运行 {len(coverage_build.verification_results)} 个 maintained gates，"
        f"失败 {sum(result.get('status') != 'pass' for result in coverage_build.verification_results.values())} 个。"
        if coverage_build.verify_requested
        else "本次只生成 inventory，未运行 maintained gates；Evidence 为已声明，不是本次已验证。"
    )
    return f"""
      <section class="coverage-summary">
        <div class="summary-cards">{cards}</div>
        <p class="definition">Coverage 统计只计算能力与规则节点；功能域 {kind_counts['group']} 个只显示聚合状态，不与叶节点混算。能力 {kind_counts['capability']}、规则 {kind_counts['policy']}。</p>
        <p class="definition">Verification：{html.escape(verification_status)}</p>
        <table class="coverage-table"><thead><tr><th>Target profile</th><th>Met</th><th>状态</th><th>Claim ceiling</th></tr></thead><tbody>{profile_rows}</tbody></table>
        {warning_html}
      </section>
    """


def render_html(
    tree: TcoNode,
    source: Path,
    model: Path,
    coverage_build: CoverageBuild,
    section_start_line: int,
    generated_at: str,
) -> str:
    coverage_by_id = {node["id"]: node for node in coverage_build.nodes}
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(tree.title)} TCO</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --ink: #172033;
      --muted: #64748b;
      --line: #0f766e;
      --node: #ecfeff;
      --node-strong: #99f6e4;
      --branch: #ffffff;
      --rule: #94a3b8;
      --accent: #0f766e;
    }}
    body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: Arial, "PingFang SC", sans-serif; }}
    header {{ position: sticky; top: 0; z-index: 2; padding: 16px 24px; background: #134e4a; color: white; }}
    h1 {{ margin: 0 0 6px; font-size: 20px; letter-spacing: 0; }}
    .meta {{ color: #ccfbf1; font-size: 12px; line-height: 1.5; }}
    main {{ max-width: 1440px; padding: 18px 24px 48px; }}
    .definition {{ margin: 0 0 14px; padding: 10px 12px; border-left: 3px solid var(--accent); background: white; border-radius: 6px; color: #334155; line-height: 1.55; }}
    .toolbar {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 14px; align-items: center; }}
    .toolbar label {{ display: inline-flex; align-items: center; gap: 6px; color: var(--muted); font-size: 13px; }}
    select {{ border: 1px solid var(--rule); background: white; color: var(--ink); padding: 7px 10px; border-radius: 6px; }}
    button {{ border: 1px solid var(--rule); background: white; color: var(--ink); padding: 8px 12px; border-radius: 6px; cursor: pointer; }}
    details {{ margin: 8px 0; }}
    summary {{ cursor: pointer; }}
    .tco-node {{ border-left: 2px dashed var(--line); padding-left: 14px; margin-left: 10px; }}
    .tco-node > summary {{ display: flex; justify-content: space-between; gap: 12px; padding: 9px 12px; border-radius: 6px; background: var(--node-strong); font-weight: 700; }}
    body.m-only .tsp-grid {{ display: none; }}
    body.m-only .tco-node.detail-visible > .tsp-grid {{ display: block; }}
    body.m-only .tco-node.detail-visible > summary {{ outline: 2px solid #0f766e; outline-offset: 2px; }}
    .summary-meta {{ display: inline-flex; align-items: center; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }}
    .node-id {{ color: var(--muted); font-weight: 400; font-size: 12px; }}
    .tsp-grid {{ margin: 8px 0 12px 18px; }}
    .tsp-branch {{ border-left: 2px dashed var(--line); padding-left: 12px; }}
    .tsp-branch > summary {{ width: fit-content; min-width: 96px; padding: 5px 8px; border-radius: 5px; background: var(--node); color: #115e59; font-weight: 700; }}
    .branch-body {{ background: var(--branch); border: 1px solid #cbd5e1; border-radius: 6px; margin: 6px 0 10px 12px; padding: 10px 12px; line-height: 1.5; }}
    .branch-body p {{ margin: 0; }}
    .branch-body ol {{ margin: 0; padding-left: 22px; }}
    .branch-body ul {{ margin: 0; padding-left: 18px; }}
    .branch-body li {{ margin: 5px 0; }}
    .branch-body .line {{ display: inline-block; min-width: 64px; color: var(--muted); font-size: 12px; }}
    .empty {{ color: var(--muted); }}
    .muted {{ color: var(--muted); }}
    .subfeatures {{ margin-left: 18px; }}
    .subfeatures > summary {{ width: fit-content; padding: 5px 8px; border-radius: 5px; background: #ccfbf1; color: #115e59; font-weight: 700; }}
    .children {{ margin-left: 8px; }}
    .coverage-summary {{ margin: 0 0 14px; }}
    .summary-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; }}
    .summary-card {{ display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 10px 12px; border-radius: 6px; background: white; border: 1px solid #dbe4ee; }}
    .summary-card strong {{ font-size: 20px; }}
    .coverage-warnings {{ margin-top: 8px; padding: 8px 10px; border-left: 3px solid #f59e0b; background: #fffbeb; border-radius: 6px; color: #713f12; }}
    .coverage-warnings p {{ margin: 4px 0; }}
    .coverage-badge {{ display: inline-block; min-width: 72px; padding: 2px 7px; border-radius: 999px; font-size: 12px; font-weight: 700; text-align: center; border: 1px solid transparent; }}
    .node-kind {{ display: inline-block; padding: 2px 7px; border-radius: 999px; font-size: 12px; font-weight: 700; border: 1px solid #cbd5e1; background: #fff; }}
    .kind-group {{ color: #334155; }}
    .kind-capability {{ color: #166534; }}
    .kind-policy {{ color: #7c2d12; }}
    .state-unknown {{ color: #475569; background: #f1f5f9; border-color: #cbd5e1; }}
    .state-not_started {{ color: #7f1d1d; background: #fee2e2; border-color: #fecaca; }}
    .state-design_only {{ color: #6b21a8; background: #f3e8ff; border-color: #e9d5ff; }}
    .state-schema_validator {{ color: #1d4ed8; background: #dbeafe; border-color: #bfdbfe; }}
    .state-test_bound {{ color: #0f766e; background: #ccfbf1; border-color: #99f6e4; }}
    .state-bounded_runtime {{ color: #166534; background: #dcfce7; border-color: #bbf7d0; }}
    .state-integrated_runtime {{ color: #064e3b; background: #a7f3d0; border-color: #6ee7b7; }}
    .coverage-kv {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px 12px; margin: 0 0 10px; }}
    .coverage-kv dt {{ color: var(--muted); font-size: 12px; }}
    .coverage-kv dd {{ margin: 2px 0 0; font-weight: 700; }}
    .coverage-panel h3 {{ margin: 12px 0 6px; font-size: 14px; }}
    .claim-ceiling {{ margin: 8px 0; }}
    .coverage-counts {{ margin: 6px 0; }}
    .coverage-counts .count {{ margin: 0 8px 0 3px; color: var(--muted); }}
    .evidence-list {{ list-style: none; padding-left: 0 !important; }}
    .evidence-list li {{ display: grid; grid-template-columns: 72px minmax(0, 1fr) minmax(0, 1.8fr) max-content; gap: 10px; align-items: start; padding: 6px 0; border-bottom: 1px solid #e2e8f0; }}
    .evidence-list li > span {{ min-width: 0; }}
    .evidence-kind {{ color: var(--muted); font-size: 12px; }}
    .evidence-label {{ overflow-wrap: anywhere; word-break: break-word; line-height: 1.35; }}
    .evidence-ref {{ color: #334155; font-family: Menlo, Consolas, monospace; font-size: 12px; overflow-wrap: anywhere; word-break: break-word; white-space: normal; line-height: 1.35; }}
    .verify-result {{ padding: 2px 6px; border-radius: 999px; font-size: 12px; font-weight: 700; }}
    .evidence-list .verify-result {{ justify-self: start; white-space: nowrap; }}
    .verify-pass {{ color: #166534; background: #dcfce7; }}
    .verify-fail, .verify-timeout {{ color: #991b1b; background: #fee2e2; }}
    .verify-not-run {{ color: #475569; background: #f1f5f9; }}
    .coverage-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    .coverage-table th, .coverage-table td {{ text-align: left; vertical-align: top; border-bottom: 1px solid #e2e8f0; padding: 7px 6px; }}
    .coverage-table th {{ color: var(--muted); font-weight: 700; }}
    [data-depth="0"] > summary {{ background: #5eead4; }}
    [data-depth="1"] > summary {{ background: #99f6e4; }}
    [data-depth="2"] > summary {{ background: #ccfbf1; }}
    [data-depth="3"] > summary {{ background: #ecfeff; }}
    @media (max-width: 760px) {{
      main {{ padding: 12px; }}
      .node-id {{ display: none; }}
      .tco-node {{ margin-left: 0; padding-left: 10px; }}
      .tsp-grid {{ margin-left: 8px; }}
      .evidence-list li {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(tree.title)} TCO</h1>
    <div class="meta">source: {html.escape(str(source))} · model: {html.escape(str(model))} · coverage: {html.escape(str(coverage_build.model_path))} · section line {section_start_line} · generated: {generated_at}</div>
  </header>
  <main>
    <p class="definition">TCO = Testing Coverage Outline。这里把 Business Rules 拆成真实可实现的单功能 M；每个 M 用 Topic / Scope / Purpose 统一建模。Ref Info 只保留没有进入 Scope 的原文说明、当前实现状态、claim ceiling 和 repo 现状；没有额外信息时保持空白。</p>
    {render_coverage_summary(coverage_build)}
    <div class="toolbar">
      <button type="button" onclick="expandAll()">全部展开</button>
      <button type="button" onclick="showOnlyM()">只保留 M</button>
      <button type="button" onclick="hideRefInfo()">隐藏 Ref Info</button>
      <label>Coverage
        <select id="coverageFilter" onchange="applyFilters()">
          <option value="">全部</option>
          {"".join(f'<option value="{state}">{coverage_label(state)}</option>' for state in COVERAGE_STATES)}
        </select>
      </label>
      <label>Node kind
        <select id="nodeKindFilter" onchange="applyFilters()">
          <option value="">全部</option>
          <option value="group">{NODE_KIND_LABELS["group"]}</option>
          <option value="capability">{NODE_KIND_LABELS["capability"]}</option>
          <option value="policy">{NODE_KIND_LABELS["policy"]}</option>
        </select>
      </label>
      <label>Scope completeness
        <select id="scopeCompletenessFilter" onchange="applyFilters()">
          <option value="">全部</option>
          <option value="complete">Scope 覆盖完整</option>
          <option value="partial">Scope 部分覆盖</option>
          <option value="none">Scope 无覆盖</option>
          <option value="empty">无 Scope</option>
        </select>
      </label>
    </div>
    {render_tco_node(tree, coverage_by_id)}
  </main>
  <script>
    function openVisibleMContainers() {{
      document.querySelectorAll('.tco-node').forEach(node => {{
        if (!node.hidden) node.open = true;
      }});
      document.querySelectorAll('.subfeatures').forEach(group => {{
        const hasVisibleChild = Array.from(group.querySelectorAll('.tco-node')).some(child => !child.hidden);
        group.open = hasVisibleChild;
      }});
    }}

    function clearVisibleNodeDetails() {{
      document.querySelectorAll('.tco-node.detail-visible').forEach(node => {{
        node.classList.remove('detail-visible');
      }});
    }}

    function expandAll() {{
      document.body.classList.remove('m-only');
      clearVisibleNodeDetails();
      document.querySelectorAll('details').forEach(detail => detail.open = true);
    }}

    function hideRefInfo() {{
      document.body.classList.remove('m-only');
      clearVisibleNodeDetails();
      document.querySelectorAll('.tsp-branch').forEach(branch => {{
        branch.open = branch.querySelector('summary').textContent !== 'Ref Info';
      }});
    }}

    function showOnlyM() {{
      applyFilters();
      document.body.classList.add('m-only');
      clearVisibleNodeDetails();
      document.querySelectorAll('.tsp-branch').forEach(branch => branch.open = false);
      openVisibleMContainers();
    }}

    function directTspBranches(node) {{
      const grid = Array.from(node.children).find(child => child.classList.contains('tsp-grid'));
      if (!grid) return [];
      return Array.from(grid.querySelectorAll('.tsp-branch'));
    }}

    function toggleNodeDetails(node) {{
      const wasVisible = node.classList.contains('detail-visible');
      clearVisibleNodeDetails();
      if (wasVisible) return;
      node.open = true;
      node.classList.add('detail-visible');
      directTspBranches(node).forEach(branch => branch.open = true);
    }}

    function initializeNodeDetailClicks() {{
      document.querySelectorAll('.tco-node > summary').forEach(summary => {{
        summary.addEventListener('click', event => {{
          if (!document.body.classList.contains('m-only')) return;
          event.preventDefault();
          event.stopPropagation();
          toggleNodeDetails(summary.parentElement);
        }});
      }});
    }}

    function currentFilters() {{
      return {{
        coverageState: document.getElementById('coverageFilter').value,
        nodeKind: document.getElementById('nodeKindFilter').value,
        scopeCompleteness: document.getElementById('scopeCompletenessFilter').value,
      }};
    }}

    function matchesFilters(node, filters) {{
      const coverageMatch = !filters.coverageState || node.dataset.coverageState === filters.coverageState;
      const kindMatch = !filters.nodeKind || node.dataset.nodeKind === filters.nodeKind;
      const scopeMatch = !filters.scopeCompleteness || node.dataset.scopeCompleteness === filters.scopeCompleteness;
      return coverageMatch && kindMatch && scopeMatch;
    }}

    function hasActiveFilter(filters) {{
      return Boolean(filters.coverageState || filters.nodeKind || filters.scopeCompleteness);
    }}

    function applyFilters() {{
      const filters = currentFilters();
      const active = hasActiveFilter(filters);
      const nodes = Array.from(document.querySelectorAll('.tco-node'));
      nodes.forEach(node => {{
        node.dataset.selfMatch = (!active || matchesFilters(node, filters)) ? 'true' : 'false';
        node.dataset.visibleMatch = node.dataset.selfMatch;
      }});
      nodes.slice().reverse().forEach(node => {{
        const descendantMatch = Array.from(node.querySelectorAll('.tco-node')).some(child => child.dataset.visibleMatch === 'true');
        const visible = node.dataset.selfMatch === 'true' || descendantMatch;
        node.dataset.visibleMatch = visible ? 'true' : 'false';
        node.hidden = !visible;
        if (visible && active) node.open = true;
      }});
      if (active) openVisibleMContainers();
      document.querySelectorAll('.tco-node.detail-visible').forEach(node => {{
        if (node.hidden) node.classList.remove('detail-visible');
      }});
    }}

    function applyCoverageFilter() {{
      applyFilters();
    }}

    initializeNodeDetailClicks();
  </script>
</body>
</html>
"""


def build(
    source: Path,
    model_path: Path,
    coverage_model_path: Path,
    output_dir: Path,
    section_title: str,
    verify: bool,
    strict_coverage: bool,
    verify_nodes: list[str],
) -> dict[str, Any]:
    repo_root = Path.cwd().resolve()
    source = source.resolve()
    model_path = model_path.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    markdown = source.read_text(encoding="utf-8")
    section_start_line, section_lines = extract_section_lines(markdown, section_title)
    bullet_root = parse_bullets(section_lines)
    model = load_model(model_path)
    tree, missing_refs = build_tco_tree(model, bullet_root)
    coverage_build = build_coverage(
        tree=tree,
        coverage_model_path=coverage_model_path,
        repo_root=repo_root,
        verify=verify,
        strict_coverage=strict_coverage,
        verify_nodes=verify_nodes,
        target_profiles=model.get("target_profiles", []),
    )

    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    html_path = output_dir / "kym_business_rules_tco.html"
    json_path = output_dir / "kym_business_rules_tco.json"
    manifest_path = output_dir / "kym_business_rules_tco_manifest.json"
    coverage_json_path = output_dir / "kym_business_rules_tco_coverage.json"
    coverage_manifest_path = output_dir / "kym_business_rules_tco_coverage_manifest.json"

    html_output = render_html(tree, source, model_path, coverage_build, section_start_line, generated_at)
    json_output = json.dumps(tree.to_dict(), ensure_ascii=False, indent=2) + "\n"
    html_path.write_text(html_output, encoding="utf-8")
    json_path.write_text(json_output, encoding="utf-8")

    node_count = count_nodes(tree)
    ref_info_node_count = count_ref_info_nodes(tree)
    leaf_coverage_nodes = [node for node in coverage_build.nodes if node.get("node_kind") != "group"]
    coverage_state_counts = state_counts(leaf_coverage_nodes)
    direct_coverage_state_counts = state_counts(leaf_coverage_nodes, key="direct_coverage_state")
    node_kind_counts = {
        kind: sum(node.get("node_kind") == kind for node in coverage_build.nodes)
        for kind in sorted(NODE_KINDS)
    }
    coverage_state_counts_by_kind = {
        kind: state_counts([node for node in coverage_build.nodes if node.get("node_kind") == kind])
        for kind in sorted(NODE_KINDS)
    }
    group_aggregate_counts: dict[str, int] = {}
    for node in coverage_build.nodes:
        if node.get("node_kind") != "group":
            continue
        status = str(node.get("aggregate_status", "unknown"))
        group_aggregate_counts[status] = group_aggregate_counts.get(status, 0) + 1
    verified_gate_count = len(coverage_build.verification_results)
    failed_verified_gates = [
        gate
        for gate, result in coverage_build.verification_results.items()
        if result.get("status") != "pass"
    ]
    normalized_verification_results = {
        gate: {
            "status": result.get("status"),
            "exit_code": result.get("exit_code"),
            "command": result.get("command"),
        }
        for gate, result in sorted(coverage_build.verification_results.items())
    }
    coverage_payload = {
        "schema": "semx.visualization.tco_coverage.v1",
        "generated_at": generated_at,
        "source": str(source),
        "tco_model": str(model_path),
        "coverage_model": str(coverage_build.model_path),
        "verify": {
            "requested": verify,
            "verify_nodes": verify_nodes,
            "verified_gate_count": verified_gate_count,
            "failed_verified_gates": failed_verified_gates,
            "results": normalized_verification_results,
        },
        "summary": {
            "node_count": node_count,
            "coverage_state_counts": coverage_state_counts,
            "direct_coverage_state_counts": direct_coverage_state_counts,
            "node_kind_counts": node_kind_counts,
            "coverage_state_counts_by_kind": coverage_state_counts_by_kind,
            "group_aggregate_counts": group_aggregate_counts,
            "target_profiles": coverage_build.target_profiles,
            "warning_count": len(coverage_build.warnings),
        },
        "warnings": coverage_build.warnings,
        "nodes": coverage_build.nodes,
        "root": coverage_build.root,
        "target_profiles": coverage_build.target_profiles,
        "authority_note": (
            "Coverage is a derived repo evidence inventory. It is not KB canonical truth, "
            "not implementation approval, and not a Runtime Kernel completion claim."
        ),
    }
    coverage_json_path.write_text(json.dumps(coverage_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    coverage_manifest = {
        "schema": "semx.visualization.tco_coverage_manifest.v1",
        "generated_at": generated_at,
        "source": str(source),
        "tco_model": str(model_path),
        "coverage_model": str(coverage_build.model_path),
        "node_count": node_count,
        "coverage_state_counts": coverage_state_counts,
        "direct_coverage_state_counts": direct_coverage_state_counts,
        "node_kind_counts": node_kind_counts,
        "coverage_state_counts_by_kind": coverage_state_counts_by_kind,
        "group_aggregate_counts": group_aggregate_counts,
        "target_profiles": coverage_build.target_profiles,
        "warning_count": len(coverage_build.warnings),
        "warnings": coverage_build.warnings,
        "verify_requested": verify,
        "verify_nodes": verify_nodes,
        "verified_gate_count": verified_gate_count,
        "failed_verified_gates": failed_verified_gates,
        "verification_results": normalized_verification_results,
        "outputs": {
            "html": str(html_path),
            "coverage_json": str(coverage_json_path),
        },
        "authority_note": "Derived coverage inventory only; it does not promote TCO or Dashboard state to KB truth.",
    }
    coverage_manifest_path.write_text(
        json.dumps(coverage_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "schema": "semx.visualization.tco_manifest.v1",
        "generated_at": generated_at,
        "source": str(source),
        "model": str(model_path),
        "coverage_model": str(coverage_build.model_path),
        "section": section_title,
        "section_start_line": section_start_line,
        "node_count": node_count,
        "ref_info_node_count": ref_info_node_count,
        "empty_ref_info_node_count": node_count - ref_info_node_count,
        "missing_ref_count": len(missing_refs),
        "missing_refs": missing_refs,
        "outputs": {
            "html": str(html_path),
            "json": str(json_path),
            "coverage_json": str(coverage_json_path),
            "coverage_manifest": str(coverage_manifest_path),
        },
        "authority_note": "Derived TCO visualization only; KYM Markdown and KB contracts remain authoritative.",
    }
    manifest_output = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    manifest_path.write_text(manifest_output, encoding="utf-8")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TCO Generator for KYM Business Rules.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Markdown source file.")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL, help="TCO model JSON.")
    parser.add_argument("--coverage-model", type=Path, default=DEFAULT_COVERAGE_MODEL, help="TCO coverage model JSON.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory.")
    parser.add_argument("--section", default=SECTION_TITLE, help="Bullet section title to extract.")
    parser.add_argument("--verify", action="store_true", help="Run maintained gates referenced by the coverage model.")
    parser.add_argument(
        "--verify-node",
        action="append",
        default=[],
        help="When --verify is set, only run gates referenced by this TCO node. May be repeated.",
    )
    parser.add_argument("--strict-coverage", action="store_true", help="Fail closed on strict coverage quality warnings.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = build(
        source=args.source,
        model_path=args.model,
        coverage_model_path=args.coverage_model,
        output_dir=args.output_dir,
        section_title=args.section,
        verify=args.verify,
        strict_coverage=args.strict_coverage,
        verify_nodes=args.verify_node,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
