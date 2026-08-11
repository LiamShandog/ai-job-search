---
framework_version: 1.0.0
---

# Interview Preparation Guide

<!-- SETUP: STAR examples are personalized by running /setup based on your actual experience -->

## STAR Format

Structure answers as: **Situation** (context), **Task** (your responsibility), **Action** (what you did), **Result** (outcome).

Keep answers to 1-2 minutes. Be specific. End with what you learned or would do differently.

## STAR Candidates (Complete Manually)

<!-- /setup Path A identified these from the CV, LinkedIn, and transcript. The
stubs are deliberately not filled in: the situation/task/action/result details
are yours, and an interview answer invented by an assistant is worse than no
answer. Fill each one out in your own words before you interview. Aim to have
1-6 fully written before the first phone screen. -->

### 1. The compute-cost optimization (initiative, systems thinking)
**Source:** CV — Thomas Cavanagh Construction
**What happened:** Recurring dispatch compute costs ran \$100+/week; you rearchitected the data access to cache locally instead of querying the ontology, bringing it to single digits.
**Why it matters:** Best available evidence of unprompted initiative and of understanding cost as an engineering constraint. Answers "tell me about a time you improved something nobody asked you to", "describe a technical trade-off you made", "how do you think about performance".
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

### 2. Restoring broken telematics ingestion (debugging under pressure)
**Source:** CV — Cavtera
**What happened:** Live equipment telematics were down; you fixed broken ingestion APIs and rebuilt the Python transform pipeline handling 10,000+ records/day against a database of millions.
**Why it matters:** Debugging a production system with real users affected. Answers "walk me through the hardest bug you have debugged", "tell me about a time you fixed something you did not build", "how do you approach an unfamiliar codebase".
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

### 3. Digitizing dispatch for a 100+ driver fleet (stakeholder translation)
**Source:** CV and LinkedIn — Thomas Cavanagh Construction
**What happened:** You replaced 4+ hours of daily dispatcher phone calls and dozens of spreadsheets by modeling fleet data as an ontology, working directly with staff across every division.
**Why it matters:** **This is the single most important example for Forward Deployed Engineer interviews.** It is exactly the job: sit with non-technical operators, understand the workflow, build the software. Answers "tell me about working with non-technical stakeholders", "how do you gather requirements", "describe something you built that changed how people work".
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

### 4. Leading the QADT software team (leadership, delegation)
**Source:** CV — Queen's Aerospace Design Team, Automation Manager
**What happened:** You direct a 15-person software team, delegate work, onboard new ROS 2 contributors, and maintain a cross-platform Docker build, for the SAE Aero 2027 competition.
**Why it matters:** Leadership at a scale most undergraduate candidates cannot claim. Answers "tell me about leading a team", "how do you handle an underperforming teammate", "how do you onboard someone", "describe a time you delegated something you would rather have done yourself".
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

### 5. The autonomous Mars rover (technical depth, end-to-end ownership)
**Source:** CV and personal site
**What happened:** A four-wheeled rover that maps, localizes, and navigates autonomously — ROS 2 and SLAM on a Raspberry Pi 4 for perception and decisions, with a low-level Arduino system for motor drivers, encoder feedback, and PID control.
**Why it matters:** Your strongest robotics artifact, and it spans the full stack from high-level autonomy to motor control. Answers "walk me through a project you are proud of", "tell me about a time you integrated two systems", "what would you do differently".
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

### 6. Officiating hockey (composure, conflict, authority)
**Source:** LinkedIn — Hockey Eastern Ontario, 2.5 years
**What happened:** Officiated games for players aged 7-15, making split-second rulings, managing on-ice conflict, and enforcing safety rules while dealing with players, coaches, and other officials.
**Why it matters:** Non-technical, memorable, and it directly addresses the thing you named as your own friction point — holding authority and being taken seriously as the youngest person in the room. Answers "tell me about a high-pressure decision", "describe a conflict you defused", "a time someone disagreed with your call".
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

