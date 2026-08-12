"""Guards for the /document skill spec (step 4 of the daily loop).

The skill is a markdown spec (the spec IS the implementation). Two invariants
carry real risk here, because this is the only loop skill that both writes the
application record and holds a tool that sends:

- Nothing is inferred. A packet in outbox/ is not a submission, and neither is
  `processed` status. An invented tracker row is authoritative to every reader
  downstream, so the user's arguments are the only evidence accepted.
- /outcome Rule 6 says follow-up drafts "must not be wired to tools that do
  [send]". This skill holds slack_send_message, so the follow-up branch and note
  drafts are prohibited outright rather than merely discouraged.
"""
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / ".claude" / "skills" / "daily-document" / "SKILL.md"


def _flat(text: str) -> str:
    """Collapse whitespace so assertions survive prose re-wrapping."""
    return " ".join(text.split())


def _sections(text: str) -> dict:
    parts = text.split("\n## ")
    result = {}
    for part in parts[1:]:
        heading, _, body = part.partition("\n")
        result[heading.strip()] = body
    return result


class DocumentSkillSpec(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text(encoding="utf-8")
        self.flat = _flat(self.text)
        self.sections = {k: _flat(v) for k, v in _sections(self.text).items()}

    def test_skill_file_exists_with_lint_compliant_header(self):
        self.assertTrue(SKILL.is_file(), "skill spec missing")
        self.assertTrue(
            self.text.startswith("---\n"),
            "skill spec must start with YAML frontmatter at byte 0 (no BOM, no blank line)",
        )
        self.assertIn("name: document", self.text)

    def test_a_packet_is_never_treated_as_a_submission(self):
        rule = self.sections["The rule this skill exists to hold"]
        self.assertIn("A packet in `outbox/` is not a submission", rule)
        self.assertIn("not from `processed` status", rule)
        self.assertIn("not from a route", rule)
        self.assertIn("A packet is not a submission", self.sections["Important Rules"])

    def test_no_arguments_means_sync_only(self):
        self.assertIn(
            "run the `/notion-sync` half only",
            self.sections["The rule this skill exists to hold"],
        )

    def test_outcome_remains_the_sole_tracker_writer(self):
        step2 = self.sections["Step 2: Record each outcome"]
        self.assertIn("never writes `job_search_tracker.csv` itself", step2)
        self.assertIn("sole mover to `applied`", step2)
        self.assertIn("`/outcome` is the sole tracker writer", self.sections["Important Rules"])

    def test_follow_up_branch_and_note_drafts_are_prohibited(self):
        """/outcome Rule 6 vs a skill holding slack_send_message."""
        step2 = self.sections["Step 2: Record each outcome"]
        self.assertIn("Never enter `/outcome` Step 2b", step2)
        self.assertIn("must not be wired to tools that do", step2)
        self.assertIn("Never post a thank-you note draft to Slack", step2)
        self.assertIn(
            "Never enter the follow-up branch, and never post note drafts to Slack",
            self.sections["Important Rules"],
        )

    def test_outcome_detail_is_never_invented(self):
        step2 = self.sections["Step 2: Record each outcome"]
        self.assertIn("The argument is the whole answer", step2)
        self.assertIn("Tick a stage only when the user typed one", step2)
        self.assertIn("Never prompt mid-batch, and never guess", step2)

    def test_ambiguous_selector_records_nothing(self):
        step1 = self.sections["Step 1: Resolve the named applications"]
        self.assertIn("record nothing for that token", step1)
        self.assertIn("An ambiguous selector records nothing", self.sections["Important Rules"])

    def test_notion_sync_runs_after_the_outcome_writes(self):
        step3 = self.sections["Step 3: Sync to Notion"]
        self.assertIn("after every outcome write has finished", step3)
        self.assertIn("clean outcome here, not a failure", step3)

    def test_slack_preflight_uses_the_tool_list_not_a_shell_probe(self):
        preflight = self.sections["Step 0: Preflight"]
        self.assertIn("session tool list", preflight)
        self.assertIn("Never run `claude mcp list`", preflight)


if __name__ == "__main__":
    unittest.main()
