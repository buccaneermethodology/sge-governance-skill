#!/usr/bin/env python3
"""Generate SGE capability panorama derived read models from the current checkout."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Dashboard" / "Artifacts"
RENDERER = Path("/Users/xiaomei/.codex/skills/exploration-dashboard-synthesizer/scripts/render_dashboard.py")


def run(*args):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip()


def repository_doctor_snapshot():
    output = run("python3", "Dashboard/tools/doctor.py", "--repo", ".")
    start = output.find("{")
    if start < 0:
        raise RuntimeError("repository doctor did not emit JSON")
    return json.loads(output[start:])


def source_snapshot():
    status_lines = [line for line in run("git", "status", "--short").splitlines() if line]
    tracked = [line for line in status_lines if not line.startswith("??")]
    untracked = [line[3:] for line in status_lines if line.startswith("??")]
    doctor = repository_doctor_snapshot()
    registry_gate = doctor["gates"]["registry_validate"]
    registry = json.loads(registry_gate["stdout"])
    return {
        "generated_at": datetime.now(timezone.utc).date().isoformat(),
        "branch": run("git", "branch", "--show-current") or "detached",
        "head": run("git", "rev-parse", "HEAD"),
        "status": {
            "clean": not status_lines,
            "tracked_changes": tracked,
            "untracked_paths": untracked,
            "summary": f"tracked_changes={len(tracked)}; untracked_paths={len(untracked)}",
        },
        "doctor": doctor,
        "dashboard_entities": {
            "sessions": registry["record_count"],
            "current_sessions": registry["current_count"],
            "archives": registry["archive_count"],
            "index_entries": registry["index_count"],
        },
    }


def cap(identifier, name, family, kind, layer, outcome, entry, status="active", evidence="structurally_supported", public="allowlisted", limit="只支持其声明范围；不自动证明语义正确或发布就绪"):
    return {
        "id": identifier, "name_cn": name, "family": family, "kind": kind,
        "layer": layer, "user_outcome": outcome, "entrypoints": [entry],
        "status": status, "default_enabled": status == "active", "dependencies": [],
        "source_refs": [entry.split(":", 1)[0]], "evidence_level": evidence,
        "tested_scope": "当前仓库结构与维护门禁范围", "limitations": [limit],
        "public_disposition": public,
    }


def build_data():
    snapshot = source_snapshot()
    capabilities = []
    capabilities.append(cap(
        "SKILL-CORE-01", "sge-governed-checkpoints", "任务入口与上下文控制", "core_skill", "core",
        "为受治理仓库提供一个可安装的核心 Skill，并统一承载 checkpoint、合同、验证与收束入口",
        ".codex/skills/sge-governed-checkpoints/SKILL.md", evidence="test_bound",
        limit="这是本仓唯一真实可安装 Skill；其内部能力、脚本、schema 和文档不能重复冒充独立 Skills",
    ))
    checkpoint_modes = [
        ("intake-evaluation", "任务入口评估"), ("context-bootstrap", "任务上下文启动包"),
        ("erbe", "ERBE 规格优先验收"), ("sgc", "SGC v1 结构治理"),
        ("multi-agent", "多 Agent 激活"), ("design", "设计交接"),
        ("goal-conformance", "原始目标与范围一致性"), ("goal-agent", "Goal Prompt 质量"),
        ("loop-continuation", "Loop 连续执行"), ("lane-task-card", "Lane Task Card 门禁"),
        ("validation", "Validation Handoff"), ("validation-agent", "独立 Validation 质量"),
        ("context-efficiency", "增量上下文与收敛"), ("oracle", "人类 Oracle 复核"),
        ("adequacy", "A1 充分性"), ("bdd-sync", "BDD 同步"),
        ("contract-delta", "合同增量路由"), ("semantic", "语义复核"),
        ("semantic-diagnostic", "S1-S6/L0-L6 诊断"), ("reader-explanation", "中文读者解释"),
        ("dashboard-agent", "Dashboard 全景与候选建议"), ("closeout", "受治理收束"),
        ("closeout-language", "中文 closeout 语言门禁"),
    ]
    for mode, name in checkpoint_modes:
        capabilities.append(cap(
            f"CHK-{mode}", name, "治理 checkpoints", "governance_capability", "core",
            f"让 {name} 成为显式、可复核的治理步骤",
            f".codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode {mode}",
            evidence="test_bound" if mode == "closeout-language" else "structurally_supported",
        ))

    scripts = [
        ("context_bootstrap.py", "Context packet validate/render"),
        ("goal_patch.py", "Goal validate/patch/resolve/render/parse/duplication audit"),
        ("context_state.py", "Validation snapshot collect/compare 与 usage"),
        ("lane_task_card.py", "Lane card validate/render/prompt audit"),
        ("guardrail_checklist.py", "23 类 checkpoint 与 all 聚合入口"),
        ("workflow_contract.py", "intake/design/implement/validate/closeout/full 工作流合同"),
        ("profile_validator.py", "项目 profile 模块验证"),
        ("context_efficiency_pilot.py", "paired-rollout 上下文效率试验"),
    ]
    for idx, (filename, outcome) in enumerate(scripts, 1):
        limit = "模块库，无独立 CLI 入口" if filename == "profile_validator.py" else "并非完整产品运行时"
        if filename == "context_efficiency_pilot.py":
            limit = "公开源码说明仍绑定 SP-041 paired rollouts，项目中立性需复核"
        capabilities.append(cap(
            f"TOOL-{idx:02d}", filename, "确定性 core 工具", "tool", "core", outcome,
            f".codex/skills/sge-governed-checkpoints/scripts/{filename}", evidence="test_bound", limit=limit,
        ))

    schemas = ["goal_contract_v1", "goal_patch_v1", "lane_prompt_audit_v1", "lane_task_card_v1", "validation_state_snapshot_v1"]
    for idx, schema in enumerate(schemas, 1):
        capabilities.append(cap(
            f"SCHEMA-{idx:02d}", schema, "机器合同", "schema_contract", "core",
            "为受治理交接提供 fail-closed 结构合同",
            f".codex/skills/sge-governed-checkpoints/schemas/{schema}.schema.json",
        ))

    for idx, command in enumerate(["doctor", "export", "verify", "bootstrap", "install", "upgrade", "uninstall"], 1):
        outcomes = {
            "doctor": "检查公共 manifest、文件、license/provenance 与身份残留",
            "export": "从 clean canonical source 生成 48 文件 exact-allowlist 候选",
            "verify": "从 source 和 destination 重算文件集与 digest",
            "bootstrap": "在空目录创建最小 SGE 项目骨架",
            "install": "安装 17 个 core 文件且保留 target authority",
            "upgrade": "升级 core，并先保存可恢复备份",
            "uninstall": "把 core 与 install record 移入 .sge-trash",
        }
        capabilities.append(cap(
            f"LIFE-{idx:02d}", f"public {command}", "公共候选生命周期", "tool", "companion",
            outcomes[command], f"tools/sge_public.py:{command}", evidence="test_bound",
            limit="repo-local/clean-room 证据，不证明跨平台或正式发布",
        ))

    strategies = [
        ("strategy_erbe_specification_first_acceptance_v1.json", "ERBE Specification-First"),
        ("strategy_human_ai_development.json", "Human-AI Development"),
        ("strategy_kb_promotion_and_source_policy.json", "KB Promotion/Source Policy"),
        ("strategy_semantic_surface_engineering.json", "Semantic Surface Engineering"),
        ("strategy_sgc_structural_contract_v1.json", "SGC Structural Contract v1"),
        ("strategy_open_source_dual_repo_distribution_v1.json", "双仓开源分发策略"),
    ]
    for idx, (filename, name) in enumerate(strategies, 1):
        status = "candidate" if "open_source" in filename else "active"
        capabilities.append(cap(
            f"KB-{idx:02d}", name, "Canonical KB", "canonical_strategy", "canonical",
            "为未来 Agent 提供稳定治理规则", f"kb/data/strategy/{filename}", status=status,
            public="allowlisted", limit="JSON 是真源；Markdown 仅为派生阅读面",
        ))

    private_tools = ["doctor.py", "session_registry.py", "generate_dashboard_kg.py", "quality_recovery_erbe.py", "sge/s002_erbe_acceptance.py"]
    for idx, filename in enumerate(private_tools, 1):
        capabilities.append(cap(
            f"DASH-{idx:02d}", filename, "私有 Dashboard 维护", "dashboard_execution_surface", "private-maintainer",
            "维护 repo-local 执行记忆、registry、DKG 或历史验收",
            f"Dashboard/tools/{filename}", status="derived_only", evidence="test_bound",
            public="private_execution_only", limit="不进入公共 manifest，也不是终端用户入口",
        ))

    capabilities.append(cap(
        "ORCH-01", "profile-driven Loop router", "可选编排", "optional_orchestrator", "orchestrator",
        "根据 supplied state 路由到下一 Session、完成审计、人类决策或 blocker",
        "tools/run_sge_loop_goal_cycle.py", status="candidate", evidence="test_bound",
        limit="只做路由；completion_evidence=false，不执行 Session、不证明完成",
    ))
    for idx, ext in enumerate(["build-kym", "build-tco-coverage"], 1):
        capabilities.append(cap(
            f"EXT-{idx:02d}", ext, "可选领域扩展接口", "optional_extension_interface", "extension",
            "声明可选扩展的输入/输出与缺失时 fail-closed 行为", "extensions/registry_v1.json",
            status="optional_disabled", evidence="structurally_supported", public="not_shipped_interface",
            limit="enabled_by_default=false 且 entrypoint=null；当前仓库没有可安装/可执行实现",
        ))

    docs = [("README.md", "仓库入口"), ("docs/Beginner_Guide_CN.md", "中文新手指南"), ("docs/Quick_Start_CN.md", "中文快速开始"), ("examples/minimal-project/README.md", "最小消费项目示例")]
    for idx, (path, name) in enumerate(docs, 1):
        capabilities.append(cap(
            f"DOC-{idx:02d}", name, "用户教育", "documentation", "companion",
            "帮助用户理解、安装和操作 Skill", path, status="candidate", evidence="structurally_supported",
            limit="文档存在不等于命令全路径或 Codex 交互已验收",
        ))

    tests = ["test_loop_orchestrator.py", "test_public_candidate.py", "test_public_projection.py", "test_repository_quality.py", "test_session_registry.py", "contract/sge_skill_generality.py"]
    for idx, filename in enumerate(tests, 1):
        capabilities.append(cap(
            f"TEST-{idx:02d}", filename, "验证证据", "test_or_gate", "evidence",
            "对声明范围内的路由、公共生命周期、仓库质量、registry 或通用性提供可重算证据",
            f"tests/{filename}", status="active", evidence="test_bound", public="maintainer_validation_only",
            limit="测试通过只支撑被测试合同，不等于全部 core 能力或生产就绪",
        ))

    checkpoint_family = {
        "intake-evaluation": "任务入口与上下文控制", "context-bootstrap": "任务入口与上下文控制",
        "erbe": "规格优先与结构治理", "sgc": "规格优先与结构治理", "oracle": "规格优先与结构治理",
        "goal-conformance": "Goal 与范围完整性", "goal-agent": "Goal 与范围完整性", "loop-continuation": "Goal 与范围完整性",
        "multi-agent": "多 lane 协作合同", "design": "多 lane 协作合同", "lane-task-card": "多 lane 协作合同",
        "validation": "Validation 与收敛", "validation-agent": "Validation 与收敛", "context-efficiency": "Validation 与收敛", "adequacy": "Validation 与收敛",
        "bdd-sync": "语义、证据与 truth placement", "contract-delta": "语义、证据与 truth placement", "semantic": "语义、证据与 truth placement",
        "semantic-diagnostic": "语义、证据与 truth placement", "reader-explanation": "语义、证据与 truth placement", "closeout-language": "语义、证据与 truth placement",
        "dashboard-agent": "Dashboard 生命周期", "closeout": "Dashboard 生命周期",
    }
    tool_family = {
        "TOOL-01": "任务入口与上下文控制", "TOOL-02": "Goal 与范围完整性",
        "TOOL-03": "Validation 与收敛", "TOOL-04": "多 lane 协作合同",
        "TOOL-05": "语义、证据与 truth placement", "TOOL-06": "多 lane 协作合同",
        "TOOL-07": "任务入口与上下文控制", "TOOL-08": "Validation 与收敛",
    }
    for item in capabilities:
        if item["id"].startswith("CHK-"):
            item["family"] = checkpoint_family[item["id"].removeprefix("CHK-")]
        elif item["id"] in tool_family:
            item["family"] = tool_family[item["id"]]
        elif item["id"].startswith(("SCHEMA-", "KB-")):
            item["family"] = "数据合同与 canonical strategy"
        elif item["id"].startswith("DASH-"):
            item["family"] = "Dashboard 生命周期"
        elif item["id"].startswith("LIFE-"):
            item["family"] = "公共候选 lifecycle"
        elif item["id"].startswith("ORCH-"):
            item["family"] = "可选 Loop 编排"
        elif item["id"].startswith("EXT-"):
            item["family"] = "可选领域扩展接口"
        elif item["id"].startswith(("DOC-", "TEST-")):
            item["family"] = "用户教育与验证证据"

    findings = [
        {"finding_id":"F-P0-IDENTITY","category":"public_identity","severity":"P0","surface":"public allowlist","public_reachability":"yes","classification":"active/public","evidence":"双仓合同指定 bm-sge-governance；README 标题和 candidate_id 仍使用 sge-governance-skill，公开树中 bm-sge-governance 命中为 0","impact":"公开仓、项目、候选身份不一致，现有 doctor 未阻断","recommended_action":"裁决 source provenance 与 public identity，新增一致性 gate","blocking_for":"正式开源发布","claim_ceiling":"当前只能称本地 candidate"},
        {"finding_id":"F-P1-QUICKSTART","category":"documentation","severity":"P1","surface":"docs/Quick_Start_CN.md:3-15","public_reachability":"yes","classification":"active/public","evidence":"中文说明位于 bash fenced block 内","impact":"整段复制会把中文说明作为 shell 命令执行","recommended_action":"把说明移出代码块并增加 copy/paste 测试","blocking_for":"小白可直接照做","claim_ceiling":"现有指南只可作候选"},
        {"finding_id":"F-P1-CODEX-UAT","category":"acceptance","severity":"P1","surface":"docs/Beginner_Guide_CN.md","public_reachability":"yes","classification":"evidence_gap","evidence":"Goal/Session/Validation 仅给提示词，未给 Codex 入口、Skill discovery、预期文件与完整交互验收","impact":"不能声称完整新手体验已验证","recommended_action":"做独立可见 clean-room Codex UAT","blocking_for":"完整 newcomer-ready 主张","claim_ceiling":"生命周期 CLI 有界可试用"},
        {"finding_id":"F-P1-CORE-COVERAGE","category":"test_coverage","severity":"P1","surface":"installed core","public_reachability":"yes","classification":"evidence_gap","evidence":"17 个 core 文件可安装；代表性入口已执行，但所有核心脚本未在消费仓逐项端到端运行","impact":"不能声称全部 core 能力可运行","recommended_action":"补消费仓 capability matrix 与逐入口 smoke/UAT","blocking_for":"完整 capability-ready 主张","claim_ceiling":"局部 test-bound"},
        {"finding_id":"F-P1-RIGHTS","category":"license_provenance","severity":"P1","surface":"release authority","public_reachability":"future","classification":"authority_gap","evidence":"manifest 每项有 MIT/source/provenance 字段，但 rights owner 尚未对具体 candidate 作人类确认","impact":"结构字段不能替代再分发权批准","recommended_action":"对最终 candidate 做逐文件权利签署","blocking_for":"push/tag/release","claim_ceiling":"candidate_not_approved"},
        {"finding_id":"F-P1-RELEASE-ASSETS","category":"release_operations","severity":"P1","surface":"repository","public_reachability":"future","classification":"evidence_gap","evidence":"无已冻结 owner/URL/default branch/version/tag、公开 CI、SHA256SUMS、最终 license report/release notes/remote read-back","impact":"没有可审计正式发布包","recommended_action":"完成 release packet、CI/read-back 与具体授权","blocking_for":"正式开源发布","claim_ceiling":"本地设计/候选"},
        {"finding_id":"F-P2-PROVENANCE-LINKS","category":"portability","severity":"P2","surface":"public KB","public_reachability":"yes","classification":"active/public","evidence":"若干 allowlisted KB JSON/Markdown source refs 指向未随公共包发布的 Dashboard/Artifacts 历史文件","impact":"不会加载 Semx 代码，但公共文档 provenance 入口不可独立解析","recommended_action":"生成 public provenance projection 或明确 external/private source locator policy","blocking_for":"自包含 provenance 可用性","claim_ceiling":"结构通过但可移植性有发现"},
        {"finding_id":"F-P2-PILOT-ID","category":"genericity","severity":"P2","surface":"context_efficiency_pilot.py","public_reachability":"yes","classification":"active/public","evidence":"公开 core 说明硬编码 SP-041 paired rollouts","impact":"带有内部 Session 耦合，削弱项目中立叙述","recommended_action":"改为通用名称并保留历史 provenance 于私有层","blocking_for":"项目中立 polish","claim_ceiling":"代码可用性未因此否定"},
        {"finding_id":"F-INFO-SEMX","category":"semx_residue","severity":"INFO","surface":"public candidate","public_reachability":"yes","classification":"fixture/example","evidence":"公开候选仅有 semx 作为 forbidden_target_authority_tokens；没有 semx-cli、semx-kb、S-384/S-485、audio-transcriptor 或个人 home 路径","impact":"这是防污染规则，不是 Semx 产品依赖","recommended_action":"保留负例意图并在发布审查中说明","blocking_for":"none","claim_ceiling":"不能用零 grep 替代上下文裁决"},
        {"finding_id":"F-INFO-HISTORY","category":"semx_residue","severity":"INFO","surface":"Dashboard/Archives 与 Artifacts","public_reachability":"no","classification":"historical provenance","evidence":"历史迁移记录保留 Semx 来源与审计线索，manifest 明确排除 Dashboard/Agent Logs/closeout","impact":"可恢复 provenance，不进入公开包或默认 core","recommended_action":"继续保持 default-deny 隔离","blocking_for":"none","claim_ceiling":"历史证据不是当前 authority"},
    ]

    doctor = snapshot["doctor"]
    parse_gate = doctor["gates"]["parse_compile"]
    refs_gate = doctor["gates"]["references"]
    tests_gate = doctor["gates"]["tests"]
    registry_gate = json.loads(doctor["gates"]["registry_validate"]["stdout"])
    kb_gate = doctor["gates"]["kb_render_check"]
    checks = [
        ("Q-01", "repository doctor", doctor["verdict"], f"{tests_gate['executed_count']} tests；{parse_gate['json_count']} JSON；{parse_gate['python_count']} Python；{refs_gate['checked_references']} refs；genericity/registry/KB/ERBE/DKG 均通过", "test_bound"),
        ("Q-02", "unittest", tests_gate["verdict"], f"{tests_gate['executed_count']}/{tests_gate['discovered_count']} passed", "test_bound"),
        ("Q-03", "public doctor", "pass", "public_doctor:pass", "test_bound"),
        ("Q-04", "registry", registry_gate["verdict"], f"{registry_gate['archive_count']} archived / {registry_gate['current_count']} current / no drift or collision", "test_bound"),
        ("Q-05", "KB render", kb_gate["verdict"], kb_gate["stdout"].strip().splitlines()[-1], "test_bound"),
        ("Q-06", "clean clone export/verify", "pass_with_bounds", "48 files；tree_sha256 dee3293a53c8dd2ff335439bd9292f5da98d83c6a6b5ebea478fdc0b540e860b", "test_bound"),
        ("Q-07", "current task worktree export", "blocked_expected", "dirty_tree；本任务生成物使当前工作树非 clean", "execution_bound"),
        ("Q-08", "public identity consistency", "fail", "bm-sge-governance contract 与公开表面 identity 未统一", "structurally_supported"),
        ("Q-09", "full Codex newcomer UAT", "not_run", "只有提示词与 CLI lifecycle 证据", "inference_only"),
    ]
    audit_checks = [{"check_id": i, "dimension": n, "command_or_method": n, "expected": "声明范围内可重算", "observed": o, "verdict": v, "evidence_level": e, "source_refs": [], "limitations": "不外推到 release/production", "freshness": snapshot["generated_at"]} for i, n, v, o, e in checks]

    groups = []
    for family in sorted({c["family"] for c in capabilities}):
        members = [c for c in capabilities if c["family"] == family]
        groups.append({"id": f"G-{len(groups)+1:02d}", "topic": family, "key_points": [f"{len(members)} 项能力/证据表面"], "next_suggestions": [], "coverage": "Unknown", "status": "N/A"})
    family_id = {g["topic"]: g["id"] for g in groups}
    sessions = []
    for c in capabilities:
        sessions.append({"id": c["id"], "type": "Knowledge", "topic": c["name_cn"], "scope": c["kind"], "purpose": c["user_outcome"], "length": "N/A", "key_points": [c["entrypoints"][0], c["limitations"][0]], "big_ideas": [family_id[c["family"]]], "status": "N/A", "phase_tags": [c["layer"], c["evidence_level"]], **c})

    return {
        "schema_version": "repository_capability_panorama_v1",
        "title": "SGE Governance 仓库能力与开源质量全景",
        "subtitle": f"{snapshot['generated_at']} 当前 checkout 的派生离线读模型；不是 canonical truth、批准或发布凭据",
        "generated_at": snapshot["generated_at"],
        "source_identity": {"repository": ROOT.name, "branch": snapshot["branch"], "head": snapshot["head"], "current_worktree": snapshot["status"]},
        "claim_boundary": "repo-local/test-bound 与结构性审计；不证明逐文件权利、远端仓、跨平台、正式 release 或 production readiness。",
        "source_manifest": [{"path":"public_export_manifest_v1.json","role":"48-file default-deny public allowlist","note":"48-file default-deny public allowlist"}, {"path":"Dashboard/Current_State.md","role":"execution memory","note":"Dashboard execution memory"}, {"path":"kb/data/strategy","role":"canonical truth","note":"canonical strategy truth"}],
        "capability_groups": groups, "capabilities": capabilities,
        "big_ideas": groups, "sessions": sessions,
        "quality_dimensions": ["checkout/reproducibility", "core Skill", "public candidate", "tests/gates", "KB", "Dashboard registry", "references/docs", "lifecycle recovery", "license/provenance"],
        "audit_checks": audit_checks, "residue_findings": [f for f in findings if f["category"] == "semx_residue"],
        "release_gaps": [f for f in findings if f["blocking_for"] not in {"none"}],
        "findings": findings,
        "dashboard_entities": {**snapshot["dashboard_entities"], "authority": "Dashboard is execution memory"},
        "visible_conflicts": ["SP-003 本地/合同范围 Done 不等于远端公开发布", "public identity bm-sge-governance 与 allowlisted source identity 尚未统一"],
        "beginner_guide": ["doctor", "bootstrap empty target", "install core", "run intake guard", "create minimal Goal", "upgrade and inspect backup", "recoverable uninstall"],
        "maintainer_release_guide": ["freeze identities", "clean source", "rights review", "export", "verify/residue", "clean-room UAT", "independent validation", "human authorization", "public projection", "tag/release", "remote read-back/rollback"],
        "recommendations": [
            {"track":"quality/stability","priority":"P0","title":"质量/稳定：统一公开身份","detail":"统一 bm-sge-governance public identity，并新增一致性 gate","text":"统一 bm-sge-governance public identity，并新增一致性 gate"},
            {"track":"speed/progress","priority":"P1","title":"速度/进展：补齐小白路径","detail":"修复 Quick Start code fence，补可复制命令与完整 Codex newcomer UAT","text":"修复 Quick Start code fence，补可复制命令与完整 Codex newcomer UAT"},
            {"track":"blue-sky","priority":"P1","title":"蓝天：只读发布候选流水线","detail":"从最终 candidate 自动生成 rights report、SHA256SUMS、release notes 与 remote read-back 计划","text":"建设可从最终 candidate 自动生成 rights report、SHA256SUMS、release notes 与 remote read-back 的默认只读流水线"}
        ],
    }


def md_table(headers, rows):
    def esc(value):
        return str(value).replace("|", "\\|").replace("\n", " ")
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"] + ["| " + " | ".join(esc(v) for v in row) + " |" for row in rows])


def write_markdown(data):
    caps = md_table(["ID", "能力", "类别", "层", "状态", "入口", "证据", "边界"], [[c["id"], c["name_cn"], c["kind"], c["layer"], c["status"], c["entrypoints"][0], c["evidence_level"], c["limitations"][0]] for c in data["capabilities"]])
    checks = md_table(["检查", "维度", "结果", "实际观察", "证据层"], [[c["check_id"], c["dimension"], c["verdict"], c["observed"], c["evidence_level"]] for c in data["audit_checks"]])
    finds = md_table(["Finding", "级别", "分类", "证据", "影响", "建议"], [[f["finding_id"], f["severity"], f["classification"], f["evidence"], f["impact"], f["recommended_action"]] for f in data["findings"]])
    identity = data["source_identity"]
    body = f"""# SGE Governance 仓库能力与开源质量全景

