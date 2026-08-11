---
framework_version: 1.0.0
---

# Standing Answer Bank

Reusable answers to the screening questions that recur across almost every
application. Built 2026-08-09 after the Pylon, Palantir FDSE and Arctic Lake
submissions, once it became clear the same eight or nine questions were being
re-reasoned from scratch each time.

**What this is for.** Application-portal questions are discovered when the form
is opened, not when the posting is read — Lever's public API returns no form
fields at all, and only Greenhouse exposes them in advance. So a per-posting
workflow cannot pre-empt them. What it *can* do is recognise that most of these
questions are not posting-specific: work authorization, graduation date,
availability, relocation and school-return answers are the same on every form.
Those live here, written once and pasted.

**What this is not.** It is not a substitute for `08-application-forms.md`,
which governs how posting-*specific* fields get drafted. Anything that needs the
posting — "why this company", a role-specific pitch, a competency question about
their domain — is drafted per application under that file. Only the invariants
live here.

## Grounding

Every answer below is defensible from the union of `01-candidate-profile.md`,
`cv/main_example.tex` and `CLAUDE.md`'s Candidate Profile section, or is copied
from an answer already submitted to an employer (Pylon and Palantir FDSE, both
2026-08-09). Nothing here introduces a new claim. If a fact changes, change it
here **and** in `01-candidate-profile.md` — an answer bank that drifts from the
profile is worse than no answer bank, because it gets pasted without rereading.

## Rules that must not be broken

1. **Graduation is always "May 2028".** Never 2029. The 12-16 month placement
   would move it, but writing 2029 presumes an offer he does not have. State
   availability separately instead. (`01-candidate-profile.md`)
2. **The application email is always `liamshan13@gmail.com`.** Every employer
   reply must land there. Never a work address.
3. **Work-authorization answers are given honestly, every time.** Both submitted
   applications declared "no authorization, sponsorship required". Canadians
   enter the US easily as visitors, which makes people assume work is equally
   simple; it is not, and an employer that discovers the mismatch after an offer
   withdraws it.
4. **India and China are excluded** (stated 2026-08-09). Relocation answers say
   "anywhere except India and China", not "anywhere".
5. **Never claim US Person status, clearance eligibility, or a clearance held.**
   See section 3.

---

## 1. Identity and contact

| Field | Exact value |
|---|---|
| Preferred name | Liam Shannon |
| Legal name | Liam Hunter Shannon |
| Email (always this one) | liamshan13@gmail.com |
| Phone | +1 (613) 700-4626 |
| Location | Ottawa, ON, Canada (term-time Kingston, ON) |
| LinkedIn | https://linkedin.com/in/liamshannon0 |
| GitHub | https://github.com/LiamShandog |
| Personal site | https://liamshannon.vercel.app |
| Citizenship | Canadian citizen (no second passport) |
| Languages | English - native; French - fluent (second language) |
| Pronouns, if asked | supply your own; not recorded here |

## 2. Education

| Field | Exact value |
|---|---|
| University | Queen's University, Kingston, ON, Canada |
| Faculty | Stephen J. R. Smith Faculty of Engineering and Applied Science |
| Degree | BASc in Mechatronics and Robotics Engineering |
| Dates | September 2024 - **Expected May 2028** |
| Current year | Third year (as of the 2026-27 academic year) |
| GPA | 4.19 / 4.30 cumulative |
| Honours | Dean's Scholar, Winter 2025 (4.30 term GPA) |
| High school | Sacred Heart High School, Ottawa, ON - Sep 2020 to Jun 2024 |
| Certification | Palantir Foundry & AIP Builder Foundations, April 2025 |

If a form asks for expected graduation as a **month/year dropdown**: `05/2028`.

## 3. Work authorization - the highest-stakes cluster

Get these wrong and an offer gets withdrawn. Answer exactly as written.

