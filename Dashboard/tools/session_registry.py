#!/usr/bin/env python3
"""Maintain the Dashboard current/index/archive Session registry.

Dashboard Markdown remains execution-memory authority. This tool only validates
and mechanically projects that memory into a compact current surface, a full
locator index, and lossless historical archives.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SESSION_ID_RE = re.compile(r"^S-(\d{3})(?:-([A-Z0-9]+))?$")
SP_RE = re.compile(r"\bSP-\d{3}\b")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
STANDARD_STATUSES = {"To do", "Doing", "Done", "Cancelled"}
LEGACY_HEADERS = [
    "ID",
    "Topic",
    "Scope",
    "Purpose",
    "Track",
    "Priority",
    "Historical Status Snapshot",
    "Depends On",
    "Deliverable",
    "Exit Criteria",
    "Next Step",
    "Notes",
]
REGISTRY_HEADERS = [
    "Session Key",
    "Historical ID",
    "Parent",
    "Topic",
    "Scope",
    "Purpose",
    "Track",
    "Priority",
    "Status",
    "Historical Status Snapshot",
    "Depends On",
    "Deliverable",
    "Exit Criteria",
    "Next Step",
    "Notes",
]
INDEX_HEADERS = [
    "Session Key",
    "Historical ID",
    "Parent",
    "Status",
    "Location",
    "Primary Evidence",
    "Topic",
]
SESSION_SOURCE_REF_RE = re.compile(
    r"Dashboard/Sessions\.md "
    r"(S-\d{3}(?:\s+to\s+S-\d{3}|(?:/S-\d{3})*)?)"
)
PARENT_RE = re.compile(r"^(?:SP-\d{3}|LEGACY)$")
ARCHIVE_NAME_RE = re.compile(r"^(?:SP-\d{3}|Legacy_S001-S279|Legacy_Unassigned)\.md$")
FROZEN_MIGRATION_PROVENANCE: dict[str, int | str] = {
    "source_path": "Dashboard/Sessions.md",
    "source_sha256": "current-worktree",
    "source_line_count": 0,
    "source_record_count": 0,
    "source_narrative_line_count": 0,
    "source_narrative_sha256": "not_applicable",
}


class RegistryError(ValueError):
    """A fail-closed registry input or projection error with a stable code."""

    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


@dataclass(frozen=True)
class SessionRecord:
    session_key: str
    historical_id: str
    parent: str
    topic: str
    scope: str
    purpose: str
    track: str
    priority: str
    status: str
    historical_status: str
    depends_on: str
    deliverable: str
    exit_criteria: str
    next_step: str
    notes: str
    source_line: int

    @property
    def anchor(self) -> str:
        return anchor_for(self.session_key)

    @property
    def numeric_id(self) -> int:
        match = SESSION_ID_RE.fullmatch(self.historical_id)
        if not match:
            raise ValueError(f"invalid Historical ID: {self.historical_id}")
        return int(match.group(1))

    @property
    def suffix(self) -> str:
        match = SESSION_ID_RE.fullmatch(self.historical_id)
        if not match:
            raise ValueError(f"invalid Historical ID: {self.historical_id}")
        return match.group(2) or ""

    def registry_cells(self) -> list[str]:
        return [
            self.session_key,
            self.historical_id,
            self.parent,
            self.topic,
            self.scope,
            self.purpose,
            self.track,
            self.priority,
            self.status,
            self.historical_status,
            self.depends_on,
            self.deliverable,
            self.exit_criteria,
            self.next_step,
            self.notes,
        ]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def anchor_for(session_key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", session_key.lower()).strip("-")


def split_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        raise ValueError("not a Markdown table row")
    body = stripped[1:-1]
    cells: list[str] = []
    current: list[str] = []
    index = 0
    while index < len(body):
        char = body[index]
        if char == "\\" and index + 1 < len(body) and body[index + 1] == "|":
            current.append("|")
            index += 2
            continue
        if char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        index += 1
    cells.append("".join(current).strip())
    return cells


def escape_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def render_row(cells: Iterable[str]) -> str:
    return "| " + " | ".join(escape_cell(cell) for cell in cells) + " |"


def strip_code(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def normalize_status(snapshot: str) -> str:
    value = strip_code(snapshot)
    if value == "Cancelled":
        return "Cancelled"
    if (
        value.startswith("Done")
        or value.startswith("done")
        or value == "bounded evaluator slice passed"
        or value.startswith("Provider observation materialized")
    ):
        return "Done"
    if value.startswith("Doing"):
        return "Doing"
    if (
        value == "To do"
        or value.startswith("Partial")
        or value.startswith("PARTIAL")
        or value.startswith("Blocked")
    ):
        return "To do"
    raise ValueError(f"unmapped historical status snapshot: {snapshot!r}")


def infer_parent(values: dict[str, str]) -> str:
    for field in (
        "Topic",
        "Scope",
        "Purpose",
        "Depends On",
        "Deliverable",
        "Exit Criteria",
        "Next Step",
        "Notes",
    ):
        match = SP_RE.search(values.get(field, ""))
        if match:
            return match.group(0)
    return "LEGACY"


def canonical_key(parent: str, historical_id: str) -> str:
    if not SESSION_ID_RE.fullmatch(historical_id):
        raise ValueError(f"unsupported session identity: {historical_id}")
    return f"{parent}/{historical_id}"


def repair_legacy_cells(cells: list[str], line_no: int) -> list[str]:
    historical_id = strip_code(cells[0]) if cells else ""
    if historical_id == "S-224" and len(cells) == 13:
        return cells[:8] + [f"{cells[8]}; {cells[9]}"] + cells[10:]
    if historical_id == "S-377" and len(cells) == 11:
        return cells + [""]
    if len(cells) != len(LEGACY_HEADERS):
        raise ValueError(
            f"Dashboard/Sessions.md:{line_no}: expected {len(LEGACY_HEADERS)} cells, "
            f"got {len(cells)} for {historical_id or 'unknown row'}"
        )
    return cells


def parse_legacy_sessions(path: Path) -> tuple[list[SessionRecord], str, dict[str, int | str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    records: list[SessionRecord] = []
    narrative_lines: list[str] = []
    header_seen = False
    for line_no, line in enumerate(lines, start=1):
        if not line.startswith("|"):
            narrative_lines.append(line)
            continue
        cells = split_markdown_row(line)
        first = strip_code(cells[0]) if cells else ""
        if first == "ID":
            header_seen = True
            continue
        if first.startswith("---"):
            continue
        if not SESSION_ID_RE.fullmatch(first):
            narrative_lines.append(line)
            continue
        if not header_seen:
            raise ValueError(f"{path}:{line_no}: Session row appears before header")
        cells = repair_legacy_cells(cells, line_no)
        values = {
            header: strip_code(cell)
            for header, cell in zip(LEGACY_HEADERS, cells)
        }
        parent = infer_parent(values)
        records.append(
            SessionRecord(
                session_key=canonical_key(parent, values["ID"]),
                historical_id=values["ID"],
                parent=parent,
                topic=values["Topic"],
                scope=values["Scope"],
                purpose=values["Purpose"],
                track=values["Track"],
                priority=values["Priority"],
                status=normalize_status(values["Historical Status Snapshot"]),
                historical_status=values["Historical Status Snapshot"],
                depends_on=values["Depends On"],
                deliverable=values["Deliverable"],
                exit_criteria=values["Exit Criteria"],
                next_step=values["Next Step"],
                notes=values["Notes"],
                source_line=line_no,
            )
        )
    narrative = "\n".join(narrative_lines).rstrip() + "\n"
    metadata: dict[str, int | str] = {
        "source_path": str(path),
        "source_sha256": sha256_text(text),
        "source_line_count": len(lines),
        "source_record_count": len(records),
        "source_narrative_line_count": len(narrative_lines),
        "source_narrative_sha256": sha256_text(narrative),
    }
    ensure_unique(records)
    return records, narrative, metadata


def ensure_unique(records: Iterable[SessionRecord]) -> None:
    seen: dict[str, SessionRecord] = {}
    for record in records:
        existing = seen.get(record.session_key)
        if existing is not None:
            raise ValueError(
                f"duplicate canonical Session Key {record.session_key}: "
                f"lines {existing.source_line} and {record.source_line}"
            )
        seen[record.session_key] = record


def keep_current(record: SessionRecord) -> bool:
    return record.status in {"To do", "Doing"} or record.numeric_id >= 450


def archive_filename(record: SessionRecord) -> str:
    if record.parent != "LEGACY":
        return f"{record.parent}.md"
    if record.numeric_id <= 279:
        return "Legacy_S001-S279.md"
    return "Legacy_Unassigned.md"


def sort_key(record: SessionRecord) -> tuple[int, str, str]:
    return (record.numeric_id, record.suffix, record.parent)


def rewrite_archive_links(value: str) -> str:
    value = value.replace("(Artifacts/", "(../../Artifacts/")
    value = value.replace("(../examples/", "(../../../examples/")
    return value


def render_registry_table(records: list[SessionRecord], archive: bool = False) -> str:
    lines = [
        render_row(REGISTRY_HEADERS),
        render_row(["---"] * len(REGISTRY_HEADERS)),
    ]
    for record in sorted(records, key=sort_key):
        cells = record.registry_cells()
        if archive:
            cells = [
                rewrite_archive_links(cell) if index >= 10 else cell
                for index, cell in enumerate(cells)
            ]
        cells[0] = f'<a id="{record.anchor}"></a>`{record.session_key}`'
        cells[1] = f"`{record.historical_id}`"
        cells[8] = f"`{record.status}`"
        cells[9] = f"`{record.historical_status}`"
        lines.append(render_row(cells))
    return "\n".join(lines)


def existing_primary_evidence(record: SessionRecord, repo: Path) -> str:
    for label, target in LINK_RE.findall(record.deliverable):
        if target.startswith(("http://", "https://", "#")):
            continue
        candidate = (repo / "Dashboard" / target).resolve()
        try:
            candidate.relative_to(repo.resolve())
        except ValueError:
            continue
        if candidate.exists():
            return f"[{label}]({target})"
    return "—"


def render_current(records: list[SessionRecord]) -> str:
    return "\n".join(
        [
            "# Sessions",
            "",
            "本文件只保留当前与近期 Session。全量定位请使用 [Session Index](Session_Index.md)，完整历史请使用 [Session Archives](Archives/Sessions/)。",
            "",
            "Session 的 canonical identity 是 `Parent/Historical ID`。历史 ID 可能重复；例如 `SP-063/S-478` 与 `SP-064/S-478` 是两条不同记录，禁止按裸 `S-478` first-wins。",
            "",
            "迁移前的表外执行说明完整保存在 [Legacy Execution Notes](Archives/Sessions/Legacy_Execution_Notes.md)。",
            "",
            render_registry_table(records),
            "",
        ]
    )


def render_index(records: list[SessionRecord], current_keys: set[str], repo: Path) -> str:
    lines = [
        "# Session Index",
        "",
        "这是 Dashboard Session 的全量定位入口，不是 canonical KB truth。`Session Key` 唯一；`Historical ID` 仅为兼容检索别名。",
        "",
        render_row(INDEX_HEADERS),
        render_row(["---"] * len(INDEX_HEADERS)),
    ]
    for record in sorted(records, key=sort_key):
        if record.session_key in current_keys:
            target = f"Sessions.md#{record.anchor}"
            label = "current"
        else:
            filename = archive_filename(record)
            target = f"Archives/Sessions/{filename}#{record.anchor}"
            label = "archive"
        cells = [
            f'<a id="{record.anchor}"></a>`{record.session_key}`',
            f"`{record.historical_id}`",
            record.parent,
            f"`{record.status}`",
            f"[{label}]({target})",
            existing_primary_evidence(record, repo),
            record.topic,
        ]
        lines.append(render_row(cells))
    lines.append("")
    return "\n".join(lines)


def render_archive(records: list[SessionRecord], filename: str) -> str:
    return "\n".join(
        [
            f"# Session Archive: {filename.removesuffix('.md')}",
            "",
            "本文件保存已关闭历史 Session 的完整 Dashboard 行。当前入口见 [Sessions](../../Sessions.md)，全量定位见 [Session Index](../../Session_Index.md)。",
            "",
            render_registry_table(records, archive=True),
            "",
        ]
    )


def render_legacy_notes(narrative: str, metadata: dict[str, int | str]) -> str:
    return "\n".join(
        [
            "# 历史 Session 表外执行说明",
            "",
            "以下内容从重构前 `Dashboard/Sessions.md` 原样迁移。它是历史执行记忆，不是当前状态或 canonical truth；当前入口见 [Sessions](../../Sessions.md)。",
            "",
            f"- Source SHA-256：`{metadata['source_sha256']}`",
            f"- Source narrative SHA-256：`{metadata['source_narrative_sha256']}`",
            f"- Source narrative lines：`{metadata['source_narrative_line_count']}`",
            "",
            "## 原始表外内容",
            "",
            narrative.rstrip(),
            "",
        ]
    )


def migrate(repo: Path) -> dict[str, object]:
    dashboard = repo / "Dashboard"
    source = dashboard / "Sessions.md"
    records, narrative, source_metadata = parse_legacy_sessions(source)
    if len(records) != 487:
        raise ValueError(f"expected frozen migration baseline of 487 records, got {len(records)}")

    current = [record for record in records if keep_current(record)]
    archived = [record for record in records if not keep_current(record)]
    current_keys = {record.session_key for record in current}
    archive_groups: dict[str, list[SessionRecord]] = {}
    for record in archived:
        archive_groups.setdefault(archive_filename(record), []).append(record)

    archive_root = dashboard / "Archives" / "Sessions"
    archive_root.mkdir(parents=True, exist_ok=True)
    expected_archive_files = set(archive_groups) | {
        "Legacy_Execution_Notes.md",
        "archive_manifest.json",
    }
    for old in archive_root.iterdir():
        if old.is_file() and old.name not in expected_archive_files:
            raise ValueError(f"unexpected existing archive file would be orphaned: {old}")

    source.write_text(render_current(current), encoding="utf-8")
    (dashboard / "Session_Index.md").write_text(
        render_index(records, current_keys, repo), encoding="utf-8"
    )
    for filename, group in sorted(archive_groups.items()):
        (archive_root / filename).write_text(
            render_archive(group, filename), encoding="utf-8"
        )
    (archive_root / "Legacy_Execution_Notes.md").write_text(
        render_legacy_notes(narrative, source_metadata), encoding="utf-8"
    )

    collisions: dict[str, list[str]] = {}
    for record in records:
        collisions.setdefault(record.historical_id, []).append(record.session_key)
    collisions = {
        historical_id: keys
        for historical_id, keys in collisions.items()
        if len(keys) > 1
    }
    manifest: dict[str, object] = {
        "schema_version": "dashboard_session_archive_manifest_v1",
        "created_by_session": "sge-governance-skill-maintenance",
        "source": source_metadata,
        "record_count": len(records),
        "current_count": len(current),
        "archive_count": len(archived),
        "index_count": len(records),
        "canonical_key_count": len({record.session_key for record in records}),
        "historical_id_collision_count": len(collisions),
        "historical_id_collisions": collisions,
        "current_retention": {
            "statuses": ["To do", "Doing"],
            "recent_numeric_floor": 450,
        },
        "archive_files": {
            filename: len(group) for filename, group in sorted(archive_groups.items())
        },
        "legacy_repairs": {
            "S-224": "joined the accidental extra Deliverable cell",
            "S-377": "added the missing empty Notes cell",
        },
        "claim_ceiling": "DASHBOARD_SESSION_EXECUTION_MEMORY_REFACTORED_ONLY",
    }
    (archive_root / "archive_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def parse_registry_file(path: Path) -> list[SessionRecord]:
    if not path.is_file() or path.is_symlink():
        raise RegistryError("malformed_registry", f"registry file is not a regular file: {path}")
    records: list[SessionRecord] = []
    header: list[str] | None = None
    header_count = 0
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = split_markdown_row(line)
        plain = [strip_code(re.sub(r'<a id="[^"]+"></a>', "", cell)) for cell in cells]
        if plain and plain[0] == "Session Key":
            if plain != REGISTRY_HEADERS:
                raise RegistryError("malformed_registry", f"{path}:{line_no}: invalid registry header")
            if header is not None:
                raise RegistryError("malformed_registry", f"{path}:{line_no}: duplicate registry header")
            header = plain
            header_count += 1
            continue
        if plain and plain[0].startswith("---"):
            continue
        if not header:
            continue
        if len(plain) != len(REGISTRY_HEADERS):
            raise RegistryError("malformed_registry", f"{path}:{line_no}: malformed registry row")
        values = dict(zip(header, plain))
        record = SessionRecord(
            session_key=values["Session Key"],
            historical_id=values["Historical ID"],
            parent=values["Parent"],
            topic=values["Topic"],
            scope=values["Scope"],
            purpose=values["Purpose"],
            track=values["Track"],
            priority=values["Priority"],
            status=values["Status"],
            historical_status=values["Historical Status Snapshot"],
            depends_on=values["Depends On"],
            deliverable=values["Deliverable"],
            exit_criteria=values["Exit Criteria"],
            next_step=values["Next Step"],
            notes=values["Notes"],
            source_line=line_no,
        )
        if not PARENT_RE.fullmatch(record.parent):
            raise RegistryError("malformed_registry", f"{path}:{line_no}: invalid Parent")
        if not SESSION_ID_RE.fullmatch(record.historical_id):
            raise RegistryError("malformed_registry", f"{path}:{line_no}: invalid Historical ID")
        if record.session_key != canonical_key(record.parent, record.historical_id):
            raise RegistryError("malformed_registry", f"{path}:{line_no}: canonical key mismatch")
        if record.status not in STANDARD_STATUSES:
            raise RegistryError("unknown_status", f"{path}:{line_no}: non-standard Status")
        records.append(record)
    if header_count != 1:
        raise RegistryError("malformed_registry", f"{path}: expected exactly one registry header")
    if not records:
        raise RegistryError("malformed_registry", f"{path}: registry table is empty")
    try:
        ensure_unique(records)
    except ValueError as exc:
        raise RegistryError("duplicate_canonical_key", str(exc)) from exc
    return records


def parse_index(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = split_markdown_row(line)
        plain = [strip_code(re.sub(r'<a id="[^"]+"></a>', "", cell)) for cell in cells]
        if plain and plain[0] == "Session Key":
            header = plain
            continue
        if plain and plain[0].startswith("---"):
            continue
        if not header:
            continue
        if len(plain) != len(INDEX_HEADERS):
            raise ValueError(f"{path}:{line_no}: malformed index row")
        rows.append(dict(zip(header, plain)))
    return rows


def _regular_file(path: Path, error_code: str, message: str) -> None:
    if not path.is_file() or path.is_symlink():
        raise RegistryError(error_code, message)


def _archive_inventory(archive_root: Path) -> tuple[list[Path], Path]:
    if not archive_root.is_dir() or archive_root.is_symlink():
        raise RegistryError("unexpected_archive_surface", "archive root is not a regular directory")
    archive_paths: list[Path] = []
    notes_path = archive_root / "Legacy_Execution_Notes.md"
    manifest_path = archive_root / "archive_manifest.json"
    for path in sorted(archive_root.iterdir(), key=lambda item: item.name):
        if path.is_symlink() or not path.is_file():
            raise RegistryError("unexpected_archive_surface", f"unexpected archive surface: {path.name}")
        if path.name in {notes_path.name, manifest_path.name}:
            continue
        if not ARCHIVE_NAME_RE.fullmatch(path.name):
            raise RegistryError("unexpected_archive_surface", f"unexpected archive file: {path.name}")
        archive_paths.append(path)
    _regular_file(notes_path, "legacy_notes_surface_invalid", "Legacy_Execution_Notes.md is missing or invalid")
    return archive_paths, notes_path


def _collect_authoritative_records(
    repo: Path,
) -> tuple[list[SessionRecord], list[SessionRecord], list[Path], Path]:
    dashboard = repo / "Dashboard"
    current = parse_registry_file(dashboard / "Sessions.md")
    archive_root = dashboard / "Archives" / "Sessions"
    archive_paths, notes_path = _archive_inventory(archive_root)
    archives: list[SessionRecord] = []
    for path in archive_paths:
        rows = parse_registry_file(path)
        for record in rows:
            if archive_filename(record) != path.name:
                raise RegistryError(
                    "unexpected_archive_surface",
                    f"archive filename does not match record identity: {path.name}",
                )
        archives.extend(rows)
    records = current + archives
    try:
        ensure_unique(records)
    except ValueError as exc:
        raise RegistryError("duplicate_canonical_key", str(exc)) from exc
    return records, current, archive_paths, notes_path


def _manifest(records: list[SessionRecord], current: list[SessionRecord]) -> dict[str, object]:
    archive_groups: dict[str, list[SessionRecord]] = {}
    for record in records:
        if not keep_current(record):
            archive_groups.setdefault(archive_filename(record), []).append(record)
    collisions: dict[str, list[str]] = {}
    for record in records:
        collisions.setdefault(record.historical_id, []).append(record.session_key)
    return {
        "schema_version": "dashboard_session_archive_manifest_v1",
        "created_by_session": "sge-governance-skill-maintenance",
        "source": FROZEN_MIGRATION_PROVENANCE,
        "record_count": len(records),
        "current_count": len(current),
        "archive_count": len(records) - len(current),
        "index_count": len(records),
        "canonical_key_count": len({record.session_key for record in records}),
        "historical_id_collision_count": sum(1 for keys in collisions.values() if len(keys) > 1),
        "historical_id_collisions": {
            historical_id: keys
            for historical_id, keys in collisions.items()
            if len(keys) > 1
        },
        "current_retention": {
            "statuses": ["To do", "Doing"],
            "recent_numeric_floor": 450,
        },
        "archive_files": {
            filename: len(group) for filename, group in sorted(archive_groups.items())
        },
        "legacy_repairs": {
            "S-224": "joined the accidental extra Deliverable cell",
            "S-377": "added the missing empty Notes cell",
        },
        "claim_ceiling": "DASHBOARD_SESSION_EXECUTION_MEMORY_REFACTORED_ONLY",
    }


def build_expected_projection(repo: Path, records: list[SessionRecord]) -> dict[str, str]:
    current = [record for record in records if keep_current(record)]
    archive_groups: dict[str, list[SessionRecord]] = {}
    for record in records:
        if not keep_current(record):
            archive_groups.setdefault(archive_filename(record), []).append(record)
    expected = {
        "Dashboard/Sessions.md": render_current(current),
        "Dashboard/Session_Index.md": render_index(records, {record.session_key for record in current}, repo),
        "Dashboard/Archives/Sessions/archive_manifest.json": (
            json.dumps(_manifest(records, current), ensure_ascii=False, indent=2) + "\n"
        ),
    }
    for filename, group in archive_groups.items():
        expected[f"Dashboard/Archives/Sessions/{filename}"] = render_archive(group, filename)
    return expected


def _projection_diff(repo: Path, expected: dict[str, str], archive_paths: list[Path]) -> list[str]:
    actual_paths = {
        "Dashboard/Sessions.md",
        "Dashboard/Session_Index.md",
        "Dashboard/Archives/Sessions/archive_manifest.json",
        *(path.relative_to(repo).as_posix() for path in archive_paths),
    }
    drift: list[str] = []
    for relative in sorted(actual_paths | set(expected)):
        path = repo / relative
        expected_text = expected.get(relative)
        if expected_text is None or not path.is_file() or path.is_symlink():
            drift.append(relative)
        elif path.read_text(encoding="utf-8") != expected_text:
            drift.append(relative)
    return drift


def _assert_safe_projection_targets(
    repo: Path,
    expected: dict[str, str],
    archive_paths: list[Path],
) -> None:
    """Reject non-regular projection targets before either check or apply.

    A derived surface may be absent (that is repairable drift), but an existing
    symlink, device, directory, or path below a symlinked parent is not a safe
    registry target.  Checking this before computing a check verdict also keeps
    `--check` and `--apply` on the same fail-closed boundary.
    """
    repo_root = repo.resolve()
    targets = set(expected)
    targets.update(path.relative_to(repo).as_posix() for path in archive_paths)
    for relative in sorted(targets):
        path = repo / relative
        for parent in (path.parent, *path.parents):
            if parent == repo.parent:
                break
            try:
                parent_stat = parent.lstat()
            except FileNotFoundError:
                raise RegistryError(
                    "unsafe_projection_target",
                    f"projection parent is missing: {parent.relative_to(repo)}",
                ) from None
            if stat.S_ISLNK(parent_stat.st_mode) or not stat.S_ISDIR(parent_stat.st_mode):
                raise RegistryError(
                    "unsafe_projection_target",
                    f"projection parent is not a regular directory: {parent.relative_to(repo)}",
                )
            if parent == repo:
                break
        try:
            target_stat = path.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(target_stat.st_mode) or not stat.S_ISREG(target_stat.st_mode):
            raise RegistryError(
                "unsafe_projection_target",
                f"projection target is not a regular file: {relative}",
            )
        try:
            path.resolve().relative_to(repo_root)
        except ValueError as exc:
            raise RegistryError(
                "unsafe_projection_target",
                f"projection target escapes repository: {relative}",
            ) from exc


def _assert_no_authoritative_record_loss(repo: Path, records: list[SessionRecord]) -> None:
    """Use prior derived evidence only to stop loss; never to recreate a record."""
    dashboard = repo / "Dashboard"
    candidate_keys = {record.session_key for record in records}
    index_path = dashboard / "Session_Index.md"
    if index_path.exists():
        try:
            indexed_keys = {row["Session Key"] for row in parse_index(index_path)}
        except (ValueError, KeyError):
            indexed_keys = set()
        missing_keys = sorted(indexed_keys - candidate_keys)
        if missing_keys:
            raise RegistryError(
                "missing_authoritative_record_source",
                "authoritative record source is missing for locator key(s): "
                + ", ".join(missing_keys[:5]),
            )
    manifest_path = dashboard / "Archives" / "Sessions" / "archive_manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            recorded_count = manifest.get("record_count")
            if isinstance(recorded_count, int) and recorded_count > len(records):
                raise RegistryError(
                    "missing_authoritative_record_source",
                    "authoritative record source is missing: current record count is smaller "
                    f"than prior manifest ({len(records)} < {recorded_count})",
                )
        except json.JSONDecodeError:
            # A malformed derived manifest is repairable drift, not a record source.
            pass


def _registry_summary(records: list[SessionRecord]) -> dict[str, object]:
    current = [record for record in records if keep_current(record)]
    collisions: dict[str, list[str]] = {}
    for record in records:
        collisions.setdefault(record.historical_id, []).append(record.session_key)
    return {
        "record_count": len(records),
        "current_count": len(current),
        "archive_count": len(records) - len(current),
        "index_count": len(records),
        "historical_id_collisions": {
            historical_id: keys
            for historical_id, keys in collisions.items()
            if len(keys) > 1
        },
    }


def validate(repo: Path) -> dict[str, object]:
    records, _, archive_paths, _ = _collect_authoritative_records(repo)
    expected = build_expected_projection(repo, records)
    _assert_safe_projection_targets(repo, expected, archive_paths)
    _assert_no_authoritative_record_loss(repo, records)
    drift = _projection_diff(repo, expected, archive_paths)
    if drift:
        raise RegistryError("projection_drift", f"registry projection drift: {', '.join(drift)}")
    return {
        "schema_version": "dashboard_session_registry_validation_v1",
        "verdict": "pass",
        **_registry_summary(records),
    }


def reconcile(repo: Path, mode: str) -> dict[str, object]:
    if mode not in {"check", "apply"}:
        raise RegistryError("invalid_reconcile_mode", "reconcile requires exactly one of --check or --apply")
    records, _, archive_paths, _ = _collect_authoritative_records(repo)
    expected = build_expected_projection(repo, records)
    _assert_safe_projection_targets(repo, expected, archive_paths)
    _assert_no_authoritative_record_loss(repo, records)
    drift = _projection_diff(repo, expected, archive_paths)
    result: dict[str, object] = {
        "schema_version": "dashboard_session_registry_reconcile_v1",
        "drift_files": drift,
        "write_performed": False,
        **_registry_summary(records),
    }
    if mode == "check":
        result["verdict"] = "pass" if not drift else "drift"
        return result
    if not drift:
        result.update({"verdict": "pass", "changed_files": []})
        return result
    for relative in sorted(expected):
        path = repo / relative
        if not path.is_file() or path.is_symlink() or path.read_text(encoding="utf-8") != expected[relative]:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected[relative], encoding="utf-8")
    for path in archive_paths:
        relative = path.relative_to(repo).as_posix()
        if relative not in expected:
            path.unlink()
    validate(repo)
    result.update({"verdict": "pass", "changed_files": drift, "write_performed": True})
    return result


def reference_map(repo: Path) -> dict[str, list[str]]:
    dashboard = repo / "Dashboard"
    records = parse_registry_file(dashboard / "Sessions.md")
    archive_root = dashboard / "Archives" / "Sessions"
    for path in sorted(archive_root.glob("*.md")):
        if path.name != "Legacy_Execution_Notes.md":
            records.extend(parse_registry_file(path))
    mapping: dict[str, list[str]] = {}
    for record in records:
        mapping.setdefault(record.historical_id, []).append(record.session_key)
    return mapping


def rewrite_session_reference_text(
    text: str,
    mapping: dict[str, list[str]],
) -> tuple[str, list[str]]:
    ambiguous: list[str] = []

    def replace(match: re.Match[str]) -> str:
        expression = match.group(1)
        historical_ids = re.findall(r"S-\d{3}", expression)
        resolved: list[str] = []
        for historical_id in historical_ids:
            matches = mapping.get(historical_id, [])
            if len(matches) != 1:
                ambiguous.append(historical_id)
                return match.group(0)
            resolved.append(matches[0])
        if " to " in expression:
            rewritten = f"{resolved[0]} to {resolved[1]}"
        else:
            rewritten = ", ".join(resolved)
        return f"Dashboard/Session_Index.md {rewritten}"

    return SESSION_SOURCE_REF_RE.sub(replace, text), ambiguous


def migrate_references(repo: Path) -> dict[str, object]:
    mapping = reference_map(repo)
    candidate_paths = sorted((repo / "kb" / "data").rglob("*.json"))
    candidate_paths += [
        repo / "Dashboard" / filename
        for filename in (
            "Current_State.md",
            "Big_Ideas.md",
            "Stage_Plans.md",
            "Decisions.md",
            "Risks.md",
            "Quality_Metrics.md",
            "Artifacts_Index.md",
        )
    ]
    changed: list[str] = []
    ambiguous: dict[str, list[str]] = {}
    for path in candidate_paths:
        if not path.exists():
            continue
        before = path.read_text(encoding="utf-8")
        after, unresolved = rewrite_session_reference_text(before, mapping)
        if unresolved:
            ambiguous[path.relative_to(repo).as_posix()] = sorted(set(unresolved))
        if after != before:
            path.write_text(after, encoding="utf-8")
            changed.append(path.relative_to(repo).as_posix())
    return {
        "schema_version": "dashboard_session_reference_migration_v1",
        "changed_files": changed,
        "changed_file_count": len(changed),
        "ambiguous_references": ambiguous,
        "verdict": "pass" if not ambiguous else "pass_with_ambiguous_historical_refs_preserved",
    }


def _error_result(error: Exception) -> dict[str, object]:
    error_code = error.error_code if isinstance(error, RegistryError) else "malformed_registry"
    return {
        "schema_version": "dashboard_session_registry_reconcile_v1",
        "verdict": "error",
        "error_code": error_code,
        "message": str(error),
        "write_performed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("validate",):
        sub = subparsers.add_parser(command)
        sub.add_argument("--repo", default=".")
        sub.add_argument("--output")
    reconcile_parser = subparsers.add_parser("reconcile")
    reconcile_parser.add_argument("--repo", default=".")
    reconcile_mode = reconcile_parser.add_mutually_exclusive_group(required=True)
    reconcile_mode.add_argument("--check", action="store_true")
    reconcile_mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    exit_code = 0
    try:
        if args.command == "migrate":
            result = migrate(repo)
        elif args.command == "validate":
            result = validate(repo)
        elif args.command == "reconcile":
            result = reconcile(repo, "check" if args.check else "apply")
            if result["verdict"] == "drift":
                exit_code = 1
        else:
            result = migrate_references(repo)
    except (RegistryError, ValueError, OSError, json.JSONDecodeError) as exc:
        result = _error_result(exc)
        exit_code = 2
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.command != "reconcile" and args.output:
        output = (repo / args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if exit_code:
        raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
