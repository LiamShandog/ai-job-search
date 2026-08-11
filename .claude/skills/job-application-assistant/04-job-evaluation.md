---
framework_version: 1.2.2
---

# Job Evaluation Framework

<!-- SETUP: Skill match areas and career goals are personalized by running /setup -->

## Eligibility Gate — run before scoring

If the candidate is not a citizen or permanent resident of the country they are applying in, run this first. It is a hard filter, not a scoring dimension, and it is separate from work-permit *timing*: timing asks "can they work the required hours yet?", eligibility asks "are they permitted to hold this job at all?". A candidate can pass timing and still be categorically excluded.

Read the posting's eligibility / work rights / "who can apply" section **verbatim** and classify:

| Posting wording | Verdict |
|-----------------|---------|
| Names a **citizenship or permanent-residency requirement** ("must be a citizen of X", "permanent resident", "PR required", "full working rights" where the employer means citizen/PR) | **FAIL — hard stop.** Do not score, do not draft. Quote the exact wording back to the user. |
| Requires a **security clearance** at any level | **FAIL** in most countries, since clearance is normally gated on citizenship. Verify the specific scheme rather than assuming. |
| **Explicitly names** the candidate's permit class, or says "international applicants welcome", "visa holders considered", "we sponsor" | **PASS** — verified acceptance. Worth noting as a positive in the application. |
| **Silent** on citizenship or residency | **PROCEED, but mark unverified.** Check the employer's own careers or international-applicant page before drafting. |

**Two rules that are easy to get wrong:**

1. **Silence is not permission.** Large graduate programs frequently gate eligibility on their own website rather than in the job ad. Highest-risk categories: professional-services firms, government and defence, banking, telecommunications, and anything touching critical infrastructure.
2. **A company-wide "we accept international applicants" statement is not role-level permission.** The common pattern is a general welcome followed by a *named list* of the specific programs or service lines it covers. Confirm the **specific posting or stream** appears on that list before drafting.

**Report an eligibility failure to the user with the quoted source** rather than silently dropping the role. They may know something about their own status that the profile does not record.

If the candidate's permit also constrains *hours* or *start date* (a student visa with a term-time cap, a permit that begins on graduation), record that as a second gate under this section during `/setup`, with the specific dates. Do not merge it with the eligibility question above — they fail for different reasons and need different answers.

A role that fails this gate is not scored and not drafted. Everything below applies only to roles that pass it.

### Candidate-specific eligibility facts (Liam Shannon)

**Status:** Canadian citizen. No second citizenship, no other passport, no
pre-existing right to work anywhere else. Because the search is worldwide, this
gate will fire often - run it *first*, before spending effort on scoring.

