#!/usr/bin/env python3
"""Generate a read-only Dashboard governance graph.

The generated graph is a Dashboard read model. Markdown Dashboard files remain
the authority for execution state; kb remains the authority for canonical
project truth.
"""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from session_registry import SessionRecord, parse_registry_file


ID_RE = re.compile(r"\b(?:BI|SP|S|QM)-[0-9]{3}(?:-[A-Z0-9]+)?\b")
ARTIFACT_RE = re.compile(r"(Dashboard/Artifacts/[A-Za-z0-9_.\-/]+|Artifacts/[A-Za-z0-9_.\-/]+|Dashboard/[A-Za-z0-9_.\-/]+\.md)")

VISUAL_LAYERS = {
    "Dashboard": {"name": "L0 Dashboard", "x": 0.0, "color": (42, 92, 170), "size": 18.0},
    "ControlSurface": {"name": "L1 Control Surfaces", "x": 260.0, "color": (38, 139, 210), "size": 14.0},
    "BigIdea": {"name": "L2 Big Ideas", "x": 520.0, "color": (0, 128, 96), "size": 16.0},
    "StagePlan": {"name": "L3 Stage Plans", "x": 780.0, "color": (181, 137, 0), "size": 15.0},
    "Session": {"name": "L4 Sessions", "x": 1040.0, "color": (108, 113, 196), "size": 10.0},
    "Artifact": {"name": "L5 Artifacts", "x": 1300.0, "color": (203, 75, 22), "size": 8.0},
    "QualityMetric": {"name": "L6 Quality Metrics", "x": 1560.0, "color": (133, 153, 0), "size": 11.0},
}

DEFAULT_VISUAL_LAYER = {"name": "L9 Other", "x": 1820.0, "color": (101, 123, 131), "size": 8.0}


@dataclass(frozen=True)
class Row:
    line: int
    values: dict[str, str]


def _strip_cell(value: str) -> str:
    return value.strip().strip("`").strip()


def parse_table(path: Path) -> list[Row]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header: list[str] | None = None
    rows: list[Row] = []
    for line_no, line in enumerate(lines, start=1):
        if not line.startswith("|"):
            continue
        cells = [_strip_cell(cell) for cell in line.strip().strip("|").split("|")]
        if cells and cells[0] == "ID":
            header = cells
            continue
        if not header or not cells or cells[0].startswith("---"):
            continue
        if len(cells) < len(header):
            continue
        values = {name: cells[index] for index, name in enumerate(header)}
        rows.append(Row(line=line_no, values=values))
    return rows