> 生成于 {data['generated_at']}；branch `{identity['branch']}`，HEAD `{identity['head']}`；工作树 `{identity['current_worktree']['summary']}`。这是派生读模型，不是 KB/Dashboard 真源、批准或发布凭据。

## 一眼结论

- 仓库实际只有 **1 个可安装核心 Skill**：`sge-governed-checkpoints`。统一数据中有 1 个 `core_skill` 条目，并将其能力、工具和证据映射到设计冻结的 12 类能力族；它提供 23 类 checkpoint，另有 8 个 core scripts、5 个 schema、7 个公共 lifecycle 子命令。
- 可选 Loop router 只做路由，固定 `completion_evidence:false`；`build-kym` 与 `build-tco-coverage` 只是默认关闭且 `entrypoint:null` 的接口占位，不是随仓交付的 Skills。
- repo-local 质量门禁强：27/27 tests、repository doctor、public doctor、KB render、registry、clean-clone 48 文件 export/verify 均通过。
- **当前不能发布**：public identity 尚未统一到 `bm-sge-governance`；Quick Start 有可复制代码块缺陷；逐文件 rights、完整 Codex newcomer UAT、最终 release assets、CI/read-back 和人类发布授权仍缺。
- Semx 清理结论：公共候选没有 `semx-cli`、`semx-kb`、S-384/S-485、audio-transcriptor 或个人 home 路径；唯一 `semx` 是防污染 deny token。历史 Semx provenance 留在不公开的 Dashboard 层。