| Market | Reality |
|---|---|
| **Canada** | Unrestricted. No gate concerns. |
| **United States** | Needs employer cooperation. Canadian citizens have no automatic US work right; student interns normally need a **J-1** intern/trainee visa, arranged via the employer or a designated sponsor. TN status does not apply (it requires a completed degree and a listed profession). Large tech employers hire Canadian interns routinely and have this process; smaller companies often do not. **PROCEED but mark unverified** unless the posting names international or Canadian applicants. Ask early in the process rather than after an offer. |
| **UK / Ireland / EU / elsewhere** | Requires a work permit or an internship-specific scheme (e.g. the UK's Government Authorised Exchange route). Employer must be willing and, in the UK, licensed to sponsor. **PROCEED but mark unverified.** |
| **Fully remote** | Check where the employer can legally engage a Canada-based contractor or employee. "Remote" frequently means "remote within country X". |

**Hard fails to watch for, which recur in exactly the companies Liam named as targets:**

- **"Must be a US person" / "US citizen or permanent resident"** - standard on US defence, space, and government-adjacent work. This catches **Palantir's US government business**, Anduril, SpaceX (ITAR), Lockheed, and similar. Palantir's commercial and non-US roles, and its UK and Canadian offices, are not necessarily affected - check the specific posting rather than writing the company off.
- **Any security clearance requirement** at any level, in any country. Clearances are normally gated on citizenship of that country.
- **ITAR or export-control restrictions** - common across aerospace and defence, which overlaps Liam's aerospace interest. A posting can be an excellent skills fit and still be a categorical no.

### CANDIDATE OVERRIDE (2026-08-09): apply under uncertainty, never drop

**Liam's explicit instruction: "When there is any uncertainty in whether I could
actually work a specific job, I'd rather apply than ignore it. I want to apply to
as many jobs as possible."**

This overrides the default posture of this gate and of the bulleted hard-fail list
above. Uncertainty no longer *excludes* a posting - it only labels it. Apply this
three-way split and **surface every posting in all three buckets**. Nothing is
dropped silently, and nothing is withheld from his view.

| Evidence | Verdict |
|---|---|
| **The employer's own posting text** states a barrier he cannot meet, quoted verbatim - e.g. IBM Hursley's *"you must have permanent residency to work in the UK"*, or Palantir Seattle's *"Active US Security clearance, or eligibility and willingness to obtain a US Security clearance"* | **NOT RECOMMENDED - but still listed, still quoted, still his call.** Clearance and ITAR bars are legal, not preferences, so an application cannot succeed however strong the fit. Rank these last rather than hiding them. |
| **Second-hand or inferred** - a community tracker's 🇺🇸/🛂 marker, a flag propagated from a *different* req at the same employer, a "this type of company usually requires" assumption, anything not read from the posting itself | **APPLY.** Note the concern in one line, then treat the posting as live. Tracker markers are volunteer-maintained and are frequently stale or simply wrong. |
| **Silent or ambiguous** on citizenship, residency, or sponsorship | **APPLY.** Do not research silence into a rejection. Employers often state a default they will waive for a candidate they want. |

**Practical consequences:**

- Never exclude a posting because a *different* role at the same employer required citizenship. Palantir is the standing example: its US government work is gated, its UK and commercial roles are not.
- "Does not offer sponsorship" is **not** a hard fail. It is a reason to apply and ask.
- Where a posting is a strong skills match and the only doubt is work authorization, that doubt is **an interview question, not a filter**. Apply, and ask early who handles authorization.
- Keep reporting the concern every time. Applying anyway is Liam's decision to make with the facts in front of him; it is never a reason to stop surfacing them.

**Where the "not recommended" label will legitimately recur** (still listed, still
his decision): US defence, space, and government-adjacent work - Palantir's US
government business, Anduril, SpaceX and other ITAR-restricted aerospace,
Lockheed, RTX, Northrop, and any posting naming a security clearance.

**Report a failure with the quoted wording** rather than silently dropping the
posting, and never assume silence means permission. For US postings in
particular, the employer's own university-recruiting or FAQ page is usually more
informative than the job ad.

## Language Gate — run before scoring

No dimension or gate anywhere in this framework currently checks a posting's language requirements against what the candidate actually speaks - it is not one of the five Scoring Dimensions below, not a field `/scrape` or `/rank` track, and not something `/apply`'s language detection (Step 1, which already extracts a posting's required language generically) has anywhere to report to. This gate adds that check, structured the same way as the Eligibility Gate above: read the posting, classify against profile data, and treat a hard mismatch as FAIL before scoring.

Read the posting's language requirements as stated for **the role itself** — not the language the ad happens to be written in. A posting written in a language you don't work in, for a role that only needs languages you do work in on the job, passes fine; only an explicit job-condition requirement ("fluent X required," "must communicate with the Y team in Z") triggers this check. For each language the posting requires as a job condition, compare it against your Languages table in CLAUDE.md / `01-candidate-profile.md`:

| Posting requirement vs. your Languages table | Verdict |
|---|---|
| Requires a language **not on your table at all** (e.g. "fluent Polish required," "must communicate with the Warsaw team in Russian," and you list no Polish/Russian row) | **FAIL — hard stop.** Do not score, do not draft. Quote the exact requirement line. |
| Requires a language you **do** list, but the posting's stated bar (as written — "fluent," "native," "C1+," "business-level") reads as plausibly **higher** than your declared level | **FLAG, then proceed.** Not a fail. Score and draft normally, but surface the gap explicitly in your report to the user (quote both the posting's requirement and your declared level) so they can judge it themselves — bars like "fluent" vary a lot by company and geography, and a recruiter may be flexible. Never silently drop the posting and never silently treat it as a clean pass. |
| Requires a language you list, at or below your declared level (or the posting doesn't specify a level at all — just names the language) | **PASS.** No note needed. |

Judge the level comparison the same way you judge everything else in this framework: read both sides as written and reason about it, don't force either into a rigid scale — CEFR letters, LinkedIn-style buckets ("professional working proficiency"), and plain-English words ("conversational," "fluent," "native") all appear in the wild and don't map onto each other precisely. When genuinely unsure whether a stated bar exceeds the candidate's level, prefer FLAG over a silent PASS — the human is meant to be the tiebreaker, not the gate.

**Worked example:** a candidate whose Languages table lists Spanish (Native) and English (B1/B2). A posting requiring "fluent Russian" → **FAIL**, Russian isn't declared at all. A posting requiring "fluent English" → **FLAG**, English is declared but "fluent" plausibly exceeds B1/B2 — score and draft the application, but tell the candidate this posting's bar may be a stretch and let them decide. A posting requiring "conversational English" or unspecified English → **PASS**, B1/B2 clears a "conversational" bar cleanly.

## Scoring Dimensions

Evaluate each job posting against these five dimensions:

### 1. Technical Skills Match (0-100)
How well do the required/preferred skills align with the candidate's capabilities?

| Score | Meaning |
|-------|---------|
| 80-100 | Core requirements are primary skills |
| 60-79 | Most requirements match, 1-2 gaps that are learnable |
| 40-59 | Partial match, significant upskilling needed |
| 0-39 | Fundamental mismatch |

**Strong match areas:** Palantir Foundry (ontology modeling, pipelines, transforms, OSDK, AIP - certified), TypeScript/JavaScript, React, Python data pipelines, full-stack application delivery, ROS 2, SLAM, Arduino/C-C++ embedded control, PID and closed-loop control, Docker, Git, Linux

**Moderate match areas:** Gazebo simulation, sensor integration, Raspberry Pi, SolidWorks/Onshape CAD, Altium/LTspice power electronics, SQL-style querying, large-scale data modeling, VHDL and NIOS II assembly (coursework only)

**Weak match areas / genuine gaps - never paper over these:**
- Machine learning and AI practice (no shipped models; Foundry AIP certificate and strong applied maths only)
- Cloud infrastructure: AWS, GCP, Azure, Kubernetes, Terraform
- Production software engineering process at scale: CI/CD beyond Docker builds, TDD, large-team code review culture
- Direct database ownership: Postgres/MySQL schema design, query tuning outside Foundry
- Compiled-systems depth: Rust, Go, JVM languages
- Mobile, game development, graphics, security

A posting whose core requirement sits in the weak list scores below 40 on this
dimension regardless of how strong the rest of the profile is. Say so plainly
rather than stretching the framing.

### 2. Experience Match (0-100)
Does work history align with what they're looking for?

| Score | Meaning |
|-------|---------|
| 80-100 | Direct experience in the same domain and role type |
| 60-79 | Related experience, transferable skills clear |
| 40-59 | Adjacent experience, would need to make the case |
| 0-39 | Unrelated experience |

**Calibrate against the right baseline.** Liam is applying for **internships and
co-op placements as a third-year undergraduate**, not for full-time roles. Score
experience against what internship postings ask of students, not against a
mid-level engineer's résumé. Against that baseline he is unusually strong: 1+
year of paid production software work, two employers, and a 15-person team lead
role, where most applicants have coursework and personal projects. A posting
demanding 3+ years of professional experience is a genuine mismatch; an
internship posting asking for "some programming experience" is an 85+, not a 60.

**Strong:** enterprise data platform work (Palantir Foundry), operational/logistics software for heavy industry (construction, trucking, fleet and equipment management), full-stack internal tooling, customer- and stakeholder-facing engineering, autonomous ground/air robotics in a competition setting, technical team leadership

**Moderate:** general SaaS product engineering, embedded firmware, power electronics, mechanical CAD, data engineering outside Foundry

**Entry-level / no professional experience:** ML and AI engineering, cloud/DevOps/SRE, security, mobile, quantitative finance, hardware manufacturing at scale

### 3. Behavioral/Culture Fit (0-100)
Does the role and company culture match the behavioral profile?

| Score | Meaning |
|-------|---------|
| 80-100 | Culture strongly matches behavioral preferences |
| 60-79 | Mixed signals but mostly compatible |
| 40-59 | Some friction areas |
| 0-39 | Significant culture mismatch |

**Red flags to research:** Department disorganization, work dominated by maintenance over development, poor chemistry with leadership, culture mismatches. Check reviews, media coverage, LinkedIn connections, and network contacts for insider perspective.

### 4. Location & Logistics (Pass/Fail + Notes)

**Location fails only on the two excluded countries.** Liam is open to relocating
anywhere in the world for the placement and has no commute or family constraints,
with one stated exception recorded below. Otherwise, do not reject a posting on
geography.

**Excluded countries (stated 2026-08-09): India and China.** A posting based in
either — on-site, hybrid, or "remote within" that country — is a **FAIL**. It is
not scored and not drafted. This is a stated preference, not an uncertainty about
eligibility, so the CANDIDATE OVERRIDE above does **not** apply to it: the override
governs citizenship and work-authorization doubt, not where he is willing to live.
Watch for the indirect signals as well as the obvious ones — an `in.linkedin.com`
or `cn.linkedin.com` source domain, a "Greater <city> Area" location string, or a
"remote (India only)" clause. A role that is remote *within* an excluded country
still fails, because it requires being in that country.

- Anywhere in the world except India and China, on-site or hybrid: PASS
- Remote, not tied to an excluded country: PASS
- Requires relocation (outside the excluded countries): PASS (expected and accepted)
- Based in, or remote-within, India or China: **FAIL**

**What replaces location as the real logistical filter is the term.** Check every
posting against the availability window in `01-candidate-profile.md`:

| Posting term | Verdict |
|---|---|
| 12-16 month internship / co-op / industrial placement, starting mid-2027 | **Ideal.** Lead with the availability match; it is a differentiator. |
| 6-8 month co-op starting mid-2027 | **PASS.** Good, and can be paired with a second placement to fill the window. |
| Standard 12-16 week summer 2027 internship | **PASS, with a note.** Covers only a third of the window. Worth applying to prestigious ones, but flag that a second placement will be needed. Ask whether the employer would extend. |
| Starts before May 2027 or requires term-time availability | **FAIL.** Third year runs to April 2027. |
| Full-time / new-grad role | **FAIL.** He has a final year to complete after the placement. |
| Internship for summer 2026 or earlier | **FAIL.** Expired cycle. |

Frequent international travel: PASS, and generally a positive.

### 5. Career Alignment & Motivation (0-100)
Does this role advance career goals and contain tasks that energize?

| Score | Meaning |
|-------|---------|
| 80-100 | Strongly aligned with career direction, clear growth path |
| 60-79 | Good role but only partially aligned with long-term goals |
| 40-59 | Decent job but doesn't build toward career goals |
| 0-39 | Dead end or backwards step |

**Career goals:**
- Work with the strongest engineers he can reach, and learn from them. Stated as the primary objective, explicitly ahead of compensation: "I really want to just get the absolute best possible job, to learn from the smartest people possible."
- Build the network and credibility to either found a startup or hold significant responsibility at a frontier-leading company.
- Be pushed hard. A placement that is comfortable but unchallenging counts as a failure by his own measure.
- Preserve breadth across software and hardware rather than narrowing to one layer too early.

**This dimension carries unusual weight for this candidate.** With no salary floor
and no location constraint, career alignment and calibre of team are effectively
*the* decision criteria. Weight it accordingly when the overall score is close.

**Motivation filter:**
- **Tasks that energize:** hard problems with no obvious answer; being trusted with an outcome and contributing heavily; working alongside driven, technically strong people; owning something end to end
- **Tasks that drain:** mundane and repetitive work; being overlooked or treated as less capable because he is younger; colleagues without drive
- **Non-task factors:** degree of autonomy granted to interns, technical calibre of the immediate team, whether interns ship to production, directness of feedback

**Company-calibre filter (from Liam's stated targets):** big tech and FAANG,
Palantir, and reputable companies generally. In practice, prioritize:
1. Companies where the work is genuinely frontier (AI labs, autonomy, space, defence tech, advanced infrastructure)
2. Palantir specifically - the Foundry and OSDK experience is a rare, directly transferable match, and Forward Deployed Engineer is the best-fit role in the entire search
3. Big tech with strong, long-established intern programs that give real ownership
4. Well-regarded startups where an intern's scope is large by default

**Life situation alignment:**
- **Security:** no salary baseline set; no financial constraint stated. Do not filter on compensation, but do surface unpaid or below-market offers for his judgment rather than treating them as neutral.
- **Flexibility:** fully flexible May 2027 through summer 2028. No constraints during the window. Unavailable before May 2027 (third year runs to April 2027).
- **Professional development:** the placement's learning curve and the seniority of the people he would work with matter more than title or pay. Weight mentorship quality and team calibre heavily.

## Additional gate for this candidate: internship term match

Run the term-match table in dimension 4 as a gate, not a scored note. A posting
that cannot start after May 2027, or that is a full-time/new-grad role, is a hard
FAIL regardless of how well it matches on skills - Liam has a final year to
complete. This is the single most common way a well-matched posting turns out to
be unusable, so check it early.

## Calibration from Past Applications

No data yet. `documents/applications/` is empty, so nothing here is calibrated
against real outcomes. Record results with `/outcome` as applications resolve,
then re-run `/setup` to populate this section. Until then, treat every score in
this framework as an untested estimate.

### 6. Salary Benchmark (Optional)

If the salary lookup tool is configured (`salary_data.json` exists), look up the company:
```
python salary_lookup.py "<Company Name>" --json
```

If a city is known from the posting, add `--city "<City>"` to narrow results.

Present findings as:
```
### Salary Benchmark
| Metric | Value |
|--------|-------|
| [Category] index | XX.X (+/-X.X% vs baseline) |
| Overall index | XX.X (+/-X.X% vs baseline) |
```

Interpret results relative to the baseline defined in the data file's metadata. For index-based data, higher typically means above-market compensation.

If the salary tool is not configured, skip this section.

## Output Format

Present the evaluation as:

```
## Job Fit Evaluation: [Role] at [Company]

| Dimension | Score | Notes |
|-----------|-------|-------|
| Technical Skills | XX/100 | [brief note] |
| Experience Match | XX/100 | [brief note] |
| Behavioral Fit | XX/100 | [brief note] |
| Location | PASS/FAIL | [brief note] |
| Career Alignment | XX/100 | [brief note] |

**Overall Score: XX/100** (weighted average of scored dimensions)

### Verdict: [Strong Fit / Good Fit / Moderate Fit / Weak Fit / Poor Fit]

### Key Strengths for This Role
- [bullet points]

### Gaps to Address
- [bullet points]

### Recommendation
[1-2 sentences: apply/skip/apply with caveats]

### Company Research Checklist
- [ ] Checked company website (mission, values, recent news)
- [ ] Checked review sites (Glassdoor, Jobindex, etc.)
- [ ] Checked LinkedIn for team size, recent hires, connections
- [ ] Checked media for restructuring, growth, or workplace issues
- [ ] Identified network contacts who may know the team/manager
```

## Weighting
- Technical Skills: 30%
- Experience Match: 25%
- Behavioral Fit: 15%
- Career Alignment: 30%

(Location is pass/fail, not weighted)

## Thresholds
- **Strong Fit** (75+): Definitely apply, tailor everything
- **Good Fit** (60-74): Apply, address gaps in cover letter
- **Moderate Fit** (45-59): Consider carefully, discuss with user
- **Weak Fit** (30-44): Probably skip unless strategic reasons
- **Poor Fit** (<30): Skip

## Pre-Application: Call the Employer (Best Practice)

Before writing the application, consider whether the candidate should call the contact person listed in the posting. **Only call if there are substantive questions** - never call just to "be remembered."

### When to Suggest Calling
- The posting has unclear or ambiguous requirements
- It's unclear which competencies are essential vs. nice-to-have
- The role description is vague about day-to-day tasks
- There's a named contact person who invites questions

### Good Questions to Ask
- "What are the primary challenges in this role?"
- "How is time typically divided across the listed responsibilities?"
- "Which competencies are most critical for success in this position?"
- "What does success look like in the first 6-12 months?"

### Rules for the Call
- Prepare a 30-second "elevator pitch" about your background in case they ask
- The call's purpose is **gathering information**, not delivering a pitch
- Take notes - use what you learn to tailor the application
- Reference the conversation naturally in the cover letter ("After speaking with [name], I was especially drawn to...")
