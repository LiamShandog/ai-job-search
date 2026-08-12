# The Daily Loop

Four skills that turn a pile of per-job commands into a day's work:

```
/fetch  ──▶  /preprocess  ──▶  /process  ──▶  /document
 find         decide           build          record
```

Each posts to Slack `#job-applications`, so the loop can be driven from a phone. All four run
**locally** — see [Why local](#why-local) for the reason that is not incidental.

---

## Why this exists

Every command in this repo works on one job at a time and expects a human at the keyboard. That
is correct for `/apply`, and it is why a day's queue could never be run as a sequence.

The specific blocker was structural. `/apply` Step 1 ends in the only blocking gate in the system:

> "Should I proceed with drafting the application for this role?"
> **If the user says no, stop here.**

Any wrapper batching the queue would stop at every apply-routed job. Removing the gate was the
obvious fix and the wrong one — the gate is asking something no automated pass can answer.
`CLAUDE.md` says it plainly:

> **Routing cannot judge want-level.**

`/rank` can tell you a job scores 78 and routes to `apply`. It cannot tell you whether you would
be disappointed not to hear back. That judgement is the entire basis of the apply-vs-tailor split.

**The fix is to split the gate across two skills.** `/preprocess` runs the evaluation *behind* the
gate and then stops without asking it. You read the evaluations in Slack and answer by re-routing.
The effective `route` when `/process` runs **is** the answer — so `/process` executes the whole
queue with zero interactive pauses, and no judgement was skipped.

---

## The four steps

### 1. `/fetch` — find

Runs the job-scraper skill, then `/rank`, then posts the ranked shortlist.

| | |
|---|---|
| **Arguments** | optional focus area (`/fetch robotics`) or `broad` |
| **Writes** | `job_scraper/seen_jobs.json` — new postings, then `suggested_route` on each |
| **Never** | writes `route`, writes the tracker, drafts anything |

It records `/rank`'s opinion and stops. It never promotes a job to `apply` on your behalf, because
doing so would silently answer the gate that step 2 exists to present.

### 2. `/preprocess` — decide

Runs `/apply` Steps 0–1 — the full five-part fit evaluation, including `salary_lookup.py` — over
the apply-routed jobs, then stops before the gate.

| | |
|---|---|
| **Arguments** | `selector=route` pairs, `--again` |
| **Evaluates** | `status == "ranked"` **and** effective route `apply` |
| **Writes** | prose → `job_scraper/preprocess_YYYY-MM-DD.md` (gitignored)<br>`eval_score`, `eval_verdict`, `eval_date`, `eval_file` → the entry |
| **Never** | asks the gate, infers its answer, drafts anything, changes `status` |

Only apply-routed jobs are evaluated. `/tailor` has no gate anywhere in it, so evaluating a
tailor-routed job would produce evidence for a decision nobody is being asked to make.

**The persistence split is deliberate.** `seen_jobs.json` is committed on a public repo, so the
evaluation prose goes to a gitignored markdown file and only four compact fields reach the entry.
The prose file is kept flat in `job_scraper/` because the ignore rule is `**/job_scraper/*.md` —
a subdirectory would not match it, and the evaluations would land in public.

Step 3 reads `eval_file` rather than re-running Step 1.

### 3. `/process` — build

Works the queue into `outbox/` packets. The long one: a full queue is ~90 jobs and runs for hours.

| | |
|---|---|
| **Arguments** | `selector=route` pairs, `--dry-run`, `--restart` |
| **Phase A** | effective route `apply` → `/apply` from Step 1.5 |
| **Phase B** | effective route `tailor` → `/tailor` in full |
| **Writes** | CVs, cover letters, `outbox/` packets, `processed` markers, the checkpoint |
| **Never** | writes the tracker, marks anything `expired`, builds on failure |

Phase A runs first — it is the smaller, higher-judgement set with the freshest evidence, so a
crash three hours in has already banked the work that mattered most. `base` (send `main_base.tex`
unchanged) and `skip` (gate failed) are never queued.

**Serial, one job per sub-agent.** This is a file-ownership consequence, not a speed preference.
Running `/apply` and `/tailor` concurrently would break three things at once:

- `outbox/START HERE.txt` is renumbered by every packet
- the packet-naming disambiguator reads live directory state to decide whether an employer already
  has a folder
- `seen_jobs.json` is a whole-file rewrite

For the same reason the orchestrator **re-reads `seen_jobs.json` before every job**. A copy cached
at the start and written back at the end would erase every `processed` marker earned during the
run.

**Resume is filesystem-first.** The checkpoint (`job_scraper/process_state.json`, gitignored) is
written after every job, but a job counts as done if the checkpoint says so **or** its entry reads
`processed` *and* a matching folder exists under `outbox/`. `outbox_dir` is deliberately not
trusted — the field postdates most existing entries. So deleting the checkpoint costs nothing.

**On failure: no `processed` marker, no packet.** A folder holding no PDF is worse than no folder,
because `START HERE.txt` would advertise it as ready to send. Compile and verification failures
cap at 3 attempts. One job failing never aborts the batch.

### 4. `/document` — record

Records the outcomes you name, then syncs Notion.

| | |
|---|---|
| **Arguments** | `selector=status` pairs, optionally `@YYYY-MM-DD` and `:stage` |
| **Runs** | `/outcome` per named job, then `/notion-sync` once |
| **Never** | writes the tracker itself, infers a submission, drafts or posts follow-ups |

> **A packet in `outbox/` is not a submission.**

Nothing is inferred — not from a packet existing, not from `processed` status, not from a route.
Your arguments are the only evidence anything was sent. With no arguments it runs the sync half
only. An invented tracker row is authoritative to every reader downstream, which is why this is a
prohibition rather than a preference.

**It is barred from `/outcome`'s follow-up branch.** That command's Rule 6 says follow-up drafts
"must not be wired to tools that do [send]" — and this skill holds `slack_send_message`. Follow-ups
stay a manual `/outcome followup` at the terminal, where you read the draft before anything leaves
the machine.

---

## Arguments

Routes and outcomes are passed inline as `selector=value` pairs:

```
/preprocess palantir=apply "chicago trading company"=skip
/process    netic=apply tiktok:ads-targeting=tailor
/document   sentry=applied dv-trading=applied@2026-08-10 netic=interview@2026-08-09:phone_screen
```

| Selector | Meaning |
|---|---|
| `palantir` | company name; `-` and `_` are read as spaces |
| `palantir:defense` | company, narrowed by a role keyword |
| `https://…` | one specific posting — the unambiguous escape hatch |
| `tiktok*` | **every** matching posting from that employer |

Routes are `apply` / `tailor` / `base` / `skip`. Outcomes are `/outcome`'s canonical statuses.
The two sets are disjoint on purpose (`apply` vs `applied`), so passing one where the other belongs
gets a precise error instead of a silent re-route.

**An ambiguous selector is a hard error that writes nothing.** Matching restricts by *status*
only, never by route — so a selector sees every ranked posting from that employer, not just the
queued ones. `tiktok` currently resolves to 51 postings, of which 23 are in the work queue. A
silent closest-match, or a silent match-all, is expensive in either direction. The `*` qualifier
exists so the bulk operation is available but has to be typed deliberately.

The full grammar lives in `.claude/skills/daily-preprocess/route-args.md` and is read by all three
skills rather than restated in each.

---

## Who writes what

The loop adds no new ownership. Every write still belongs to the command that always owned it.

| File | Sole writer | The loop's skills |
|---|---|---|
| `suggested_route` | `/rank` | never write it |
| `route`, `route_set_by` | the user | transcribe it, only from a typed token |
| `processed` marker, `outbox/` | `/apply`, `/tailor` | invoke them, never write it directly |
| `job_search_tracker.csv` | `/outcome` | never write it |
| `status: applied` | `/outcome` | never set it |
| `status: expired` | `/rank` | a fetch failure is a job failure, never `expired` |
| `notion_sync.json` | `/notion-sync` | invoke it |

The two route rules are mirror images: `/rank` never writes `route`, and these skills never write
`suggested_route`. Together they keep the route a stable dialogue between the ranker's opinion and
your decision.

---

## Slack

One contract, `.claude/skills/daily-fetch/slack-output.md`, read by all four skills.

- Channel `#job-applications` (`C0BPJHCTS94`).
- **Standard Markdown** — bold, links, lists, code blocks and tables all render. Verified against
  the live channel.
- 5,000 characters per message; chunk at 3,500, ≤25 job lines per message.
- Header to the channel, detail as threaded replies, footer back to the channel.
- **There is no file-upload tool.** PDFs never reach Slack; messages carry paths and links.
- Never post document contents, posting body text, or a URL taken from a posting body.

**A missing Slack connector never fails a run.** The skills print to the terminal and carry on.
This differs from `/notion-sync`, which exits cleanly when its MCP is absent — there the
destination *is* the work, here the local work is the point and Slack is only the notification.

---

## Why local

This was first built as a scheduled cloud routine. It failed for two environmental reasons that
cannot be fixed from inside the repo, and the failure is worth recording so nobody rebuilds it:

1. **The cloud sandbox blocks egress to every job host** — LinkedIn, Greenhouse, Lever, Ashby,
   Workday, Amazon, Google all returned `EGRESS_BLOCKED`. `/rank` needs posting text to score, and
   there is none. The run could list what the community trackers said and nothing more.
2. **Its GitHub credential is read-only.** `git-upload-pack` returned 200, `git-receive-pack`
   returned 403. Scraped state could never be pushed back, so every run would start blind.

Running locally removes both: the portal CLIs work, `bun` is present, nothing is blocked, and
pushes are yours.

---

## A day

```
/fetch                                  # scrape + rank, read the shortlist in Slack
/preprocess                             # evaluations for the apply-routed jobs
/process palantir=tailor etched=skip    # re-route from what you read, then build everything
                                        # ... submit from outbox/ ...
/document palantir=applied sentry=applied@2026-08-10
```

`/process --dry-run` prints the queue without drafting anything — worth running first when the
queue is large.

---

## Reference

| Thing | Where |
|---|---|
| Skill specs | `.claude/skills/daily-{fetch,preprocess,process,document}/SKILL.md` |
| Slack contract | `.claude/skills/daily-fetch/slack-output.md` |
| Argument grammar | `.claude/skills/daily-preprocess/route-args.md` |
| Tests | `tests/test_{fetch,preprocess,process,document}_skill.py`, `tests/test_daily_loop_contract.py` |
| Status lifecycle | `.claude/skills/job-scraper/SKILL.md` |
| Effort routing | `CLAUDE.md` |

The specs *are* the implementation — these are markdown, not code, so the tests pin the invariants
that would otherwise break silently.