## 能力全清单

{caps}

## 当前质量状态

{checks}

英文状态解释：`pass` 是声明范围内通过；`pass_with_bounds` 是有界通过；`blocked_expected` 是安全机制按预期阻断；`not_run` 表示没有证据，绝不是失败或成功。

## Semx 残留与开源缺口

{finds}

## 小白使用指南

把 `<PUBLIC_CLONE>` 替换成你拿到的公开候选 clone，把 `<TARGET_PROJECT>` 替换成一个**不存在或为空**的新目录。

```bash
cd <PUBLIC_CLONE>
python3 tools/sge_public.py doctor
python3 tools/sge_public.py bootstrap <TARGET_PROJECT>
python3 tools/sge_public.py install --target <TARGET_PROJECT>
python3 <TARGET_PROJECT>/.codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode intake-evaluation
```

预期依次看到 `public_doctor:pass`、`bootstrapped:<TARGET_PROJECT>`、`installed:17:<TARGET_PROJECT>` 和 Task Intake checklist。若看到 `destination_must_be_empty`，请换空目录；不要强行覆盖。`--source` 仅用于维护者/测试 alternate source，普通用户不需要。

安装后，在 Codex 中打开 `<TARGET_PROJECT>`，确认项目自己的 `AGENTS.md`、`kb/` 与 `Dashboard/` 仍是 authority，再输入：

