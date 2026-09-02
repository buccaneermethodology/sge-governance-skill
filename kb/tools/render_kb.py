from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DOC_TYPES = {
    "architecture",
    "logical_pipeline",
    "phase_spec",
    "strategy",
    "cli_spec",
    "artifact_spec",
    "evolution_log",
    "glossary",
    "adr",
}

SECTION_KINDS = {
    "narrative",
    "definition",
    "table",
    "checklist",
    "phase_contract",
    "dsl_spec",
    "json_schema_ref",
    "appendix",
}

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render SGE Governance kb Doc-as-Data JSON into Markdown.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DATA_DIR,
        help="Directory containing kb JSON sources.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_doc(path: Path, doc: dict[str, Any]) -> None:
    if doc.get("kind") == "kb_index":
        required = {"kind", "title", "version", "status", "updated_at", "output_path", "overview", "doc_groups"}
        missing = sorted(required - set(doc))
        if missing:
            raise ValueError(f"{path}: missing kb_index fields: {', '.join(missing)}")
        return

    required = {"doc_id", "doc_type", "title", "version", "status", "metadata", "sections", "output_path"}
    missing = sorted(required - set(doc))
    if missing:
        raise ValueError(f"{path}: missing fields: {', '.join(missing)}")

    if doc["doc_type"] not in DOC_TYPES:
        raise ValueError(f"{path}: unsupported doc_type {doc['doc_type']!r}")

    metadata = doc["metadata"]
    for field in ("owner", "updated_at", "source_scope"):
        if field not in metadata:
            raise ValueError(f"{path}: metadata missing field {field!r}")

    for section in doc["sections"]:
        for field in ("section_id", "heading", "kind", "content"):
            if field not in section:
                raise ValueError(f"{path}: section missing field {field!r}")
        if section["kind"] not in SECTION_KINDS:
            raise ValueError(f"{path}: unsupported section kind {section['kind']!r}")
        if section["kind"] == "phase_contract":
            phase_fields = {
                "goal",
                "inputs",
                "outputs",
                "internal_logic",
                "constraints",
                "failure_modes",
                "upstream",
                "downstream",
            }
            missing_phase_fields = sorted(phase_fields - set(section["content"]))
            if missing_phase_fields:
                raise ValueError(
                    f"{path}: phase_contract missing fields: {', '.join(missing_phase_fields)}"
                )


