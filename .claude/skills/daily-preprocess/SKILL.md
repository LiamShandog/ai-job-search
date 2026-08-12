---
name: preprocess
description: >
  Step 2 of the daily job-search loop. Runs the fit evaluation from /apply Step 1 over the
  apply-routed jobs and posts the evaluations to Slack, where the routing decision answers
  /apply's gate asynchronously. Triggers on: /preprocess, step 2 of the daily loop, evaluate the
  apply-routed jobs, pre-process the queue, run the fit evaluations
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch, Agent
---

# /preprocess - Evaluate the Apply-Routed Jobs

---

Step 2 of the four-skill daily loop: **`/fetch` → `/preprocess` → `/process` → `/document`**.

`/apply` Step 1 ends in the only blocking gate in the system — *"Should I proceed with drafting
the application for this role?"* — and that gate is what makes the queue impossible to batch. This
skill runs the evaluation behind the gate and then **stops without asking it**.

The gate is answered later, asynchronously, by re-routing: the user reads the evaluations in
Slack and passes route changes to `/process`. The `route` field is the gate's answer.

`$ARGUMENTS` is optional: `selector=route` pairs, plus the flag `--again`.

## Step 0: Preflight

1. Read `.claude/skills/daily-fetch/slack-output.md` — the Slack contract. Do not restate it.
2. Read `.claude/skills/daily-preprocess/route-args.md` — the argument grammar and the
   `route`/`route_set_by` write contract. It is the single definition; do not restate it.
3. Check Slack availability from the session tool list only. **Never run `claude mcp list`** or
   any shell probe, and never initiate OAuth. If absent, continue the run and say so once.

## Step 1: Apply route changes

Parse `$ARGUMENTS` and apply any `selector=route` pairs exactly as `route-args.md` specifies —
including its matching order, its hard per-token error on an ambiguous selector, and its rule that
every token resolves before anything is written.

Reject an outcome status (`applied`, `interview`, …) with the message that file gives: it belongs
to `/document`, not here.

Report routes applied, unmatched and ambiguous before going on.

## Step 2: Select the evaluation set

Entries where `status == "ranked"` **and** the effective route (`route` if set, else
`suggested_route`) is `apply`.

**Only apply-routed jobs.** `/tailor` has no gate anywhere in it and runs unattended, so
evaluating a tailor-routed job would produce evidence for a decision nobody is being asked to
make. `base` and `skip` are not evaluated either.

**Skip-if-fresh:** an entry whose `eval_date` is within 7 days is skipped unless `--again` was
passed. Report the skips.

**If the set is empty**, do not fall back to evaluating something else. Post one line to Slack and
exit clean:

> Nothing routed `apply`. Promote something with `/preprocess <company>=apply`, or run `/process`
> to work the tailor-routed queue.

## Step 3: Evaluate

For each job in the set, run `.claude/commands/apply.md` **Steps 0 and 1 only**, verbatim —
including the `salary_lookup.py` benchmark when it is configured, and the gates from
`04-job-evaluation.md`.

Then **stop.**

> The gate question — *"Should I proceed with drafting the application for this role?"* — is
> **not asked here**, and no answer to it is inferred. Its answer is the effective route at the
> time `/process` runs, which the user sets by re-routing after reading these evaluations.

Run the jobs one at a time. Nothing here writes a document, compiles anything, or touches
`outbox/`.

If a posting cannot be retrieved after the full escalation in `09-web-research.md`, record the
job as unevaluated with the reason and carry on. **Do not mark it `expired`** — that transition
belongs to `/rank`, and one bad fetch is not evidence a posting is dead.

## Step 4: Persist

Split deliberately, because `job_scraper/seen_jobs.json` is committed on a public repo.

**Prose** → `job_scraper/preprocess_YYYY-MM-DD.md`, one `## <Company> - <Role>` section per job
holding the five-part evaluation, the requirement coverage, and the verdict. That path is already
gitignored by the existing `**/job_scraper/*.md` rule. **Keep it flat in `job_scraper/`** — a
subdirectory would not match that pattern, and the evaluation prose would land in a public repo.

**Compact fields** → on the entry in `seen_jobs.json`, and nothing more:

| Field | Value |
|---|---|
| `eval_score` | 0-100 from Step 1's overall fit score |
| `eval_verdict` | the recommendation band (strong / moderate / weak fit) |
| `eval_date` | today, ISO |
| `eval_file` | the `preprocess_YYYY-MM-DD.md` path |

Named `eval_*` so they never collide with `/rank`'s `rank_*` fields or the scraper's coarse `fit`.
**No prose, no posting text, no quotes from the posting** goes into this file. Leave every other
field on the entry exactly as it was, and do not change `status`.

`/process` reads `eval_file` to recover this work instead of re-running Step 1.

## Step 5: Post to Slack

Use the `/preprocess` template in `slack-output.md`:

1. **Header** to the channel — how many evaluated, skipped as fresh, unevaluated.
2. **One threaded reply per job** — roughly six lines: route and both scores, then skills,
   experience, culture, salary, verdict, and the posting link.
3. **Footer** to the channel — this is the gate. It states that re-routing is how it is answered,
   and gives both commands: `/process` to keep everything as-is, or
   `/process <company>=tailor <company>=skip` to change.

Post no posting body text and no URL taken from one.

## Step 6: Report

In the terminal: counts, the file the prose went to, the `eval_*` fields written, whether Slack
was posted to, and the next command.

## Important Rules

1. **Never ask `/apply`'s gate question, and never infer its answer.** The route is the answer,
   and the user sets it.
2. **Never write a document.** No CV, no cover letter, no packet, no compile. That is `/process`.
3. **Never write `suggested_route`** — that is `/rank`'s field. Write `route` only from a literal
   token the user typed, always with `route_set_by`.
4. **Never change `status`.** An evaluated job stays `ranked` until `/process` marks it
   `processed`.
5. **Never write `job_search_tracker.csv`.** `/outcome` is its sole writer.
6. **Evaluation prose never enters `seen_jobs.json`** and never reaches Slack beyond the compact
   summary lines. That file is public; the prose file is not.
7. **A Slack failure is not a run failure.** The evaluations are the work.