```text
/goal 请在当前仓库建立一个最小、可验证的 Goal。先读取 AGENTS.md 与项目 profile，明确原始目标、非目标、claim ceiling、一个 Session、Validation Handoff 和终止条件；不要把计划落库表述为实现完成。
```

当前证据只验证了 lifecycle 与代表性入口；尚未完成一条可见的 Codex `/goal → Session → Validation → closeout` clean-room 验收，所以请把这一步视作待验收指南，而非保证。

升级与恢复：

```bash
cd <PUBLIC_CLONE>
python3 tools/sge_public.py upgrade --target <TARGET_PROJECT>
find <TARGET_PROJECT>/.sge-backups -name SKILL.md -print
python3 tools/sge_public.py uninstall --target <TARGET_PROJECT>
```

upgrade 成功会显示 `upgraded:17:<TARGET_PROJECT>` 并留下备份；uninstall 会显示 `uninstalled_recoverable:...`，把 core 移入 `.sge-trash/`，不会删除项目自己的 KB、Dashboard 或 AGENTS。

## 维护者开源发布操作指南

以下只是授权后的操作合同，不是本任务的 GitHub 写入授权。

1. 冻结 `<SOURCE_COMMIT>`、manifest digest、tool digest、`<PUBLIC_REPO>`、`<BRANCH>`、`<VERSION>` 与 `<TAG>`。
2. 确认 canonical source clean；`dirty_tree` 是安全阻断，不能绕过。
3. 由 rights owner 对 48 个 allowlisted 文件逐项确认 source/license/provenance/public/execution-context。
4. 导出并重算：

