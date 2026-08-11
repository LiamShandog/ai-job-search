"""Guards for the outbox submission-packet contract.

`/apply` and `/tailor` are markdown specs (the spec IS the implementation), so
these tests pin the invariants that would otherwise break silently and only be
noticed when a recruiter receives the wrong thing:

  - the recruiter-facing filenames inside a packet, which must NOT carry the
    company name (the folder is for the candidate; the filename is what lands
    in the employer's ATS);
  - the compile-in-place rule -- `cover.cls` and
    `\\fontspec[Path = OpenFonts/fonts/raleway/]` resolve relative to
    `cover_letters/`, so a build run inside `outbox/` fails or silently loses
    the Raleway font;
  - `outbox_dir` surviving a `/rank` rewrite, the same way `cv_file` does;
  - `outbox/` staying out of git -- the PDFs are caught by the blanket `*.pdf`
    rule, but APPLY.txt and START HERE.txt are not, and they name the employers
    applied to and set out where the candidate is weak.
"""
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
APPLY = REPO / ".claude" / "commands" / "apply.md"
TAILOR = REPO / ".claude" / "commands" / "tailor.md"
RANK = REPO / ".claude" / "commands" / "rank.md"
SCRAPER_SKILL = REPO / ".claude" / "skills" / "job-scraper" / "SKILL.md"
GITIGNORE = REPO / ".gitignore"

PACKET_STEP = "Step 5.6"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class PacketStepTests(unittest.TestCase):
    def test_both_commands_define_the_packet_step(self):
        for path in (APPLY, TAILOR):
            with self.subTest(command=path.name):
                text = read(path)
                self.assertIn(PACKET_STEP, text)
                self.assertIn("outbox/", text)

    def test_packet_step_follows_the_state_write(self):
        """5.6 must come after 5.5 -- the outbox_dir it writes lands on the
        entry Step 5.5 creates, so the order is load-bearing."""
        for path in (APPLY, TAILOR):
            with self.subTest(command=path.name):
                text = read(path)
                self.assertLess(
                    text.index("Step 5.5"),
                    text.index(PACKET_STEP),
                    f"{path.name}: Step 5.6 must be documented after Step 5.5",
                )

    def test_recruiter_facing_filenames_are_pinned(self):
        """These exact names are what an employer's ATS receives."""
        self.assertIn("Liam Shannon - CV.pdf", read(APPLY))
        self.assertIn("Liam Shannon - Cover Letter.pdf", read(APPLY))
        # /tailor never writes a cover letter.
        self.assertIn("Liam Shannon - CV.pdf", read(TAILOR))
        self.assertNotIn("Liam Shannon - Cover Letter.pdf", read(TAILOR))

    def test_folder_naming_convention_is_stated(self):
        for path in (APPLY, TAILOR):
            with self.subTest(command=path.name):
                self.assertIn("outbox/<Company> - <Role>", read(path))

    def test_pdfs_are_copied_never_moved(self):
        """Moving the PDF would strand the source's sibling output and break a
        re-compile."""
        for path in (APPLY, TAILOR):
            with self.subTest(command=path.name):
                self.assertRegex(read(path), r"[Cc]opy\s*(--|—|-)\s*never move")

    def test_never_compile_inside_outbox(self):
        for path in (APPLY, TAILOR):
            with self.subTest(command=path.name):
                self.assertIn("Never compile inside `outbox/`", read(path))

    def test_apply_explains_why_compiling_in_outbox_breaks(self):
        """The reason has to travel with the rule, or a later edit 'simplifies'
        it away."""
        text = read(APPLY)
        self.assertIn("cover.cls", text)
        self.assertIn("OpenFonts/fonts/raleway/", text)

    def test_apply_txt_is_part_of_the_packet(self):
        for path in (APPLY, TAILOR):
            with self.subTest(command=path.name):
                self.assertIn("APPLY.txt", read(path))

    def test_start_here_index_is_updated_but_never_reversed(self):
        """/apply and /tailor add to READY TO SEND; they must never pull an
        entry back out of ALREADY SUBMITTED or DROPPED."""
        for path in (APPLY, TAILOR):
            with self.subTest(command=path.name):
                text = read(path)
                self.assertIn("START HERE.txt", text)
                self.assertIn("READY TO SEND", text)
                self.assertIn("ALREADY SUBMITTED", text)
                self.assertIn("DROPPED", text)


class OutboxDirFieldTests(unittest.TestCase):
    def test_both_commands_write_outbox_dir(self):
        for path in (APPLY, TAILOR):
            with self.subTest(command=path.name):
                self.assertIn("outbox_dir", read(path))

    def test_schema_documents_outbox_dir(self):
        """The job-scraper skill is the canonical schema definition."""
        self.assertIn("outbox_dir", read(SCRAPER_SKILL))

    def test_rank_never_drops_outbox_dir(self):
        """Same protection cv_file has -- a re-rank must not discard it."""
        text = read(RANK)
        never_drop = [
            line for line in text.splitlines() if "never drop" in line
        ]
        self.assertTrue(never_drop, "rank.md lost its never-drop rule")
        self.assertTrue(
            any("outbox_dir" in line for line in never_drop),
            "outbox_dir must appear in rank.md's never-drop-on-rewrite list",
        )

    def test_sources_stay_outside_the_packet(self):
        """cv_file/cover_letter_file point at the sources, not the packet --
        /outcome, /interview, /notion-sync and /html-report all read them."""
        self.assertIn("cv/main_<company>_<role>", read(APPLY))
        self.assertIn("cover_letters/cover_<company>_<role>", read(APPLY))
        self.assertIn("cv/main_<company>_<role>", read(TAILOR))


class GitignoreTests(unittest.TestCase):
    def test_outbox_is_ignored(self):
        self.assertIn("outbox/", read(GITIGNORE))

    def test_git_actually_ignores_a_packet_note(self):
        """The blanket *.pdf rule already hid the PDFs; the .txt notes are the
        ones that were exposed. Skips cleanly outside a git checkout."""
        probe = "outbox/Some Company - Some Role/APPLY.txt"
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
        self.assertEqual(
            result.returncode, 0, f"git does not ignore {probe}"
        )


if __name__ == "__main__":
    unittest.main()
