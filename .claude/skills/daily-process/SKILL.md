---
name: process
description: >
  Step 3 of the daily job-search loop. Works the queued postings into submission packets - the
  rest of /apply on apply-routed jobs, /tailor on tailor-routed ones - checkpointing after every
  job, and posts a one-line index of every document built to Slack. Triggers on: /process,
  step 3 of the daily loop, process the queue, build the queued applications, work the job queue
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch, Agent
---

# /process - Build the Queued Applications

---

Step 3 of the four-skill daily loop: **`/fetch` → `/preprocess` → `/process` → `/document`**.

This is the long one. Every queued job gets a tailored CV, a compile, a PDF verification and an
`outbox/` packet. A full queue is currently ~92 jobs and runs for hours, so the design priority is
**resumability and failure isolation**, not speed.

`$ARGUMENTS` is optional: `selector=route` pairs, plus the flags `--dry-run` and `--restart`.

## Step 0: Preflight

1. Read `.claude/skills/daily-fetch/slack-output.md` and
   `.claude/skills/daily-preprocess/route-args.md`. Both are single definitions; do not restate
   them.
2. **`cv/main_base.tex` must exist.** Abort with a clear message if it does not. `/tailor`
   silently degrades to `cv/main_example.tex` with a warning when the base CV is missing, and 85
   of those warnings is a wasted afternoon — the whole queue would be tailored from the wrong
   source.
3. **`pdflatex` must resolve.** Abort if not. The active `liam-onepage` template declares it, and
   nothing downstream can verify a PDF that was never built.
4. `pdftotext` is a **soft** check. If it is missing, warn **once for the batch** — not once per
   job — and carry on with the visual PDF read alone, as `/apply` Step 5d already allows.
5. Check Slack from the session tool list only. **Never run `claude mcp list`.** Absent → continue
   and say so once.
6. **Post the plan before starting**: the queue size, the phase order, and that this will take
   hours with progress posts every 10 jobs. A silent multi-hour run is indistinguishable from a
   hung one.

## Step 1: Apply route changes

Apply any `selector=route` pairs exactly as `route-args.md` specifies. Reject outcome statuses —
they belong to `/document`. Report applied, unmatched and ambiguous before building the queue.

## Step 2: Build the queue

Two phases, in this order:

| Phase | Selector | Command |
|---|---|---|
| A | `status == "ranked"`, effective route `apply` | `/apply` from Step 1.5 |
| B | `status == "ranked"`, effective route `tailor` | `/tailor` |

**Phase A first, deliberately.** It is the smaller, higher-judgment set, and its `/preprocess`
evidence is freshest now. A crash three hours in has then already banked the work that mattered
most.

`base` and `skip` are **never** queued. `base` means send `cv/main_base.tex` unchanged and has no
build step; `skip` failed a gate.

### Resume

A job is already done — skip it — when **either**:

- the checkpoint records it as `ok`, **or**
- its `seen_jobs.json` entry reads `processed` **and** a folder matching `<Company> - ` exists
  under `outbox/` (glob `outbox/*`, case-insensitive).

**Do not trust the `outbox_dir` field for this.** It postdates most existing `processed` entries —
today it is set on 2 of 25, while 11 packets exist on disk. The filesystem is the source of truth.

That disjunction is why the checkpoint is an accelerator and never the record: delete it and the
run still resumes correctly. `--restart` discards it and rebuilds the queue from scratch.

`--dry-run` prints the queue — phase, company, role, effective route, and what would be skipped as
already done — and exits without drafting anything.

## Step 3: Work the queue

**One job at a time, each inside its own `Agent` sub-agent.** The orchestrator holds only the
queue and the checkpoint.

Two reasons, and the second is the binding one:

- **Context.** 92 jobs of research, rewriting and compile logs will exhaust a single context long
  before job 92. A per-job agent bounds it. `/rank` Step 2 already uses this pattern.
- **File ownership.** Serial execution is what lets `/apply` and `/tailor` run *exactly as
  written*, including their Step 5.5 state write and Step 5.6 packet assembly. Running them
  concurrently would break three things at once: `outbox/START HERE.txt` is renumbered by every
  packet; the packet-naming disambiguator reads live directory state to decide whether an employer
  already has a folder; and `seen_jobs.json` is a whole-file rewrite. Any future `--parallel`
  would have to hoist all three into the orchestrator — a deliberate deviation from those
  commands' documented ownership. Do not add it casually.

**Re-read `job_scraper/seen_jobs.json` from disk before every job.** `/apply` and `/tailor`
Step 5.5 rewrite it whole; a copy cached at the start and written back at the end would silently
erase the `processed` marker of every job already completed.