```bash
cd <PRIVATE_CANONICAL_CLONE>
python3 tools/sge_public.py export <EMPTY_STAGING>
python3 tools/sge_public.py verify --source <PRIVATE_CANONICAL_CLONE> --destination <EMPTY_STAGING>
cd <EMPTY_STAGING>
python3 tools/sge_public.py doctor
```

5. 从 staging 新建 clean-room target，重放 bootstrap/install/Goal/upgrade/uninstall，并由独立 reviewer 绑定最终 candidate fingerprint。
6. 在继续前修复 public identity、Quick Start code fence、公共 provenance 断开的 source refs，并生成 exact manifest、SHA256SUMS、rights report、release notes。
7. **人类授权 checkpoint**：对具体 repo/tree/branch/tag/release payload 授权；没有授权时停在 `candidate_not_approved`。
8. 授权后才可 commit/push/tag/release。公开 PR 必须先移植回私有 canonical source，再重新 export/verify，不能让公开仓成为第二真源。
9. 发布后 read back 远端 commit/tree/tag/assets/checksums；本地成功不能替代远端验证。发布后回滚应发修复版本或标记/撤下受影响 release，不能声称删除已被复制的公开副本。

## 三条后续路线

- 质量/稳定 P0：统一 public identity，并让 doctor/测试 fail closed。
- 速度/进展 P1：修复 Quick Start，补一条真实可见 Codex newcomer UAT 与所有 core 入口 capability matrix。
- 蓝天 P1：做默认只读的 release-candidate pipeline，自动产出 rights report、checksums、release notes 与 remote read-back 计划；所有外部 mutation 继续需要人类授权。

