---
name: document
description: >
  Step 4 of the daily job-search loop. Records the outcome of applications the user names via
  /outcome, syncs the pipeline to Notion, and posts a completion summary to Slack. Triggers on:
  /document, step 4 of the daily loop, record the applications I sent, log outcomes and sync,
  close out the daily loop
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch, Agent
---

# /document - Record Outcomes and Sync

---

Step 4 of the four-skill daily loop: **`/fetch` → `/preprocess` → `/process` → `/document`**.

`$ARGUMENTS` is optional: `selector=status` pairs, where the status comes from `/outcome`'s
canonical vocabulary and may carry `@YYYY-MM-DD` and `:stage`.

```
/document palantir=applied sentry=applied@2026-08-10 netic=interview@2026-08-09:phone_screen
```

## The rule this skill exists to hold

> **A packet in `outbox/` is not a submission.**

Nothing here infers, proposes or defaults an outcome — not from a packet existing, not from
`processed` status, not from a route, not from how long something has been sitting. The user's
arguments are the only evidence that anything was sent, and they are the only source of the
outcome facts `/outcome` Step 2 would otherwise ask for interactively.

This is a restatement of the framework's own boundary: `processed` means the documents exist,
`applied` means it was submitted, and only the user knows which happened.

With no `selector=status` pairs supplied, run the `/notion-sync` half only (Step 3) and say so.

## Step 0: Preflight

1. Read `.claude/skills/daily-fetch/slack-output.md` and
   `.claude/skills/daily-preprocess/route-args.md`. Single definitions; do not restate them.
2. Check Slack from the session tool list only. **Never run `claude mcp list`**, never initiate
   OAuth. Absent → continue and say so once.

## Step 1: Resolve the named applications

Parse `$ARGUMENTS` per `route-args.md`, using its **outcome-status** value set. Reject a route
value (`apply`, `tailor`, `base`, `skip`) with the message that file gives — it belongs to
`/preprocess` or `/process`.

Resolve selectors against entries at `processed`, `ranked` or `applied`. An ambiguous selector is
a hard per-token error: post the numbered disambiguation list, record nothing for that token, and
carry on with the rest. Recording an outcome against the wrong requisition is not recoverable by
re-running.

## Step 2: Record each outcome

For each resolved job, run `.claude/commands/outcome.md` with the company and role, supplying the
user's stated outcome as the answer to its Step 2 classification.

- **The argument is the whole answer.** `palantir=applied@2026-08-10` says submitted, on that
  date. Nothing else is invented — no employer feedback, no interview impressions, no reason for
  a rejection.
- `outcome.md`'s Notes gets exactly one dated line naming its source, e.g.
  `2026-08-11: Submitted 2026-08-10. Recorded by /document from the user's instruction.`
- **Tick a stage only when the user typed one** (`:phone_screen`). Never infer a stage from a
  status.
- Let `/outcome` do its own work: its Step 3 archive, its Step 4 tracker write, and its Step 4b
  move of the `seen_jobs.json` entry to `applied`. **This skill never writes
  `job_search_tracker.csv` itself** — `/outcome` is its sole writer and the sole mover to
  `applied`, across the whole loop.
- Where `/outcome` Step 1 finds no tracker row and would normally collect the details
  interactively, fill them from what is already on record — company, role and `source` from the
  `seen_jobs.json` entry, `channel` from `apply_host`, the packet's `APPLY.txt` if one exists. If
  a required field genuinely is not on record, **skip that job and report it**. Never prompt
  mid-batch, and never guess.

### Two prohibitions

1. **Never enter `/outcome` Step 2b, the follow-up branch, and never post follow-up text to
   Slack.** `/outcome` Rule 6 says follow-up drafts are draft-only and "must not be wired to tools
   that do [send]" — and this skill holds `slack_send_message`, which is exactly such a tool.
   Follow-ups stay a manual `/outcome followup` at the terminal, where the user reads the draft
   before anything leaves the machine.
2. **Never post a thank-you note draft to Slack.** `/outcome` Step 3 offers one when a stage is
   ticked; surface that offer in the terminal only.

## Step 3: Sync to Notion

Run `.claude/commands/notion-sync.md` once, after every outcome write has finished, so the board
reflects the new statuses rather than the ones from before this run.

Keep its Step 1 preflight intact: if the Notion MCP is unavailable, it says so in one line and
exits: that is a clean outcome here, not a failure. The outcomes are already recorded; the sync is
a mirror.

## Step 4: Post to Slack

Use the `/document` template in `slack-output.md` — a single message:

```
**Documentation complete — 2026-08-11**
Outcomes recorded (3): Palantir → applied (2026-08-10) · Sentry → applied · DV Trading → rejected
Tracker: 3 rows updated · seen_jobs: 2 → applied, 1 no matching entry
Notion: 41 rows synced (3 created, 38 updated) — [board](https://…)
```

Report skipped and ambiguous tokens on their own line. Post no note drafts, no employer
correspondence, and no document contents.

## Step 5: Report

Terminal summary: outcomes recorded, tracker rows written, `seen_jobs.json` entries moved, the
Notion result, anything skipped with its reason, and the next command — `/fetch` to start
tomorrow's loop.

## Important Rules

1. **A packet is not a submission.** Never infer an outcome from `outbox/`, from `processed`, or
   from a route.
2. **`/outcome` is the sole tracker writer.** This skill never writes `job_search_tracker.csv`
   and never moves an entry to `applied` by hand.
3. **Never enter the follow-up branch, and never post note drafts to Slack.** Drafts stay on the
   machine.
4. **Never invent outcome detail.** Status, date and stage come from the user's arguments;
   everything else comes from what is already on record.
5. **An ambiguous selector records nothing.** A misattributed outcome is not fixable by re-running.
6. **A missing Notion or Slack connector is not a run failure.** The outcome records are the work.
