# /html-report - Generate Application Tracker Dashboard

Generate a self-contained HTML dashboard from `job_search_tracker.csv`, the application archives under `documents/applications/`, and the prepared-but-unsubmitted jobs in `job_scraper/seen_jobs.json`. The output is a single `.html` file — no server, no dependencies — that can be opened directly in a browser.

## Step 0: Parse Arguments

- No argument → output to `reports/application-dashboard.html`
- A path argument (e.g. `/html-report ~/Desktop/report.html`) → use that path
- `--open` flag → after writing, tell the user to open the file (cannot open a browser directly)

Create `reports/` if it does not exist.

---

## Step 1: Collect Data

Read in parallel:

1. **`job_search_tracker.csv`** — the primary source. Parse every row into a record with fields:
   `date`, `company`, `sector`, `role`, `role_type`, `channel`, `status`, `contact_person`, `fit_rating`, `notes`, `cv_file`, `cover_letter_file`, `source`

2. **`documents/applications/*/outcome.md`** — for each resolved application, read the outcome file to get the exact interview stages reached (the checkboxes) and any notes. Merge this into the matching tracker row by company+role fuzzy match (lowercase, ignore punctuation). If an archive exists for a row but there is no match, attach it as extra context anyway.

3. **`job_scraper/seen_jobs.json`** — take entries with `"status": "processed"`: documents prepared and verified by `/apply` or `/tailor`, not yet submitted. Read `title`, `company`, `url`, `processed_date`, `processed_by`, `cv_file`, `cover_letter_file`, and `rank_score` where present. The file may be missing (no `/scrape` has run) — carry on with the tracker alone.

   **Join these against the tracker rows before counting anything.** Match on the posting URL first (the entry's `url` against the tracker's `source`), falling back to company + role case-insensitively only when no URL matches — the same rule `/outcome` Step 4b and `/notion-sync` Step 2 use, and for the same reason: a naive company+title match binds the record to the wrong requisition at an employer running several similar postings. **A job present in both is a tracker row and is not Prepared** — it was submitted, and the tracker is authoritative. Each job appears exactly once in the report.

Status normalisation — map values to six canonical buckets before computing stats:
- `processed` (from `seen_jobs.json`, no tracker row) → **Prepared** (documents ready, not sent)
- `applied` → **Active** (resume submitted, no further signal)
- `interview` → **Interview**
- `offer` → **Offer**
- `hired` → **Hired**
- `rejected` / `no_response` / `no response` / `offer_declined` / `interview_only` / `withdrawn` → **Rejected/Closed**

`applied` in `seen_jobs.json` is never read here — that job has a tracker row, and the tracker row is what the report renders.

---

## Step 2: Compute Summary Stats

**Prepared is not an application.** Nothing was submitted, so it is excluded from every rate below and from the total. It is reported as its own count — a to-do list, not a result. Mixing it into the total would silently deflate the interview rate every time a batch of documents is prepared.

From the normalised data compute:

- **Total applications** — every bucket except Prepared
- **Prepared** — its own count, reported separately
- **By status bucket:** count per bucket, Prepared included
- **By sector:** count per unique sector value (applications only — Prepared rows have no sector)
- **By channel:** online vs referral vs other (applications only)
- **By year/season:** group by the `date` field (which may be a year like `2025` or a full date)
- **Funnel rates:** what % progressed past resume screen (reached Interview or beyond). The funnel measures what happens *after* submission, so Prepared sits ahead of it and is never a funnel stage
- **Rejection rate:** Rejected/Closed ÷ Total with a resolved status (exclude Active and Prepared)

---

## Step 3: Generate the HTML

Write a single self-contained HTML file. All CSS is inline in a `<style>` block. All JS is inline in a `<script>` block. Draw the doughnut and bar charts as hand-generated inline SVG — no Chart.js, no CDN, no external dependencies of any kind. The report must render fully offline on every open.

**Escaping (required):** HTML-escape every CSV/outcome-file value (`&` `<` `>` `"` `'`) before interpolating it into the page — this includes table cells, `title` attributes on truncated notes, and any text placed inside SVG (`<text>` labels, chart tooltips). Notes and company names copied from job postings routinely contain these characters; unescaped, they break the layout or inject markup into a page the user opens routinely.

### Layout