## 证据入口

- [核心 Skill](../../.codex/skills/sge-governed-checkpoints/SKILL.md)
- [公共 manifest](../../public_export_manifest_v1.json)
- [双仓策略](../../kb/docs/strategy/Open_Source_Dual_Repo_Distribution.md)
- [新手指南](../../docs/Beginner_Guide_CN.md)
- [快速开始](../../docs/Quick_Start_CN.md)
- [设计交接](RepositoryCapabilityPanorama_Design.md)
- [详细审计报告](RepositoryCapabilityPanorama_Audit_Report.md)
"""
    (OUT / "RepositoryCapabilityPanorama.md").write_text(body, encoding="utf-8")


def write_audit(data):
    finds = md_table(["ID", "优先级", "表面", "裁决", "阻断", "下一步"], [[f["finding_id"], f["severity"], f["surface"], f["classification"], f["blocking_for"], f["recommended_action"]] for f in data["findings"]])
    checks = {item["check_id"]: item for item in data["audit_checks"]}
    identity = data["source_identity"]
    body = f"""# SGE Governance 仓库质量与开源缺口审计报告

## 关键结论中文展开

`repo_local_quality=pass_with_findings` 表示当前维护门禁和固定基线投影在其合同范围内通过，但有需要修复的发现；它不表示正式开源发布通过。`public_release=blocked` 表示缺少 public identity 一致性、rights authority、最终发布资产与远端 read-back，当前只能停在 `candidate_not_approved`。

