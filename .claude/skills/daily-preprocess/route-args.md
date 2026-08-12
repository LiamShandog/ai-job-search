# Route and outcome argument grammar

The single definition of the inline-argument grammar used by `/preprocess`, `/process` and
`/document`, and of the contract for writing `route` / `route_set_by` into
`job_scraper/seen_jobs.json`. All three skills read this file. Do not restate it in a `SKILL.md`.

Drift in the ambiguity rule below is the expensive kind: `tiktok` currently matches 23 queued
postings, so a silent "closest match" or a silent "all of them" costs 23 unwanted `/apply` runs.

---

## Shape

```
/preprocess palantir=apply "chicago trading company"=skip tiktok:ads-targeting=apply
/process    netic=apply tiktok*=skip
/document   palantir=applied sentry=applied@2026-08-10 dv-trading=rejected
```

Whitespace-separated `<selector>=<value>` pairs. Quote a selector containing spaces. In an
unquoted selector, `-` and `_` are treated as spaces for matching, so `dv-trading` matches
`DV Trading`.

## Selectors

| Form | Meaning |
|---|---|
| `palantir` | Company string |
| `"jane street"` | Company string containing spaces |
| `palantir:defense` | Company, narrowed by a role keyword matched case-insensitively as a substring of `title` |
| `https://…` or an exact `seen_jobs.json` key | One specific entry. The unambiguous escape hatch |
| `tiktok*` | **Every** matching posting from that employer. Bulk, and deliberately explicit |

## Values

**`/preprocess` and `/process`** take a route: `apply` | `tailor` | `base` | `skip`.

**`/document`** takes a tracker status from `/outcome`'s canonical vocabulary:
`drafted` | `applied` | `interview` | `offer` | `hired` | `rejected` | `no_response` |
`offer_declined` | `withdrawn`, optionally suffixed:

- `@YYYY-MM-DD` — the date the thing happened (submission date, interview date).
- `:stage` — the stage to tick, e.g. `netic=interview@2026-08-09:phone_screen`.

**The two sets are disjoint on purpose** (`apply` the route vs `applied` the status). Each skill
rejects the other's values with a precise message rather than a generic parse error:

> `applied` is an outcome status, not a route — did you mean `/document`?

That check catches a real typo, in the direction that would otherwise silently re-route a job.

## Matching algorithm

Identical in all three skills.

1. If the selector contains `://` or is an exact key in `seen["…"]` → that single entry. Done.
2. Otherwise casefold and strip both sides, then compare against the entry's `company`:
   exact equality first; only if that yields **zero** candidates, retry with `startswith`, then
   with substring. Never match against `title` unless a `:role-keyword` was supplied.
3. Restrict candidates by status:
   - `/preprocess`, `/process`: `status == "ranked"` only. An entry already `processed` or
     `applied` cannot be re-routed — report it and skip. This mirrors `/rank` Step 4's
     never-move-backwards rule.
   - `/document`: `processed`, `ranked` or `applied`.
4. **Exactly one candidate** → apply the write.
5. **Zero candidates** → write nothing for that token; collect it into an "unmatched" list reported
   at the end and in Slack.
6. **More than one candidate** → **hard error for that token only.** Print and post a numbered
   disambiguation list (company, title, key), write nothing for it, and carry on with the other
   tokens. The user re-issues with `company:role-keyword`, the URL, or `company*`.

Rule 6 is not caution for its own sake, and the numbers are larger than they look. Matching is
restricted by **status only** (step 3), never by route — so a selector sees every ranked posting
from that employer, not just the ones queued for work. Today:

| Selector | Ranked entries matched | Of those, in the apply/tailor queue |
|---|---|---|
| `tiktok` | 51 | 23 |
| `jane street` | 15 | 3 |
| `microsoft` | 8 | 5 |
| `drw` | 8 | 1 |

So `tiktok*=apply` would route **51** postings, not the 23 a reader thinking in queue terms would
expect. That gap is the reason the disambiguation list prints counts and the `*` qualifier has to
be typed deliberately.

## Atomicity

Parse and resolve **every** token before writing anything. A malformed pair, an unknown route, or
a value from the wrong set aborts the whole route phase with **no writes at all**.

Ambiguous and unmatched tokens are the single exception — they are skipped individually, because
they are per-token problems rather than a malformed invocation.

## Writing `route` and `route_set_by`

One write point per skill, its `Step 1: Apply route changes`. Read-modify-write of
`job_scraper/seen_jobs.json` (top level `{"seen": {key: {…}}}`); serialize with
`json.dump(..., indent=2, ensure_ascii=False)` to reproduce the existing formatting.

```json
"route": "apply",
"route_set_by": "user 2026-08-11"
```

`route_set_by` already exists in the data with exactly this shape. Keep `user` verbatim rather
than naming the skill: the route is the user's decision and the skill is only the transcription
mechanism, and anything grepping the field keeps working.

**Do not refresh the date when the route is unchanged** — it records when the decision was made,
not when it was last seen.

### Invariants

- **Never write `suggested_route`.** That field is `/rank`'s output. `/rank`'s own rule — *"Never
  write the `route` field"* — is the mirror image of this one, and the pair is what keeps the route
  a stable dialogue between the ranker's opinion and the user's decision.
- **Never write `route` from anything except a literal `selector=route` token the user typed.**
  Not from an evaluation score, not from a Slack reply, not from inference about what they
  probably meant.
- **Never change `status` as part of a route write.**
- **Never drop or reorder any other field** on the entry — `rank_score`, `strengths`, `gaps`,
  `processed_date`, `cv_file`, `outbox_dir` and the rest all survive untouched.
- **Re-read the file from disk before every job** in a batch. `/apply` and `/tailor` Step 5.5
  rewrite `seen_jobs.json` whole; a copy cached at the start and written back at the end would
  silently erase the `processed` markers of everything already completed.

## Reporting

Every skill using this grammar reports, in the terminal and in its Slack header:

```
Routes applied: 3 (palantir → apply, optiver → skip, roblox → tailor)
Unmatched: 1 (etched — no ranked entry)
Ambiguous: 1 (tiktok — 23 matches, use tiktok:<role keyword> or tiktok*)
```

A run where every token was ambiguous or unmatched still proceeds to its main work with the routes
unchanged; it does not abort.
