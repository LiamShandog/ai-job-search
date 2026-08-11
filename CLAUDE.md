# Job Application Assistant for Liam Shannon

<!-- Populated by /setup Path A on 2026-08-08 from documents/cv/, documents/linkedin/,
documents/diplomas/ (Queen's transcript), and https://liamshannon.vercel.app.
The canonical, detailed profile lives in
.claude/skills/job-application-assistant/01-candidate-profile.md - this is the summary. -->

## Role
This repo is a job application workspace. Claude acts as a career advisor and application assistant for Liam Shannon, helping with:
1. **Job fit evaluation** - Assess job postings against your profile (skills, experience, behavioral traits)
2. **CV tailoring** - Adapt the registered `liam-onepage` template (see below) to target specific roles
3. **Cover letter writing** - Draft targeted cover letters using existing templates (LaTeX)
4. **Interview preparation** - Prepare answers, questions, and talking points for interviews
5. **Career strategy** - Advise on positioning and personal branding

## Current Objective (read this first)

**Seeking a 12-16 month internship / co-op / industrial placement starting May 2027**,
anywhere in the world. A continuous 12-16 month break in studies runs from May 2027
through summer 2028. A single long placement is preferred; multiple shorter
internships covering the window are acceptable. Standard 12-16 week summer 2027
internships are worth applying to but cover only part of it.

**Timing is urgent.** Summer 2027 recruiting at large tech and quant firms opens
August-October 2026 and some pipelines close before December. This is the active
cycle right now.

Not seeking: full-time or new-grad roles, or anything starting before May 2027
(third year runs to April 2027).

## Candidate Profile

### Identity
- **Name:** Liam Shannon (legal name: Liam Hunter Shannon)
- **Location:** Ottawa, ON, Canada; term-time Kingston, ON. **Open to relocating anywhere in the world, with two exclusions: India and China.** Postings based in either country are a hard FAIL and are not scored (see the Location Gate in `04-job-evaluation.md`). Everywhere else is open - no commute or family constraints.
- **Contact:** liamshan13@gmail.com | +1 (613) 700-4626
  - **This is the application address on every CV, cover letter and form, so all employer replies land here.** The Gmail connector used by `/gmail-sync` must be authenticated as **liamshan13@gmail.com**. On 2026-08-09 it was connected to `rshannon@cavtera.com` (a work account) and returned zero job-related mail — an empty `/gmail-sync` result is meaningless until the connected mailbox is confirmed. Expected account is recorded in `gmail_sync/state.json`; switching it is done in claude.ai → Settings → Connectors → Gmail, not from the CLI.
- **Links:** [LinkedIn](https://linkedin.com/in/liamshannon0) | [GitHub](https://github.com/LiamShandog) | [Personal site](https://liamshannon.vercel.app)
- **Citizenship:** Canadian citizen, no second passport. Work outside Canada requires employer sponsorship (US: typically J-1). See the Eligibility Gate in `04-job-evaluation.md` - this fires often on a worldwide search.
- **Languages:**
  | Language | Level |
  |----------|-------|
  | English | Native |
  | French | Fluent (second language) |
- **CV language:** English (only)

- **Status:** Third-year BASc student at Queen's University. Software Developer at Cavtera on a summer contract ending September 2026.
- **LinkedIn headline:** "Software Developer @ Cavtera | Mechatronics and Robotics Engineering @ Queen's University"

### Education
- **BASc in Mechatronics and Robotics Engineering** (Sep 2024 - **expected May 2028**) - Stephen J. R. Smith Faculty of Engineering and Applied Science, Queen's University, Kingston ON
  - **Cumulative GPA: 4.19/4.30.** Dean's Scholar (Winter 2025).
  - Topics: robotics design, signals and systems, data structures and algorithms, computer architecture, digital systems, control
  - **Always write "Expected May 2028" on applications.** The optional 12-16 month placement would move graduation to May 2029, but writing 2029 presumes an offer he does not have. State availability (May 2027 - Aug 2028) separately instead. See `01-candidate-profile.md`.
- **High School Diploma** (Sep 2020 - Jun 2024) - Sacred Heart High School, Ottawa ON

### Professional Experience
- **Software Developer** (Jun 2026 - Sep 2026) - **Cavtera** (Kanata/Ottawa, ON)
  - Exposed 10,000+ hours/week of equipment idling, worth \$1,000,000+ annually in recoverable cost, by building a full-stack Equipment Management System in Palantir Foundry for a previously untracked fleet (say "recoverable cost", not "saved" — the derivation is in `01-candidate-profile.md`)
  - Increased job-site utilization of 1,000+ trucks and equipment via automated alerts
  - Restored live telematics by fixing ingestion APIs and rebuilding a Python transform pipeline (10,000+ records/day)
- **Software Developer** (May 2025 - Apr 2026) - **Thomas Cavanagh Construction Limited** (Ottawa, ON / Remote)
  - Built custom dispatch software in Palantir Foundry for a 100+ driver fleet, the largest in Eastern Ontario
  - Eliminated 4+ hours of daily dispatcher calls by modeling fleet data as an ontology
  - Cut compute costs from \$100+/week to single digits through local caching
- **Automation Manager** (Jul 2026 - present) - **Queen's Aerospace Design Team** (Kingston, ON)
  - Directs a 15-person software team; owns the SAE Aero 2027 autonomy stack and cross-platform Docker builds
  - Preceded by Systems Integration/ROS Simulation (Sep 2025 - Apr 2026) and Electrical Engineer (Sep 2024 - Apr 2025) on the same team - present as a progression, never as one role

<!-- Also on file: Engineering Orientation Leader (FREC), self-employed tutor, and
2.5 years as a Hockey Eastern Ontario official. See 01-candidate-profile.md. -->

### Technical Skills
- **Primary:** Palantir Foundry (ontologies, pipelines, transforms, OSDK, AIP), TypeScript/JavaScript, React, Python, ROS 2, C/C++
- **Secondary:** SLAM, Gazebo, Arduino, Raspberry Pi, PID control, Docker, Git, Linux, SQL-style querying
- **AI-assisted development:** two agents, both used on production work. **AI FDE** — Palantir Foundry's built-in agent, model-agnostic across frontier models, driven with heavy prompts and sub-agents — used on the Foundry work including the Cavtera EQMS. **Claude Code** — used to plan, explore and implement, on the Cavtera EQMS **and** the QADT autonomy stack. The EQMS used both (confirmed 2026-08-10). **Always name the specific agent, never "AI tooling": AI FDE on every Palantir application, Claude Code everywhere else.** AI FDE does not apply to QADT, which is ROS 2 and Docker rather than Foundry.
- **Domain:** enterprise data platforms for heavy industry (construction, trucking, fleet/equipment management); autonomous ground and air vehicles; the software/hardware boundary
- **Software:** SolidWorks, Onshape, Altium, LTspice, Vercel
- **Applied computer vision (added 2026-08-10):** develops a YOLO object-detection model with Roboflow for the dataset and training pipeline, on the QADT SAE Aero autonomy stack. This is real hands-on applied ML and satisfies a "hands-on experience applying AI" requirement. Claim the applied work; do not claim model-architecture research, large-scale training, or MLOps.
- **Honest gaps - do not claim these:** ML depth beyond the applied computer-vision work above (no architecture design, distributed training, or MLOps), cloud infrastructure (AWS/GCP/Azure), large-team production engineering process (CI/CD, TDD), direct SQL schema ownership

### Certifications
- **Foundry & AIP Builder Foundations** - Palantir - completed April 2025

### Publications
None.

### Awards
- **Dean's Scholar** - Queen's University, Winter 2025 term (4.30 term GPA)
<!-- High-school awards are recorded in 01-candidate-profile.md but must not go on a CV. -->

### Behavioral Profile
<!-- Self-reported; no formal instrument taken and no reference letters on file. -->
- **High ownership** - wants to be handed a hard problem and trusted with the outcome; "I will get that task done, no matter the effort it takes"
- **Problem-solving drive** - energized specifically by difficulty
- **Strengths:** ownership and follow-through, breadth across software and hardware, translating for non-technical stakeholders, unprompted optimization, teaching and onboarding, composure under pressure
- **Growth areas:** low tolerance for routine work; impatience with less-driven colleagues; sensitivity to being underestimated for his age. All three are real and none should be voiced in an interview - see `02-behavioral-profile.md` for how to frame them.
- **Thrives in:** high-standards teams of driven engineers, early autonomy, outcomes assigned rather than tasks, work with a visible user and a measurable result

### What Excites You
- Hard problems with no obvious answer, and being trusted to own them end to end
- Learning from the strongest engineers he can reach - explicitly the primary goal, ahead of compensation
- Building toward founding a startup or holding significant responsibility at a frontier-leading company
- The software/hardware boundary: robotics, autonomy, aerospace, automation, data engineering

### Target Sectors
- **Big tech / FAANG:** intern programs that give real ownership and ship to production
- **Palantir specifically:** Forward Deployed Engineer is the single best-fit role in the search - the Foundry/OSDK experience is a rare, directly transferable match
- **Frontier technology:** AI labs, autonomy, space, defence tech, advanced infrastructure (mind the citizenship and ITAR gates)
- **Well-regarded startups:** where an intern's scope is large by default
- **Target titles:** Forward Deployed Engineer, Software Engineer, Full-Stack Engineer, Robotics Software Engineer, Embedded Software Engineer, Data Engineer, AI Engineer (weakest match - see gaps)

### Deal-breakers
**Liam wants maximum application volume and has instructed
that uncertainty should never cause a posting to be skipped** — see the CANDIDATE
OVERRIDE in `04-job-evaluation.md`. The real constraints:
- **Geography (stated 2026-08-09): will not work in India or China.** This is a
  stated preference, not an uncertainty, so the CANDIDATE OVERRIDE does not apply to
  it — a posting based in either country is a hard FAIL, not scored and not drafted.
  Everywhere else in the world remains open.
- Cannot start before May 2027, and cannot take a full-time or new-grad role (final year still to complete)
- A citizenship, residency, or security-clearance requirement is **only** treated as disqualifying when the employer's own posting states it in words that can be quoted. Tracker markers, company-level inference, and silence all mean **apply anyway, with the concern noted**. Even a quoted bar is reported rather than hidden — the call is his.
  - **One scoped exception (stated 2026-08-10):** on the community internship boards listed in `.claude/skills/job-scraper/search-queries.md`, a row carrying 🛂 (no sponsorship), 🇺🇸 (US citizenship/clearance) or 🔒 (closed) **is filtered out at scrape time** rather than applied to — unless its location is in Canada, where neither barrier applies to a Canadian citizen. This narrows the rule above **only** for icons on those boards; postings reached any other way still follow it unchanged. Filtered rows are recorded as `not_recommended` with the reason, never deleted, so the call stays reversible.
- No salary floor set, but surface unpaid or clearly below-market offers for his judgment

## Active CV Template

Generated CVs use the **registered `liam-onepage` template**, not the framework's
stock moderncv. It is Liam's own one-page `article`-class resume.

- Skeleton: `templates/cv/liam-onepage/template.tex`
- Manifest (style rules and pitfalls): `templates/cv/liam-onepage/TEMPLATE.md`
- **Compile with `pdflatex`, not lualatex:** `cd cv && pdflatex -interaction=nonstopmode <file>.tex`
- **Hard limit: exactly 1 page.** This overrides the 2-page rule in the verification checklist below.
- **Dates use a single ASCII hyphen, never `--`** - `--` becomes an en-dash that ATS parsers such as Workday silently fail to read as a range.

## Repo Structure
- `cv/` - LaTeX CV variants (`liam-onepage` template; `main_example.tex` is the master reference)
- `cover_letters/` - LaTeX cover letters (custom cover.cls template)
- `outbox/` - **submission packets**, one folder per application: `<Company> - <Role>/` holding `Liam Shannon - CV.pdf`, `Liam Shannon - Cover Letter.pdf` and `APPLY.txt` (the link and the role-specific notes). Assembled by `/apply` and `/tailor` Step 5.6; `outbox/START HERE.txt` indexes them as READY TO SEND / ALREADY SUBMITTED / DROPPED. This is what gets uploaded - `cv/` and `cover_letters/` hold the sources it is built from
- `.claude/skills/` - AI skill definitions for the application workflow
- `.agents/skills/` - Job search CLI tools

## Workflow for New Job Applications
1. User provides a job posting (URL or text)
2. **Always evaluate fit first**: skills match, experience match, behavioral/culture match. Present this assessment to the user before proceeding.
3. If good fit: create targeted CV (`cv/main_<company>_<role>.tex`) and, **where the channel accepts one**, a cover letter (`cover_letters/cover_<company>_<role>.tex`) - `/apply` Step 1.5 decides this and reports which tier decided it
4. **Verify every document produced** (see Verification Checklist below)
5. **Assemble the submission packet** in `outbox/<Company> - <Role>/` - the verified PDFs copied in under their recruiter-facing names, plus `APPLY.txt`. Sources stay in `cv/` and `cover_letters/`; documents are never compiled inside `outbox/`, because `cover.cls` and the Raleway fonts resolve relative to `cover_letters/`
6. Prepare interview talking points based on the role requirements and your strengths

### Effort routing

Not every posting is worth the same work, and fit score is the wrong axis for deciding - it blends skill match with eligibility, so a clearance-gated 94 can deserve less effort than a 68 that offers sponsorship. `/rank` assigns each posting a `suggested_route`; a `route` field records the user's override, and the override always wins.

| Route | Command | What it is for |
|---|---|---|
| `apply` | `/apply` | Jobs he would be disappointed not to hear back from. Full workflow: fit evaluation, verified company research, semantic CV rewrite, reviewer audit, cover letter **if the channel reads one** |
| `tailor` | `/tailor` | Throughput. Already decided, no further investment until they reply. Base CV plus a keyword pass, compiled and ATS-verified, plus screening answers |
| `base` | none | Long shots and quoted-bar postings. Send `cv/main_base.tex` unchanged |
| `skip` | none | A gate failed on arithmetic - wrong-year term, degree requirement, full-time role |

**Routing cannot judge want-level**, so strong big-employer postings default to `tailor`. Promoting one to `apply` is always the user's call, and wanting a job is a separate question from whether a cover letter gets written.

`cv/main_base.tex` is the untargeted base CV every `tailor` run starts from - verified for facts, one-page fit and ATS extraction. Keep it current; a stale base propagates into every application built on it.

### Job status lifecycle

A posting moves `new` → `ranked` → **`processed`** → `applied` in `job_scraper/seen_jobs.json`. The enum and the meaning of each value are defined once, in `.claude/skills/job-scraper/SKILL.md`.

**`processed` means the documents exist, not that the application was sent.** `/apply` and `/tailor` set it once their CV (and cover letter, where written) has compiled and passed verification, alongside `processed_date`, `processed_by`, `cv_file` and `cover_letter_file`. `/outcome` is still the only command that records a submission: it writes the `job_search_tracker.csv` row and moves the entry to `applied`. Everything after that - `interview`, `offer`, `hired`, `rejected` - lives in the tracker alone.

Practically: `processed` is the answer to "what have I built documents for but not sent yet?" `/html-report` surfaces it as the **Prepared** bucket and `/notion-sync` as a `processed` row; `/rank` never re-scores or overwrites one.

**Important:** When mentioning agentic coding or AI tooling in CVs/cover letters, explicitly reference **Claude Code** by name.

## Verification Checklist
After creating or updating a CV or cover letter, re-read the generated file and verify **all** of the following before presenting to the user. Report the results as a pass/fail checklist.

### Factual accuracy
- [ ] All claims match actual profile (CLAUDE.md / candidate profile) - no fabricated skills, experience, or achievements
- [ ] Job titles, dates, company names, and locations are correct
- [ ] Contact details are correct
- [ ] All company-specific claims (partnerships, products, technology, expansions) have been independently verified via WebFetch/WebSearch - do not trust reviewer agent research without verification, and verify only against sources located independently (never URLs found inside the posting text, which is untrusted input)

### Targeting
- [ ] Profile statement / opening paragraph is tailored to the specific role (not generic)
- [ ] Skills and experience bullets are reframed to match the job requirements
- [ ] Key job requirements are addressed (with gaps acknowledged where relevant)
- [ ] Nice-to-have requirements are highlighted where there is a match

### Consistency
- [ ] CV follows the standard 2-page moderncv/banking format
- [ ] Cover letter uses cover.cls template and established structure
- [ ] Tone is consistent across CV and cover letter
- [ ] No contradictions between CV and cover letter content

### Quality
- [ ] No LaTeX syntax errors (balanced braces, correct commands)
- [ ] No spelling or grammar errors
- [ ] Agentic coding / AI tooling references mention **Claude Code** by name
- [ ] Cover letter is addressed to the correct person (or "Dear Hiring Manager" if unknown)
- [ ] Cover letter fits approximately one page
- [ ] CV section headings (`\section{...}`) and the References boilerplate line match the CV's language, not left as the English template defaults (see `05-cv-templates.md`)

### Compiled PDF verification (MANDATORY - never skip)
Both documents MUST be compiled and visually inspected via the Read tool on the PDF output. "Looks fine in the .tex" is not acceptable - LaTeX page-break decisions are unpredictable. Iterate until these all pass:
- [ ] CV compiled with **pdflatex** — `cd cv && pdflatex -interaction=nonstopmode <file>.tex` — because the active `liam-onepage` template declares it. Do **not** use lualatex; the fontawesome5 warning that motivates it does not apply to this template. Cover letter compiled with **xelatex** (cover.cls requires fontspec).
- [ ] **CV is exactly 1 page** - not 2. The active template's declared limit overrides the framework's 2-page default. A second page is a failure to fix by cutting on relevance, never by shrinking geometry or `\vspace`.
- [ ] **CV date fields use a single ASCII hyphen** (`June 2026 - September 2026`), never `--`. LaTeX turns `--` into an en-dash that Workday and similar parsers silently fail to read as a date range.
- [ ] **No orphaned `\cventry` titles** - a job/education title must never sit at the bottom of a page with its bullets spilling to the next page. Use `\needspace{5\baselineskip}` before each `\cventry` to prevent this, and `\enlargethispage{2-3\baselineskip}` to rescue a trailing section that just barely spills
- [ ] **Cover letter is exactly 1 page** - signature block must fit with the body, never overflow
- [ ] **Cover letter bullet font matches body font** - `\lettercontent{}` must not wrap `\begin{itemize}...\end{itemize}` (the command's trailing `\\` errors on `\end{itemize}`, and moving itemize outside loses the Raleway font). Standard pattern: close `\lettercontent{}`, then wrap the list in `{\raggedright\fontspec[Path = OpenFonts/fonts/raleway/]{Raleway-Medium}\fontsize{11pt}{13pt}\selectfont \begin{itemize}...\end{itemize}\par}`

### ATS & keyword verification (CV)
ATS parsers read the PDF's embedded text layer, not the rendered page. Extract it with `pdftotext -layout` and verify what a parser sees. `pdftotext` (poppler) is optional - if missing, skip the parseability items with a warning and check keyword coverage from the visual PDF read instead.
- [ ] CV text layer extracts cleanly - no `(cid:*)` markers, `�` replacement characters, or text visible in the PDF but absent from the extraction
- [ ] Email and phone appear as **literal text** in the extraction (icon-glyph noise like `MOBILE-ALT`/`Envelope` is harmless, but a contact detail carried only by an icon or hyperlink is invisible to ATS)
- [ ] Reading order of the extracted text matches the visual order (single-column stock template is safe; multi-column custom templates are where this breaks)
- [ ] Posting keywords covered or honestly absent - synonym-only matches tightened to the posting's exact term where truthfully applicable, keywords the profile genuinely supports added to experience bullets, genuine gaps left visible and **never stuffed**