### 7. The buck converter design (hardware depth)
**Source:** LinkedIn — QADT Electrical Engineer
**What happened:** Designed buck converter circuits in LTspice and Altium stepping 44V down to 15V, 5.2V, and 3.3V; analyzed datasheets to select component values; proposed a modular 12S 3P battery architecture.
**Why it matters:** Only needed for embedded, hardware, or controls interviews, where it shows real electrical competence rather than software-only robotics. Answers "tell me about a hardware design decision", "how do you work from a datasheet".
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

## Common Tough Questions

### "Walk me through how you got to \$1,000,000 in client savings."

**This now has a real derivation. Learn it cold — it is the single most likely
follow-up question in any interview, and answering it well is a differentiator.**

**The answer, in the order to say it:**

1. **The problem.** A large Cavtera client ran 100+ trucks and 1,000+ pieces of equipment that were **previously untracked entirely**. Equipment sat on jobsites depreciating and unused, with no visibility into whether another site needed it more.
2. **The measurement — lead with this, it is the strongest part.** Once the Equipment Management System instrumented the fleet, it showed **10,000+ equipment-hours per week sitting idle** while other jobsites needed those units. That is a measured figure from the system, not an estimate.
3. **The arithmetic, with assumptions stated out loud.** ~10,000 idle hours/week annualizes to roughly **500,000 idle equipment-hours per year** at 50 weeks. Recovering even **10%** of that, valued conservatively at about **\$20 per equipment-hour**, is **~\$1,000,000 per year**.
4. **Show you know it is conservative.** Reaching only \$1M against 500,000 annual idle hours implies about **\$2/hour**, far below any real construction equipment rate. The figure has substantial headroom, which is exactly why you are comfortable stating it.
5. **Be precise about the verb.** The system *exposed* \$1M+ in recoverable cost. Turning it into cash required the client to reallocate equipment. Say this unprompted — volunteering the distinction between identified and realized savings reads as commercial maturity, and it pre-empts the sharpest version of the follow-up.

**Anticipate these follow-ups:**

- *"Where does \$20/hour come from?"* — Own it as an assumption, not a lookup: it is a deliberately conservative stand-in for the blended cost of owning an idle unit (depreciation, financing, insurance, and the rental you pay elsewhere because this one is stranded). Say you would refine it per equipment class with the client's own rates.
- *"Did they actually realize the savings?"* — Utilization improved after the automated alerts shipped. Be honest that you do not have an audited post-deployment delta, and say what you would measure: idle hours per unit per week, before versus after, by equipment class.
- *"Isn't some idle time unavoidable?"* — Yes, and this is a good sign you understand the domain. Equipment needs maintenance windows, weather stops work, and some slack is deliberate. That is precisely why the derivation recovers only 10% rather than all of it.

**Two things worth doing before the Cavtera contract ends in September 2026, while
you still have access:**

1. **Quantify the post-alert utilization improvement.** With a measured before/after, "saved" becomes fully supportable and you can drop the hedge entirely.
2. **Ask the account lead whether the client stated its own savings figure.** An attributed number cannot be attacked, only checked — it is the strongest possible version of this claim.

### "You are a third-year student. Why should we give you this?"
> Answer with scope, not enthusiasm: over a year of paid production software
> work across two employers, systems that operations staff use daily, and a
> 15-person team whose software stack you own. Then the availability point — you
> can commit 12-16 months, where most candidates offer four.

### "Why are you leaving Cavtera?"
> Nothing to defend here: it was a summer contract with a defined September 2026
> end date, taken while studying. Say that plainly and move to what you are
> looking for next. No negativity, no over-explanation.

