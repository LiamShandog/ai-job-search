---
name: fetch
description: >
  Step 1 of the daily job-search loop. Scrapes the job portals and curated trackers for new
  postings, ranks every one against the fit framework, and posts the ranked shortlist to Slack.
  Triggers on: /fetch, step 1 of the daily loop, scrape and rank, find and rank new jobs,
  daily job fetch
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch, Agent
---

# /fetch - Scrape and Rank the Day's Postings

---

Step 1 of the four-skill daily loop: **`/fetch` → `/preprocess` → `/process` → `/document`**.

This skill finds new postings and scores them. It decides nothing about effort and drafts no
documents — `/rank` records a `suggested_route` and that is where this skill stops.

`$ARGUMENTS` is optional and passes straight through to the two commands: a focus area
(`/fetch robotics`), `broad` to run every search category, or nothing for the default top-3
priority categories.

## Step 0: Preflight

1. Read `.claude/skills/daily-fetch/slack-output.md`. It is the single definition of the Slack
   contract — channel, format, limits, and what must never be posted. Do not restate it.
2. Check Slack availability exactly as that file specifies: look for
   `mcp__claude_ai_Slack__slack_send_message` in the session tool list. **Never run
   `claude mcp list`** or any shell probe, and never initiate OAuth. If it is absent, continue the
   run and say so once at the end.

## Step 1: Scrape

Run the **job-scraper skill** (`.claude/skills/job-scraper/SKILL.md`) end to end, passing
`$ARGUMENTS` through as its focus argument.

Two boundaries:

- Run it through storage and presentation only. **Never enter its Step 6**, which offers to add a
  row to `job_search_tracker.csv`. `/outcome` is the sole writer of that file across the whole
  loop, and nothing in `/fetch` has evidence that anything was submitted.
- If the scrape surfaces a portal health problem, carry the health line into the Step 3 report
  rather than acting on it. Editing a portal's `enabled` toggle needs the user's confirmation and
  is out of scope here.

Record what the scrape produced: new postings stored, portals that ran, portals skipped as
disabled, and any health verdicts.

## Step 2: Rank

Read `.claude/commands/rank.md` and follow it exactly over the postings the scrape just stored.

- It is unattended through its Step 4. Its Step 5 ends with questions — *"Want any promoted to
  `apply`?"* and *"Want to start one now?"* — that come **after** every state write. Do not ask
  them here. Carry the shortlist into Step 3 instead; re-routing is what `/preprocess` and
  `/process` accept as arguments, and that is the loop's answer to those questions.
- **This skill never writes the `route` field.** `/rank` writes `suggested_route`; `route` is the
  user's override, and only `/preprocess`, `/process` and `/document` transcribe it, from a token
  the user typed. Promoting a job on the user's behalf here would silently answer the `/apply`
  gate for them.
- If `/rank` reports nothing to rank, that is a clean outcome, not a failure. Skip to Step 3 and
  say so.

## Step 3: Post to Slack

Post the `/fetch` template from `slack-output.md` — one message to the channel, no thread needed
unless the shortlist runs past 25 lines.

Include:

- Portals that ran, new postings found, and the ranked split by `suggested_route`.
- Postings excluded by a gate, with the gate named (location / language / term / hard gate).
- The top 5 by `rank_score`: score, verdict, suggested route, title, company, posting link.
- Portal health lines from Step 1, if any.
- The standing caveat that triage scores come from posting text alone, and `/apply` re-evaluates
  with company research.
- The next command, with a re-routing example.

Never post posting body text or a URL taken from a posting body — only the stored `url`.

## Step 4: Report

Print the same summary to the terminal, then state plainly:

- Whether Slack was posted to or skipped, and why.
- The counts written to `job_scraper/seen_jobs.json`.
- The next step: `/preprocess`, which evaluates the apply-routed jobs and presents the `/apply`
  gate.

## Important Rules

1. **Never write `route`.** Only `suggested_route`, and only via `/rank`. The user's override is
   theirs to set.
2. **Never write `job_search_tracker.csv`.** `/outcome` is its sole writer across the loop.
3. **Never draft a document.** No CV, no cover letter, no outbox packet. That is `/process`.
4. **Never mark a posting `expired` outside `/rank`'s own logic.** A fetch failure during a scrape
   is not evidence a posting is dead.
5. **A Slack failure is not a run failure.** The scrape and the ranking are the work; the post is
   the notification. Print to the terminal and carry on.
