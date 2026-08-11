# /notion-sync - Push Ranked Jobs and Applications to a Notion Database

You are publishing a **read-only view** of the job search into the user's Notion workspace: one database row per job, with a detailed page per shortlisted match. The repo files stay the system of record - `job_scraper/seen_jobs.json` owns scraped/ranked jobs and `job_search_tracker.csv` owns applications. Notion is a disposable presentation layer on top of them; nothing ever syncs back.

This command requires the **Notion MCP server** (OAuth). It reads state, upserts pages, and stops - it never ranks, applies, or edits repo files. Notion is the in-tree reference binding; the sync contract itself is tool-agnostic (see "Adapting to Another Tool" at the end - only the two sections marked *(Notion binding)* are tool-specific).

## Lane: `/html-report` vs `/notion-sync`

Both present the same tracker data; they own different moments. `/html-report` is the **deep-review lane**: a self-contained offline dashboard with charts and a filterable table, regenerated at your desk. `/notion-sync` is the **glanceable lane**: the current state of the pipeline, reachable anywhere Notion runs (desktop, web, phone). They compose rather than compete - after `/outcome` records a result, re-run either or both to refresh the views.

Follow these steps **in order**.

---

## Step 0: Parse Input

`$ARGUMENTS` may contain:

- Nothing → sync ranked jobs with score ≥ 60 (Good Fit and above) plus every tracked application
- `--min-score <N>` → override the score threshold
- `--all` → sync every ranked job regardless of score
- `--rebuild` → re-fetch and rewrite page bodies too (see Step 5 - normally bodies are write-once)

---

## Step 1: Preflight the Connection *(Notion binding)*

The command is **silently optional**: when the destination is not reachable, the outcome is one clear message and a clean exit - nothing else in the framework notices this command exists.

1. Check that Notion MCP tools are available in this session (tool names starting with `mcp__notion__` or similar). Determine this from the session's own tool list **only** - never by running shell commands like `claude mcp list`, which would interrupt the user with a permission prompt before the graceful exit. If the tools are not available, stop and tell the user how to connect:
   > Notion MCP isn't connected. Run `claude mcp add --transport http notion https://mcp.notion.com/mcp`, then start a **new session** (servers added mid-session are only picked up on restart), run `/mcp` there to complete the OAuth login, and re-run `/notion-sync`.
2. Verify the connection with one cheap call (e.g. a workspace search). An auth error → tell the user to re-authenticate via `/mcp` and stop. Never retry in a loop.
3. The Notion MCP server is interactively authenticated, so "connected but not authenticable right now" (expired OAuth, headless/CI context where the login flow cannot run) gets the same graceful exit as "not configured": state the reason in one line and stop. This includes the configured-but-unauthenticated state where the server exposes only its auth handshake and no data tools - **never initiate the OAuth flow from this command and never ask whether to authenticate now**; the one line points at `/mcp` and the command ends there. Authenticating is the user's move, made outside this command.

---

## Step 2: Build the Sync Set (local data only - no external calls yet)

Validate the cheap, local precondition before creating anything external. A run with nothing to sync must exit with **zero side effects** - no database created, no state file written.

1. Read `job_scraper/seen_jobs.json` and `job_search_tracker.csv` (either may be missing).
2. Select `seen_jobs.json` entries with status `ranked` **or `processed`** whose `rank_score` meets the threshold from Step 0. `--all` lifts the threshold entirely. A `processed` entry still carries the `rank_score` `/rank` gave it, so the threshold applies unchanged; an ad-hoc `processed` entry created from a pasted URL has no `rank_score` and always syncs regardless of threshold - the candidate has already invested in it, so it belongs on the board.
3. Every tracker row joins the sync set (an applied-to job always syncs, ranked or not), matched to `seen_jobs.json` entries case-insensitively on company + role where possible. Tracker rows with no `seen_jobs.json` entry sync too - build their Key as `<company>_<role>` lowercased with underscores.

   **Join tracker rows on the posting URL first**, falling back to company + role only when no URL matches. Name matching alone is unsafe: a tracker role of "Forward Deployed Software Engineer, Internship - Commercial" contains "Software Engineer Intern" as a substring, so a naive company+title match binds the application to the wrong requisition at the same employer, and the mis-joined row then reports an application that was never made.

