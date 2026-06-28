# Usage Guide

## The Workflow

Career Search Tools is designed around a 6-phase workflow. Each phase builds on the last.

---

## Phase 1: Profile Setup (one-time, ~15 minutes)

```
/setup-profile
```

The skill walks you through two phases:
1. **Professional Facts** — your work history, skills, education, and projects
2. **Narrative** — your positioning statement, target roles, and preferred resume template

**Output:**
- `job-search/profile/profile.md` — your professional facts
- `job-search/profile/narrative.md` — your story and positioning
- `job-search/profile/references.md` — an empty references template to fill in

**To update your profile later:** run `/setup-profile` again and choose which phase to re-run.

---

## Phase 2: Target a Company

```
/research-company acme-corp
/add-position acme-corp senior-software-engineer
/find-hiring-team acme-corp senior-software-engineer
```

**`/research-company <company>`**
Guides you through structured company research. You'll be directed to check LinkedIn, Crunchbase, Glassdoor, and recent news. The skill synthesizes what you find into `research.md`.

*Tip: use exact company slugs (kebab-case). "Acme Corp" becomes `acme-corp`.*

**`/add-position <company> <role>`**
Paste the full job description when prompted. The skill extracts must-have skills and ATS keywords automatically.

**`/find-hiring-team <company> <role>`**
Guides you to find the hiring manager, likely panel, and recruiter on LinkedIn. Records findings in `team.md`.

---

## Phase 3: Apply

```
/tailor-resume acme-corp senior-software-engineer
/write-cover-letter acme-corp senior-software-engineer
/export-resume acme-corp senior-software-engineer
/apply-ats acme-corp senior-software-engineer workday
```

**`/tailor-resume`**
Produces a resume tailored to the JD. Includes an ATS keyword gap analysis — missing keywords are flagged with suggested placements.

**`/write-cover-letter`**
Writes a concise, specific cover letter that references the company's actual work and addresses the hiring manager by name (if found).

**`/export-resume`**
Exports to DOCX by default. Options:
- `/export-resume acme-corp senior-software-engineer` → `resume.docx`
- `/export-resume acme-corp senior-software-engineer json` → `resume.json`
- `/export-resume acme-corp senior-software-engineer pdf` → `resume.pdf` (requires PDF engine)

**`/apply-ats`**
Generates pre-written answers for common ATS fields. If you know the ATS, add it as an argument: `workday`, `greenhouse`, or `lever`.

---

## Phase 4: Outreach

```
/outreach "Jane Smith" acme-corp senior-software-engineer
```

Generates cold and warm outreach variants: LinkedIn connection request, LinkedIn message, email, and warm intro (if applicable).

*Tip: send outreach before or after applying — both approaches work. Before applying builds a relationship; after applying follows up on a submitted application.*

---

## Phase 5: Interview

```
/prep-interview acme-corp senior-software-engineer
# Then practice with the agent:
# "interview-coach for acme-corp senior-software-engineer"
/post-interview acme-corp senior-software-engineer
```

**`/prep-interview`** — generates likely questions, STAR story suggestions, and a company cheat sheet. Saved to `tracking.md`.

**`interview-coach` agent** — conducts a realistic mock interview with per-answer feedback. Start by saying: *"interview-coach for acme-corp senior-software-engineer"*

**`/post-interview`** — run within 24 hours of any interview. Generates distinct thank-you notes for each interviewer and a structured debrief.

---

## Phase 6: Track and Decide

```
/pipeline
/analyze-offer acme-corp senior-software-engineer
```

**`/pipeline`** — reads all `tracking.md` files and generates a cross-company status dashboard. Run weekly.

**`/analyze-offer`** — enter offer details to get total comp estimate, market benchmarking guidance, and a negotiation script.

---

## Tips

**Missing context files:** If a skill can't find a file (e.g., `research.md` doesn't exist yet), it will ask you to provide the missing information inline. You don't need to run skills in strict order — though the workflow above produces the best results.

**Multiple positions at one company:** Run `/add-position <company> <role>` multiple times with different role names. Each gets its own directory.

**Updating your profile:** Re-run `/setup-profile` at any time to refresh either phase. All downstream files remain unchanged — they use the profile at the time each skill was run.