| Question as commonly worded | Answer |
|---|---|
| Are you legally authorized to work in **the United States**? | **No** |
| Are you legally authorized to work in **Canada**? | **Yes** - Canadian citizen, no sponsorship needed |
| Are you legally authorized to work in **the UK / EU / elsewhere**? | **No** |
| Will you now or in the future require sponsorship for employment visa status (e.g. H-1B)? | **Yes** - both halves, "now" and "in the future" |
| Are you a **U.S. Person** as defined for export control / ITAR purposes? | **No.** A U.S. Person is a US citizen, lawful permanent resident, refugee or asylee. He is none of these. |
| Do you hold an active **security clearance**? | **No** |
| Are you **eligible to obtain** a US security clearance? | **No** - US clearances are normally gated on US citizenship. Do not answer "yes, willing to obtain". |
| Do you have a criminal record / are you eligible to be bonded? | Answer honestly; nothing recorded here. |

**Sponsorship free-text box** (42 words) - as submitted to Pylon:

>>>
Yes. I am a Canadian citizen. For a Summer 2027 internship in the United States I would need J-1 exchange visitor sponsorship through a designated sponsor, which is the standard route for Canadian students, and I am happy to do the legwork on it.
<<<

**Current visa status** (51 words) - as submitted to Pylon:

>>>
None. I am a Canadian citizen and hold no US visa. For a Summer 2027 internship I would expect to come in on a J-1 exchange visitor visa arranged through a designated sponsor, which is the standard route for Canadian students, and I am glad to handle the paperwork on my end.
<<<

**Short dropdown / one-liner variant** (11 words):

>>>
No current US visa - Canadian citizen, would require J-1 sponsorship
<<<

**UK variant** (38 words) - matches what was declared on the Palantir FDSE form:

>>>
I do not currently hold the right to work in the UK. I am a Canadian citizen and would require visa sponsorship. I would relocate to London and am glad to handle the paperwork on my end.
<<<

## 4. Availability, term and relocation

| Question | Answer |
|---|---|
| Earliest start date | **May 2027** (third year runs to April 2027) |
| Available until | **August 2028** |
| Preferred length | A single 12-16 month placement; multiple shorter placements covering the window are acceptable |
| Will you return to school after the internship? | **Yes** - final year, graduating May 2028 |
| Will you have at least one term/semester remaining after? | **Yes** |
| Are you available for a Summer 2027 internship? | **Yes** |
| Willing to work in person / on-site? | **Yes** |
| Willing to relocate? | **Yes - anywhere except India and China** |
| Willing to travel? | **Yes** - up to and including 25-50%; treated as a positive |
| Notice period | None |
| Salary expectations | No floor set. Prefer "open, and aligned with your standard intern band". **If a number is mandatory, ask Liam before inventing one.** |

**Availability free-text** (46 words):

>>>
I am available from May 2027 through August 2028. My third year of study runs to April 2027 and I return for my final year after the placement, graduating in May 2028. A continuous 12 to 16 month placement is what I am looking for, but I am flexible on structure.
<<<

**Why the long availability window** (61 words) - use when a form asks about a
non-standard term, or when the posting is summer-only:

>>>
My program allows a 12 to 16 month break in studies between third and final year, so I am available from May 2027 straight through to August 2028 rather than only over the summer. If the internship is a fixed summer term I am still interested; I would simply look to pair it with a second placement to cover the rest of the window.
<<<

## 5. Recurring free-text answers

### Self-introduction (98 words)

>>>
I am a third-year Mechatronics and Robotics Engineering student at Queen's University with over a year of production software delivery behind me. At two companies I built on Palantir Foundry for heavy-industry operators: dispatch software for a 100+ driver fleet, and an equipment management system for a client whose 1,000+ trucks were entirely untracked, which exposed 10,000+ equipment-hours a week lost to idling. Outside work I direct a 15-person software team building an autonomy stack for a fixed-wing drone competition. I am looking for a 12 to 16 month placement starting May 2027.
<<<

**Short variant** (49 words):

>>>
Third-year Mechatronics and Robotics Engineering student at Queen's with over a year of production software delivery on Palantir Foundry for construction and fleet operators, plus a 15-person student software team I direct. Available May 2027 to August 2028 and looking for a long placement rather than a single summer.
<<<

### Startup experience (178 words) - as submitted to Pylon

>>>
Yes. Cavtera, where I am a Software Developer now. It is a construction technology company in Kanata North that launched publicly in June 2026, the same month I started, spun out of Thomas Cavanagh Construction to commercialize the Palantir Foundry systems that business had run internally for years.

