from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
GLOSSARY_PATH = REPO_ROOT / "data/glossary.json"
RENDERED_GLOSSARY_PATH = REPO_ROOT / "docs/Glossary.md"

ROOT_KEYS = {
    "doc_id",
    "doc_type",
    "title",
    "version",
    "status",
    "output_path",
    "metadata",
    "sections",
}
METADATA_KEYS = {"owner", "updated_at", "source_scope", "depends_on_docs", "tags", "version"}
SECTION_KEYS = {"section_id", "heading", "kind", "content"}
CONTENT_KEYS = {"entries"}
LEGACY_ENTRY_KEYS = {"term", "definition", "notes"}
STRUCTURED_ENTRY_KEYS = {
    "term",
    "definition",
    "full_name",
    "scope",
    "owner",
    "authority",
    "purpose",
    "relationship",
    "contains",
    "governs",
    "owns",
    "does_not_own",
    "boundary",
    "related_concepts",
    "source_refs",
    "notes",
}
STRUCTURED_REQUIRED_FIELDS = {
    "term",
    "definition",
    "scope",
    "owner",
    "authority",
    "boundary",
    "related_concepts",
    "source_refs",
}
BOUNDARY_KEYS = {"not", "claim_ceiling", "forbidden_overreads"}
BOUNDARY_REQUIRED_FIELDS = {"not", "claim_ceiling", "forbidden_overreads"}
STRING_LIST_FIELDS = {
    "contains",
    "governs",
    "owns",
    "does_not_own",
    "related_concepts",
    "source_refs",
}
STRING_FIELDS = {
    "doc_id",
    "doc_type",
    "title",
    "version",
    "status",
    "output_path",
    "owner",
    "updated_at",
    "section_id",
    "heading",
    "kind",
    "term",
    "definition",
    "full_name",
    "scope",
    "authority",
    "purpose",
    "relationship",
    "notes",
}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str
    severity: str = "error"

    def as_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "path": self.path,
            "message": self.message,
            "severity": self.severity,
        }


@dataclass(frozen=True)
class SourceRefStatus:
    term: str
    source_ref: str
    path_exists: bool
    repo_boundary: bool
    authority_suitability: str

    def as_dict(self) -> dict[str, object]:
        return {
            "term": self.term,
            "source_ref": self.source_ref,
            "path_exists": self.path_exists,
            "repo_boundary": self.repo_boundary,
            "authority_suitability": self.authority_suitability,
        }


@dataclass(frozen=True)
class RelatedConceptRef:
    term: str
    related_concept: str
    path: str
    selected: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "term": self.term,
            "related_concept": self.related_concept,
            "path": self.path,
            "selected": self.selected,
        }


@dataclass(frozen=True)
class RenderParity:
    checked: bool
    matched: bool
    idempotent: bool
    rendered_path: str | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "checked": self.checked,
            "matched": self.matched,
            "idempotent": self.idempotent,
            "rendered_path": self.rendered_path,
        }


@dataclass(frozen=True)
class ValidationReport:
    accepted: bool
    issues: tuple[ValidationIssue, ...]
    profiles: dict[str, int]
    unresolved_related_concepts: tuple[RelatedConceptRef, ...]
    selected_unresolved_related_concepts: tuple[RelatedConceptRef, ...]
    source_refs: tuple[SourceRefStatus, ...]
    render_parity: RenderParity

    def as_dict(self) -> dict[str, Any]:
        return {
            "accepted": self.accepted,
            "issues": [issue.as_dict() for issue in self.issues],
            "profiles": dict(self.profiles),
            "unresolved_related_concepts": [
                ref.as_dict() for ref in self.unresolved_related_concepts
            ],
            "selected_unresolved_related_concepts": [
                ref.as_dict() for ref in self.selected_unresolved_related_concepts
            ],
            "source_refs": [status.as_dict() for status in self.source_refs],
            "render_parity": self.render_parity.as_dict(),
        }


