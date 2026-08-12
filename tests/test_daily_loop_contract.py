"""Cross-cutting guards for the four daily-loop skills.

Each skill has its own spec test. This file pins the invariants that live
*between* them - the ones no single-skill test can see, and that break quietly
when one skill is edited in isolation:

- the shared reference files exist and are referenced rather than restated, so
  the ambiguity rule cannot drift into three divergent copies;
- `allowed-tools` stays a comma-separated string in all four, because
  lint_skills.py only validates the bun-run paths when it parses as a string and
  silently skips a YAML list;
- no spec claims a Slack file-upload capability, because the connector has none;
- the /process checkpoint is genuinely ignored by git, not merely listed.
"""
import subprocess
import sys
import unittest
from pathlib import Path

try:
    import yaml
    _HAVE_YAML = True
except ImportError:
    _HAVE_YAML = False

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / ".claude" / "skills"
SLACK_CONTRACT = SKILLS / "daily-fetch" / "slack-output.md"
ROUTE_ARGS = SKILLS / "daily-preprocess" / "route-args.md"

LOOP = {
    "daily-fetch": "fetch",
    "daily-preprocess": "preprocess",
    "daily-process": "process",
    "daily-document": "document",
}


def _flat(text: str) -> str:
    return " ".join(text.split())


def _frontmatter(text: str) -> str:
    end = text.index("\n---", 4)
    return text[4:end]


class DailyLoopContract(unittest.TestCase):
    def test_all_four_skills_exist_with_the_expected_trigger(self):
        for directory, name in LOOP.items():
            path = SKILLS / directory / "SKILL.md"
            with self.subTest(skill=directory):
                self.assertTrue(path.is_file(), f"{directory}/SKILL.md missing")
                text = path.read_text(encoding="utf-8")
                self.assertTrue(
                    text.startswith("---\n"),
                    f"{directory} must start with frontmatter at byte 0 (no BOM)",
                )
                self.assertIn(f"name: {name}", text)

    @unittest.skipUnless(_HAVE_YAML, "PyYAML not installed")
    def test_allowed_tools_is_a_string_not_a_list(self):
        """lint_skills.py does `if isinstance(allowed, str)` before validating
        the bun-run paths inside it. A YAML list parses fine and silently skips
        that validation, so the constraint is invisible until a path rots."""
        for directory in LOOP:
            with self.subTest(skill=directory):
                text = (SKILLS / directory / "SKILL.md").read_text(encoding="utf-8")
                data = yaml.safe_load(_frontmatter(text))
                self.assertIsInstance(
                    data.get("allowed-tools"),
                    str,
                    f"{directory}: allowed-tools must be one comma-separated string",
                )

    def test_description_carries_an_explicit_trigger_list(self):
        """Skills auto-trigger on description. `process` and `document` are
        common English words, so the trigger list must be narrow and literal."""
        for directory in LOOP:
            with self.subTest(skill=directory):
                text = (SKILLS / directory / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("Triggers on:", _frontmatter(text))

    def test_shared_contracts_exist(self):
        self.assertTrue(SLACK_CONTRACT.is_file(), "slack-output.md missing")
        self.assertTrue(ROUTE_ARGS.is_file(), "route-args.md missing")

    def test_every_skill_references_the_slack_contract(self):
        for directory in LOOP:
            with self.subTest(skill=directory):
                text = (SKILLS / directory / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("slack-output.md", text)

    def test_route_taking_skills_reference_the_argument_contract(self):
        for directory in ("daily-preprocess", "daily-process", "daily-document"):
            with self.subTest(skill=directory):
                text = (SKILLS / directory / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("route-args.md", text)

    def test_ambiguity_rule_lives_in_the_shared_contract(self):
        """`tiktok` matches 23 queued postings. A silent closest-match here
        costs 23 unwanted /apply runs, which is why this is pinned centrally."""
        text = _flat(ROUTE_ARGS.read_text(encoding="utf-8"))
        self.assertIn("hard error for that token only", text)
        self.assertIn("write nothing for it", text)

    def test_route_set_by_shape_is_pinned(self):
        text = _flat(ROUTE_ARGS.read_text(encoding="utf-8"))
        self.assertIn("route_set_by", text)
        self.assertIn("user 2026-08-11", text)
        self.assertIn("Never write `suggested_route`", text)

    def test_no_skill_claims_a_slack_upload_capability(self):
        """The connector has no file-upload tool; PDFs never reach Slack."""
        forbidden = ("files.upload", "slack_upload", "upload_file")
        for directory in LOOP:
            text = (SKILLS / directory / "SKILL.md").read_text(encoding="utf-8")
            for token in forbidden:
                with self.subTest(skill=directory, token=token):
                    self.assertNotIn(token, text)

    def test_git_actually_ignores_the_process_checkpoint(self):
        """It names employers, roles and packet paths, and this repo is public.
        Skips cleanly outside a git checkout."""
        probe = "job_scraper/process_state.json"
        try:
            result = subprocess.run(
                ["git", "check-ignore", "-q", probe],
                cwd=REPO,
                capture_output=True,
            )
        except (OSError, FileNotFoundError):
            self.skipTest("git unavailable")
        if result.returncode == 128:
            self.skipTest("not a git checkout")
        self.assertEqual(result.returncode, 0, f"git does not ignore {probe}")

    @unittest.skipUnless(_HAVE_YAML, "PyYAML not installed")
    def test_lint_skills_passes(self):
        result = subprocess.run(
            [sys.executable, str(REPO / "tools" / "lint_skills.py")],
            cwd=REPO,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