Nobody had time to give me small work. In my first weeks I built a full-stack Equipment Management System for a client whose 1,000+ trucks and pieces of equipment were entirely untracked; it measured 10,000+ equipment-hours a week lost to idling, worth over $1,000,000 a year in recoverable cost. When the ingestion APIs feeding live telematics broke, that was my problem to fix, so I rebuilt the pipeline and added alerting nobody had asked for.

That is the environment I want more of. I like being trusted with something that matters before anyone is certain I can do it, and I learn fastest around people who know more than me. My earlier role at Thomas Cavanagh Construction was not a startup, it was the established business Cavtera spun out of.
<<<

**Guardrails baked in - do not edit these out:** Thomas Cavanagh is named as
*not* a startup; the Queen's Aerospace Design Team is named as a student team,
not a company; no claim of founding status, equity or employee number.

### Hardest technical problem (short, 96 words)

>>>
At Cavtera I inherited an equipment telematics integration that had silently stopped working. The failure sat across a boundary I did not own - a third-party API on one side, a Foundry transform pipeline on the other - and both looked healthy in isolation, so I had to work backwards from bad data to find where records were being dropped. I rebuilt the Python transform to parse 10,000+ records a day correctly and to fail loudly rather than quietly. The expensive failures are the ones that produce plausible output from incomplete input.
<<<

### Something not on your resume (168 words)

>>>
Nutrition. I know an unreasonable amount about it for someone who does not do it professionally - macronutrient composition from memory, why two people eating identical calories end up in different places depending on protein, training load and sleep, and why fat loss, muscle gain and sport performance are three genuinely different problems rather than one.

It started selfishly. I was a chubby teenager and decided to change it, which meant learning the subject properly instead of following whatever was loudest. I started training at sixteen and have not stopped since, including on the days I did not feel like it. That consistency is the part I am actually proud of, more than the knowledge.

What keeps me interested is how much confidently delivered nonsense there is in the field, and that obesity is an enormous problem that is not obviously unsolvable. I would like to do something about that eventually.
<<<

### "Why do you want to work here" - SKELETON ONLY

**Do not paste a generic version of this.** It is the one recurring question
that is genuinely posting-specific, and a generic answer is worse than a short
one. Draft it per application under `08-application-forms.md`, using this shape:

1. One verified, specific fact about what *this* employer does — verified per
   `09-web-research.md`, from their own domain, never from the posting text
2. The single piece of his experience that connects to it, with its number
3. What he wants from the role, in his own register (learning from strong
   engineers; being trusted with an outcome; a visible user)

Do not claim culture fit. Demonstrate it with the example.

### How did you hear about us

Answer honestly per posting. The `portal` field in `job_scraper/seen_jobs.json`
records the true source for every tracked job — LinkedIn, the company careers
site, or a community tracker. If the form has a "job board" option and the job
came from a tracker, "LinkedIn" or "online job board" is the honest choice.

## 6. Quick dropdown reference

| Prompt | Selection |
|---|---|
| Degree level | Bachelor's |
| Field of study | Engineering / Computer Engineering (Mechatronics and Robotics if listed) |
| Expected graduation | 05/2028 |
| Class year | Junior / third year |
| Are you a student? | Yes |
| Require sponsorship? | Yes |
| Authorized to work in the US? | No |
| Authorized to work in Canada? | Yes |
| US Person (export control)? | No |
| Security clearance | None |
| Veteran status / disability / EEO | Voluntary — his choice, nothing recorded here |
| Willing to relocate | Yes (except India, China) |
| Gender / race / ethnicity | Voluntary — his choice, nothing recorded here |

## 7. Consistency checks before submitting

- Graduation on the form matches the CV: **May 2028**
- Email on the form matches the CV: **liamshan13@gmail.com**
- The sponsorship answer matches whatever the cover letter says about visas
- If the employer runs separate FDSE and SWE tracks (Palantir), the role
  confirmation matches the application actually being submitted — see the
  `skip_reason` recorded on both Palantir SWE entries in `seen_jobs.json`
- Availability stated as May 2027 - August 2028, never as a graduation year change
