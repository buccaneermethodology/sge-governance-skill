#!/usr/bin/env python3
"""Generate the repository quality panorama derived read model."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
DASHBOARD = ROOT / "Dashboard"
ARTIFACTS = DASHBOARD / "Artifacts"


def clean(value: str) -> str:
    value = re.sub(r"<a\s+[^>]+></a>", "", value)
    value = re.sub(r"`([^`]*)`", r"\1", value)
    return value.strip()


def markdown_table(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    for start, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        if start + 1 >= len(lines) or not re.match(r"^\s*\|(?:\s*:?-{3,}:?\s*\|)+\s*$", lines[start + 1]):
            continue
        headers = [clean(cell) for cell in line.strip().strip("|").split("|")]
        rows: list[dict[str, str]] = []
        for raw in lines[start + 2 :]:
            if not raw.lstrip().startswith("|"):
                break
            cells = [clean(cell) for cell in raw.strip().strip("|").split("|")]
            if len(cells) != len(headers):
                continue
            rows.append(dict(zip(headers, cells)))
        return rows
    return []


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git_output(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False).stdout.strip()


def inventory(pattern: str) -> list[str]:
    return sorted(rel(path) for path in ROOT.glob(pattern) if path.is_file())


def as_session(row: dict[str, str], source: str) -> dict[str, object]:
    status = row.get("Status", "Unknown")
    session_id = row.get("Session Key") or row.get("ID") or "unknown"
    session_type = "Proposed" if status == "To do" else "Exploration"
    return {
        "id": session_id,
        "historical_id": row.get("Historical ID", ""),
        "type": session_type,
        "topic": row.get("Topic", ""),
        "scope": row.get("Scope", ""),
        "purpose": row.get("Purpose", ""),
        "length": "Unknown" if session_type == "Exploration" else "N/A",
        "key_points": [row.get("Deliverable", ""), row.get("Exit Criteria", "")],
        "big_ideas": ["BI-001"],
        "status": status,
        "phase_tags": [row.get("Parent", ""), row.get("Track", "")],
        "stage_plan": row.get("Parent", ""),
        "surface": "archive" if "/Archives/" in source else "current",
        "priority": row.get("Priority", ""),
        "depends_on": row.get("Depends On", ""),
        "next_step": row.get("Next Step", ""),
        "notes": row.get("Notes", ""),
        "source": source,
    }


def knowledge_session(session_id: str, topic: str, source: str, items: list[str], group: str) -> dict[str, object]:
    return {
        "id": session_id,
        "type": "Knowledge",
        "topic": topic,
        "scope": f"{len(items)} 个当前工作树表面",
        "purpose": "提供全仓导航与质量审计入口",
        "length": "N/A",
        "key_points": items[:12],
        "big_ideas": [group],
        "status": "N/A",
        "phase_tags": ["repository-inventory"],
        "priority": "",
        "stage_plan": "",
        "surface": "inventory",
        "source": source,
        "item_count": len(items),
        "all_items": items,
    }


def main() -> None:
    big_rows = markdown_table(DASHBOARD / "Big_Ideas.md")
    stage_rows = markdown_table(DASHBOARD / "Stage_Plans.md")
    current_rows = markdown_table(DASHBOARD / "Sessions.md")
    archive_rows = markdown_table(DASHBOARD / "Archives/Sessions/SP-001.md")
    decision_rows = markdown_table(DASHBOARD / "Decisions.md")
    risk_rows = markdown_table(DASHBOARD / "Risks.md")
    exception_rows = markdown_table(DASHBOARD / "Exceptions.md")

    big_ideas = [
        {
            "id": row["ID"],
            "topic": row["Topic"],
            "key_points": [row["Scope"], row["Purpose"], f"父面状态快照：{row.get('Historical Status Snapshot', 'Unknown')}", row.get("Notes", "")],
            "next_suggestions": [row.get("Next Step", "")],
            "coverage": "Unknown",
            "status": row.get("Historical Status Snapshot", ""),
            "source": "Dashboard/Big_Ideas.md",
        }
        for row in big_rows
    ]
    big_ideas.extend([
        {"id":"BQ-EXEC","topic":"执行记忆与证据拓扑","key_points":["Dashboard 是 execution memory，不是 canonical truth。","保留父面、Session、closeout、Validation 和 registry 的冲突。"],"next_suggestions":["先修复当前 active/public surface 的阻断项，再讨论发布。"],"coverage":"Unknown","status":"N/A","source":"derived grouping"},
        {"id":"BQ-QUALITY","topic":"公共边界与质量状态","key_points":["审计残留身份、缺失引用、可重跑门禁和开源 readiness。"],"next_suggestions":["以 default-deny 清单、断链 gate 和 clean-room 验收推进。"],"coverage":"Unknown","status":"N/A","source":"derived grouping"}
    ])

    sessions = [as_session(row, "Dashboard/Archives/Sessions/SP-001.md") for row in archive_rows]
    sessions.extend(as_session(row, "Dashboard/Sessions.md") for row in current_rows)

    artifact_files = inventory("Dashboard/Artifacts/*")
    agent_logs = inventory("Dashboard/Agent_Logs/*")
    kb_json = inventory("kb/data/**/*.json")
    kb_docs = inventory("kb/docs/**/*.md")
    skill_files = inventory(".codex/skills/**/*")
    test_files = inventory("tests/**/*")
    dashboard_control = [
        "Dashboard/Current_State.md", "Dashboard/Big_Ideas.md", "Dashboard/Stage_Plans.md",
        "Dashboard/Sessions.md", "Dashboard/Session_Index.md", "Dashboard/Decisions.md",
        "Dashboard/Risks.md", "Dashboard/Exceptions.md", "Dashboard/Rules.md", "Dashboard/Methodology.md"
    ]
    sessions.extend([
        knowledge_session("BQ-K1", "Dashboard 控制面", "Dashboard/", dashboard_control, "BQ-EXEC"),
        knowledge_session("BQ-K2", "Dashboard artifacts", "Dashboard/Artifacts/", artifact_files, "BQ-EXEC"),
        knowledge_session("BQ-K3", "Agent Logs", "Dashboard/Agent_Logs/", agent_logs, "BQ-EXEC"),
        knowledge_session("BQ-K4", "KB canonical JSON", "kb/data/", kb_json, "BQ-QUALITY"),
        knowledge_session("BQ-K5", "KB reader Markdown", "kb/docs/", kb_docs, "BQ-QUALITY"),
        knowledge_session("BQ-K6", "Repo-local Skill 与治理工具", ".codex/skills/", skill_files, "BQ-QUALITY"),
        knowledge_session("BQ-K7", "Tests 与验证表面", "tests/", test_files, "BQ-QUALITY"),
        knowledge_session("BQ-K8", "Decisions", "Dashboard/Decisions.md", [f"{r.get('ID')}: {r.get('Decision')} [{r.get('Status')}]" for r in decision_rows], "BQ-EXEC"),
        knowledge_session("BQ-K9", "Risks", "Dashboard/Risks.md", [f"{r.get('ID')}: {r.get('Topic')} [{r.get('Status')}]" for r in risk_rows], "BQ-EXEC"),
        knowledge_session("BQ-K10", "Exceptions", "Dashboard/Exceptions.md", [f"{r.get('ID')}: {r.get('Topic')} [{r.get('Status')}]" for r in exception_rows], "BQ-EXEC"),
    ])

    stage_plans = []
    for row in stage_rows:
        stage_plans.append({
            "id": row["ID"], "topic": row["Topic"], "scope": row["Scope"],
            "purpose": row["Purpose"], "sessions": row["Sessions"], "current_entry": row["Current Entry"],
            "required_gates": row["Required Gates"], "status": row["Status"],
            "big_ideas": ["BI-001"],
            "claim_ceiling": row["Claim Ceiling"], "next": row["Next"], "source":"Dashboard/Stage_Plans.md"
        })

    manifest_path = DASHBOARD / "Archives/Sessions/archive_manifest.json"
    archive_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_manifest = [
        {"path":"Dashboard/","note":f"控制面 {len(dashboard_control)}；artifacts {len(artifact_files)}；Agent Logs {len(agent_logs)}"},
        {"path":"kb/data/","note":f"canonical JSON {len(kb_json)}"},
        {"path":"kb/docs/","note":f"reader Markdown {len(kb_docs)}"},
        {"path":".codex/skills/","note":f"Skill/tool files {len(skill_files)}"},
        {"path":"tests/","note":f"test files {len(test_files)}"},
        {"path":"git","note":f"branch={git_output('branch', '--show-current')} HEAD={git_output('rev-parse', 'HEAD')}"},
        {"path":"git status at generation","note":git_output("status", "--short") or "clean"},
        {"path":"Dashboard/Archives/Sessions/archive_manifest.json","note":json.dumps(archive_manifest, ensure_ascii=False, sort_keys=True)}
    ]
    data = {
        "schema_version":"exploration_dashboard_v1",
        "title":"SGE Governance Skill 仓库质量 Dashboard 全景",
        "subtitle":"2026-09-02 当前工作树派生、离线、可筛选读模型；不是 canonical truth、批准凭据或完成证明",
        "generated_at":"2026-09-02",
        "generated_on":"2026-09-02",
        "claim_boundary":"仅用于导航当前 Dashboard/KB/Skill/tests/Git 与审计冲突；不得把本 HTML 当作 SP-001 完成或公共发布就绪证据。",
        "big_ideas":big_ideas,
        "stage_plans":stage_plans,
        "sessions":sessions,
        "recommendations":[
            {"id":"RQ-P0-1","priority":"P0","topic":"完成并独立验证 SP-001/S-012","reason":"当前 Stage Plan 与 Current State 均表明 S-012 Doing，SP-001 completion rule 未满足。"},
            {"id":"RQ-P0-2","priority":"P0","topic":"清理 active/public legacy 与 registry drift","reason":"archive manifest 仍含 Semx 绝对路径、S-485 和与当前 Session 数不一致的计数。"},
            {"id":"RQ-P1-1","priority":"P1","topic":"建立静态引用完整性 gate","reason":"避免 reader Markdown、Skill 和 Dashboard 使用不存在或大小写漂移的目标。"}
        ],
        "source_manifest":source_manifest,
        "visible_conflicts":[
            {"id":"CONFLICT-01","severity":"blocking-for-sp001-completion","evidence":["Dashboard/Big_Ideas.md: BI-001 historical status Done","Dashboard/Stage_Plans.md: SP-001 Doing","Dashboard/Sessions.md: SP-001/S-012 Doing"],"meaning":"父面状态未对齐；不得依据 BI-001 或 S-006 的旧结论宣称当前 SP-001 complete。"},
            {"id":"CONFLICT-02","severity":"blocking-for-registry-cleanliness","evidence":["Dashboard/Archives/Sessions/archive_manifest.json: created_by_session=S-485","source_path=/Users/.../semx-cli/Dashboard/Sessions.md","record_count=11/current_count=5"],"meaning":"派生 manifest 仍保留 Semx 来源并可能落后于新增 S-012。"}
        ]
    }

    json_path = ARTIFACTS / "RepositoryQualityPanorama_Data.json"
    md_path = ARTIFACTS / "RepositoryQualityPanorama.md"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# SGE Governance Skill 仓库质量 Dashboard 全景",
        "",
        "> 这是 2026-09-02 当前工作树的派生读模型，不是 `kb/` 真源、Dashboard 状态 authority、批准凭据或完成证明。",
        "",
        "## Big Idea: 可复用 SGE 语义治理工程与质量状态",
        "- Big Idea Length: Unknown",
        "- Coverage: Unknown",
        "- Key Points:",
        "  - SP-001 当前父状态为 `Doing`，当前入口 S-012 也是 `Doing`；旧 S-006 closeout 不覆盖新发现的 active legacy。",
        "  - 当前全景覆盖 Dashboard 控制面、Stage Plans、Sessions、Decisions、Risks、Exceptions、Artifacts、Agent Logs、KB、Skill、tests 与 Git。",
        "- Next Suggestions:",
        "  - 优先完成 S-012、修复 active/public legacy 与 registry 派生漂移，再进入 SP-002 公共候选工作。",
        "",
        "### Sessions",
        "| Session ID | Session Type | Topic | Scope | Purpose | Length (minutes) | Key Points |",
        "|------------|--------------|-------|-------|---------|-------------------|------------|",
    ]
    for session in sessions:
        points = "；".join(str(item) for item in session.get("key_points", []) if item)
        cells = [str(session.get(key, "")) for key in ("id", "type", "topic", "scope", "purpose", "length")]
        lines.append("| " + " | ".join(cell.replace("|", "\\|").replace("\n", " ") for cell in [*cells, points]) + " |")
    lines.extend([
        "", "### Assumptions", "- `Coverage` 没有可靠量化依据，因此保持 `Unknown`。",
        "- 历史 `Done` 只表示对应有界 Session 的旧终态，不自动覆盖后续新增 S-012。",
        "", "### Unresolved Questions", "- S-012 尚无 closeout/独立 Validation/post-closeout evidence 时，SP-001 不可声明完成。",
        "- 是否公开发布属于未来 SP-002 和人类授权事项，本全景不作决定。", "",
        "## 可见冲突", "",
        "- `BI-001=Done` 与 `SP-001=Doing`、`S-012=Doing` 不一致。",
        "- `archive_manifest.json` 仍含 `S-485`、Semx 绝对路径和旧计数，需以 registry check 结果判断漂移。",
        "", "## Source Manifest", "",
        f"- Dashboard artifacts: {len(artifact_files)}",
        f"- Agent Logs: {len(agent_logs)}",
        f"- KB JSON: {len(kb_json)}；KB reader Markdown: {len(kb_docs)}",
        f"- Skill/tool files: {len(skill_files)}；tests: {len(test_files)}",
        f"- Git HEAD: `{git_output('rev-parse', 'HEAD')}`；branch: `{git_output('branch', '--show-current')}`",
        "- 详细路径、Stage Plan 字段、状态、source metadata 与冲突见同名 JSON 和 HTML 详情抽屉。", ""
    ])
    md_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