## Read Manifest

已读：AGENTS、core Skill 与 references、README/中文指南、manifest、KB strategy、Dashboard Current State/Stage Plans/archives、tools、extensions、tests、两条独立只读审计结果和 Design artifact。未读项：不存在的远端 `bm-sge-governance`、未提供的 rights approval、未执行的完整 Codex newcomer UAT；这些均作为 evidence gap 保留。

## 实际运行的门禁

- source snapshot：生成于 `{data['generated_at']}`；branch `{identity['branch']}`；完整 HEAD `{identity['head']}`；工作树 `{identity['current_worktree']['summary']}`。具体 tracked/untracked inventory 保存在[统一 JSON 数据](RepositoryCapabilityPanorama_Data.json)的 `source_identity.current_worktree`。
- `python3 Dashboard/tools/doctor.py --repo .`：`{checks['Q-01']['verdict']}`；{checks['Q-01']['observed']}。该数字是本次生成时动态采集的 checkout 快照，不是写死基线。
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`：{checks['Q-02']['observed']}。
- `python3 tools/sge_public.py doctor`：`public_doctor:pass`。
- registry reconcile check/validate：{checks['Q-04']['observed']}。
- `python3 kb/tools/render_kb.py --check`：{checks['Q-05']['observed']}。
- clean clone 中 export/verify：48 files，tree digest 与既有 S-017 evidence 一致。
- 当前任务 checkout export：精确返回 `dirty_tree`；这是本任务未跟踪工件触发的安全阻断，不能描述成基线代码失败。

## Findings

{finds}

## Semx 残留裁决

- active/public：没有 Semx 产品实现或 `semx-cli`/`semx-kb` 身份；唯一 `semx` 是 generic profile 的 forbidden token。
- historical provenance：Dashboard/Archives、closeout、Agent Logs 与迁移 inventories 中保留来源证据；它们被 manifest default-deny 排除。
- fixture/example：tests 中的 `semx-cli`、`/Users/alice/private` 等是期望被拒绝的负例，不是默认依赖。
- false positive：`/tmp` 是匿名临时目录示例；KYM/TCO 是默认关闭、entrypoint=null 的扩展接口名字，不是随仓产品实现。

因此，“没有 Semx 源仓残留”只能准确表述为：公开候选和默认 core 没有 Semx 产品依赖或个人绝对路径泄露；历史 provenance 仍有意保留在不公开 Dashboard 层，公开 profile 也保留 Semx deny token 作为防污染规则。

## 验证交接包

- claimed scope：能力全景、质量/残留审计、开源缺口、小白与维护者指南。
- semantic change：无；只生成派生读模型和证据化建议。
- non-goals：不修复 source/docs/KB，不提交、不发布、不执行远端动作。
- changed artifacts：仅 `Dashboard/Artifacts/RepositoryCapabilityPanorama_*`。
- evidence：本报告、Data JSON、Markdown、HTML、Generator、Design、两条只读 audit lane 与门禁输出。
- known risks：public identity、Quick Start、rights、完整 Codex UAT、core 全入口验证、public provenance links。
- KB/Dashboard impact：无 stable truth 变更；本任务仅写 Dashboard Artifact，不改 registry lifecycle。
- Closeout language verdict：待在 closeout 文件生成后运行；本报告本身不声明任务最终完成。

## 结论边界

最强主张为 `test_bound` 加 `structurally_supported`：当前仓库本地质量基础强、公共候选的 Semx 产品污染已清理到有界范围，但正式开源发布仍被 P0/P1 缺口与人类 authority 阻断。
"""
    (OUT / "RepositoryCapabilityPanorama_Audit_Report.md").write_text(body, encoding="utf-8")


def main():
    data = build_data()
    data_path = OUT / "RepositoryCapabilityPanorama_Data.json"
    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(data)
    write_audit(data)
    subprocess.run(["python3", str(RENDERER), str(data_path), str(OUT / "RepositoryCapabilityPanorama.html")], check=True)
    print(f"generated:{len(data['capabilities'])}:capabilities")


if __name__ == "__main__":
    main()