### "You do not have any machine learning / cloud / large-scale production experience."
> Acknowledge it directly, then bridge honestly. You have shipped production
> data pipelines and full-stack applications, and you have the mathematical
> foundation (A+ in linear algebra, calculus, complex analysis, signals and
> systems; probability and numerical optimization upcoming). Do not oversell the
> AIP certificate as ML experience. Name what you would need to learn and how
> you have taught yourself comparable things before — Foundry itself was learned
> on the job.

### "How do you handle work that is routine or unglamorous?"
> **Highest-risk question for you**, given that mundane tasks genuinely drain
> you. Do not say that. Every engineering role contains migration, maintenance,
> documentation, and support. Answer with a real instance of doing unexciting
> work well — normalizing thousands of rows of messy truck data is not
> glamorous, and neither is maintaining a cross-platform Docker build — and then
> what you do to stay engaged: automating it, or understanding why it exists.

### "Where do you see yourself in 5 years?"
> You have a real answer: significant technical responsibility at a company
> working on hard problems, or founding something. Tie it to the role — what you
> want to learn from *this* team that gets you there. Avoid implying you will
> leave to start a company at the first opportunity.

### "What is your biggest weakness?"
> Use impatience with slow-moving or low-standards environments, framed
> concretely and with a mitigation you actually practice. Do not use the version
> where the weakness is other people; "I do not love working with mundane
> employees" is true but must never be said in an interview.

### "Why this company specifically?"
> Customize per company. Must reference: specific projects, company values, market position, or team structure. Never give a generic answer.

### Questions to ask about the placement term
> Because the 12-16 month window is central, ask directly: Can the internship be
> extended beyond the standard term? Do you take co-op students for 12 months? If
> the answer is a fixed 12-16 weeks, ask about returning for a second term. And
> for anything outside Canada, ask early who handles work authorization and
> whether they have sponsored a Canadian student before.

### "Why this company specifically?"
> Customize per company. Must reference: specific projects, company values, market position, or team structure. Never give a generic answer.

## Questions You Should Ask Interviewers

### About the Role
- "What does a typical week look like in this role?"
- "What would success look like in the first 6 months?"
- "What's the biggest challenge the team is facing right now?"

### About the Team
- "How big is the team, and how do you divide work?"
- "What does the development/project lifecycle look like, from idea to production?"
- "How do you onboard new team members?"

### About Tech & Growth
- "What's your current tech stack for [relevant area]?"
- "Is there room to grow into more architectural or strategic decisions?"
- "How does the team stay current with new tools and methods?"

### About Culture (use these to prevent disappointment)
- "How would you describe the team culture?"
- "What does professional development look like here?"
- "Is there flexibility for remote/hybrid work?"
- "What's the balance between development/new projects and maintenance work?"
- "How would you describe the leadership style in this team?"
- "What do people who thrive here have in common?"

## Phone/Video Interview Tips
- Have STAR examples written out (use this file)
- Keep a glass of water nearby
- Smile when speaking (it changes your tone)
- Ask for clarification if a question is vague
- It's OK to take 5 seconds to think before answering
- End with: "Is there anything else you'd like to know about my background?"

## After the Application (Best Practice)

### Follow-Up Etiquette
- **Don't call to "stand out"** or to learn more about the role post-submission - this risks a negative impression
- If the employer specified a timeline, respect it and wait
- If no timeline was given and significant time has passed (2+ weeks), a brief call to ask about status is acceptable
- If you have genuinely new, relevant information to share, a short follow-up is fine

### Thank-You Notes
- When you receive any update (interview invitation, rejection, or status update), send a brief thank-you message
- Express appreciation for their time and the process
- Keep it short (2-3 sentences)

## Roleplay Guidelines
When the user asks for interview practice:
1. Ask which role/company to simulate
2. Start with easy warm-up questions ("Tell me about yourself")
3. Progress to role-specific technical questions
4. Include 1-2 behavioral questions using the competencies from the job posting
5. End with a tough question or curveball
6. After each answer, give brief feedback: what worked, what to sharpen
7. Suggest which STAR example would work best for each question
