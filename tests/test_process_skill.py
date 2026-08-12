"""Guards for the /process skill spec (step 3 of the daily loop).

The skill is a markdown spec (the spec IS the implementation). A full queue is
~92 jobs and runs for hours, so the invariants worth pinning are the ones that
decide whether an interrupted run is recoverable and whether a single bad job
can corrupt the rest:

- serial execution, because /apply and /tailor Step 5.6 renumber a shared index
  and read live directory state when naming packets;
- re-reading seen_jobs.json per job, because those commands rewrite it whole;
- filesystem-first resume, because outbox_dir is set on only 2 of 25 existing
  processed entries while 11 packets exist on disk;
- no processed marker and no packet on failure, because START HERE.txt would
  otherwise advertise an empty folder as ready to send.
"""
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / ".claude" / "skills" / "daily-process" / "SKILL.md"
GITIGNORE = REPO / ".gitignore"


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


class ProcessSkillSpec(unittest.TestCase):
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
        self.assertIn("name: process", self.text)

    def test_apply_phase_runs_before_tailor_phase(self):
        queue = self.sections["Step 2: Build the queue"]
        self.assertIn("Phase A first", queue)
        self.assertLess(
            queue.index("effective route `apply`"),
            queue.index("effective route `tailor`"),
            "the apply phase must be specified before the tailor phase",
        )

    def test_base_and_skip_are_never_queued(self):
        self.assertIn("`base` and `skip` are **never** queued", self.sections["Step 2: Build the queue"])

    def test_runs_serially_with_the_file_ownership_reasons_stated(self):
        """Parallelism would break three things at once; name all three."""
        work = self.sections["Step 3: Work the queue"]
        self.assertIn("One job at a time", work)
        self.assertIn("START HERE.txt", work)
        self.assertIn("disambiguator", work)
        self.assertIn("whole-file rewrite", work)

    def test_seen_jobs_is_reread_before_every_job(self):
        self.assertIn("Re-read `job_scraper/seen_jobs.json` from disk before every job",
                      self.sections["Step 3: Work the queue"])
        self.assertIn("Re-read `seen_jobs.json` before every job",
                      self.sections["Important Rules"])

    def test_resume_is_filesystem_first_and_distrusts_outbox_dir(self):
        queue = self.sections["Step 2: Build the queue"]
        self.assertIn("glob `outbox/*`", queue.lower())
        self.assertIn("Do not trust the `outbox_dir` field", queue)
        self.assertIn("filesystem is the source of truth", queue)

    def test_checkpoint_is_written_after_every_job(self):
        checkpoint = self.sections["Step 4: Checkpoint"]
        self.assertIn("job_scraper/process_state.json", checkpoint)
        self.assertIn("after every job", checkpoint)

    def test_checkpoint_path_is_actually_gitignored(self):
        """It names employers, roles and packet paths; this repo is public."""
        self.assertIn("**/job_scraper/process_state.json", GITIGNORE.read_text(encoding="utf-8"))

    def test_compile_failures_are_capped(self):
        work = self.sections["Step 3: Work the queue"]
        self.assertIn("**3** compile-and-fix attempts", work)

    def test_failure_writes_no_marker_and_no_packet(self):
        work = self.sections["Step 3: Work the queue"]
        self.assertIn("write no `processed` marker and create no `outbox/` folder", work)
        self.assertIn("Never write the `processed` marker or create a packet for a failed job",
                      self.sections["Important Rules"])

    def test_fetch_failure_is_not_expired(self):
        self.assertIn("Never mark it `expired`", self.sections["Step 3: Work the queue"])

    def test_one_failure_never_aborts_the_batch(self):
        self.assertIn("Nothing a single job does aborts the batch",
                      self.sections["Step 3: Work the queue"])

    def test_preflight_aborts_without_the_base_cv(self):
        """/tailor degrades silently to main_example.tex - 85 of those is a wasted run."""
        preflight = self.sections["Step 0: Preflight"]
        self.assertIn("cv/main_base.tex", preflight)
        self.assertIn("Abort", preflight)
        self.assertIn("pdflatex", preflight)

    def test_index_is_one_line_per_job_and_never_apply_txt(self):
        index = self.sections["Step 5: Post the index"]
        self.assertIn("One line per job", index)
        self.assertIn("Never post `APPLY.txt` contents", index)

    def test_tracker_is_only_named_in_a_never_clause(self):
        self.assertIn("Never write `job_search_tracker.csv`", self.sections["Important Rules"])

    def test_never_compile_inside_outbox(self):
        self.assertIn("Never compile inside `outbox/`", self.sections["Important Rules"])


if __name__ == "__main__":
    unittest.main()
