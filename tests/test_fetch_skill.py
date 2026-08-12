"""Guards for the /fetch skill spec (step 1 of the daily loop).

The skill is a markdown spec (the spec IS the implementation), so these tests
pin the invariants that would break silently: the header format lint_skills.py
enforces, the scrape-then-rank order, and the two file-ownership boundaries
that keep /fetch from answering decisions it has no evidence for - promoting a
`route` on the user's behalf, and writing a tracker row for an application
nobody has sent.
"""
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / ".claude" / "skills" / "daily-fetch" / "SKILL.md"
SLACK = REPO / ".claude" / "skills" / "daily-fetch" / "slack-output.md"


def _flat(text: str) -> str:
    """Collapse whitespace so assertions survive prose re-wrapping.

    These specs are hard-wrapped at ~95 columns, so any phrase long enough to
    be worth pinning is also long enough to straddle a line break.
    """
    return " ".join(text.split())


def _sections(text: str) -> dict:
    """Split a skill spec into {heading: body} by '##' headers.

    Splitting this way lets a fork's extra sections sit between the ones under
    test without shifting which text a given assertion sees.
    """
    parts = text.split("\n## ")
    result = {}
    for part in parts[1:]:
        heading, _, body = part.partition("\n")
        result[heading.strip()] = body
    return result


class FetchSkillSpec(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text(encoding="utf-8")
        self.sections = {k: _flat(v) for k, v in _sections(self.text).items()}

    def test_skill_file_exists_with_lint_compliant_header(self):
        self.assertTrue(SKILL.is_file(), "skill spec missing")
        self.assertTrue(
            self.text.startswith("---\n"),
            "skill spec must start with YAML frontmatter at byte 0 (no BOM, no blank line)",
        )
        self.assertIn("name: fetch", self.text)

    def test_scrape_runs_before_rank(self):
        headings = list(self.sections)
        scrape = next(i for i, h in enumerate(headings) if "Scrape" in h)
        rank = next(i for i, h in enumerate(headings) if "Rank" in h)
        self.assertLess(scrape, rank, "the scrape step must be specified before the rank step")

    def test_never_promotes_a_route_on_the_users_behalf(self):
        """/rank owns suggested_route; `route` is the user's override.

        Promoting here would silently answer the /apply gate that /preprocess
        exists to present.
        """
        rank_step = self.sections["Step 2: Rank"]
        self.assertIn("suggested_route", rank_step)
        self.assertIn("never writes the `route` field", rank_step)
        self.assertIn("Never write `route`", self.sections["Important Rules"])

    def test_tracker_is_only_ever_named_in_a_never_clause(self):
        """/outcome is the sole tracker writer across the whole loop."""
        self.assertIn("Never write `job_search_tracker.csv`", self.sections["Important Rules"])
        self.assertIn("Never enter its Step 6", self.sections["Step 1: Scrape"])

    def test_slack_preflight_uses_the_tool_list_not_a_shell_probe(self):
        preflight = self.sections["Step 0: Preflight"]
        self.assertIn("session tool list", preflight)
        self.assertIn("claude mcp list", preflight)
        self.assertIn("Never run", preflight)

    def test_slack_absence_does_not_abort_the_run(self):
        """Unlike /notion-sync, the local work is the point here."""
        self.assertIn("continue the run", self.sections["Step 0: Preflight"])
        self.assertIn("not a run failure", self.sections["Important Rules"])

    def test_shared_slack_contract_is_referenced_not_restated(self):
        self.assertTrue(SLACK.is_file(), "shared Slack contract missing")
        self.assertIn("slack-output.md", self.text)
        self.assertIn("Do not restate it", self.sections["Step 0: Preflight"])


if __name__ == "__main__":
    unittest.main()
