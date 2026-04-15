#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

STOP_WORDS = {
    "a", "all", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "get", "go", "how", "i", "in", "into", "is", "it", "look", "me", "my",
    "of", "on", "or", "request", "sent", "specific", "that", "the", "this",
    "to", "up", "use", "want", "with", "you",
}
LOW_SIGNAL_TOKENS = {
    "available", "codex", "library", "might", "populate", "prompt", "relevant",
    "skill", "skills",
}
GENERIC_SINGLE_TOKEN_SKILL_NAMES = {
    "build", "learn", "plan", "qa", "review", "ship",
}
THRESHOLD = 0.14


@dataclass
class Skill:
    name: str
    description: str
    path: Path


def resolve_skills_dir() -> Path:
    override = os.environ.get("PROMPT_ORACLE_SKILLS_DIR", "").strip()
    candidates = []
    if override:
        candidates.append(Path(override).expanduser())
    candidates.extend([
        Path(__file__).resolve().parents[2],
        Path.home() / ".openclaw" / "skills",
        Path.home() / ".codex" / "skills",
    ])
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Match an inbound prompt to installed Codex skills."
    )
    parser.add_argument("--prompt", help="Prompt text to analyze.")
    parser.add_argument("--prompt-file", help="Path to a file containing the prompt.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of markdown.",
    )
    args = parser.parse_args()
    if not args.prompt and not args.prompt_file:
        parser.error("Provide --prompt or --prompt-file")
    return args


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return args.prompt.strip()
    return Path(args.prompt_file).read_text(encoding="utf-8").strip()


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9][a-z0-9+.#/-]*", text.lower())
    return [normalize_token(word) for word in words if normalize_token(word)]


def make_bigrams(tokens: list[str]) -> set[str]:
    return {
        f"{left} {right}"
        for left, right in zip(tokens, tokens[1:])
        if left and right
    }


def normalize_token(token: str) -> str:
    token = token.strip("-_/")
    if not token or token in STOP_WORDS:
        return ""
    for suffix in ("ing", "edly", "ed", "ers", "er", "ies", "s"):
        if token.endswith(suffix) and len(token) > len(suffix) + 2:
            if suffix == "ies":
                token = token[:-3] + "y"
            else:
                token = token[: -len(suffix)]
            break
    return token


def extract_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", ""
    parts = text.split("---", 2)
    if len(parts) < 3:
        return "", ""
    raw = parts[1]
    lines = raw.splitlines()
    name = ""
    description = ""
    for index, line in enumerate(lines):
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip('"\'')
            continue
        if not line.startswith("description:"):
            continue
        rest = line.split(":", 1)[1].strip()
        if rest in {">", "|"}:
            chunks = []
            for continuation in lines[index + 1 :]:
                if continuation.startswith(" ") or continuation.startswith("\t"):
                    chunks.append(continuation.strip())
                elif not continuation.strip():
                    continue
                else:
                    break
            description = " ".join(chunks).strip().strip('"\'')
        else:
            description = rest.strip().strip('"\'')
        break
    return name, description


def iter_skills() -> Iterable[Skill]:
    skills_dir = resolve_skills_dir()
    for path in sorted(skills_dir.glob("*/SKILL.md")):
        parent = path.parent.name
        if parent.startswith(".") or "quarantine" in parent:
            continue
        text = path.read_text(encoding="utf-8")
        name, description = extract_frontmatter(text)
        if not name:
            name = parent
        if not description:
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            description = lines[1] if len(lines) > 1 else ""
        yield Skill(name=name, description=description, path=path)


def has_explicit_skill_mention(prompt_text: str, skill_name: str) -> bool:
    skill_name = skill_name.lower().strip()
    if not skill_name:
        return False
    patterns = [
        rf"(^|\s)/{re.escape(skill_name)}($|\s)",
        rf"(^|\s)use\s+{re.escape(skill_name)}($|\s)",
        rf"(^|\s){re.escape(skill_name)}\s+skill($|\s)",
        rf"(^|\s)skill\s+{re.escape(skill_name)}($|\s)",
        rf"`{re.escape(skill_name)}`",
    ]
    if any(re.search(pattern, prompt_text) for pattern in patterns):
        return True
    return any(ch in skill_name for ch in "-_/ ") and skill_name in prompt_text


def score_skill(prompt: str, skill: Skill) -> tuple[float, list[str]]:
    prompt_text = prompt.lower()
    prompt_token_list = tokenize(prompt)
    prompt_tokens = set(prompt_token_list)
    prompt_bigrams = make_bigrams(prompt_token_list)
    name_token_list = tokenize(skill.name.replace("-", " "))
    name_tokens = set(name_token_list)
    name_bigrams = make_bigrams(name_token_list)
    desc_tokens = set(tokenize(skill.description))

    overlap_name = {token for token in (prompt_tokens & name_tokens) if token not in LOW_SIGNAL_TOKENS}
    overlap_desc = {token for token in (prompt_tokens & desc_tokens) if token not in LOW_SIGNAL_TOKENS}

    score = 0.0
    reasons: list[str] = []

    if has_explicit_skill_mention(prompt_text, skill.name):
        score += 1.2
        reasons.append("explicitly named")

    if overlap_name:
        score += 0.45 + (0.18 * len(overlap_name))
        reasons.append("name overlap: " + ", ".join(sorted(overlap_name)[:4]))

    if len(name_tokens) >= 2 and name_tokens.issubset(prompt_tokens):
        score += 0.72
        reasons.append("full name intent")
    elif prompt_bigrams & name_bigrams:
        score += 0.34
        reasons.append("name phrase intent")

    if overlap_desc:
        score += min(0.7, 0.12 * len(overlap_desc))
        reasons.append("description overlap: " + ", ".join(sorted(overlap_desc)[:5]))

    desc_text = skill.description.lower()
    if any(
        phrase in desc_text and phrase in prompt_text
        for phrase in (
            "a/b test",
            "landing page",
            "jira",
            "playwright",
            "figma",
            "seo",
            "pricing",
            "react",
            "python",
            "email",
            "skill library",
            "local skill",
        )
    ):
        score += 0.22
        reasons.append("shared domain phrase")

    if "build" in prompt_tokens and any(token in desc_tokens for token in {"build", "create", "creating"}):
        score += 0.14
        reasons.append("creation intent")

    if any(token in prompt_tokens for token in {"find", "discover", "match", "analyze"}) and any(
        token in desc_tokens for token in {"find", "discover", "search", "match", "analyze"}
    ):
        score += 0.14
        reasons.append("discovery intent")

    if (
        skill.name.lower() in GENERIC_SINGLE_TOKEN_SKILL_NAMES
        and len(name_tokens) == 1
        and not has_explicit_skill_mention(prompt_text, skill.name)
    ):
        score -= 0.18
        reasons.append("generic single-token name")

    asks_for_skill = "skill" in prompt_text or "skills" in prompt_text
    asks_for_creation = any(term in prompt_text for term in ("build", "create", "make"))
    asks_for_matching = any(
        term in prompt_text
        for term in ("relevant", "match", "matching", "which skills", "skill library", "available skill")
    )
    is_skill_tool = "skill" in skill.name.lower() or "skill" in desc_text

    if asks_for_skill and asks_for_creation and is_skill_tool and any(
        term in desc_text for term in ("create", "creating", "new skill", "update an existing skill")
    ):
        score += 0.34
        reasons.append("skill creation fit")

    if asks_for_skill and asks_for_creation and "creator" in skill.name.lower():
        score += 0.18
        reasons.append("creator name fit")

    if asks_for_skill and asks_for_matching and is_skill_tool and any(
        term in desc_text for term in ("relevant", "match", "matching", "search", "find", "local skill")
    ):
        score += 0.34
        reasons.append("skill routing fit")

    normalized = score / max(1.0, len(name_tokens) * 0.8 + len(desc_tokens) * 0.08)
    return normalized, reasons


def make_markdown(prompt: str, matches: list[dict]) -> str:
    lines = [f'Relevant skills for: "{prompt}"', ""]
    if not matches:
        lines.append("- No strong local skill matches found.")
        return "\n".join(lines)

    for match in matches:
        reason = "; ".join(match["reasons"][:2]) if match["reasons"] else "general relevance"
        lines.append(
            f'- `{match["name"]}` — score {match["score"]:.2f}; {reason}; {match["path"]}'
        )

    lines.extend(["", "Ready-to-paste skill hints:"])
    for match in matches:
        lines.append(f'`use {match["name"]}`')
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    prompt = read_prompt(args)
    matches = []
    for skill in iter_skills():
        score, reasons = score_skill(prompt, skill)
        if score >= THRESHOLD:
            matches.append(
                {
                    "name": skill.name,
                    "description": skill.description,
                    "path": str(skill.path),
                    "score": round(score, 4),
                    "reasons": reasons,
                }
            )

    matches.sort(key=lambda item: (-item["score"], item["name"]))

    if args.json:
        print(json.dumps({"prompt": prompt, "matches": matches}, indent=2))
        return

    print(make_markdown(prompt, matches))


if __name__ == "__main__":
    main()
