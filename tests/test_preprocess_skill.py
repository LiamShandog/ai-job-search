"""Guards for the /preprocess skill spec (step 2 of the daily loop).

The skill is a markdown spec (the spec IS the implementation). The invariant
worth pinning hardest is the one the whole four-skill split exists for: this
skill runs the evaluation behind /apply's blocking gate and then STOPS without
asking it, because the route - set later by the user - is the gate's answer.
Silently asking or inferring that answer would collapse the loop back into an
interactive command.

The second is the public-repo boundary: seen_jobs.json is committed on this
fork, so evaluation prose goes to a gitignored file and only compact eval_*
fields reach the entry.
"""
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / ".claude" / "skills" / "daily-preprocess" / "SKILL.md"
ROUTE_ARGS = REPO / ".claude" / "skills" / "daily-preprocess" / "route-args.md"


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


class PreprocessSkillSpec(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text(encoding="utf-8")
        self.sections = {k: _flat(v) for k, v in _sections(self.text).items()}

    def test_skill_file_exists_with_lint_compliant_header(self):
        self.assertTrue(SKILL.is_file(), "skill spec missing")
        self.assertTrue(
            self.text.startswith("---\n"),
            "skill spec must start with YAML frontmatter at byte 0 (no BOM, no blank line)",
        )
        self.assertIn("name: preprocess", self.text)

    def test_runs_apply_step_1_then_stops_before_the_gate(self):
        """The reason this skill exists. Do not let it drift."""
        evaluate = self.sections["Step 3: Evaluate"]
        self.assertIn("Steps 0 and 1 only", evaluate)
        self.assertIn("Should I proceed with drafting the application for this role?", evaluate)
        self.assertIn("not asked here", evaluate)
        self.assertIn("no answer to it is inferred", evaluate)

    def test_the_route_is_documented_as_the_gates_answer(self):
        self.assertIn("`route` field is the gate's answer", _flat(self.text))
        self.assertIn(
            "Never ask `/apply`'s gate question, and never infer its answer",
            self.sections["Important Rules"],
        )

    def test_evaluation_set_is_apply_routed_ranked_entries_only(self):
        step2 = self.sections["Step 2: Select the evaluation set"]
        self.assertIn('status == "ranked"', step2)
        self.assertIn("Only apply-routed jobs", step2)
        self.assertIn("`base` and `skip` are not evaluated", step2)

    def test_empty_set_exits_clean_without_a_fallback(self):
        step2 = self.sections["Step 2: Select the evaluation set"]
        self.assertIn("do not fall back", step2)
        self.assertIn("exit clean", step2)

    def test_prose_goes_to_the_gitignored_file_not_seen_jobs(self):
        """seen_jobs.json is committed on a public repo; the prose file is not."""
        step4 = self.sections["Step 4: Persist"]
        self.assertIn("job_scraper/preprocess_YYYY-MM-DD.md", step4)
        self.assertIn("**/job_scraper/*.md", step4)
        self.assertIn("Keep it flat", step4)
        self.assertIn("No prose, no posting text", step4)

    def test_only_compact_eval_fields_reach_seen_jobs(self):
        step4 = self.sections["Step 4: Persist"]
        for field in ("eval_score", "eval_verdict", "eval_date", "eval_file"):
            self.assertIn(field, step4)
        self.assertIn("do not change `status`", step4)

    def test_fetch_failure_is_not_expired(self):
        """`expired` is /rank's transition to own."""
        self.assertIn("Do not mark it `expired`", self.sections["Step 3: Evaluate"])

    def test_shared_contracts_are_referenced_not_restated(self):
        self.assertTrue(ROUTE_ARGS.is_file(), "shared route-args contract missing")
        preflight = self.sections["Step 0: Preflight"]
        self.assertIn("route-args.md", preflight)
        self.assertIn("slack-output.md", preflight)
        self.assertIn("do not restate", preflight.lower())

    def test_slack_preflight_uses_the_tool_list_not_a_shell_probe(self):
        preflight = self.sections["Step 0: Preflight"]
        self.assertIn("session tool list", preflight)
        self.assertIn("Never run `claude mcp list`", preflight)

    def test_tracker_is_only_named_in_a_never_clause(self):
        self.assertIn(
            "Never write `job_search_tracker.csv`", self.sections["Important Rules"]
        )


if __name__ == "__main__":
    unittest.main()
