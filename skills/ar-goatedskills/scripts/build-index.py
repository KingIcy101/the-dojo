#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path


SKILL_FILE_NAME = "SKILL.md"
SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUT = SKILL_DIR / "skill-index.json"
HOME = Path.home()
WORKSPACE_DIR_NAMES = {"skills", ".skills"}
EXCLUDED_SEGMENTS = {
    ".git",
    "__pycache__",
    "goatedskills",
    "node_modules",
    "vendor_imports",
}
EXCLUDED_PART_PATTERNS = [
    re.compile(r"^skills-archive", re.IGNORECASE),
    re.compile(r"^skills-backup", re.IGNORECASE),
    re.compile(r".*quarantine.*", re.IGNORECASE),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the local find-local-skills index.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--mirror-out", action="append", type=Path, default=[])
    parser.add_argument("--workspace-root", action="append", type=Path, default=[])
    return parser.parse_args()


def normalized_parts(path: Path) -> list[str]:
    return [part.lower() for part in path.parts]


def is_excluded(path: Path) -> bool:
    for part in normalized_parts(path):
        if part in EXCLUDED_SEGMENTS:
            return True
        if any(pattern.match(part) for pattern in EXCLUDED_PART_PATTERNS):
            return True
    return False


def read_description(skill_md: Path) -> str:
    try:
        content = skill_md.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""

    frontmatter = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", content, re.DOTALL)
    if frontmatter:
        lines = frontmatter.group(1).splitlines()
        for index, line in enumerate(lines):
            if not line.startswith("description:"):
                continue
            remainder = line.split(":", 1)[1].strip()
            collected: list[str] = []
            if remainder and remainder not in {">", "|", ">-", "|-"}:
                collected.append(remainder.strip('"').strip("'"))
            for follow in lines[index + 1 :]:
                if not follow.startswith((" ", "\t")):
                    break
                stripped = follow.strip()
                if stripped:
                    collected.append(stripped)
            description = re.sub(r"\s+", " ", " ".join(collected)).strip()
            if description:
                return description

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(("#", "---")):
            continue
        if len(stripped) >= 20:
            return stripped[:300]

    return ""


def explicit_home_roots() -> list[tuple[str, Path]]:
    return [
        ("codex", HOME / ".codex" / "skills"),
        ("claude", HOME / ".claude" / "skills"),
        ("agents", HOME / ".agents" / "skills"),
        ("cursor", HOME / ".cursor" / "skills"),
        ("cursor", HOME / ".cursor" / "skills-cursor"),
        ("factory", HOME / ".factory" / "skills"),
        ("gemini", HOME / ".gemini" / "antigravity" / "skills"),
    ]


def extra_roots_from_env() -> list[tuple[str, Path]]:
    value = os.environ.get("FIND_LOCAL_SKILLS_DIRS", "").strip()
    if not value:
        return []
    roots: list[tuple[str, Path]] = []
    for raw in value.split(os.pathsep):
        raw = raw.strip()
        if raw:
            roots.append(("env", Path(raw).expanduser()))
    return roots


def discover_workspace_roots(root: Path, max_depth: int = 4) -> list[Path]:
    discovered: list[Path] = []
    queue: list[tuple[Path, int]] = [(root, 0)]
    seen: set[str] = set()

    while queue:
        current, depth = queue.pop(0)
        try:
            resolved = current.resolve()
        except OSError:
            continue
        key = str(resolved)
        if key in seen:
            continue
        seen.add(key)

        if not current.is_dir() or is_excluded(current):
            continue

        if current.name in WORKSPACE_DIR_NAMES:
            discovered.append(current)
            continue

        if depth >= max_depth:
            continue

        try:
            children = sorted(
                (child for child in current.iterdir() if child.is_dir()),
                key=lambda child: child.name.lower(),
            )
        except OSError:
            continue

        for child in children:
            queue.append((child, depth + 1))

    return discovered


def dedupe_roots(candidates: list[tuple[str, Path]]) -> list[tuple[str, Path, Path]]:
    roots: list[tuple[str, Path, Path]] = []
    seen: set[str] = set()

    for source, path in candidates:
        path = path.expanduser()
        if not path.exists() or not path.is_dir() or is_excluded(path):
            continue
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if is_excluded(resolved):
            continue
        key = str(resolved)
        if key in seen:
            continue
        seen.add(key)
        roots.append((source, path, resolved))

    return roots


def iter_skill_dirs(root: Path) -> list[Path]:
    skill_dirs: list[Path] = []
    try:
        children = sorted(
            (child for child in root.iterdir() if child.is_dir()),
            key=lambda child: child.name.lower(),
        )
    except OSError:
        return skill_dirs

    for child in children:
        if is_excluded(child):
            continue
        if (child / SKILL_FILE_NAME).exists():
            skill_dirs.append(child)
            continue
        try:
            grandchildren = sorted(
                (grandchild for grandchild in child.iterdir() if grandchild.is_dir()),
                key=lambda grandchild: grandchild.name.lower(),
            )
        except OSError:
            continue
        for grandchild in grandchildren:
            if is_excluded(grandchild):
                continue
            if (grandchild / SKILL_FILE_NAME).exists():
                skill_dirs.append(grandchild)
    return skill_dirs


def root_has_skill_children(root: Path) -> bool:
    return bool(iter_skill_dirs(root))


def build_index(args: argparse.Namespace) -> dict:
    workspace_inputs = [Path.cwd(), *args.workspace_root]
    root_candidates: list[tuple[str, Path]] = []

    for workspace_root in workspace_inputs:
        workspace_root = workspace_root.expanduser()
        if workspace_root.exists() and workspace_root.is_dir():
            for skill_root in discover_workspace_roots(workspace_root):
                root_candidates.append(("workspace", skill_root))

    root_candidates.extend(explicit_home_roots())
    root_candidates.extend(extra_roots_from_env())

    roots = [root for root in dedupe_roots(root_candidates) if root_has_skill_children(root[1])]

    entries_by_name: dict[str, dict] = {}
    duplicates: dict[str, list[dict[str, str]]] = {}
    missing: list[str] = []

    for source, root_path, resolved_root in roots:
        for child in iter_skill_dirs(root_path):
            skill_md = child / SKILL_FILE_NAME
            description = read_description(skill_md)
            if not description:
                missing.append(child.name)
                continue

            entry = {
                "name": child.name,
                "description": description,
                "location": str(skill_md),
                "source": source,
                "root": str(root_path),
                "resolvedRoot": str(resolved_root),
            }

            existing = entries_by_name.get(child.name)
            if existing:
                duplicates.setdefault(child.name, []).append(entry)
                continue

            entries_by_name[child.name] = entry

    payload = {
        "generatedAt": dt.datetime.now().astimezone().isoformat(),
        "cwd": str(Path.cwd()),
        "eligibleCount": len(entries_by_name),
        "missingCount": len(sorted(set(missing))),
        "duplicateNameCount": len(duplicates),
        "roots": [
            {
                "source": source,
                "path": str(root_path),
                "resolvedPath": str(resolved_root),
            }
            for source, root_path, resolved_root in roots
        ],
        "excludedRules": {
            "segments": sorted(EXCLUDED_SEGMENTS),
            "patterns": [pattern.pattern for pattern in EXCLUDED_PART_PATTERNS],
        },
        "eligible": [entries_by_name[name] for name in sorted(entries_by_name)],
        "missing": sorted(set(missing)),
        "duplicates": duplicates,
    }
    return payload


def write_payload(payload: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    payload = build_index(args)

    primary_out = args.out.expanduser()
    write_payload(payload, primary_out)

    for mirror_out in args.mirror_out:
        write_payload(payload, mirror_out.expanduser())

    print(
        f"wrote {primary_out} eligible={payload['eligibleCount']} "
        f"missing={payload['missingCount']} duplicates={payload['duplicateNameCount']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