def render_narrative(content: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for paragraph in content.get("paragraphs", []):
        lines.append(paragraph)
        lines.append("")

    bullets = content.get("bullets", [])
    for bullet in bullets:
        lines.append(f"- {bullet}")
    if bullets:
        lines.append("")

    ordered = content.get("ordered", [])
    for item in ordered:
        lines.append(f"1. {item}")
    if ordered:
        lines.append("")

    for block in content.get("code_blocks", []):
        language = block.get("language", "")
        lines.append(f"```{language}")
        lines.append(block["content"])
        lines.append("```")
        lines.append("")

    return lines


def render_definition(content: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for entry in content.get("entries", []):
        term = f"**{entry['term']}**"
        if entry.get("full_name"):
            term = f"{term} ({entry['full_name']})"
        definition = f"{term}: {entry['definition']}"
        if entry.get("notes"):
            definition = f"{definition} {entry['notes']}"
        lines.append(f"- {definition}")
        details = render_definition_details(entry)
        lines.extend(f"  - {detail}" for detail in details)
    if lines:
        lines.append("")
    return lines


def coerce_markdown_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    return [str(value)]


def render_definition_details(entry: dict[str, Any]) -> list[str]:
    details: list[str] = []
    scalar_fields = [
        ("Scope", "scope"),
        ("Owner", "owner"),
        ("Authority", "authority"),
        ("Purpose", "purpose"),
        ("Relationship", "relationship"),
    ]
    for label, key in scalar_fields:
        if entry.get(key):
            details.append(f"{label}: {entry[key]}")

    list_fields = [
        ("Contains", "contains"),
        ("Governs", "governs"),
        ("Owns", "owns"),
        ("Does not own", "does_not_own"),
    ]
    for label, key in list_fields:
        values = coerce_markdown_list(entry.get(key))
        if values:
            details.append(f"{label}: " + "; ".join(values))

    boundary = entry.get("boundary")
    if isinstance(boundary, dict):
        not_values = coerce_markdown_list(boundary.get("not"))
        if not_values:
            details.append("Not: " + "; ".join(not_values))
        claim_ceiling = boundary.get("claim_ceiling")
        if claim_ceiling:
            details.append(f"Claim ceiling: {claim_ceiling}")
        forbidden_overreads = coerce_markdown_list(boundary.get("forbidden_overreads"))
        if forbidden_overreads:
            details.append("Forbidden overreads: " + "; ".join(forbidden_overreads))
    elif boundary:
        details.append(f"Boundary: {boundary}")

    related = coerce_markdown_list(entry.get("related_concepts"))
    if related:
        details.append("Related: " + ", ".join(related))

    source_refs = coerce_markdown_list(entry.get("source_refs"))
    if source_refs:
        details.append("Source refs: " + ", ".join(f"`{ref}`" for ref in source_refs))

    return details


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|")


def render_table(content: dict[str, Any]) -> list[str]:
    columns = content.get("columns", [])
    rows = content.get("rows", [])
    if not columns:
        return []

    lines = [
        "| " + " | ".join(markdown_escape(str(column)) for column in columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_escape(str(cell)) for cell in row) + " |")
    lines.append("")
    return lines


def render_checklist(content: dict[str, Any]) -> list[str]:
    lines = [f"- [ ] {item}" for item in content.get("items", [])]
    if lines:
        lines.append("")
    return lines


def render_appendix(content: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for subsection in content.get("subsections", []):
        lines.append(f"### {subsection['title']}")
        lines.append("")
        lines.extend(render_narrative(subsection))
    return lines


def render_phase_contract(content: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    phase_fields = [
        ("Goal", content.get("goal", "")),
        ("Inputs", content.get("inputs", [])),
        ("Outputs", content.get("outputs", [])),
        ("Internal Logic", content.get("internal_logic", [])),
        ("Constraints", content.get("constraints", [])),
        ("Failure Modes", content.get("failure_modes", [])),
        ("Upstream", content.get("upstream", [])),
        ("Downstream", content.get("downstream", [])),
    ]

    for heading, value in phase_fields:
        lines.append(f"### {heading}")
        lines.append("")
        if isinstance(value, str):
            if value:
                lines.append(value)
                lines.append("")
            else:
                lines.append("_None_")
                lines.append("")
            continue

        if isinstance(value, list) and value:
            marker = "1." if heading == "Internal Logic" else "-"
            for item in value:
                lines.append(f"{marker} {item}")
            lines.append("")
            continue

        lines.append("_None_")
        lines.append("")

    return lines


def render_section(section: dict[str, Any]) -> list[str]:
    kind = section["kind"]
    content = section["content"]

    if kind == "phase_contract":
        lines = render_phase_contract(content)
    elif kind in {"narrative", "dsl_spec", "json_schema_ref"}:
        lines = render_narrative(content)
    elif kind == "definition":
        lines = render_definition(content)
    elif kind == "table":
        lines = render_table(content)
    elif kind == "checklist":
        lines = render_checklist(content)
    elif kind == "appendix":
        lines = render_appendix(content)
    else:
        lines = [f"_Unsupported section kind: {kind}_", ""]

    constraints = section.get("constraints", [])
    if constraints:
        lines.append("**Section Constraints**")
        lines.append("")
        for constraint in constraints:
            lines.append(f"- {constraint}")
        lines.append("")

    if not lines or lines[-1] != "":
        lines.append("")
    return lines


def render_doc(doc: dict[str, Any]) -> str:
    lines = [f"# {doc['title']}", ""]
    metadata = doc["metadata"]
    lines.append(
        f"_Owner: {metadata['owner']} | Version: {doc['version']} | "
        f"Status: {doc['status']} | Updated: {metadata['updated_at']}_"
    )
    lines.append("")

    for section in doc["sections"]:
        lines.append(f"## {section['heading']}")
        lines.append("")
        lines.extend(render_section(section))

    lines.append("## Source Scope")
    lines.append("")
    for source in metadata["source_scope"]:
        lines.append(f"- `{source}`")
    lines.append("")

    depends = metadata.get("depends_on_docs", [])
    if depends:
        lines.append("## Related Docs")
        lines.append("")
        for doc_id in depends:
            lines.append(f"- `{doc_id}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_index(doc: dict[str, Any]) -> str:
    lines = [f"# {doc['title']}", ""]
    lines.append(f"_Version: {doc['version']} | Status: {doc['status']} | Updated: {doc['updated_at']}_")
    lines.append("")

    for paragraph in doc.get("overview", []):
        lines.append(paragraph)
        lines.append("")

    scope = doc.get("current_scope", [])
    if scope:
        lines.append("## Current Scope")
        lines.append("")
        for item in scope:
            lines.append(f"- {item}")
        lines.append("")

    workflow = doc.get("build_process", [])
    if workflow:
        lines.append("## Build Process")
        lines.append("")
        for item in workflow:
            lines.append(f"1. {item}")
        lines.append("")

    lines.append("## Document Map")
    lines.append("")
    for group in doc["doc_groups"]:
        lines.append(f"### {group['heading']}")
        lines.append("")
        for item in group.get("items", []):
            lines.append(f"- [{item['title']}]({item['path']}): {item['summary']}")
        lines.append("")

    source_notes = doc.get("source_notes", [])
    if source_notes:
        lines.append("## Source Notes")
        lines.append("")
        for note in source_notes:
            lines.append(f"- {note}")
        lines.append("")

    open_questions = doc.get("open_questions", [])
    if open_questions:
        lines.append("## Open Questions")
        lines.append("")
        for question in open_questions:
            lines.append(f"- {question}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_file(path: Path, data_dir: Path) -> Path:
    doc = load_json(path)
    validate_doc(path, doc)
    output_path = data_dir.parent / doc["output_path"]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rendered = render_index(doc) if doc.get("kind") == "kb_index" else render_doc(doc)
    output_path.write_text(rendered, encoding="utf-8")
    return output_path


def main() -> None:
    args = parse_args()
    data_dir = args.data_dir.resolve()
    rendered_paths = []
    for path in sorted(data_dir.rglob("*.json")):
        rendered_paths.append(render_file(path, data_dir))

    for path in rendered_paths:
        print(path.relative_to(data_dir.parent))


if __name__ == "__main__":
    main()
