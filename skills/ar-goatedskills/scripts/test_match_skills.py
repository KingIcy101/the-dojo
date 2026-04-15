#!/usr/bin/env python3
import unittest
from pathlib import Path

from match_skills import Skill, score_skill


class PromptOracleMatcherTests(unittest.TestCase):
    def test_code_review_beats_generic_review_for_pre_merge_prompt(self):
        prompt = "review my code before I merge"
        skills = [
            Skill(
                name="review",
                description=(
                    "Pre-landing PR review. Analyzes diff against the base branch for SQL safety, "
                    "LLM trust boundary violations, conditional side effects, and other structural issues."
                ),
                path=Path("/tmp/review/SKILL.md"),
            ),
            Skill(
                name="code-review",
                description=(
                    "Automated code review for pull requests using specialized review patterns. "
                    "Use when the user asks to review code, review a PR, or check this PR."
                ),
                path=Path("/tmp/code-review/SKILL.md"),
            ),
        ]

        ranked = sorted(
            (
                {
                    "name": skill.name,
                    "score": score_skill(prompt, skill)[0],
                }
                for skill in skills
            ),
            key=lambda item: (-item["score"], item["name"]),
        )

        self.assertEqual(ranked[0]["name"], "code-review")


if __name__ == "__main__":
    unittest.main()