4. **A previously synced job whose status has since moved off `ranked` still syncs** - `skipped`, `expired`, `not_recommended`, `applied`. (`processed` is already in the selected set via rule 2 and needs no rescue.) Selecting only `ranked` entries would strand those rows at whatever they said when they were last seen, which is how a board ends up showing `ranked` for a posting the user consciously dropped weeks ago. This is also what makes Step 4's "set Status to `expired` rather than deleting" reachable at all. Such entries update **properties only** and never get a body rewrite. Jobs that have *never* been synced and are not `ranked` stay out - this rule keeps existing rows honest, it does not widen the set.
5. **Status precedence:** the tracker wins. A job that is `ranked` in `seen_jobs.json` but `interview` in the tracker syncs as `interview`. The same applies to `processed`: once a tracker row exists the application has been submitted, so a `processed` entry with a tracker row syncs as `applied` (or whatever the row says) - `processed` only ever reaches the board for a job with **no** tracker row, which is exactly what makes it readable as "documents ready, not sent". Jobs only in `seen_jobs.json` keep their stored status.
6. **If the sync set is empty** (no ranked entries meet the threshold and there are no tracker rows), say "Nothing to sync - run `/scrape` and `/rank` first" (or, when jobs exist but all score below the threshold, say so and suggest `--min-score`/`--all`) and **stop**.
7. State the counts before touching the destination: how many rows will be created or checked, and the threshold in effect.

---

## Step 3: Load Sync State and Locate the Database *(Notion binding)*

1. Read `job_scraper/notion_sync.json`. Structure:
   ```json
   { "database_id": "...", "database_url": "...", "last_sync": "YYYY-MM-DD" }
   ```
2. If it exists, verify the database id still resolves in Notion. If the database was deleted, treat this as a first run.
3. **First run:** search the workspace for a database named "Job Search Pipeline". If none exists, ask the user where to create it (top-level page or an existing page they name), then create it with exactly these properties:

   | Property | Type | Values / notes |
   |----------|------|----------------|
   | Name | title | `<Role> — <Company>` |
   | Company | rich text | |
   | Score | number | 0-100 from `rank_score` |
   | Verdict | select | Strong Fit / Good Fit / Moderate Fit / Weak Fit / Poor Fit |
   | Status | select | ranked / processed / applied / interview / offer / hired / rejected / no response / withdrawn / expired / skipped. `processed` means the documents are prepared and verified but not submitted - the actionable bucket on this board |
   | Route | select | apply / tailor / base / skip - the effort routing from `/rank`. Write the **effective** route: the entry's `route` (the user's override) when set, otherwise `suggested_route`. Leave empty for entries that have neither, and for applied rows, where the routing question is settled. **Keep it populated for `processed` rows** - the route is why the documents look the way they do, and it is still worth seeing next to a job that has not been sent |
   | Fit | select | high / medium / low (scraper quick-fit). Kept for schema continuity, but **hidden in the default view** - every synced row is ranked or applied, so it already carries a Verdict, and the scrape-time quick-fit is both coarser and systematically more pessimistic. Do not un-hide it |
   | Deadline | date | omit when unknown |
   | First seen | date | |
   | Ranked | date | `rank_date` from `seen_jobs.json`; omit when not ranked |
   | Applied on | date | tracker `date` column; omit when not in the tracker |
   | Channel | select | tracker `channel` column (e.g. portal / email / referral); options grow as values appear |
   | CV file | rich text | tracker `cv_file` column, falling back to the `seen_jobs.json` entry's `cv_file` for a `processed` row with no tracker row - the filename only, never document content |
   | Cover letter | rich text | tracker `cover_letter_file` column, same fallback - the filename only, never document content |
   | URL | url | posting URL |
   | Key | rich text | the job's key in `seen_jobs.json` - dedup anchor, never edited by hand |

   The tracker-sourced properties (Applied on, Channel) stay empty for jobs that have no tracker row - they fill in once `/outcome` records the application. CV file and Cover letter fill in earlier, as soon as `/apply` or `/tailor` marks the job `processed`. Only filenames ever sync; document contents stay local.

4. **Existing database with missing properties:** if the located database predates a schema addition (a property from the table above does not exist), add the missing properties to the database before upserting. Never remove or retype existing properties. The same applies to a **select option** that does not yet exist (`processed` or `skipped` on Status, or any Route value): add the option, never retype the property or drop existing options.
5. **Set the default view's columns** to `Company, Name, Route, Verdict, Status, URL`, in that order, and leave every other property hidden. This is the glanceable set - what the user reads on a phone. Score, Deadline, the tracker fields and `Key` all stay on the row and are still synced; they are simply not shown by default. Note that Notion pins the **title** property as the first rendered column in a table view regardless of the configured order, so `Name` may appear ahead of `Company` in the UI even when the view is configured as above.
6. **Hide `Fit` in the default view** whenever the property exists and is visible. Every synced row is ranked or applied and therefore already carries a Verdict, which is computed from the fetched posting against the full framework; the scrape-time quick-fit is a snippet-level guess and disagrees with the Verdict far more often than it agrees. Leaving both visible invites the weaker number to be read as a second opinion. Hide, do not delete - `Fit` still means something in `seen_jobs.json` for unranked entries, which never reach this board.
7. Write `job_scraper/notion_sync.json` with the database id and URL. This file is personal state and is gitignored - never commit it.