def load_glossary(path: Path = GLOSSARY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_glossary(
    doc: dict[str, Any],
    *,
    repo_root: Path = REPO_ROOT,
    selected_terms: set[str] | None = None,
    enforce_selected: bool = False,
    check_render_parity: bool = False,
    rendered_markdown_path: Path | None = None,
) -> ValidationReport:
    selected_terms = selected_terms or set()
    issues: list[ValidationIssue] = []
    source_refs: list[SourceRefStatus] = []
    unresolved_refs: list[RelatedConceptRef] = []
    profiles = {
        "legacy_definition_only": 0,
        "v2_1_structured": 0,
    }

    _check_required_keys(doc, ROOT_KEYS, "$", "root", issues)
    _check_unknown_keys(doc, ROOT_KEYS, "$", "unknown_root_key", issues)
    if doc.get("doc_type") != "glossary":
        _issue(issues, "invalid_doc_type", "$.doc_type", "doc_type must be glossary")

    metadata = doc.get("metadata")
    if isinstance(metadata, dict):
        _check_required_keys(metadata, {"owner", "updated_at", "source_scope"}, "$.metadata", "metadata", issues)
        _check_unknown_keys(metadata, METADATA_KEYS, "$.metadata", "unknown_metadata_key", issues)
        for field in ("source_scope", "depends_on_docs", "tags"):
            if field in metadata:
                _expect_string_list(metadata[field], f"$.metadata.{field}", issues)
    else:
        _issue(issues, "wrong_type", "$.metadata", "metadata must be an object")

    sections = doc.get("sections")
    if not isinstance(sections, list) or not sections:
        _issue(issues, "wrong_type", "$.sections", "sections must be a non-empty list")
        sections = []

    section_ids: set[str] = set()
    terms: set[str] = set()
    entries: list[tuple[dict[str, Any], str]] = []
    for section_index, section in enumerate(sections):
        section_path = f"$.sections[{section_index}]"
        if not isinstance(section, dict):
            _issue(issues, "wrong_type", section_path, "section must be an object")
            continue
        _check_required_keys(section, SECTION_KEYS, section_path, "section", issues)
        _check_unknown_keys(section, SECTION_KEYS, section_path, "unknown_section_key", issues)
        section_id = section.get("section_id")
        if isinstance(section_id, str):
            if section_id in section_ids:
                _issue(issues, "duplicate_section_id", f"{section_path}.section_id", f"duplicate section_id {section_id!r}")
            section_ids.add(section_id)
        content = section.get("content")
        if not isinstance(content, dict):
            _issue(issues, "wrong_type", f"{section_path}.content", "section content must be an object")
            continue
        _check_unknown_keys(content, CONTENT_KEYS, f"{section_path}.content", "unknown_section_content_key", issues)
        section_entries = content.get("entries")
        if not isinstance(section_entries, list) or not section_entries:
            _issue(issues, "missing_entries", f"{section_path}.content.entries", "content.entries must be a non-empty list")
            continue
        for entry_index, entry in enumerate(section_entries):
            entry_path = f"{section_path}.content.entries[{entry_index}]"
            if not isinstance(entry, dict):
                _issue(issues, "wrong_type", entry_path, "entry must be an object")
                continue
            term = entry.get("term")
            if isinstance(term, str):
                if term in terms:
                    _issue(issues, "duplicate_term", f"{entry_path}.term", f"duplicate term {term!r}")
                terms.add(term)
            entries.append((entry, entry_path))

    for entry, entry_path in entries:
        profile = _entry_profile(entry)
        profiles[profile] += 1
        _validate_entry_shape(
            entry,
            entry_path,
            issues,
            profile=profile,
            selected_terms=selected_terms,
            enforce_selected=enforce_selected,
        )

    for entry, entry_path in entries:
        term = str(entry.get("term", ""))
        selected = term in selected_terms
        for related in _string_values(entry.get("related_concepts")):
            if related not in terms:
                ref = RelatedConceptRef(
                    term=term,
                    related_concept=related,
                    path=f"{entry_path}.related_concepts",
                    selected=selected,
                )
                unresolved_refs.append(ref)
                if enforce_selected and selected:
                    _issue(
                        issues,
                        "unresolved_selected_related_concept",
                        ref.path,
                        f"{term!r} references non-canonical related concept {related!r}",
                    )
        for source_ref in _string_values(entry.get("source_refs")):
            status = _source_ref_status(term, source_ref, repo_root)
            source_refs.append(status)
            if not status.repo_boundary:
                _issue(
                    issues,
                    "source_ref_outside_repo",
                    f"{entry_path}.source_refs",
                    f"source_ref {source_ref!r} escapes repo boundary",
                )
            elif not status.path_exists:
                _issue(
                    issues,
                    "source_ref_missing_path",
                    f"{entry_path}.source_refs",
                    f"source_ref {source_ref!r} does not exist",
                )

    render_parity = _render_parity(doc, rendered_markdown_path) if check_render_parity else RenderParity(False, False, False)
    if check_render_parity and not render_parity.matched:
        _issue(issues, "render_drift", "$", "rendered Markdown differs from expected Glossary.md")
    if check_render_parity and not render_parity.idempotent:
        _issue(issues, "render_not_idempotent", "$", "render_doc is not idempotent for this glossary payload")

    selected_unresolved = tuple(ref for ref in unresolved_refs if ref.selected)
    return ValidationReport(
        accepted=not issues,
        issues=tuple(issues),
        profiles=profiles,
        unresolved_related_concepts=tuple(unresolved_refs),
        selected_unresolved_related_concepts=selected_unresolved,
        source_refs=tuple(source_refs),
        render_parity=render_parity,
    )


def _entry_profile(entry: dict[str, Any]) -> str:
    keys = set(entry)
    if keys <= LEGACY_ENTRY_KEYS:
        return "legacy_definition_only"
    return "v2_1_structured"


def _validate_entry_shape(
    entry: dict[str, Any],
    entry_path: str,
    issues: list[ValidationIssue],
    *,
    profile: str,
    selected_terms: set[str],
    enforce_selected: bool,
) -> None:
    allowed = LEGACY_ENTRY_KEYS if profile == "legacy_definition_only" else STRUCTURED_ENTRY_KEYS
    _check_required_keys(entry, {"term", "definition"}, entry_path, "entry", issues)
    _check_unknown_keys(entry, allowed, entry_path, "unknown_entry_key", issues)

    term = entry.get("term")
    selected = isinstance(term, str) and term in selected_terms
    if enforce_selected and selected and profile != "v2_1_structured":
        _issue(issues, "selected_term_not_structured", entry_path, f"selected term {term!r} must use v2_1_structured profile")

    if profile == "v2_1_structured":
        _check_required_keys(entry, STRUCTURED_REQUIRED_FIELDS, entry_path, "structured entry", issues)
        for field in STRING_LIST_FIELDS:
            if field in entry:
                require_non_empty = enforce_selected and selected and field in {"related_concepts", "source_refs"}
                _expect_string_list(entry[field], f"{entry_path}.{field}", issues, require_non_empty=require_non_empty)
        boundary = entry.get("boundary")
        if not isinstance(boundary, dict):
            _issue(issues, "wrong_type", f"{entry_path}.boundary", "boundary must be an object")
        else:
            _check_required_keys(boundary, BOUNDARY_REQUIRED_FIELDS, f"{entry_path}.boundary", "boundary", issues)
            _check_unknown_keys(boundary, BOUNDARY_KEYS, f"{entry_path}.boundary", "unknown_boundary_key", issues)
            _expect_string_list(boundary.get("not"), f"{entry_path}.boundary.not", issues, require_non_empty=True)
            _expect_string(boundary.get("claim_ceiling"), f"{entry_path}.boundary.claim_ceiling", issues, require_non_empty=True)
            _expect_string_list(
                boundary.get("forbidden_overreads"),
                f"{entry_path}.boundary.forbidden_overreads",
                issues,
                require_non_empty=True,
            )

    for field, value in entry.items():
        if field in STRING_FIELDS:
            _expect_string(value, f"{entry_path}.{field}", issues, require_non_empty=field in {"term", "definition"})


def _source_ref_status(term: str, source_ref: str, repo_root: Path) -> SourceRefStatus:
    repo_root = repo_root.resolve()
    candidate = (repo_root / source_ref).resolve(strict=False)
    repo_boundary = _is_relative_to(candidate, repo_root)
    path_exists = repo_boundary and candidate.exists()
    authority_suitability = _authority_suitability(source_ref, repo_boundary)
    return SourceRefStatus(
        term=term,
        source_ref=source_ref,
        path_exists=path_exists,
        repo_boundary=repo_boundary,
        authority_suitability=authority_suitability,
    )


def _authority_suitability(source_ref: str, repo_boundary: bool) -> str:
    if not repo_boundary:
        return "rejected"
    if source_ref.startswith("kb/data/") or source_ref.startswith("kb/docs/"):
        return "canonical_kb"
    if source_ref.startswith("Dashboard/"):
        return "dashboard_provenance"
    if (
        source_ref.startswith("tests/")
        or source_ref.startswith("semx/schemas/")
        or source_ref.startswith("semx/runners/")
        or source_ref.startswith("examples/artifacts/")
        or source_ref.startswith(".codex/skills/")
    ):
        return "test_or_runtime_contract"
    return "review_required"


def _render_parity(doc: dict[str, Any], rendered_markdown_path: Path | None) -> RenderParity:
    render_kb = _load_render_kb_module()
    rendered_once = render_kb.render_doc(doc)
    rendered_twice = render_kb.render_doc(copy.deepcopy(doc))
    idempotent = rendered_once == rendered_twice
    expected_path = rendered_markdown_path or RENDERED_GLOSSARY_PATH
    if expected_path.exists():
        expected = expected_path.read_text(encoding="utf-8")
        matched = rendered_once == expected
    else:
        matched = False
    return RenderParity(
        checked=True,
        matched=matched,
        idempotent=idempotent,
        rendered_path=str(expected_path),
    )


def _load_render_kb_module() -> Any:
        path = REPO_ROOT / "tools/render_kb.py"
    spec = importlib.util.spec_from_file_location("semx_kb_render_kb", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load render_kb.py from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _check_required_keys(
    value: dict[str, Any],
    required: set[str],
    path: str,
    label: str,
    issues: list[ValidationIssue],
) -> None:
    missing = sorted(required - set(value))
    for key in missing:
        _issue(issues, "missing_field", f"{path}.{key}", f"{label} missing required field {key!r}")


def _check_unknown_keys(
    value: dict[str, Any],
    allowed: set[str],
    path: str,
    code: str,
    issues: list[ValidationIssue],
) -> None:
    unknown = sorted(set(value) - allowed)
    for key in unknown:
        _issue(issues, code, f"{path}.{key}", f"unknown field {key!r}")


def _expect_string(value: Any, path: str, issues: list[ValidationIssue], *, require_non_empty: bool = False) -> None:
    if not isinstance(value, str):
        _issue(issues, "wrong_type", path, "value must be a string")
        return
    if require_non_empty and not value.strip():
        _issue(issues, "empty_value", path, "string value must be non-empty")


def _expect_string_list(
    value: Any,
    path: str,
    issues: list[ValidationIssue],
    *,
    require_non_empty: bool = False,
) -> None:
    if not isinstance(value, list):
        _issue(issues, "wrong_type", path, "value must be a list of strings")
        return
    if require_non_empty and not value:
        _issue(issues, "empty_value", path, "list value must be non-empty")
    for index, item in enumerate(value):
        if not isinstance(item, str):
            _issue(issues, "wrong_type", f"{path}[{index}]", "list item must be a string")
        elif require_non_empty and not item.strip():
            _issue(issues, "empty_value", f"{path}[{index}]", "list item must be non-empty")


def _string_values(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _issue(issues: list[ValidationIssue], code: str, path: str, message: str) -> None:
    issues.append(ValidationIssue(code=code, path=path, message=message))


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Glossary V2.1 integrity boundaries.")
    parser.add_argument("path", nargs="?", type=Path, default=GLOSSARY_PATH)
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    parser.add_argument("--selected-term", action="append", default=[])
    parser.add_argument("--enforce-selected", action="store_true")
    parser.add_argument("--render-parity", action="store_true")
    parser.add_argument("--rendered-markdown", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = validate_glossary(
        load_glossary(args.path),
        repo_root=args.repo,
        selected_terms=set(args.selected_term),
        enforce_selected=args.enforce_selected,
        check_render_parity=args.render_parity,
        rendered_markdown_path=args.rendered_markdown,
    )
    if args.json:
        print(json.dumps(report.as_dict(), indent=2, ensure_ascii=False))
    else:
        print(f"accepted={str(report.accepted).lower()}")
        print(f"issues={len(report.issues)}")
        print(f"profiles={report.profiles}")
        print(f"unresolved_related_concepts={len(report.unresolved_related_concepts)}")
        print(f"selected_unresolved_related_concepts={len(report.selected_unresolved_related_concepts)}")
    return 0 if report.accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