def parse_stage_plan_table(path: Path) -> list[Row]:
    """Parse normal Stage Plan rows plus current-status mini tables.

    Most Stage Plan rows use the standard `ID` table shape. A few current
    status sections intentionally use a compact human-facing table headed
    `当前 ID`; those rows are still Stage Plan source records for the DKG read
    model and must not be dropped.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    header: list[str] | None = None
    current_section: tuple[str, str] | None = None
    parsed_rows: list[tuple[Row, str]] = []
    aliases = {
        "当前 ID": "ID",
        "当前权威状态": "Status",
        "入口与边界": "Current Entry",
    }
    for line_no, line in enumerate(lines, start=1):
        heading = re.match(r"^##\s+(SP-[0-9]{3})[:：]\s*(.+?)\s*$", line)
        if heading:
            title = re.sub(r"\s*（[^）]*）\s*$", "", heading.group(2)).strip()
            current_section = (heading.group(1), title)
            header = None
            continue
        if not line.startswith("|"):
            continue
        cells = [_strip_cell(cell) for cell in line.strip().strip("|").split("|")]
        if cells and cells[0] in {"ID", "当前 ID"}:
            table_kind = "current_status" if cells[0] == "当前 ID" else "standard"
            header = [aliases.get(cell, cell) for cell in cells]
            continue
        if not header or not cells or cells[0].startswith("---"):
            continue
        if len(cells) < len(header):
            continue
        values = {name: cells[index] for index, name in enumerate(header)}
        if (
            current_section
            and values.get("ID") == current_section[0]
            and not values.get("Topic")
        ):
            values["Topic"] = current_section[1]
        parsed_rows.append((Row(line=line_no, values=values), table_kind))

    ordered_ids: list[str] = []
    standard_by_id: dict[str, Row] = {}
    current_by_id: dict[str, Row] = {}
    for row, table_kind in parsed_rows:
        identifier = row.values.get("ID", "")
        if not identifier:
            continue
        if identifier not in ordered_ids:
            ordered_ids.append(identifier)
        if table_kind == "standard":
            standard_by_id[identifier] = row
        else:
            current_by_id[identifier] = row

    rows: list[Row] = []
    for identifier in ordered_ids:
        standard = standard_by_id.get(identifier)
        current = current_by_id.get(identifier)
        source_row = current or standard
        if source_row is None:
            continue
        values: dict[str, str] = {}
        if standard:
            values.update(standard.values)
        if current:
            values.update(current.values)
        rows.append(Row(line=source_row.line, values=values))
    return rows


def add_node(nodes: dict[str, dict[str, Any]], node: dict[str, Any]) -> None:
    existing = nodes.get(node["id"])
    if existing is None:
        nodes[node["id"]] = node
        return
    if existing != node:
        raise ValueError(
            f"duplicate graph node id with conflicting content: {node['id']}"
        )


def add_edge(edges: list[dict[str, Any]], source: str, target: str, edge_type: str, **attrs: Any) -> None:
    if not source or not target or source == target:
        return
    edge_id = f"{source}->{edge_type}->{target}"
    if any(edge["id"] == edge_id for edge in edges):
        return
    edge = {"id": edge_id, "source": source, "target": target, "type": edge_type}
    edge.update({key: value for key, value in attrs.items() if value not in ("", None, [])})
    edges.append(edge)


def ensure_track_reference_node(
    nodes: dict[str, dict[str, Any]],
    track_id: str,
    source_path: str,
    source_line: int,
) -> None:
    """Materialize an explicitly non-authoritative node for legacy track refs.

    Historical Session rows can retain a BI identifier that no longer has an
    active Big_Ideas.md row. Keeping that locator is useful, but an edge must
    never silently point outside the graph or recreate the identifier as an
    active BigIdea.
    """
    if track_id in nodes:
        return
    add_node(nodes, {
        "id": track_id,
        "type": "LegacyTrackReference",
        "title": f"{track_id} historical Session track reference",
        "status": "referenced_only_not_registered",
        "authority": "non_authoritative_locator_only",
        "source": {"path": source_path, "line": source_line},
    })


def validate_edge_endpoints(
    nodes: dict[str, dict[str, Any]],
    edges: list[dict[str, Any]],
) -> None:
    dangling = [
        edge for edge in edges
        if edge["source"] not in nodes or edge["target"] not in nodes
    ]
    if dangling:
        examples = ", ".join(edge["id"] for edge in dangling[:5])
        raise ValueError(
            f"graph contains {len(dangling)} dangling edge endpoints: {examples}"
        )


def ids_in(text: str) -> list[str]:
    seen: list[str] = []
    for match in ID_RE.findall(text or ""):
        if match not in seen:
            seen.append(match)
    return seen


def artifact_paths(text: str) -> list[str]:
    paths: list[str] = []
    for match in ARTIFACT_RE.findall(text or ""):
        path = match
        if path.startswith("Artifacts/"):
            path = f"Dashboard/{path}"
        if path not in paths:
            paths.append(path)
    return paths


def path_node_id(path: str) -> str:
    return f"artifact:{path}"


def load_session_records(dashboard: Path) -> list[tuple[SessionRecord, str]]:
    located: list[tuple[SessionRecord, str]] = [
        (record, "Dashboard/Sessions.md")
        for record in parse_registry_file(dashboard / "Sessions.md")
    ]
    archive_root = dashboard / "Archives" / "Sessions"
    for path in sorted(archive_root.glob("*.md")):
        if path.name == "Legacy_Execution_Notes.md":
            continue
        relative = path.relative_to(dashboard.parent).as_posix()
        located.extend(
            (record, relative) for record in parse_registry_file(path)
        )
    return located


def session_resolver(
    located: list[tuple[SessionRecord, str]],
) -> tuple[dict[str, list[str]], dict[str, SessionRecord]]:
    by_historical: dict[str, list[str]] = {}
    by_key: dict[str, SessionRecord] = {}
    for record, _ in located:
        if record.session_key in by_key:
            raise ValueError(f"duplicate canonical Session Key: {record.session_key}")
        by_key[record.session_key] = record
        by_historical.setdefault(record.historical_id, []).append(record.session_key)
    return by_historical, by_key


def resolve_session_refs(
    historical_id: str,
    by_historical: dict[str, list[str]],
    parent_context: str | None = None,
) -> list[str]:
    matches = list(by_historical.get(historical_id, []))
    if parent_context:
        contextual = [
            key for key in matches if key.startswith(f"{parent_context}/")
        ]
        if contextual:
            return contextual
    return matches


def build_graph(repo_root: Path, created_by_session: str, created_at: str) -> dict[str, Any]:
    dashboard = repo_root / "Dashboard"
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    located_sessions = load_session_records(dashboard)
    by_historical, _session_by_key = session_resolver(located_sessions)

    add_node(nodes, {"id": "dashboard", "type": "Dashboard", "title": "Semx Dashboard", "authority": "execution_memory"})
    add_node(nodes, {"id": "file:Dashboard/Current_State.md", "type": "ControlSurface", "title": "Current Execution Surface", "path": "Dashboard/Current_State.md"})
    add_node(nodes, {"id": "file:Dashboard/Artifacts_Index.md", "type": "ControlSurface", "title": "Dashboard Artifacts Index", "path": "Dashboard/Artifacts_Index.md"})
    add_edge(edges, "dashboard", "file:Dashboard/Current_State.md", "HAS_CONTROL_SURFACE")
    add_edge(edges, "dashboard", "file:Dashboard/Artifacts_Index.md", "HAS_CONTROL_SURFACE")

    for row in parse_table(dashboard / "Big_Ideas.md"):
        value = row.values
        node_id = value["ID"]
        status = value.get("Status") or value.get("Historical Status Snapshot", "")
        add_node(nodes, {
            "id": node_id,
            "type": "BigIdea",
            "title": value.get("Topic", ""),
            "status": status,
            "scope": value.get("Scope", ""),
            "purpose": value.get("Purpose", ""),
            "next_step": value.get("Next Step", ""),
            "source": {"path": "Dashboard/Big_Ideas.md", "line": row.line},
        })
        add_edge(edges, "dashboard", node_id, "HAS_BIG_IDEA")
        for path in artifact_paths(" ".join(value.values())):
            aid = path_node_id(path)
            add_node(nodes, {"id": aid, "type": "Artifact", "path": path, "title": Path(path).name})
            add_edge(edges, node_id, aid, "REFERENCES_ARTIFACT")

    for row in parse_stage_plan_table(dashboard / "Stage_Plans.md"):
        value = row.values
        node_id = value["ID"]
        add_node(nodes, {
            "id": node_id,
            "type": "StagePlan",
            "title": value.get("Topic", ""),
            "status": value.get("Status", ""),
            "purpose": value.get("Purpose", ""),
            "next_step": value.get("Next Step", ""),
            "source": {"path": "Dashboard/Stage_Plans.md", "line": row.line},
        })
        add_edge(edges, "dashboard", node_id, "HAS_STAGE_PLAN")
        for ref in ids_in(value.get("Backlog", "")):
            if ref.startswith("S-"):
                for resolved in resolve_session_refs(ref, by_historical, node_id):
                    add_edge(edges, node_id, resolved, "HAS_BACKLOG_SESSION")
            else:
                add_edge(edges, node_id, ref, "HAS_BACKLOG_SESSION")

    for record, source_path in located_sessions:
        node_id = record.session_key
        add_node(nodes, {
            "id": node_id,
            "type": "Session",
            "historical_id": record.historical_id,
            "parent_stage_plan": record.parent,
            "title": record.topic,
            "status": record.status,
            "historical_status_snapshot": record.historical_status,
            "priority": record.priority,
            "track": record.track,
            "scope": record.scope,
            "purpose": record.purpose,
            "deliverable": record.deliverable,
            "exit_criteria": record.exit_criteria,
            "next_step": record.next_step,
            "notes": record.notes,
            "source": {"path": source_path, "line": record.source_line},
        })
        add_edge(edges, "dashboard", node_id, "HAS_SESSION")
        for track in ids_in(record.track):
            if track.startswith("BI-"):
                ensure_track_reference_node(
                    nodes, track, source_path, record.source_line
                )
                add_edge(edges, track, node_id, "OWNS_SESSION")
                add_edge(edges, node_id, track, "BELONGS_TO")
        for dep in ids_in(record.depends_on):
            if dep.startswith("S-"):
                for resolved in resolve_session_refs(dep, by_historical, record.parent):
                    add_edge(edges, node_id, resolved, "DEPENDS_ON")
            else:
                add_edge(edges, node_id, dep, "DEPENDS_ON")
        for path in artifact_paths(" ".join([record.deliverable, record.notes])):
            aid = path_node_id(path)
            add_node(nodes, {"id": aid, "type": "Artifact", "path": path, "title": Path(path).name})
            add_edge(edges, node_id, aid, "PRODUCES_OR_REFERENCES")
        if record.historical_id == "S-199":
            for reconciled in ["S-167", "S-169", "S-171", "S-172", "S-174", "S-178", "S-183"]:
                for resolved in resolve_session_refs(reconciled, by_historical):
                    add_edge(edges, node_id, resolved, "RECONCILES")
        if record.historical_id == "S-236":
            for produced in [
                "Dashboard/Current_State.md",
                "Dashboard/Artifacts_Index.md",
                "Dashboard/Artifacts/S236_DashboardOperatingBalance_Recommendations.md",
                "Dashboard/Artifacts/S236_DashboardStewardshipControlSurfaces_Closeout.md",
            ]:
                aid = path_node_id(produced)
                add_node(nodes, {"id": aid, "type": "Artifact", "path": produced, "title": Path(produced).name})
                add_edge(edges, node_id, aid, "PRODUCES")

    for row in parse_table(dashboard / "Quality_Metrics.md"):
        value = row.values
        metric_id = value.get("ID", "")
        if not metric_id.startswith("QM-"):
            continue
        add_node(nodes, {
            "id": metric_id,
            "type": "QualityMetric",
            "title": value.get("Metric", ""),
            "status": value.get("Status", ""),
            "definition": value.get("Definition", ""),
            "source": {"path": "Dashboard/Quality_Metrics.md", "line": row.line},
        })
        add_edge(edges, "dashboard", metric_id, "HAS_QUALITY_METRIC")

    current_text = (dashboard / "Current_State.md").read_text(encoding="utf-8")
    for ref in ids_in(current_text):
        if ref.startswith("S-"):
            for resolved in resolve_session_refs(ref, by_historical):
                add_edge(edges, "file:Dashboard/Current_State.md", resolved, "RECOMMENDS_OR_MENTIONS")
        elif ref in nodes:
            add_edge(edges, "file:Dashboard/Current_State.md", ref, "RECOMMENDS_OR_MENTIONS")
    for path in artifact_paths((dashboard / "Artifacts_Index.md").read_text(encoding="utf-8")):
        aid = path_node_id(path)
        add_node(nodes, {"id": aid, "type": "Artifact", "path": path, "title": Path(path).name})
        add_edge(edges, "file:Dashboard/Artifacts_Index.md", aid, "INDEXES")

    validate_edge_endpoints(nodes, edges)
    graph = {
        "schema_id": "semx.dashboard_kg.dkg_l1",
        "schema_version": "dkg-l1.0",
        "graph_layer": "DKG-L1",
        "authority": {
            "truth_source_root": "Dashboard",
            "truth_source_kind": "markdown_execution_memory",
            "projection_role": "read_only_generated_dashboard_governance_projection",
            "kb_role": "canonical_truth_reference_only",
            "runtime_role": "runtime_reference_only",
        },
        "metadata": {
            "created_by_session": created_by_session,
            "created_at": created_at,
            "source_files": [
                "Dashboard/Big_Ideas.md",
                "Dashboard/Stage_Plans.md",
                "Dashboard/Sessions.md",
                "Dashboard/Session_Index.md",
                "Dashboard/Archives/Sessions/archive_manifest.json",
                "Dashboard/Quality_Metrics.md",
                "Dashboard/Current_State.md",
                "Dashboard/Artifacts_Index.md",
            ],
        },
        "nodes": sorted(nodes.values(), key=lambda node: node["id"]),
        "edges": sorted(edges, key=lambda edge: edge["id"]),
        "query_examples": query_examples(nodes, edges),
    }
    return graph


def query_examples(nodes: dict[str, dict[str, Any]], edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def outgoing(source: str, edge_type: str) -> list[str]:
        return [edge["target"] for edge in edges if edge["source"] == source and edge["type"] == edge_type]

    def incoming(target: str, edge_type: str) -> list[str]:
        return [edge["source"] for edge in edges if edge["target"] == target and edge["type"] == edge_type]

    open_stage_plans = [
        {"id": node["id"], "title": node.get("title"), "next_step": node.get("next_step")}
        for node in nodes.values()
        if node.get("type") == "StagePlan" and node.get("status") == "todo"
    ]
    bi015_sessions = [
        {"id": sid, "title": nodes[sid].get("title"), "status": nodes[sid].get("status"), "next_step": nodes[sid].get("next_step")}
        for sid in outgoing("BI-015", "OWNS_SESSION")
        if sid in nodes
    ]
    def unique_session_key(historical_id: str) -> str | None:
        matches = [
            node["id"]
            for node in nodes.values()
            if node.get("type") == "Session"
            and node.get("historical_id") == historical_id
        ]
        return matches[0] if len(matches) == 1 else None

    s199 = unique_session_key("S-199")
    s236 = unique_session_key("S-236")
    s199_reconciled = [
        {"id": sid, "title": nodes.get(sid, {}).get("title"), "next_step": nodes.get(sid, {}).get("next_step")}
        for sid in outgoing(s199, "RECONCILES") if s199
    ]
    s236_artifacts = [
        {"id": aid, "path": nodes.get(aid, {}).get("path"), "title": nodes.get(aid, {}).get("title")}
        for aid in outgoing(s236, "PRODUCES") if s236
    ]
    s199_dependents = [
        {"id": sid, "title": nodes.get(sid, {}).get("title"), "status": nodes.get(sid, {}).get("status")}
        for sid in incoming(s199, "DEPENDS_ON") if s199
    ]
    return [
        {
            "id": "DQ-001",
            "question": "Which Stage Plans are currently open?",
            "answer_type": "answerable_from_dkg",
            "answer": open_stage_plans,
        },
        {
            "id": "DQ-002",
            "question": "Which Sessions belong to BI-015 and what is their current posture?",
            "answer_type": "answerable_from_dkg",
            "answer": bi015_sessions,
        },
        {
            "id": "DQ-003",
            "question": "What did S-199 reconcile?",
            "answer_type": "answerable_from_dkg",
            "answer": s199_reconciled,
        },
        {
            "id": "DQ-004",
            "question": "What artifacts did S-236 produce?",
            "answer_type": "answerable_from_dkg",
            "answer": s236_artifacts,
        },
        {
            "id": "DQ-005",
            "question": "Which Sessions explicitly depend on S-199?",
            "answer_type": "answerable_from_dkg",
            "answer": s199_dependents,
        },
        {
            "id": "DQ-006",
            "question": "Can Dashboard KG answer whether runtime validation passed?",
            "answer_type": "not_authorized_from_dkg",
            "answer": "No. DKG-L1 is Dashboard execution-memory projection only; runtime/test pass-fail belongs to test outputs, validation reports, or closeout evidence.",
        },
    ]


def write_query_report(graph: dict[str, Any], out: Path) -> None:
    lines = [
        "# Dashboard KG Query Report",
        "",
        f"_Generated by: {graph['metadata']['created_by_session']} | Date: {graph['metadata']['created_at']}_",
        "",
        "This report demonstrates the current Dashboard KG query pack. It is a read model over Dashboard Markdown, not canonical KB truth.",
        "",
    ]
    for query in graph["query_examples"]:
        lines.append(f"## {query['id']} {query['question']}")
        lines.append("")
        lines.append(f"Answer type: `{query['answer_type']}`")
        lines.append("")
        answer = query["answer"]
        if isinstance(answer, list):
            if not answer:
                lines.append("- No matching records.")
            for item in answer:
                item_id = item.get("id", "")
                title = item.get("title") or item.get("path") or ""
                detail = item.get("next_step") or item.get("status") or ""
                lines.append(f"- `{item_id}` {title} — {detail}")
        else:
            lines.append(str(answer))
        lines.append("")
    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def graphology_attributes(item: dict[str, Any], excluded: set[str]) -> dict[str, Any]:
    attrs: dict[str, Any] = {}
    for key, value in item.items():
        if key in excluded or value in ("", None, [], {}):
            continue
        if isinstance(value, (str, int, float, bool)):
            attrs[key] = value
        else:
            attrs[key] = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return attrs


def to_graphology(graph: dict[str, Any]) -> dict[str, Any]:
    """Convert DKG-L1 to Graphology's serialized JSON shape.

    Gephi Lite imports Graphology JSON with node `key` fields. The DKG-L1
    projection intentionally uses `id`, so the visual export stays separate.
    """
    return {
        "options": {
            "type": "directed",
            "multi": True,
            "allowSelfLoops": False,
        },
        "attributes": {
            "name": "Semx Dashboard Operating Graph",
            "schema_id": graph.get("schema_id", ""),
            "schema_version": graph.get("schema_version", ""),
            "graph_layer": graph.get("graph_layer", ""),
            "authority": json.dumps(graph.get("authority", {}), ensure_ascii=False, sort_keys=True),
            "created_by_session": graph.get("metadata", {}).get("created_by_session", ""),
            "created_at": graph.get("metadata", {}).get("created_at", ""),
        },
        "nodes": [
            {
                "key": node["id"],
                "attributes": {
                    "label": node.get("title") or node["id"],
                    **graphology_attributes(node, {"id", "title"}),
                },
            }
            for node in graph["nodes"]
        ],
        "edges": [
            {
                "key": edge["id"],
                "source": edge["source"],
                "target": edge["target"],
                "attributes": {
                    "label": edge.get("type", ""),
                    **graphology_attributes(edge, {"id", "source", "target"}),
                },
            }
            for edge in graph["edges"]
        ],
    }


def _xml_text(value: Any) -> str:
    if value in ("", None, [], {}):
        return ""
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def visual_style_for(node: dict[str, Any]) -> dict[str, Any]:
    return VISUAL_LAYERS.get(node.get("type", ""), DEFAULT_VISUAL_LAYER)


def visual_positions(nodes: list[dict[str, Any]]) -> dict[str, tuple[float, float]]:
    by_type: dict[str, list[dict[str, Any]]] = {}
    for node in nodes:
        by_type.setdefault(node.get("type", ""), []).append(node)
    positions: dict[str, tuple[float, float]] = {}
    for node_type, typed_nodes in by_type.items():
        layer = VISUAL_LAYERS.get(node_type, DEFAULT_VISUAL_LAYER)
        ordered = sorted(typed_nodes, key=lambda item: item["id"])
        count = len(ordered)
        spacing = 42.0 if count <= 80 else max(12.0, 3300.0 / count)
        start_y = -((count - 1) * spacing) / 2.0
        for index, node in enumerate(ordered):
            positions[node["id"]] = (layer["x"], start_y + index * spacing)
    return positions


def write_gexf(graph: dict[str, Any], out: Path) -> None:
    """Write a Gephi / Gephi Lite compatible GEXF visual export."""
    ET.register_namespace("", "http://www.gexf.net/1.3")
    ET.register_namespace("viz", "http://www.gexf.net/1.3/viz")
    gexf = ET.Element(
        "{http://www.gexf.net/1.3}gexf",
        {
            "version": "1.3",
        },
    )
    meta = ET.SubElement(gexf, "{http://www.gexf.net/1.3}meta")
    ET.SubElement(meta, "{http://www.gexf.net/1.3}creator").text = "Semx Dashboard KG"
    ET.SubElement(meta, "{http://www.gexf.net/1.3}description").text = (
        "Generated Dashboard Operating Graph visual export. "
        "Dashboard Markdown remains the authority for execution memory."
    )
    graph_el = ET.SubElement(
        gexf,
        "{http://www.gexf.net/1.3}graph",
        {
            "mode": "static",
            "defaultedgetype": "directed",
        },
    )

    node_attr_keys = [
        "type",
        "visual_layer",
        "status",
        "priority",
        "track",
        "path",
        "source",
        "scope",
        "purpose",
        "next_step",
        "notes",
    ]
    edge_attr_keys = ["type"]
    attrs_nodes = ET.SubElement(graph_el, "{http://www.gexf.net/1.3}attributes", {"class": "node"})
    for index, key in enumerate(node_attr_keys):
        ET.SubElement(attrs_nodes, "{http://www.gexf.net/1.3}attribute", {"id": f"n{index}", "title": key, "type": "string"})
    attrs_edges = ET.SubElement(graph_el, "{http://www.gexf.net/1.3}attributes", {"class": "edge"})
    for index, key in enumerate(edge_attr_keys):
        ET.SubElement(attrs_edges, "{http://www.gexf.net/1.3}attribute", {"id": f"e{index}", "title": key, "type": "string"})

    nodes_el = ET.SubElement(graph_el, "{http://www.gexf.net/1.3}nodes")
    positions = visual_positions(graph["nodes"])
    for node in graph["nodes"]:
        layer = visual_style_for(node)
        node_el = ET.SubElement(
            nodes_el,
            "{http://www.gexf.net/1.3}node",
            {
                "id": node["id"],
                "label": node.get("title") or node["id"],
            },
        )
        values_el = ET.SubElement(node_el, "{http://www.gexf.net/1.3}attvalues")
        for index, key in enumerate(node_attr_keys):
            text = layer["name"] if key == "visual_layer" else _xml_text(node.get(key))
            if text:
                ET.SubElement(values_el, "{http://www.gexf.net/1.3}attvalue", {"for": f"n{index}", "value": text})
        x, y = positions[node["id"]]
        red, green, blue = layer["color"]
        ET.SubElement(
            node_el,
            "{http://www.gexf.net/1.3/viz}position",
            {"x": f"{x:.2f}", "y": f"{y:.2f}", "z": "0.0"},
        )
        ET.SubElement(
            node_el,
            "{http://www.gexf.net/1.3/viz}color",
            {"r": str(red), "g": str(green), "b": str(blue)},
        )
        ET.SubElement(
            node_el,
            "{http://www.gexf.net/1.3/viz}size",
            {"value": f"{layer['size']:.2f}"},
        )

    edges_el = ET.SubElement(graph_el, "{http://www.gexf.net/1.3}edges")
    for edge in graph["edges"]:
        edge_el = ET.SubElement(
            edges_el,
            "{http://www.gexf.net/1.3}edge",
            {
                "id": edge["id"],
                "source": edge["source"],
                "target": edge["target"],
                "label": edge.get("type", ""),
            },
        )
        values_el = ET.SubElement(edge_el, "{http://www.gexf.net/1.3}attvalues")
        for index, key in enumerate(edge_attr_keys):
            text = _xml_text(edge.get(key))
            if text:
                ET.SubElement(values_el, "{http://www.gexf.net/1.3}attvalue", {"for": f"e{index}", "value": text})

    tree = ET.ElementTree(gexf)
    ET.indent(tree, space="  ")
    tree.write(out, encoding="utf-8", xml_declaration=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", required=True)
    parser.add_argument("--query-report", required=True)
    parser.add_argument("--graphology-out")
    parser.add_argument("--gexf-out")
    parser.add_argument("--created-by-session", default="S-237")
    parser.add_argument("--created-at", default=str(date.today()))
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    graph = build_graph(repo_root, args.created_by_session, args.created_at)
    out = Path(args.out)
    report = Path(args.query_report)
    out.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_query_report(graph, report)
    print(f"Dashboard KG: {out}")
    print(f"Query report: {report}")
    if args.graphology_out:
        graphology_out = Path(args.graphology_out)
        graphology_out.parent.mkdir(parents=True, exist_ok=True)
        graphology_out.write_text(json.dumps(to_graphology(graph), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Graphology JSON: {graphology_out}")
    if args.gexf_out:
        gexf_out = Path(args.gexf_out)
        gexf_out.parent.mkdir(parents=True, exist_ok=True)
        write_gexf(graph, gexf_out)
        print(f"GEXF: {gexf_out}")
    print(f"nodes={len(graph['nodes'])} edges={len(graph['edges'])} queries={len(graph['query_examples'])}")


if __name__ == "__main__":
    main()