### Phase A jobs

Run `.claude/commands/apply.md` from **Step 1.5 onward**. Step 1 was already run by `/preprocess`
— read its output from the entry's `eval_file` and pass it as prior context.

**Do not ask the gate.** The effective route is its answer: the job is in this queue because it is
still routed `apply` after the user saw the evaluation.

A job promoted to `apply` in *this run's own arguments* has no evaluation. Run Step 1 inline for
it, **without gating on it**, and flag it `[no pre-review]` in the index — the user's
`<company>=apply` token is itself the instruction to proceed.

### Phase B jobs

Run `.claude/commands/tailor.md` in full. It has no gates and is unattended by design.

### Per-job result

Each sub-agent returns a small JSON object and nothing larger:

```json
{"key": "...", "result": "ok|failed|skipped", "reason": "...",
 "cv_file": "...", "cover_letter_file": "...", "outbox_dir": "...", "verification": "..."}
```

The orchestrator records it and moves to the next job. **Nothing a single job does aborts the
batch.**

| Failure | Handling |
|---|---|
| Posting unretrievable after the full `09-web-research.md` escalation | `failed`, reason `fetch`. **Never mark it `expired`** — that transition belongs to `/rank`, and one bad fetch mid-batch is not evidence a posting is dead |
| A gate fails in `/tailor` Step 1 | `skipped`, reason quotes the gate. Worth reporting: it means `/rank` and the user's route disagree |
| Compile fails | Up to **3** compile-and-fix attempts, then `failed` with the first line of the LaTeX error |
| PDF visual or ATS verification fails and does not converge | Same **3**-attempt cap, then `failed` |
| `pdftotext` missing | Not a failure. The once-per-batch warning from Step 0 covers it |

**On any failure: write no `processed` marker and create no `outbox/` folder.** Both `/apply` and
`/tailor` already say the marker follows verification; a packet holding no PDF is worse than no
packet, because `START HERE.txt` would advertise it as ready to send. Leave the
`cv/main_<company>_<role>.tex` source on disk — it is gitignored and is the starting point for a
manual retry.

## Step 4: Checkpoint

Write `job_scraper/process_state.json` **after every job**, before the next one starts, so a crash
loses at most the job in flight:

```json
{
  "run_id": "2026-08-11T09:14",
  "phase": "tailor",
  "queue": [{"key": "...", "company": "...", "title": "...", "route": "tailor"}],
  "done": {"<key>": {"result": "ok", "reason": "", "cv_file": "...",
                     "outbox_dir": "...", "finished": "2026-08-11T10:02"}},
  "progress_posted_at": 40
}
```

The file is gitignored (`**/job_scraper/process_state.json`) — it names employers, roles and
packet paths.

Post a progress line to the Slack thread every **10** completions and at the phase boundary:

```
Process: 40/92 done (38 ok, 2 failed) · 1h47m elapsed · now: Roblox — SWE Intern
```

## Step 5: Post the index

Use the `/process` template in `slack-output.md`: header to the channel, the index chunked into
threaded replies at ≤25 job lines each, then the footer.

**One line per job** — company, role, which files exist, the packet path, and the apply link.
Grouped by route, with a `failed` group carrying each reason.

**Never post `APPLY.txt` contents**, CV or cover-letter text, or any posting body text. Paths and
links only.

## Step 6: Report

Terminal summary: counts by result, elapsed time, the checkpoint path, every failure with its
reason, and the next command — submit from `outbox/`, then `/document <company>=applied`.

## Important Rules

1. **Serial, one job per sub-agent.** Not a throughput preference — it is what keeps `/apply` and
   `/tailor` Step 5.5 and 5.6 correct.
2. **Re-read `seen_jobs.json` before every job.** A cached copy written back at the end erases
   every marker earned during the run.
3. **Never write the `processed` marker or create a packet for a failed job.**
4. **Never mark a posting `expired`.** That is `/rank`'s transition.
5. **Never write `job_search_tracker.csv`.** Preparing documents is not applying — `/outcome` is
   the sole writer, and a packet in `outbox/` is a document that exists, not an application that
   was sent.
6. **Never trust `outbox_dir` to decide whether a packet exists.** Glob `outbox/`.
7. **Never compile inside `outbox/`.** `cover.cls` and the Raleway fonts resolve relative to
   `cover_letters/`; a build elsewhere fails or silently loses the font. Compile in place, copy
   the PDFs out.
8. **One job's failure never aborts the batch**, and the checkpoint is written before moving on.