---

## Step 4: Upsert Database Rows

For each job in the sync set:

1. Query the database for a page whose `Key` equals the job's key.
2. **No match** → create the page with all properties from the Step 3 table, then write its body (Step 5).
3. **Match** → update **properties only**: Status, Route, Score, Verdict, Deadline, Ranked, Applied on, Channel, CV file, Cover letter. Properties are the always-current surface (bodies are write-once), so tracker updates recorded by `/outcome` and route changes made after `/rank` reach the destination exclusively through them. Do not touch the page body - the user may have added their own notes there, and clobbering them breaks trust in the whole view. (`--rebuild` is the sole exception.)
4. Never delete or archive pages, even for jobs that turned `expired` - set Status to `expired` instead. Rows the user added to the database by hand (no `Key` value) are invisible to this command.

Batch politely: if the MCP server rate-limits, back off and continue; report any page that failed rather than retrying indefinitely.

---

## Step 5: Write the Detail Page (new pages only)

The page body is what makes a row worth clicking. Build it **only from stored data and actually fetched content**:

1. **Fit summary** - a short section from `seen_jobs.json` fields: score, verdict, quick-fit level, first-seen and ranked dates. If the entry is `processed`, add a line naming `processed_date`, which command prepared it (`processed_by`), and the documents from `cv_file`/`cover_letter_file` - filenames only. If the job is in the tracker, add the application timeline (date applied, channel, current status, dated notes from the `notes` column) and name the submitted documents from `cv_file`/`cover_letter_file` (filenames only - the documents themselves never sync).
2. **The posting** - WebFetch the job URL and write a readable digest: what the role is, key requirements, practical details (location, deadline, salary if stated). Retry a 403 with browser headers per `.claude/skills/job-application-assistant/09-web-research.md` first. If the fetch still fails or redirects to a listing page, write "Posting no longer available (checked YYYY-MM-DD)" - **never reconstruct a posting from memory**.
3. **Links** - the posting URL; if `documents/applications/<company>_<role>/` exists locally, name it as the local archive path (plain text - the destination cannot link into the filesystem).

Keep the page under ~40 blocks; this is a briefing, not a mirror of the posting.

---

## Step 6: Report

```
## Pipeline Sync - YYYY-MM-DD

Database: <database_url>
Synced <N> jobs (threshold: score ≥ <T>): <C> created, <U> updated, <S> unchanged, <F> failed.

| | Title | Company | Status | Score |
|---|-------|---------|--------|-------|
| ✚ | ... | ... | ranked | 78 |
| ↻ | ... | ... | interview | 71 |
```

List failures with their error and the suggestion to re-run - the upsert is idempotent, so a re-run only touches what failed. Update `last_sync` in the sync-state file.

Remind the user once (first run only): the repo files remain the source of truth - edits made in the destination never flow back, and `/outcome` is still how application results get recorded.

---

## Important Rules

1. **One-way, always.** Destination content never flows back into `seen_jobs.json`, the tracker, or any repo file. This command reads repo state and writes the destination - both repo files are read-only to it, and the gitignored sync-state file is its **only** local write.
2. **Idempotent upsert on `Key`.** Re-running creates nothing twice; matching is on the stored key, never on fuzzy title comparison.
3. **Page bodies are write-once.** Property updates keep rows current; bodies belong to the user after creation. Only `--rebuild` may rewrite them, and it says so before doing it.
4. **Never fabricate.** A dead posting URL gets an explicit "unavailable" note, not a reconstruction. Every page claim traces to stored state or fetched content.
5. **Job data only.** The candidate profile, behavioral notes, and evaluation framework never sync - this is a pipeline view, not a profile export.
6. **Documents never leave the machine.** CVs and cover letters sync as **filenames only** - never upload, attach, or embed the documents themselves, nor HTML/text renditions of their content, into the destination. The local repo and `documents/applications/` archive are the only home for application documents; the row's page names them so the user knows what to open locally.

---

## Adapting to Another Tool (forks)

The sync contract is tool-agnostic; only the two sections marked *(Notion binding)* are tool-specific. A fork targeting a different destination (Airtable, Google Sheets, Linear, ...) keeps Steps 0, 2, 4, 5, and 6 and every Important Rule unchanged - build the same sync set, upsert on the same `Key`, keep bodies write-once and documents local - and swaps only:

- **Step 1** (connection preflight) for the target tool's MCP server or access check, keeping the silently-optional bar: not configured or not authenticable both end in one message and a clean exit
- **Step 3** (locate/create the database) for the equivalent container in the target tool, using the same property table and a renamed sync-state file

Like the portal skills, tool bindings beyond this Notion reference live in forks, where their maintainers can test them against a live workspace.