```
┌─────────────────────────────────────────────┐
│  🔍 Job Search Dashboard    Generated: DATE  │
├─────┬─────┬──────┬──────┬─────┬──────────────┤
│Total│Prep-│Active│Inter-│Offer│Rejected/     │  ← stat cards
│  N  │ared │  N   │view N│  N  │Closed  N     │
├─────┴─────┴──────┴──────┴─────┴──────────────┤
│  Status breakdown (doughnut) │ By sector (bar)│  ← charts row
├─────────────────────────────────────────────  ┤
│  By channel (bar)  │  Funnel (horizontal bar) │  ← charts row
├──────────────────────────────────────────────  ┤
│  Applications  [Status ▾] [Sector ▾] [🔍 ...]│  ← table with filters
│  date │ company │ sector │ role │ status │ ... │
│  ...                                          │
└───────────────────────────────────────────────┘
```

### Design spec

- **Colour palette:** CSS custom properties. Status colours:
  - Prepared: `#64748b` (slate) — deliberately muted, so a stack of prepared documents never reads as work in flight
  - Active: `#3b82f6` (blue)
  - Interview: `#f59e0b` (amber)
  - Offer: `#8b5cf6` (purple)
  - Hired: `#22c55e` (green)
  - Rejected/Closed: `#ef4444` (red)
- **Font:** system-ui stack, no web fonts
- **Stat cards:** white background, subtle shadow, large bold number, label below, left border in status colour
- **Charts:** contained in a 2-column grid on wide screens, stacked on narrow
- **Table:**
  - Alternating row shading
  - Status column uses a coloured pill/badge
  - `source` column renders as a hyperlink if the value is a URL (starts with `http`)
  - Empty cells render as `—`
  - Client-side filter: a text search input filters rows across company + role + sector; the status and sector dropdowns filter independently; all three combine (AND). The status dropdown includes **Prepared**, so the prepared-not-sent set can be isolated in one click — that is the view the user acts on
  - **Prepared rows** have no `sector`, `channel` or `notes`; render those `—` per the empty-cell rule rather than omitting the row. Fill `Company`, `Role` and `Source` from the `seen_jobs.json` entry, and use `processed_date` as the `Date` value so the rows sort alongside the applications
  - Rows are sorted newest-first by default (by `date` descending, then alphabetically by company)
- **Responsive:** usable at 900px+, not broken below that
- **Footer:** "Generated by Claude Code · ai-job-search · {ISO date}"

### Charts (inline SVG)

1. **Status doughnut** — slices for each status bucket including Prepared, colours from the palette above
2. **By sector bar** (horizontal) — company count per sector, sorted descending
3. **By channel bar** — online / referral / other
4. **Application funnel** (horizontal bar) — Applied → Interview → Offer → Hired, each bar = count reaching that stage. Prepared is **not** a funnel stage: nothing was submitted, so including it would make the first drop-off read as a screening failure when it is just unsent paperwork

Build each chart as a hand-written `<svg>` element: compute bar lengths/doughnut arc angles from the stats in Step 2 and emit the `<rect>`/`<path>`/`<circle>` and `<text>` elements directly — no charting library, no `<canvas>`. Each `<svg>` has `role="img"` and an `aria-label` summarizing the chart (e.g. "Status breakdown: 3 Active, 2 Interview, 1 Offer"). Wrap each in a `<div class="chart-card">` with an `<h3>` title above. Remember to escape any label/value text drawn into `<text>` nodes per the escaping rule above.

### Table: columns to include

`Date` · `Company` · `Role` · `Sector` · `Channel` · `Status` · `Notes` (truncated to 80 chars with `title` tooltip for full text) · `Source` (link or `—`)

Columns with only empty values across all rows may be omitted.

---

## Step 4: Write and Confirm

Write the complete HTML to the output path using the Write tool.

Then present:

> **Dashboard generated:** `<output path>`
>
> Open it in any browser — no server needed.
>
> **Summary:**
> - Total applications: N
> - Active: N · Interview: N · Hired: N · Rejected/Closed: N
> - Funnel: N% progressed past resume screen
> - **Prepared, not yet submitted: N** — documents are ready; `/outcome <company>` logs each one once sent
>
> Re-run `/html-report` any time after adding new entries via `/outcome` to refresh the dashboard.

Drop the Prepared line entirely when the count is zero, rather than printing "Prepared: 0" — an empty to-do is not news.

---

## Design Principles

- **Self-contained.** One file, fully offline — charts are inline SVG, no CDN or external requests of any kind.
- **Data-only.** This command reads and renders; it never writes to the tracker, the archive, or `seen_jobs.json`. It reads `seen_jobs.json` for the Prepared bucket and nothing more — status transitions there belong to `/rank`, `/apply`, `/tailor` and `/outcome`.
- **Idempotent.** Re-running overwrites the previous report at the same path — no accumulation.
- **Graceful on sparse data.** With only a few rows (as now), charts render correctly for small N; the table is the primary value. Do not suppress charts just because N is small.
- **No fabrication.** Every number in the report comes directly from the CSV or outcome files. Do not infer or estimate missing fields.
