#!/usr/bin/env python3
"""Generate the offline, full-cycle Semx Dashboard panorama.

Dashboard Markdown remains execution-memory authority.  This generator only
creates a reader-facing projection; it does not update lifecycle state.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from session_registry import parse_index, parse_registry_file, split_markdown_row  # noqa: E402


BI_PLAIN_LANGUAGE: dict[str, dict[str, str]] = {
    "BI-001": {
        "capability": "项目已经有一份正式的“施工宪法”：哪些先做、哪些不做、兼容到哪里、变更要走什么手续，都有固定入口。新接手的人不用只靠聊天记录猜边界。",
        "gap": "它解决的是大方向和不可轻易返工的边界，不会替你回答每天先做哪条任务；日常状态仍要看 Dashboard 和具体 Session。",
    },
    "BI-002": {
        "capability": "用户已经能从本地仓库路径或带现有本地 checkout 的 GitHub 输入启动 P00，得到受 schema 约束的配置和源码清单；几个选定 Java/Python 仓库以及失败输入都有回归证据。",
        "gap": "还不是一个完整的 `semx init` 工作区管理器：自动 clone、私有仓库认证、branch/subdir、monorepo、压缩包、单文件和更广语言支持都没有被统一承诺。",
    },
    "BI-003": {
        "capability": "很多阶段产物已经不再只是文档描述，而有 JSON schema、示例、正反例和校验器。使用者可以更早知道“这个文件长什么样才算合格”。",
        "gap": "P00-P17 还没有全部达到同样深度；后半段质量循环、部分 P04 分类和跨阶段统一合同仍有空白，已有 schema 也不等于语义一定正确。",
    },
    "BI-004": {
        "capability": "Semx 已有正式 V2 runtime 骨架，选定路径能从 P00 走到 P05；还存在固定 P00-P17 inventory、阶段 adapter、trace、stop/replay 等有界 RCP 证据。用户可以实际调用一组命令，而不只是阅读架构图。",
        "gap": "这不是任意仓库都能一键跑通 P00-P17，也不是通用 scheduler/executor、生产控制面或完整 Runtime Kernel。许多“后半程”仍是 adapter、validator 或 test-only slice。",
    },
    "BI-005": {
        "capability": "早期正式运行能按 run-id 保存 history/latest，用户可以 inspect、resume，并在来源 lineage 不匹配时被拒绝，减少“拿错上一次结果继续跑”的风险。",
        "gap": "这些 lineage/storage 语义还没有等宽覆盖所有阶段，也不是高可用、并发安全、可运维的生产级持久化服务。",
    },
    "BI-006": {
        "capability": "仓库已有 lint/问题发现的早期表面，能为质量循环提供起点；相关方向和输出升级目标已经被显式登记。",
        "gap": "用户还拿不到统一、丰富、可排序的 issue 模型（维度、层级、规则类别、修复提示等）；因此严肃的自动 repair planning 仍缺稳定输入。",
    },
    "BI-007": {
        "capability": "仓库已经积累人工授权的 repair-revalidation witness、失败报告和若干 P13-P17 adapter/gate 证据，能演示“发现问题后如何受控地再验证”。",
        "gap": "还没有可泛化的自动问题图、修复计划、自动 apply、post-lint 和 convergence 产品闭环；当前证据不能解读成自动修复或自动收敛。",
    },
    "BI-008": {
        "capability": "项目有维护中的 contract tests、负例、跨仓库矩阵、BDD 人类可读卡片、分层 validation runner 和 closeout 证据。用户可以看到结论由哪些检查支撑。",
        "gap": "测试通过只证明对应范围；不自动证明语义正确、任意仓库泛化或生产可靠性。非功能、mutation/adversarial、真实长期运行等覆盖仍需继续建设。",
    },
    "BI-009": {
        "capability": "第一个可信垂直切片已经从 P00-P02 扩展出选定仓库的 P00-P05 路径，能从仓库输入产出阶段 artifact，并有重复执行和回归证据。",
        "gap": "它仍是选定样本/模式上的闭环，不是所有语言、所有 repo 和所有 P00-P17 阶段的统一终端体验。",
    },
    "BI-010": {
        "capability": "CLI 已分阶段暴露 config、manifest、evidence、M0.5、semantic flow/slice、M1 candidate、inspect 和部分 RCP 命令；命令宽度基本跟着已维护的 runtime/gate 走。",
        "gap": "还没有完整 init/workspace 管理、统一自动 clone/auth、远程仓库全流程和面向普通用户的一条龙产品界面；很多命令仍偏开发者/实验者。",
    },
    "BI-011": {
        "capability": "旧 demo 逻辑与 V2 正式实现已经有 keep/shim/rewrite/retire 清单；未来碰到旧模块时，有迁移基线可查。",
        "gap": "“已经分类”不等于所有旧代码都已删除或改写；实际 retire 仍要随具体实现批次推进。",
    },
    "BI-012": {
        "capability": "Dashboard 已形成 Current State、BI、SP、完整 Session registry、归档、索引、artifact index、closeout 和 DKG 派生图。新人可以从状态入口追到历史证据，旧 Session 也不会因归档而消失。",
        "gap": "执行记忆仍可能出现不同表面更新不同步；本次就发现 Stage Plan 源有 69 条而旧 DKG 只有 68 条，以及 BI-018/部分父状态存在旧快照。还需要更强的自动新鲜度/一致性检查。",
    },
    "BI-013": {
        "capability": "Semx 已把合同优先、Dashboard 治理、KB、LLM artifact 评估、问题驱动改进、KYM/TCO 等实践封装成多项可调用 Skill，并形成清晰的人机分工和审计流程。",
        "gap": "公开版本与 repo-local 版本仍有差距，很多 Skill 尚未有独立公开仓库或跨项目验证；S-496 仍在做最终独立验证，不能说全部都已开源成熟。",
    },
    "BI-014": {
        "capability": "复杂任务可以按 Stage Plan 运行 Design、Builder、Validation、Closure 和按需 Semantic Reviewer；有 lane card、人工 checkpoint、Agent Log、Goal conformance 和 closeout 证据。管理者可以少盯过程、多看边界和例外。",
        "gap": "这仍是 repo-local、强治理的工程运行方式，不是无人值守生产编排平台；通用并行调度、成本/SLO、故障恢复和低干预长期运行仍未完成。",
    },
    "BI-015": {
        "capability": "项目已能用 TBC、Co-Sight 等报告和 Current P05 Board，把“某个样本跑通”与“某类能力可泛化”分开讨论，并保存 held-out/负例/压力样本。",
        "gap": "Arena 仍主要是评估与主张纪律的 side-lane，不是完整维护中的 benchmark 产品、任意仓库证明或自动 release gate；不少候选 Session 被刻意停放。",
    },
    "BI-016": {
        "capability": "P06 已从单文件 evaluator 演进为分层模块：RuleSet、Assessment、Validation、DecisionRecord、ReviewResolution、最小 Formalizer/Committer、operator packet/queue 和 isolated SQLite archive prototype 都有有界测试证据。",
        "gap": "仍不能把它说成生产 canonicalization：没有获批的 production archive deployment/backfill、广泛 M1 family 支持、自动人工审批替代、Provider 语义权威或任意候选的 semantic correctness。",
    },
    "BI-018": {
        "capability": "ERBE 已把高语义风险 Goal 的“什么算成功、什么必须失败”提前冻结成 Contract/Cases、可信 RED→GREEN、runner、Goal Agent 集成和 pilot；用户能在写主要实现前先看到可执行验收边界。",
        "gap": "它还没有迁移到所有 Goal，也不会由有限 examples 自动证明完整语义真理。Big_Ideas 表仍保留旧的 `To do` 快照，而 Current State 已记录 bounded implementation landed，这是需要治理的新鲜度缺口。",
    },
    "BI-019": {
        "capability": "Provider-backed 路线已在选定 Python/Java 样本上形成受审批的真实调用、source-grounded candidate 投影、P06 no-write/eligible-write 治理和有界 Arena 对比。S-536 生成的 candidate-only r013 profile comparison 显示当前 in-scope parent Profile contract/implementation 都是 26/26 Met。",
        "gap": "r013 仍是 candidate_not_approved；这不是 Coverage/P06 批准、semantic correctness、maintained promotion、canonical/production readiness 或任意 Python/Java 支持。当前只剩 H-06 Git handoff，而 Git handoff 也不会把 candidate 自动变成批准或生产真值。",
    },
}


BI_POSTURE: dict[str, str] = {
    "BI-001": "dashboard_source_stated",
    "BI-002": "dashboard_reports_bounded_evidence",
    "BI-003": "dashboard_reports_bounded_evidence",
    "BI-004": "dashboard_reports_bounded_evidence",
    "BI-005": "dashboard_reports_bounded_evidence",
    "BI-006": "design_or_candidate_only",
    "BI-007": "design_or_candidate_only",
    "BI-008": "dashboard_reports_bounded_evidence",
    "BI-009": "dashboard_reports_bounded_evidence",
    "BI-010": "dashboard_reports_bounded_evidence",
    "BI-011": "dashboard_source_stated",
    "BI-012": "dashboard_reports_bounded_evidence",
    "BI-013": "dashboard_reports_bounded_evidence",
    "BI-014": "dashboard_reports_bounded_evidence",
    "BI-015": "design_or_candidate_only",
    "BI-016": "dashboard_reports_bounded_evidence",
    "BI-018": "source_conflict",
    "BI-019": "dashboard_reports_bounded_evidence",
}

COMMON_FORBIDDEN_UPLIFTS = [
    "测试通过 ≠ 语义正确",
    "候选或 Provider observation ≠ 人工批准",
    "有界样本 ≠ 任意仓库泛化",
    "Dashboard Done ≠ canonical truth 或 production readiness",
]

BI_EXTRA_BASIS: dict[str, list[tuple[str, int, str]]] = {
    "BI-013": [("Dashboard/Current_State.md", 57, "semx-skills-提炼与开源全景s-496")],
    "BI-016": [("Dashboard/Stage_Plans.md", 139, "sp-040")],
    "BI-018": [
        ("Dashboard/Current_State.md", 183, "erbe-规划入口2026-07-26"),
        ("Dashboard/Current_State.md", 145, "sp-063-goal-effect-integrity-当前执行状态2026-07-27"),
        ("Dashboard/Stage_Plans.md", 85, "sp-062"),
        ("Dashboard/Stage_Plans.md", 59, "sp-063"),
    ],
    "BI-019": [
        ("Dashboard/Current_State.md", 3, "sp-069-provider-backed-mainline-bounded-gap-evidence-delivery-当前入口2026-08-13"),
        ("Dashboard/Stage_Plans.md", 9, "sp-069"),
    ],
}


WAVES = [
    (1, 99, "奠基期", "宪法、P00-P05 第一条正式切片、artifact store 和 CLI 起步"),
    (100, 199, "扩面期", "三仓矩阵、P05 模式、质量门、Dashboard/人机方法与 Arena"),
    (200, 279, "治理成形期", "closeout、语义审查、P06 第一版、BDD readable cards 与运行编排准备"),
    (280, 379, "RCP / P06 架构期", "Runtime Kernel target、SAG observation、P06 V2 分层与 test-store vertical slices"),
    (380, 459, "受控运行期", "RCP ledger/re-entry/repair、P00-P17 selected adapters、统一 CLI 与 Provider 薄流水线"),
    (460, 499, "验收与执行记忆强化期", "Goal effect、ERBE、Session registry、Provider-backed Target 1 与上下文启动包"),
    (500, 999, "Provider-backed 主线期", "Target 2/3、evidence integrity、Coverage 边界和当前 SP-069 gap delivery"),
]


def clean_markdown(value: str) -> str:
    value = value or ""
    value = re.sub(r"<a\s+[^>]*></a>", "", value)
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", value)
    value = value.replace("<br>", "\n").replace("`", "")
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("\\|", "|")
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"(?:,?\s+and\s+\.)$", ".", value)
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def phase_tags(*values: str) -> list[str]:
    tags = sorted(
        set(re.findall(r"\bP(?:0[0-9]|1[0-7])\b", " ".join(values))),
        key=lambda item: int(item[1:]),
    )
    return tags or ["跨周期/未标 phase"]


def status_category(value: str) -> str:
    text = clean_markdown(value).lower()
    if text.startswith("done") or text.startswith("complete"):
        return "Done"
    if text.startswith("cancel") or "deferred-by-user" in text:
        return "Cancelled"
    if text.startswith("partial"):
        return "To do"
    if text.startswith("to do") or text.startswith("todo"):
        return "To do"
    if text.startswith("doing") or "terminal pending" in text or "git handoff next" in text:
        return "Doing"
    return "Other"


def parse_tables(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    header: list[str] | None = None
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        try:
            cells = [clean_markdown(cell) for cell in split_markdown_row(line)]
        except ValueError:
            continue
        if not cells:
            continue
        if cells[0] in {"ID", "当前 ID"}:
            header = cells
            continue
        if not header or all(re.fullmatch(r":?-+:?", cell or "-") for cell in cells):
            continue
        if len(cells) != len(header):
            continue
        values = dict(zip(header, cells))
        first = values.get("ID") or values.get("当前 ID") or ""
        if re.fullmatch(r"(?:BI|SP)-\d{3}", first):
            rows.append({"line": line_no, "header": header, "values": values})
    return rows


def source_ref(path: str, line: int = 1, anchor: str = "") -> dict[str, Any]:
    suffix = f"#{anchor}" if anchor else ""
    return {
        "path": path,
        "line": line,
        "anchor": anchor,
        "display": f"{path}:{line}",
        "href": f"../../{path}{suffix}",
    }


def phase_wave(number: int) -> dict[str, Any]:
    for lower, upper, name, summary in WAVES:
        if lower <= number <= upper:
            return {"id": f"{lower:03}-{upper if upper < 999 else 'latest'}", "name": name, "summary": summary}
    return {"id": "unknown", "name": "未分类", "summary": "编号不在当前阶段带中"}


def section_context(path: Path) -> dict[str, dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    sections: dict[str, dict[str, Any]] = {}
    current: str | None = None
    buffer: list[str] = []
    for line_no, line in enumerate(lines, 1):
        match = re.match(r"^##\s+(SP-\d{3})\s*[：:/-]?\s*(.*)$", line)
        if match:
            if current and current not in sections:
                sections[current] = {"intro": clean_markdown(" ".join(buffer)), "line": start_line, "title": title}
            current = match.group(1)
            title = re.sub(r"（[^）]*）\s*$", "", match.group(2)).strip()
            start_line = line_no
            buffer = []
            continue
        if current:
            if line.startswith("## "):
                if current not in sections:
                    sections[current] = {"intro": clean_markdown(" ".join(buffer)), "line": start_line, "title": title}
                current = None
                buffer = []
            elif not line.startswith("|") and not line.startswith("#") and line.strip():
                buffer.append(line.strip())
    if current and current not in sections:
        sections[current] = {"intro": clean_markdown(" ".join(buffer)), "line": start_line, "title": title}
    return sections


def load_big_ideas(repo: Path) -> list[dict[str, Any]]:
    path = repo / "Dashboard" / "Big_Ideas.md"
    records: dict[str, dict[str, Any]] = {}
    for row in parse_tables(path):
        values = row["values"]
        identifier = values.get("ID", "")
        if not identifier.startswith("BI-") or "Topic" not in values:
            continue
        status = values.get("Historical Status Snapshot") or values.get("Status") or "Other"
        records[identifier] = {
            "kind": "Big Idea",
            "id": identifier,
            "topic": values.get("Topic", ""),
            "scope": values.get("Scope", ""),
            "purpose": values.get("Purpose", ""),
            "status_raw": status,
            "status": status_category(status),
            "exit_criteria": values.get("Exit Criteria", ""),
            "canonical_target": values.get("Canonical Target", ""),
            "next_step": values.get("Next Step", ""),
            "notes": values.get("Notes", ""),
            "source": source_ref("Dashboard/Big_Ideas.md", row["line"], identifier.lower()),
            "evidence_posture": BI_POSTURE.get(identifier, "design_or_candidate_only"),
            "source_conflict": identifier == "BI-018",
            "forbidden_uplifts": list(COMMON_FORBIDDEN_UPLIFTS),
            "phase_tags": phase_tags(*values.values()),
            **BI_PLAIN_LANGUAGE.get(identifier, {"capability": "当前能力需要从源行继续阅读。", "gap": "尚未形成人类可读缺口说明。"}),
        }
    if set(records) != set(BI_PLAIN_LANGUAGE) or set(records) != set(BI_POSTURE):
        raise ValueError(
            "Big Idea explanation keys drifted from Dashboard source: "
            f"source={sorted(records)} explanations={sorted(BI_PLAIN_LANGUAGE)} posture={sorted(BI_POSTURE)}"
        )
    return sorted(records.values(), key=lambda item: int(item["id"].split("-")[1]))


def load_sessions(repo: Path) -> list[dict[str, Any]]:
    dashboard = repo / "Dashboard"
    index_rows = parse_index(dashboard / "Session_Index.md")
    index_by_key = {row["Session Key"]: row for row in index_rows}
    located: list[tuple[Any, Path, str]] = []
    located.extend((record, dashboard / "Sessions.md", "current") for record in parse_registry_file(dashboard / "Sessions.md"))
    for path in sorted((dashboard / "Archives" / "Sessions").glob("*.md")):
        if path.name == "Legacy_Execution_Notes.md":
            continue
        located.extend((record, path, "archive") for record in parse_registry_file(path))
    sessions: list[dict[str, Any]] = []
    actual_keys = {record.session_key for record, _, _ in located}
    if actual_keys != set(index_by_key):
        raise ValueError(
            "Session index/record join drift: "
            f"missing_in_index={sorted(actual_keys - set(index_by_key))} "
            f"missing_record={sorted(set(index_by_key) - actual_keys)}"
        )
    for record, path, surface in located:
        relative = path.relative_to(repo).as_posix()
        wave = phase_wave(record.numeric_id)
        tracks = re.findall(r"BI-\d{3}", record.track)
        index_row = index_by_key[record.session_key]
        if index_row["Status"] != record.status:
            raise ValueError(
                f"Session index status drift for {record.session_key}: "
                f"index={index_row['Status']} record={record.status}"
            )
        phases = phase_tags(
            record.topic,
            record.scope,
            record.purpose,
            record.deliverable,
            record.next_step,
            record.notes,
        )
        sessions.append({
            "kind": "Session",
            "id": record.session_key,
            "historical_id": record.historical_id,
            "parent": record.parent,
            "topic": clean_markdown(record.topic),
            "scope": clean_markdown(record.scope),
            "purpose": clean_markdown(record.purpose),
            "tracks": tracks,
            "track_raw": clean_markdown(record.track),
            "priority": clean_markdown(record.priority),
            "status_raw": clean_markdown(record.status),
            "status": status_category(record.status),
            "historical_status": clean_markdown(record.historical_status),
            "depends_on": clean_markdown(record.depends_on),
            "deliverable": clean_markdown(record.deliverable),
            "exit_criteria": clean_markdown(record.exit_criteria),
            "next_step": clean_markdown(record.next_step),
            "notes": clean_markdown(record.notes),
            "surface": surface,
            "wave": wave["id"],
            "wave_name": wave["name"],
            "phase_tags": phases,
            "evidence_posture": "dashboard_source_stated",
            "source_conflict": False,
            "primary_evidence": clean_markdown(index_row.get("Primary Evidence", "")),
            "index_location": clean_markdown(index_row.get("Location", "")),
            "source": source_ref(relative, record.source_line, record.anchor),
        })
    return sorted(sessions, key=lambda item: (int(re.search(r"S-(\d{3})", item["historical_id"]).group(1)), item["id"]))


def load_stage_plans(repo: Path, sessions: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    path = repo / "Dashboard" / "Stage_Plans.md"
    rows = [row for row in parse_tables(path) if (row["values"].get("ID") or row["values"].get("当前 ID", "")).startswith("SP-")]
    parsed_lines = {row["line"] for row in rows}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line_no in parsed_lines or not line.startswith("|"):
            continue
        try:
            cells = split_markdown_row(line)
        except ValueError:
            continue
        identifier = clean_markdown(cells[0]) if cells else ""
        if re.fullmatch(r"SP-\d{3}", identifier):
            rows.append({
                "line": line_no,
                "header": ["ID", "Raw Row"],
                "values": {"ID": identifier, "Raw Row": clean_markdown(" | ".join(cells[1:]))},
            })
    rows.sort(key=lambda row: row["line"])
    sections = section_context(path)
    occurrences: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        identifier = row["values"].get("ID") or row["values"].get("当前 ID")
        occurrences[identifier].append(row)
    by_parent: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for session in sessions:
        if session["parent"].startswith("SP-"):
            by_parent[session["parent"]].append(session)
    plans: list[dict[str, Any]] = []
    for identifier, candidates in occurrences.items():
        def richness(candidate: dict[str, Any]) -> tuple[int, int]:
            values = candidate["values"]
            useful = sum(bool(values.get(key)) for key in ("Topic", "Scope", "Purpose", "Sessions", "Backlog", "Required Gates", "Gate Pack", "Claim Ceiling", "Next", "Next Step", "Notes"))
            return useful, -candidate["line"]

        rich = max(candidates, key=richness)
        current = next((candidate for candidate in candidates if "当前 ID" in candidate["values"]), None)
        values = rich["values"]
        current_values = current["values"] if current else {}
        section = sections.get(identifier, {})
        actual_sessions = by_parent.get(identifier, [])
        bis = sorted({bi for session in actual_sessions for bi in session["tracks"]})
        raw_status = (
            current_values.get("当前权威状态")
            or values.get("Historical Status Snapshot")
            or values.get("Status")
            or "Other"
        )
        evidence = current_values.get("入口与边界") or current_values.get("当前证据") or values.get("Current Entry") or ""
        intro = section.get("intro", "")
        scope = values.get("Scope") or intro
        purpose = values.get("Purpose") or "把相关 Session 作为一个有明确边界、门禁和退出条件的执行批次来管理。"
        topic = values.get("Topic") or section.get("title") or identifier
        occurrence_rows = [
            {
                "line": candidate["line"],
                "fields": candidate["values"],
                "source": source_ref("Dashboard/Stage_Plans.md", candidate["line"], identifier.lower()),
            }
            for candidate in candidates
        ]
        conflict_fields: dict[str, list[str]] = {}
        for field in (
            "Historical Status Snapshot",
            "Status",
            "当前权威状态",
            "Topic",
            "Scope",
            "Purpose",
            "Next",
            "Next Step",
            "Claim Ceiling",
        ):
            distinct = sorted(
                {
                    clean_markdown(candidate["values"].get(field, ""))
                    for candidate in candidates
                    if clean_markdown(candidate["values"].get(field, ""))
                }
            )
            if len(distinct) > 1:
                conflict_fields[field] = distinct
        plan_phases = phase_tags(
            topic,
            scope,
            purpose,
            values.get("Sessions", ""),
            values.get("Next", ""),
            values.get("Next Step", ""),
            intro,
        )
        plans.append({
            "kind": "Stage Plan",
            "id": identifier,
            "topic": topic,
            "scope": clean_markdown(scope),
            "purpose": clean_markdown(purpose),
            "status_raw": clean_markdown(raw_status),
            "status": status_category(raw_status),
            "bis": bis,
            "sessions": [session["id"] for session in actual_sessions],
            "session_count": len(actual_sessions),
            "session_status_counts": dict(Counter(session["status"] for session in actual_sessions)),
            "current_entry": clean_markdown(evidence),
            "required_gates": clean_markdown(values.get("Required Gates") or values.get("Gate Pack") or ""),
            "claim_ceiling": clean_markdown(values.get("Claim Ceiling") or values.get("Exit Criteria") or ""),
            "next_step": clean_markdown(values.get("Next") or values.get("Next Step") or ""),
            "notes": clean_markdown(values.get("Notes") or ""),
            "row_occurrences": len(candidates),
            "occurrences": occurrence_rows,
            "source_conflict": bool(conflict_fields) or len(candidates) > 1,
            "conflict_fields": conflict_fields,
            "evidence_posture": "dashboard_source_stated",
            "phase_tags": plan_phases,
            "source": source_ref("Dashboard/Stage_Plans.md", (current or rich)["line"], identifier.lower()),
            "sources": [entry["source"] for entry in occurrence_rows],
        })
    return sorted(plans, key=lambda item: int(item["id"].split("-")[1])), len(rows)


def enrich_big_ideas(big_ideas: list[dict[str, Any]], stage_plans: list[dict[str, Any]], sessions: list[dict[str, Any]]) -> None:
    for idea in big_ideas:
        identifier = idea["id"]
        owned_sessions = [session for session in sessions if identifier in session["tracks"]]
        owned_plans = [plan for plan in stage_plans if identifier in plan["bis"]]
        idea["session_count"] = len(owned_sessions)
        idea["session_status_counts"] = dict(Counter(session["status"] for session in owned_sessions))
        idea["sp_count"] = len(owned_plans)
        idea["stage_plans"] = [plan["id"] for plan in owned_plans]
        candidate_refs = [idea["source"]]
        candidate_refs.extend(
            source_ref(path, line, anchor)
            for path, line, anchor in BI_EXTRA_BASIS.get(identifier, [])
        )
        candidate_refs.extend(plan["source"] for plan in owned_plans)
        seen: set[tuple[str, int, str]] = set()
        basis_refs: list[dict[str, Any]] = []
        for ref in candidate_refs:
            identity = (ref["path"], ref["line"], ref["anchor"])
            if identity in seen:
                continue
            seen.add(identity)
            basis_refs.append(ref)
        idea["basis_refs"] = basis_refs


def build_source_manifest(repo: Path) -> list[dict[str, Any]]:
    paths = [
        "Dashboard/Big_Ideas.md",
        "Dashboard/Stage_Plans.md",
        "Dashboard/Sessions.md",
        "Dashboard/Session_Index.md",
        "Dashboard/Archives/Sessions/archive_manifest.json",
        "Dashboard/Current_State.md",
        "Dashboard/Decisions.md",
        "Dashboard/Risks.md",
        "Dashboard/Quality_Metrics.md",
        "Dashboard/Artifacts/Dashboard_Operating_Graph.json",
        "semx-kb/docs/strategy/Strategy_Semantic_Surface_Engineering.md",
        "semx-kb/docs/strategy/Strategy_Human_AI_Development.md",
        "semx-kb/data/strategy/strategy_sgc_structural_contract_v1.json",
    ]
    manifest: list[dict[str, Any]] = []
    for relative in paths:
        path = repo / relative
        text = path.read_text(encoding="utf-8")
        manifest.append({
            "path": relative,
            "sha256": sha256_file(path),
            "line_count": len(text.splitlines()),
            "href": f"../../{relative}",
        })
    archive_paths = sorted(
        path
        for path in (repo / "Dashboard" / "Archives" / "Sessions").glob("*.md")
        if path.name != "Legacy_Execution_Notes.md"
    )
    archive_digest = hashlib.sha256()
    archive_lines = 0
    for path in archive_paths:
        relative = path.relative_to(repo).as_posix()
        archive_digest.update(relative.encode("utf-8"))
        archive_digest.update(b"\0")
        archive_digest.update(path.read_bytes())
        archive_digest.update(b"\0")
        archive_lines += len(path.read_text(encoding="utf-8").splitlines())
    manifest.append({
        "path": "Dashboard/Archives/Sessions/*.md",
        "sha256": archive_digest.hexdigest(),
        "line_count": archive_lines,
        "file_count": len(archive_paths),
        "href": "../../Dashboard/Archives/Sessions/",
    })
    return manifest


def validate_data(data: dict[str, Any]) -> None:
    counts = data["counts"]
    idea_ids = {item["id"] for item in data["big_ideas"]}
    plan_ids = {item["id"] for item in data["stage_plans"]}
    session_keys = [item["id"] for item in data["sessions"]]
    if idea_ids != set(BI_PLAIN_LANGUAGE) or "BI-017" in idea_ids:
        raise ValueError(f"Big Idea inventory mismatch: {sorted(idea_ids)}")
    expected_plans = {f"SP-{number:03}" for number in range(1, 70)}
    if plan_ids != expected_plans:
        raise ValueError(
            f"Stage Plan inventory mismatch: missing={sorted(expected_plans-plan_ids)} extra={sorted(plan_ids-expected_plans)}"
        )
    if counts["stage_plan_row_occurrences"] != sum(item["row_occurrences"] for item in data["stage_plans"]):
        raise ValueError("Stage Plan occurrence total is not internally consistent")
    if len(session_keys) != len(set(session_keys)):
        raise ValueError("duplicate canonical Session Key in panorama dataset")
    if counts["sessions"] != counts["current_sessions"] + counts["archived_sessions"]:
        raise ValueError("Session current/archive totals do not close")
    if sum(counts["session_statuses"].values()) != counts["sessions"]:
        raise ValueError("Session status totals do not close")
    cross = data["registry_cross_check"]
    if not (
        counts["sessions"]
        == cross["record_count"]
        == cross["index_count"]
        == cross["dkg_sessions"]
    ):
        raise ValueError(f"Session registry/DKG cross-check mismatch: {cross}")
    required_collision_keys = {
        "SP-063/S-477", "SP-064/S-477",
        "SP-063/S-478", "SP-064/S-478",
        "SP-063/S-479", "SP-064/S-479",
    }
    if not required_collision_keys.issubset(set(session_keys)):
        raise ValueError("historical Session collision families were not all preserved")
    for idea in data["big_ideas"]:
        refs = idea.get("basis_refs", [])
        if not refs or any(not ref.get("href") for ref in refs):
            raise ValueError(f"Big Idea basis refs are incomplete: {idea['id']}")
    for identifier in ("BI-018", "BI-019"):
        idea = next(item for item in data["big_ideas"] if item["id"] == identifier)
        paths = {ref["path"] for ref in idea["basis_refs"]}
        required = {"Dashboard/Big_Ideas.md", "Dashboard/Current_State.md", "Dashboard/Stage_Plans.md"}
        if not required.issubset(paths):
            raise ValueError(f"{identifier} basis refs do not expose all claim-bearing Dashboard surfaces: {sorted(paths)}")


def build_data(repo: Path, generated_on: str) -> dict[str, Any]:
    sessions = load_sessions(repo)
    big_ideas = load_big_ideas(repo)
    stage_plans, stage_plan_occurrences = load_stage_plans(repo, sessions)
    enrich_big_ideas(big_ideas, stage_plans, sessions)
    registry_manifest = json.loads((repo / "Dashboard" / "Archives" / "Sessions" / "archive_manifest.json").read_text(encoding="utf-8"))
    dkg = json.loads((repo / "Dashboard" / "Artifacts" / "Dashboard_Operating_Graph.json").read_text(encoding="utf-8"))
    dkg_counts = Counter(node.get("type") for node in dkg.get("nodes", []))
    current_state_text = (repo / "Dashboard" / "Current_State.md").read_text(encoding="utf-8")
    bi018 = next((idea for idea in big_ideas if idea["id"] == "BI-018"), None)
    dkg_stage_plan_drift = dkg_counts["StagePlan"] != len(stage_plans)
    bi018_freshness_conflict = bool(
        bi018
        and bi018.get("status_raw") == "To do"
        and "SP-062 goal_terminal=true" in current_state_text
    )
    wave_counts = Counter(session["wave"] for session in sessions)
    waves = [
        {"id": f"{lower:03}-{upper if upper < 999 else 'latest'}", "name": name, "summary": summary, "count": wave_counts[f"{lower:03}-{upper if upper < 999 else 'latest'}"]}
        for lower, upper, name, summary in WAVES
    ]
    data_quality = []
    if dkg_stage_plan_drift:
        data_quality.append({
            "code": "DKG_STAGE_PLAN_DRIFT",
            "level": "warning",
            "title": "Stage Plan 源表与 DKG 计数不一致",
            "detail": f"Stage_Plans.md 有 {len(stage_plans)} 个唯一 SP、{stage_plan_occurrences} 次 row occurrence；当前 DKG 有 {dkg_counts['StagePlan']} 个 StagePlan。本全景以 Markdown 源表为准。",
        })
    else:
        data_quality.append({
            "code": "DKG_STAGE_PLAN_FRESH",
            "level": "info",
            "title": "Stage Plan 源表与 DKG 已对齐",
            "detail": f"Stage_Plans.md 有 {len(stage_plans)} 个唯一 SP、{stage_plan_occurrences} 次 row occurrence；当前 DKG 也有 {dkg_counts['StagePlan']} 个 StagePlan。使用 special current table 的 SP-064 已被识别为 StagePlan 节点。",
        })
    data_quality.extend([
        {
            "code": "BUILD_BASELINE_SOURCE_DRIFT",
            "level": "warning",
            "title": "生成期间 Session 源从 536 条更新为当前分母",
            "detail": f"Design 时点是 536 records / 118 current / 418 archive；生成时 repo 已更新为 {len(sessions)} / {sum(session['surface']=='current' for session in sessions)} / {sum(session['surface']=='archive' for session in sessions)}。本页按最终源重新生成，不回填旧数字。",
        }
    ])
    if bi018_freshness_conflict:
        data_quality.append({
            "code": "BI018_SOURCE_FRESHNESS_CONFLICT",
            "level": "warning",
            "title": "BI-018 父行保留旧状态快照",
            "detail": "Big_Ideas.md 的 BI-018 仍写 To do，但 Current_State.md 已明确 S-466..S-471 bounded implementation landed、SP-062 goal_terminal=true。全景保留源状态并在能力说明中标注该新鲜度缺口。",
        })
    else:
        data_quality.append({
            "code": "BI018_SOURCE_FRESHNESS_RECONCILED",
            "level": "info",
            "title": "BI-018 父行新鲜度已对齐",
            "detail": "Big_Ideas.md 的 BI-018 父行已从旧 To do 更新为 Doing，并保留 SP-062/SP-063 的 bounded claim ceiling；这不是全历史迁移、production 或 canonical authority 声明。",
        })
    data_quality.extend([
        {
            "code": "SESSION_PARENT_QUALIFIED_IDENTITY",
            "level": "info",
            "title": "历史 Session 重号已用父级身份隔离",
            "detail": "S-477、S-478、S-479 在 SP-063 与 SP-064 下都出现过；Session Key 使用 SP-xxx/S-xxx，不会把它们合并。",
        },
        {
            "code": "BI_ASSOCIATION_OVERLAP",
            "level": "info",
            "title": "一个 Session 可以属于多个 BI",
            "detail": f"BI 卡片中的 Session 数是关联数，跨 BI 相加可能大于 {len(sessions)}；这表示同一工作同时服务多个长期方向，不是重复记录。",
        },
    ])
    quality_recommendation = (
        {
            "type": "质量 / 稳定性 proposal",
            "title": "修复 Dashboard 派生新鲜度",
            "detail": "让 DKG parser 识别 Stage_Plans.md 的 special current table，并同步 parent row freshness；这是提案，不是已登记 Session。",
        }
        if dkg_stage_plan_drift or bi018_freshness_conflict
        else {
            "type": "质量 / 稳定性 proposal",
            "title": "把 Dashboard 派生新鲜度纳入例行防回归",
            "detail": "当前 DKG 已识别 SP-064 special current table，BI-018 父行也已对齐；后续重点是把这类 source-vs-derived freshness 检查维持在 Dashboard gate 中。",
        }
    )
    result = {
        "schema_version": "semx_full_cycle_dashboard_panorama_v1",
        "generated_on": generated_on,
        "authority": "Dashboard Markdown / Session registry 是 execution-memory authority；semx-kb 是 canonical truth；本 HTML 只是离线派生读模型。",
        "claim_ceiling": "current-repo-derived full-cycle Dashboard panorama；不证明生产成熟度、任意 repo 泛化或 semantic correctness。",
        "counts": {
            "big_ideas": len(big_ideas),
            "stage_plans": len(stage_plans),
            "stage_plan_row_occurrences": stage_plan_occurrences,
            "sessions": len(sessions),
            "current_sessions": sum(session["surface"] == "current" for session in sessions),
            "archived_sessions": sum(session["surface"] == "archive" for session in sessions),
            "session_statuses": dict(Counter(session["status"] for session in sessions)),
            "stage_plan_statuses": dict(Counter(plan["status"] for plan in stage_plans)),
            "big_idea_statuses": dict(Counter(idea["status"] for idea in big_ideas)),
        },
        "registry_cross_check": {
            "record_count": registry_manifest.get("record_count"),
            "current_count": registry_manifest.get("current_count"),
            "archive_count": registry_manifest.get("archive_count"),
            "index_count": registry_manifest.get("index_count"),
            "dkg_big_ideas": dkg_counts["BigIdea"],
            "dkg_stage_plans": dkg_counts["StagePlan"],
            "dkg_sessions": dkg_counts["Session"],
        },
        "current_doing_sessions": [session["id"] for session in sessions if session["status"] == "Doing"],
        "waves": waves,
        "data_quality": data_quality,
        "recommendations": [
            quality_recommendation,
            {
                "type": "速度 / 进度 proposal",
                "title": "完成 SP-069 H-06 Git handoff",
                "detail": "只完成已经 ready 的 repo handoff；保持 r013 candidate_not_approved，不把 Git 状态写成 Coverage/P06/production 批准。",
            },
            {
                "type": "探索性 proposal",
                "title": "做一个 selected repo 的新人演示入口",
                "detail": "把本全景与一个可定位的端到端样本串起来，帮助外部听众从项目方向下钻到真实 artifact；不借演示扩大产品能力主张。",
            },
        ],
        "big_ideas": big_ideas,
        "stage_plans": stage_plans,
        "sessions": sessions,
        "source_manifest": build_source_manifest(repo),
    }
    validate_data(result)
    return result


HTML_TEMPLATE = r'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; font-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'">
<title>Semx-cli 全仓全周期 Dashboard 全景图</title>
<style>
:root{color-scheme:light;--bg:#f4f7fb;--panel:#fff;--ink:#172033;--muted:#667085;--line:#dfe5ef;--brand:#3758d3;--brand2:#7a4de8;--good:#16794a;--warn:#a25b00;--bad:#b42318;--info:#2463a5;--shadow:0 12px 30px rgba(37,49,79,.08);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:linear-gradient(145deg,#eef3ff 0,#f8fafc 38%,#f5f0ff 100%);font-size:14px;line-height:1.6}.shell{max-width:1500px;margin:auto;padding:28px}.hero{padding:30px;border:1px solid rgba(55,88,211,.18);border-radius:24px;background:linear-gradient(135deg,rgba(255,255,255,.96),rgba(244,242,255,.94));box-shadow:var(--shadow)}h1{font-size:clamp(28px,4vw,48px);line-height:1.12;margin:0 0 12px;letter-spacing:-.03em}.eyebrow{color:var(--brand);font-weight:800;letter-spacing:.08em;text-transform:uppercase}.lede{font-size:17px;max-width:980px;color:#3e4a61}.ceiling{margin-top:18px;padding:14px 16px;border-left:4px solid var(--warn);background:#fff8e8;border-radius:8px}.metrics{display:grid;grid-template-columns:repeat(6,minmax(100px,1fr));gap:12px;margin-top:22px}.metric{padding:16px;background:#fff;border:1px solid var(--line);border-radius:16px}.metric b{display:block;font-size:25px;line-height:1.1}.metric span{color:var(--muted);font-size:12px}.tabs{position:sticky;top:0;z-index:20;display:flex;gap:8px;margin:18px 0;padding:10px;background:rgba(244,247,251,.92);backdrop-filter:blur(12px);border:1px solid rgba(223,229,239,.8);border-radius:16px}.tabs button,.btn{border:0;border-radius:11px;padding:10px 14px;background:#fff;color:var(--ink);cursor:pointer;font-weight:700}.tabs button.active{background:var(--brand);color:#fff}.panel{background:rgba(255,255,255,.96);border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow);padding:20px;margin:18px 0}.section-title{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:16px}.section-title h2{margin:0;font-size:22px}.section-title p{margin:0;color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.card{border:1px solid var(--line);border-radius:17px;padding:18px;background:#fff;min-width:0}.card h3{margin:4px 0 6px;font-size:18px}.card p{margin:8px 0}.subtle{color:var(--muted)}.tag-row{display:flex;flex-wrap:wrap;gap:6px}.tag,.status{display:inline-flex;align-items:center;gap:5px;border-radius:999px;padding:4px 9px;background:#eef2ff;color:#3447a5;font-size:12px;font-weight:700}.status.Done{background:#e8f7ef;color:var(--good)}.status.Doing{background:#fff2d8;color:var(--warn)}.status.To-do{background:#e8f1ff;color:var(--info)}.status.Cancelled,.status.Partial,.status.Other{background:#fbe9e7;color:var(--bad)}.cap{border-top:1px solid var(--line);padding-top:10px}.cap strong{color:var(--good)}.gap strong{color:var(--bad)}.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:9px;align-items:end}.filters .search{grid-column:span 2}.filters label{display:grid;gap:4px;color:var(--muted);font-size:12px;font-weight:700}.filters input,.filters select{width:100%;padding:10px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}.timeline{display:grid;grid-template-columns:repeat(7,1fr);gap:10px}.wave{padding:13px;border-radius:14px;background:linear-gradient(160deg,#f4f6ff,#fff);border:1px solid var(--line)}.wave b{font-size:18px}.wave small{display:block;color:var(--muted)}.notice{border:1px solid var(--line);border-left:4px solid var(--info);padding:13px 14px;border-radius:10px;background:#f7fbff;margin:9px 0}.notice.warning{border-left-color:var(--warn);background:#fffaf0}.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:14px}table{border-collapse:collapse;width:100%;min-width:1000px}th,td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:top}th{position:sticky;top:0;background:#f6f8fc;z-index:2;font-size:12px;color:var(--muted)}tr:hover td{background:#fafbff}.link-button{border:0;background:none;padding:0;color:var(--brand);font:inherit;font-weight:800;cursor:pointer;text-align:left}.truncate{max-width:430px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.pager{display:flex;align-items:center;justify-content:space-between;margin-top:12px}.pager .controls{display:flex;gap:8px}.drawer{position:fixed;inset:0;z-index:60;background:rgba(21,28,44,.48);display:none;justify-content:flex-end}.drawer.open{display:flex}.drawer-card{height:100%;width:min(720px,94vw);overflow:auto;background:#fff;padding:26px;box-shadow:-16px 0 40px rgba(0,0,0,.16)}.drawer-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-start}.drawer-head h2{margin:0}.close{border:0;background:#eef1f6;width:38px;height:38px;border-radius:50%;cursor:pointer;font-size:20px}.detail-grid{display:grid;grid-template-columns:140px 1fr;gap:9px 14px;margin-top:20px}.detail-grid dt{color:var(--muted);font-weight:700}.detail-grid dd{margin:0;white-space:pre-wrap;overflow-wrap:anywhere}.empty{text-align:center;padding:48px;color:var(--muted)}.foot{color:var(--muted);font-size:12px;padding:12px 2px 32px}.mobile-only{display:none}.source-link{color:var(--brand);font-weight:750;text-decoration:none}.source-link:hover{text-decoration:underline}.proposal{border-top:4px solid var(--brand2)}
@media(max-width:1100px){.metrics{grid-template-columns:repeat(3,1fr)}.filters{grid-template-columns:repeat(3,1fr)}.filters .search{grid-column:1/-1}.timeline{grid-template-columns:repeat(3,1fr)}}
@media(max-width:720px){.shell{padding:12px}.hero{padding:20px}.metrics,.grid,.timeline,.filters{grid-template-columns:1fr}.tabs{overflow:auto}.tabs button{white-space:nowrap}.detail-grid{grid-template-columns:1fr}.detail-grid dt{margin-top:10px}}
</style>
</head>
<body>
<main class="shell">
  <section class="hero">
    <div class="eyebrow">Semx-cli · Full repository · Full cycle</div>
    <h1>Semx-cli Dashboard 全景图</h1>
    <p class="lede">给第一次接触 Semx 的人：这张图先回答“现在用户能感觉到什么、还有什么不能做”，再允许你下钻到每一个 Big Idea、Stage Plan 和当前/归档 Session。它覆盖整个 repo 生命周期，不只展示最近一批工作。</p>
    <div class="ceiling"><strong>先记住边界：</strong><span id="claim-ceiling"></span></div>
    <div class="metrics" id="metrics"></div>
  </section>

  <nav class="tabs" aria-label="全景视图">
    <button data-view="overview" class="active">全景总览</button>
    <button data-view="bi">大方向（BI）</button>
    <button data-view="sp">执行批次（SP）</button>
    <button data-view="session">全部 Sessions</button>
    <button data-view="source">数据口径</button>
  </nav>

  <section class="panel" id="filter-panel">
    <div class="section-title"><div><h2>筛选器</h2><p>筛选只改变当前视图，不改变 Dashboard 状态。</p></div><strong id="result-count" aria-live="polite"></strong></div>
    <div class="filters">
      <label class="search">关键词<input id="q" type="search" placeholder="例如 P06、Provider、repair、S-477"></label>
      <label>状态<select id="status"><option value="">全部状态</option></select></label>
      <label>优先级<select id="priority"><option value="">全部优先级</option></select></label>
      <label>Big Idea<select id="bi"><option value="">全部 BI</option></select></label>
      <label>Stage Plan<select id="sp"><option value="">全部 SP</option></select></label>
      <label>当前/归档<select id="surface"><option value="">全部</option><option value="current">当前表</option><option value="archive">历史归档</option></select></label>
      <label>历史波次<select id="wave"><option value="">全部波次</option></select></label>
      <label>P00-P17 阶段<select id="phase"><option value="">全部阶段</option></select></label>
      <label>证据姿态<select id="posture"><option value="">全部姿态</option></select></label>
      <label>只看源冲突<select id="conflict"><option value="">全部</option><option value="yes">只看有冲突</option></select></label>
      <label>排序<select id="sort"><option value="source">源顺序</option><option value="id">ID</option><option value="priority">优先级</option><option value="status">状态</option></select></label>
      <button class="btn" id="reset">清空</button>
    </div>
  </section>

  <div id="content"></div>
  <footer class="foot" id="footer"></footer>
</main>
<aside class="drawer" id="drawer" aria-hidden="true"><div class="drawer-card"><div class="drawer-head"><div><span class="tag" id="drawer-kind"></span><h2 id="drawer-title"></h2></div><button class="close" id="drawer-close" aria-label="关闭">×</button></div><dl class="detail-grid" id="drawer-detail"></dl></div></aside>
<script id="panorama-data" type="application/json">__DATA__</script>
<script>
(() => {
  "use strict";
  const data = JSON.parse(document.getElementById("panorama-data").textContent);
  const $ = id => document.getElementById(id);
  const state = {view:"overview", page:1, pageSize:50};
  const filters = {q:$("q"),status:$("status"),priority:$("priority"),bi:$("bi"),sp:$("sp"),surface:$("surface"),wave:$("wave"),phase:$("phase"),posture:$("posture"),conflict:$("conflict")};
  const sortSelect=$("sort");
  const safe = value => String(value ?? "").replace(/[&<>\"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const statusClass = value => String(value).replaceAll(" ","-");
  const badge = value => `<span class="status ${statusClass(value)}">${safe(value)}</span>`;
  const unique = values => [...new Set(values.filter(Boolean))].sort((a,b)=>String(a).localeCompare(String(b),"zh-CN",{numeric:true}));
  const addOptions = (el, values, label=x=>x) => unique(values).forEach(value => {const o=document.createElement("option");o.value=value;o.textContent=label(value);el.appendChild(o)});
  addOptions(filters.status,[...data.big_ideas,...data.stage_plans,...data.sessions].map(x=>x.status));
  addOptions(filters.priority,data.sessions.map(x=>x.priority));
  addOptions(filters.bi,data.big_ideas.map(x=>x.id),v=>`${v} · ${data.big_ideas.find(x=>x.id===v)?.topic||""}`);
  addOptions(filters.sp,data.stage_plans.map(x=>x.id),v=>`${v} · ${data.stage_plans.find(x=>x.id===v)?.topic||""}`);
  addOptions(filters.wave,data.waves.map(x=>x.id),v=>`${v} · ${data.waves.find(x=>x.id===v)?.name||""}`);
  addOptions(filters.phase,[...data.big_ideas,...data.stage_plans,...data.sessions].flatMap(x=>x.phase_tags||[]));
  addOptions(filters.posture,[...data.big_ideas,...data.stage_plans,...data.sessions].map(x=>x.evidence_posture));

  function readHash(){const p=new URLSearchParams(location.hash.replace(/^#/,""));const view=p.get("view");if(["overview","bi","sp","session","source"].includes(view))state.view=view;state.page=Math.max(1,Number(p.get("page")||1));Object.entries(filters).forEach(([key,el])=>{if(p.has(key))el.value=p.get(key)||""});if(p.has("sort"))sortSelect.value=p.get("sort")||"source"}
  function writeHash(){const p=new URLSearchParams();p.set("view",state.view);if(state.page>1)p.set("page",String(state.page));Object.entries(filters).forEach(([key,el])=>{if(el.value)p.set(key,el.value)});if(sortSelect.value!=="source")p.set("sort",sortSelect.value);history.replaceState(null,"",`#${p}`)}
  readHash();document.querySelectorAll("[data-view]").forEach(x=>x.classList.toggle("active",x.dataset.view===state.view));

  $("claim-ceiling").textContent=data.claim_ceiling;
  const c=data.counts;
  $("metrics").innerHTML=[
    [c.big_ideas,"当前登记 BI"],[c.stage_plans,"全周期唯一 SP"],[c.sessions,"全部 Session"],[c.current_sessions,"当前表 Session"],[c.archived_sessions,"归档 Session"],[c.session_statuses.Doing||0,"正在进行 Session"]
  ].map(([v,l])=>`<div class="metric"><b>${safe(v)}</b><span>${safe(l)}</span></div>`).join("");
  $("footer").textContent=`生成日期：${data.generated_on}。${data.authority}`;

  function searchBlob(item){return Object.values(item).flatMap(v=>Array.isArray(v)?v:[typeof v==="object"?JSON.stringify(v):v]).join(" ").toLowerCase()}
  function matches(item,kind){
    const q=filters.q.value.trim().toLowerCase(); if(q&&!searchBlob(item).includes(q))return false;
    if(filters.status.value&&item.status!==filters.status.value)return false;
    if(filters.priority.value&&item.priority!==filters.priority.value)return false;
    if(filters.bi.value){const ids=kind==="bi"?[item.id]:(kind==="sp"?item.bis:item.tracks);if(!ids?.includes(filters.bi.value))return false}
    if(filters.sp.value){if(kind==="sp"&&item.id!==filters.sp.value)return false;if(kind==="session"&&item.parent!==filters.sp.value)return false;if(kind==="bi"&&!item.stage_plans?.includes(filters.sp.value))return false}
    if(filters.surface.value&&kind==="session"&&item.surface!==filters.surface.value)return false;
    if(filters.wave.value&&kind==="session"&&item.wave!==filters.wave.value)return false;
    if(filters.phase.value&&!(item.phase_tags||[]).includes(filters.phase.value))return false;
    if(filters.posture.value&&item.evidence_posture!==filters.posture.value)return false;
    if(filters.conflict.value==="yes"&&!item.source_conflict)return false;
    return true;
  }
  function filtered(kind){const items=kind==="bi"?data.big_ideas:kind==="sp"?data.stage_plans:data.sessions;const result=items.filter(x=>matches(x,kind));if(sortSelect.value==="id")result.sort((a,b)=>a.id.localeCompare(b.id,"zh-CN",{numeric:true}));if(sortSelect.value==="priority")result.sort((a,b)=>(a.priority||"Z").localeCompare(b.priority||"Z")||a.id.localeCompare(b.id,"zh-CN",{numeric:true}));if(sortSelect.value==="status")result.sort((a,b)=>a.status.localeCompare(b.status)||a.id.localeCompare(b.id,"zh-CN",{numeric:true}));return result}
  function tags(values){return (values||[]).slice(0,10).map(v=>`<span class="tag">${safe(v)}</span>`).join("")}
  function biCards(items){return `<div class="grid">${items.map(x=>`<article class="card"><div class="tag-row">${badge(x.status)}<span class="tag">${safe(x.id)}</span><span class="tag">${x.sp_count} SP · ${x.session_count} Session 关联</span><span class="tag">${x.basis_refs.length} 个证据入口</span></div><h3>${safe(x.topic)}</h3><p class="cap"><strong>用户现在能感知到：</strong>${safe(x.capability)}</p><p class="gap"><strong>还缺：</strong>${safe(x.gap)}</p><p class="subtle truncate">下一步：${safe(x.next_step||"源表未指定")}</p><button class="link-button" data-open="bi" data-id="${safe(x.id)}">查看 TSP、关联和来源 →</button></article>`).join("")}</div>`}
  function overview(){
    const items=filtered("bi"); $("result-count").textContent=`${items.length} / ${data.big_ideas.length} 个 BI`;
    const doing=data.current_doing_sessions.map(id=>data.sessions.find(x=>x.id===id)).filter(Boolean);
    return `<section class="panel"><div class="section-title"><div><h2>一句话看懂 Semx</h2><p>Semx 正在把“读代码、提炼能力、形成证据、受控提升为知识”做成一条可审计工程链。</p></div></div><div class="grid"><div class="card"><h3>已经比较强的部分</h3><p>合同/schema、选定 P00-P05 runtime、artifact lineage、维护中的 gates、Dashboard/KB 分工、受治理的人机协作，以及 P06/RCP 的多条有界 vertical slice。</p></div><div class="card"><h3>最容易被误解的部分</h3><p>大量 Done 是“一个有边界的 Session/SP 已关闭”，不是“任意 repo、完整 P00-P17、自动语义判断、生产 RCP/P06 已完成”。</p></div></div></section>
    <section class="panel"><div class="section-title"><div><h2>全周期阶段带</h2><p>按 Session 编号分段帮助新人阅读；它是导航，不是正式 release/version 划分。</p></div></div><div class="timeline">${data.waves.map(w=>`<div class="wave"><b>${w.count}</b><strong>${safe(w.name)}</strong><small>${safe(w.id)}</small><small>${safe(w.summary)}</small></div>`).join("")}</div></section>
    <section class="panel"><div class="section-title"><div><h2>现在正在做什么</h2><p>以完整 Session registry 的 Doing 状态为准。</p></div></div><div class="grid">${doing.map(x=>`<div class="card"><div>${badge(x.status)} <span class="tag">${safe(x.id)}</span></div><h3>${safe(x.topic)}</h3><p>${safe(x.purpose)}</p><p class="subtle">下一步：${safe(x.next_step)}</p><button class="link-button" data-open="session" data-id="${safe(x.id)}">查看详情 →</button></div>`).join("")}</div></section>
    <section class="panel"><div class="section-title"><div><h2>大方向：能力与缺口</h2><p>每张卡先讲用户感受，再保留原始 TSP 和证据定位。</p></div></div>${items.length?biCards(items):'<div class="empty">当前筛选没有匹配的 Big Idea。</div>'}</section>
    <section class="panel"><div class="section-title"><div><h2>下一步候选（proposal only）</h2><p>这是本次综合后给人的选择，不是已登记 BI/SP/Session，也不是执行批准。</p></div></div><div class="grid">${data.recommendations.map(x=>`<article class="card proposal"><span class="tag">${safe(x.type)}</span><h3>${safe(x.title)}</h3><p>${safe(x.detail)}</p></article>`).join("")}</div></section>`;
  }
  function biView(){const items=filtered("bi");$("result-count").textContent=`${items.length} / ${data.big_ideas.length} 个 BI`;return `<section class="panel"><div class="section-title"><div><h2>全部 Big Ideas</h2><p>BI 是长期方向，不会因某个 Session Done 自动关闭。</p></div></div>${items.length?biCards(items):'<div class="empty">没有匹配项。</div>'}</section>`}
  function tableView(kind){
    const all=filtered(kind); const total=all.length; const pages=Math.max(1,Math.ceil(total/state.pageSize));state.page=Math.min(state.page,pages);const start=(state.page-1)*state.pageSize;const rows=all.slice(start,start+state.pageSize);$("result-count").textContent=`${total} 条匹配 · 第 ${state.page}/${pages} 页`;
    const isSp=kind==="sp";
    const body=rows.map(x=>isSp?`<tr><td><button class="link-button" data-open="sp" data-id="${safe(x.id)}">${safe(x.id)}</button></td><td>${badge(x.status)}<div class="subtle truncate">${safe(x.status_raw)}</div></td><td>${safe(x.topic)}</td><td>${tags(x.bis)}</td><td>${x.session_count}</td><td><div class="truncate">${safe(x.purpose)}</div></td><td><div class="truncate">${safe(x.next_step||x.current_entry)}</div></td></tr>`:`<tr><td><button class="link-button" data-open="session" data-id="${safe(x.id)}">${safe(x.id)}</button><div class="subtle">${safe(x.historical_id)}</div></td><td>${badge(x.status)}</td><td>${safe(x.priority)}</td><td>${safe(x.parent)}</td><td>${tags(x.tracks)}</td><td>${safe(x.surface==="current"?"当前":"归档")}</td><td>${safe(x.wave_name)}</td><td><div class="truncate"><strong>${safe(x.topic)}</strong><br>${safe(x.purpose)}</div></td></tr>`).join("");
    const head=isSp?"<tr><th>SP</th><th>状态</th><th>Topic</th><th>关联 BI</th><th>Session</th><th>Purpose</th><th>Next / Entry</th></tr>":"<tr><th>Canonical Key</th><th>状态</th><th>优先级</th><th>父 SP</th><th>BI</th><th>表面</th><th>波次</th><th>Topic / Purpose</th></tr>";
    return `<section class="panel"><div class="section-title"><div><h2>${isSp?"全周期 Stage Plans":"全部当前与归档 Sessions"}</h2><p>${isSp?"同一 SP 的 current snapshot 与 full row 已按 ID 合并，源表重复仍在详情中可见。":"历史重号使用 parent-qualified canonical key 区分。"}</p></div></div>${total?`<div class="table-wrap"><table><thead>${head}</thead><tbody>${body}</tbody></table></div>`:'<div class="empty">没有匹配项。</div>'}<div class="pager"><span>每页 ${state.pageSize} 条</span><div class="controls"><button class="btn" data-page="prev" ${state.page<=1?'disabled':''}>上一页</button><button class="btn" data-page="next" ${state.page>=pages?'disabled':''}>下一页</button></div></div></section>`;
  }
  function sourceView(){
    $("result-count").textContent="完整性与证据边界";
    return `<section class="panel"><div class="section-title"><div><h2>数据质量提示</h2><p>这些不是被隐藏的瑕疵，而是接管项目时应该首先知道的 execution-memory 状态。</p></div></div>${data.data_quality.map(x=>`<div class="notice ${x.level}"><strong>${safe(x.title)}</strong><br>${safe(x.detail)}</div>`).join("")}</section>
    <section class="panel"><div class="section-title"><div><h2>完整性对账</h2><p>Markdown/registry 是真源；DKG 只做交叉检查。</p></div></div><div class="grid"><div class="card"><h3>Session registry</h3><p>HTML=${data.counts.sessions}；manifest record=${data.registry_cross_check.record_count}；index=${data.registry_cross_check.index_count}；current=${data.registry_cross_check.current_count}；archive=${data.registry_cross_check.archive_count}。</p></div><div class="card"><h3>BI / SP</h3><p>BI 源=${data.counts.big_ideas}、DKG=${data.registry_cross_check.dkg_big_ideas}；SP 源唯一=${data.counts.stage_plans}、row occurrence=${data.counts.stage_plan_row_occurrences}、旧 DKG=${data.registry_cross_check.dkg_stage_plans}。</p></div></div></section>
    <section class="panel"><div class="section-title"><div><h2>Source manifest</h2><p>本 HTML 不请求网络；每个输入在生成时记录摘要与行数。</p></div></div><div class="table-wrap"><table><thead><tr><th>Source</th><th>SHA-256</th><th>行数</th><th>文件数</th></tr></thead><tbody>${data.source_manifest.map(x=>`<tr><td><a class="source-link" href="${safe(x.href)}">${safe(x.path)}</a></td><td><code>${safe(x.sha256)}</code></td><td>${safe(x.line_count)}</td><td>${safe(x.file_count||1)}</td></tr>`).join("")}</tbody></table></div><p class="subtle">Stable architecture/contracts/terminology 仍以 semx-kb 为准；BI/SP/Session 状态仍以 Dashboard 为准；代码和 tests 只证明各自可定位的实现/检查范围。</p></section>`;
  }
  function render(){
    $("filter-panel").style.display=state.view==="source"?"none":"block";
    let out=state.view==="overview"?overview():state.view==="bi"?biView():state.view==="sp"?tableView("sp"):state.view==="session"?tableView("session"):sourceView();
    $("content").innerHTML=out;
    writeHash();
  }
  function detailEntries(kind,item){
    if(kind==="bi")return [["ID",item.id],["状态快照",item.status_raw],["证据姿态",item.evidence_posture],["P00-P17",item.phase_tags.join(", ")],["Topic",item.topic],["用户能力",item.capability],["剩余缺口",item.gap],["禁止提升",item.forbidden_uplifts.join("\n")],["Scope",item.scope],["Purpose",item.purpose],["Exit Criteria",item.exit_criteria],["Canonical Target",item.canonical_target],["关联 SP",item.stage_plans.join(", ")||"—"],["关联 Session",String(item.session_count)],["Next Step",item.next_step],["Notes",item.notes],["来源",item.source.display]];
    if(kind==="sp")return [["ID",item.id],["状态",item.status_raw],["证据姿态",item.evidence_posture],["P00-P17",item.phase_tags.join(", ")],["源冲突",item.source_conflict?JSON.stringify(item.conflict_fields,null,2):"否"],["Topic",item.topic],["关联 BI",item.bis.join(", ")||"—"],["实际 Session 数",String(item.session_count)],["Scope",item.scope],["Purpose",item.purpose],["Current Entry",item.current_entry],["Required Gates",item.required_gates],["Claim Ceiling",item.claim_ceiling],["Next Step",item.next_step],["Notes",item.notes],["源表 row 次数",String(item.row_occurrences)],["全部源行",item.occurrences.map(x=>`${x.source.display}\n${JSON.stringify(x.fields)}`).join("\n\n")],["来源",item.source.display]];
    return [["Canonical Key",item.id],["历史 ID",item.historical_id],["父级",item.parent],["状态",item.status_raw],["证据姿态",item.evidence_posture],["P00-P17",item.phase_tags.join(", ")],["历史状态说明",item.historical_status],["优先级",item.priority],["关联 BI",item.tracks.join(", ")||item.track_raw||"—"],["当前/归档",item.surface],["历史波次",item.wave_name],["Topic",item.topic],["Scope",item.scope],["Purpose",item.purpose],["Depends On",item.depends_on],["Deliverable",item.deliverable],["Primary Evidence",item.primary_evidence],["Exit Criteria",item.exit_criteria],["Next Step",item.next_step],["Notes",item.notes],["来源",item.source.display]];
  }
  function openDetail(kind,id){const list=kind==="bi"?data.big_ideas:kind==="sp"?data.stage_plans:data.sessions;const item=list.find(x=>x.id===id);if(!item)return;$("drawer-kind").textContent=item.kind;$("drawer-title").textContent=`${item.id} · ${item.topic}`;const rows=detailEntries(kind,item).filter(([,v])=>v).map(([k,v])=>`<dt>${safe(k)}</dt><dd>${k==="来源"?`<a class="source-link" href="${safe(item.source.href)}">${safe(v)}</a>`:safe(v)}</dd>`).join("");const basis=kind==="bi"?`<dt>证据入口</dt><dd>${item.basis_refs.map(ref=>`<a class="source-link" href="${safe(ref.href)}">${safe(ref.display)}</a>`).join("<br>")}</dd>`:"";$("drawer-detail").innerHTML=rows+basis;$("drawer").classList.add("open");$("drawer").setAttribute("aria-hidden","false")}
  document.addEventListener("click",e=>{const tab=e.target.closest("[data-view]");if(tab){state.view=tab.dataset.view;state.page=1;document.querySelectorAll("[data-view]").forEach(x=>x.classList.toggle("active",x===tab));render();return}const opener=e.target.closest("[data-open]");if(opener){openDetail(opener.dataset.open,opener.dataset.id);return}const page=e.target.closest("[data-page]");if(page&&!page.disabled){state.page+=page.dataset.page==="next"?1:-1;render()}});
  Object.values(filters).forEach(el=>el.addEventListener(el===filters.q?"input":"change",()=>{state.page=1;render()}));
  sortSelect.addEventListener("change",()=>{state.page=1;render()});
  $("reset").addEventListener("click",()=>{Object.values(filters).forEach(el=>el.value="");sortSelect.value="source";state.page=1;render()});
  $("drawer-close").addEventListener("click",()=>{$("drawer").classList.remove("open");$("drawer").setAttribute("aria-hidden","true")});
  $("drawer").addEventListener("click",e=>{if(e.target===$("drawer"))$("drawer-close").click()});
  document.addEventListener("keydown",e=>{if(e.key==="Escape")$("drawer-close").click()});
  render();
})();
</script>
</body>
</html>
'''


def render_html(data: dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    payload = (
        payload.replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )
    return HTML_TEMPLATE.replace("__DATA__", payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("Proj-notes/ExplorationDashboardSynthesizer-Dashboards/semx_cli_full_cycle_dashboard_panorama_2026-08-13.html"),
    )
    parser.add_argument("--generated-on", default=date.today().isoformat())
    parser.add_argument("--check", action="store_true", help="Parse and validate source; if HTML exists, also fail on render drift.")
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output if args.output.is_absolute() else repo / args.output
    data = build_data(repo, args.generated_on)
    rendered = render_html(data)
    if args.check:
        if output.exists() and output.read_text(encoding="utf-8") != rendered:
            print(f"panorama-check: drift: {output}", file=sys.stderr)
            return 2
        print(json.dumps({"verdict": "pass", "output": str(output), "output_exists": output.exists(), "counts": data["counts"]}, ensure_ascii=False))
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(json.dumps({"verdict": "generated", "output": str(output), "counts": data["counts"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
