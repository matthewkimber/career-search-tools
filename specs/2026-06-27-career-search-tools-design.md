# Career Search Tools — Plugin Design

**Date:** 2026-06-27
**Status:** Approved

---

## Context

Job searching is repetitive and cognitively expensive. People spend hours manually customizing resumes and cover letters, struggling to research companies consistently, and losing track of where they are across multiple active applications. This plugin provides a structured, compounding toolkit that gets smarter the more context a user builds up — each piece of research and each piece of writing feeds the next skill invoked.

**Target platforms:** Claude Code and Claude Cowork (identical plugin format).
**Distribution:** Public, designed for any job seeker (not personally opinionated).
**Automation level:** AI-assisted, human-executes — no MCP dependency required. Zero setup friction.
**Persistence:** File-based. All data lives in a `job-search/` directory in the user's project, which all skills read and write.

---

## Data Model

The `job-search/` directory is created by `/setup-profile` and lives at `${CLAUDE_PROJECT_DIR}/job-search/`. All skills reference this location.

```
job-search/
  profile/
    profile.md          ← background, skills, experience, work history
    narrative.md        ← positioning statement, target roles, value prop, "story"
    references.md       ← reference contacts, relationship notes, primed for which roles
  companies/
    <company-slug>/
      research.md       ← overview, culture, news, financials, key leadership (shared)
      positions/
        <role-slug>/
          jd.md         ← full job description
          team.md       ← hiring manager, panel, key contacts for this role
          materials.md  ← tailored resume + cover letter variants
          outreach.md   ← cold/warm outreach drafts, sent status, replies
          tracking.md   ← status, interview notes, next steps, offer details
  pipeline.md           ← cross-company, cross-position status dashboard
```

**Key design principle:** Company-level research (`research.md`) is written once and shared across all positions at that company. Position-level files are scoped to a specific role, supporting multiple active applications at the same company simultaneously. Slugs are kebab-case (e.g., `acme-corp`, `senior-software-engineer`).

---

## Skills (14 total)

### Foundation

**`/setup-profile`**
Guided two-phase onboarding. Phase 1 collects professional facts (background, skills, work history, education) and writes `profile.md`. Phase 2 synthesizes a positioning statement, target role definition, and unique value prop into `narrative.md`. Users can re-run either phase independently to update their profile. If `job-search/` doesn't exist, creates the full directory structure.

**Output:** `job-search/profile/profile.md`, `job-search/profile/narrative.md`, `job-search/profile/references.md` (empty template for reference contacts)

---

### Company Research

**`/research-company <company>`**
Generates a structured company research brief using a template (`templates/research-template.md`). Covers: company overview, business model, revenue/funding, products/services, culture and values, recent news, key leadership and their backgrounds, competitive landscape, and "why this company" angles. Instructs user on what to research and how, then synthesizes a formatted `research.md` from what they provide.

**Output:** `job-search/companies/<company-slug>/research.md`

---

### Position Management

**`/add-position <company> <role>`**
Initializes the position directory structure and prompts the user to paste the job description. Writes `jd.md` with the full JD plus a skills/requirements extraction. Confirms the position is now ready for other skills.

**Output:** `job-search/companies/<company-slug>/positions/<role-slug>/jd.md`

**`/find-hiring-team <company> <role>`**
Reads `jd.md` and `research.md`, then produces a structured guide for identifying the hiring manager, likely panel members, and adjacent influential contacts (e.g., potential skip-level, peers who might be interviewers). Includes specific search strategies (LinkedIn, company website, GitHub, conference talks, press) and a template for recording what's found. User fills in, skill formats into `team.md`.

**Output:** `job-search/companies/<company-slug>/positions/<role-slug>/team.md`

---

### Application Materials

**`/tailor-resume <company> <role> [template]`**
Reads `profile.md`, `narrative.md`, `research.md`, and `jd.md`. Proceeds in three steps:

1. **Template selection** — Presents available templates and prompts the user to select one (or uses the preferred template saved in `profile.md` if set). Saves the choice as the new default.
2. **Content tailoring** — Reorders and rewords experience bullets to match JD language, surfaces relevant skills, adjusts the summary/headline to match the chosen template's structure and section order.
3. **ATS optimization pass** — Performs a keyword gap analysis: extracts high-signal terms and required skills from `jd.md`, checks coverage in the tailored draft, and flags any missing terms with suggestions for where to naturally incorporate them. Includes a summary of ATS compliance (keyword coverage score, any formatting warnings).

All output follows the ATS safety rules defined in `skills/tailor-resume/ats-optimization.md`.

**Templates** (shipped in `skills/tailor-resume/templates/`):
All four templates are ATS-safe by design: standard section headings, single-column layout, no tables or graphics, plain-text contact info, consistent date formatting, no special Unicode characters. Each template file includes an ATS compliance note.
- `classic.md` — traditional chronological, safe for any industry
- `modern.md` — clean, contemporary layout; ATS-optimized single-column
- `executive.md` — senior/leadership roles; emphasizes scope, team size, and business impact
- `tech.md` — engineering roles; skills and projects section is prominent

**Supporting files:**
- `skills/tailor-resume/ats-optimization.md` — canonical ATS safety rules: approved section headings, formatting constraints, keyword strategy, file export guidance (`.docx` preferred over `.pdf` for most ATS)

**Output:** Appends to `job-search/companies/<company-slug>/positions/<role-slug>/materials.md`

**`/write-cover-letter <company> <role>`**
Reads `profile.md`, `narrative.md`, `research.md`, `jd.md`, and `team.md` (if available). Writes a cover letter that references the specific role, demonstrates knowledge of the company, connects the user's narrative to the company's needs, and names the hiring manager if known. Appends to `materials.md`.

**Output:** Appends to `job-search/companies/<company-slug>/positions/<role-slug>/materials.md`

**`/optimize-linkedin`**
Reads `profile.md` and `narrative.md`. Produces section-by-section LinkedIn optimization: headline, about section, experience bullets, skills to feature, featured section ideas, and connection/engagement recommendations. Output is ready to copy-paste and always saved to `job-search/profile/linkedin-draft.md` for reference.

**`/build-personal-site`**
Reads `profile.md` and `narrative.md`. Generates copy for a personal/portfolio website: a bio (short and long variants), a headline and tagline, project and experience write-ups formatted for a web audience, a skills section, and a contact page blurb. Output is written to `job-search/profile/personal-site-draft.md`, organized by page/section so it can be dropped into any site builder (Notion, Framer, GitHub Pages, etc.) without restructuring.

---

### Outreach

**`/outreach <person> <company> <role>`**
Reads `profile.md`, `narrative.md`, `research.md`, and `team.md`. Generates multiple outreach variants depending on relationship type: cold outreach to recruiter, cold outreach to hiring manager, warm outreach through a mutual connection, and LinkedIn connection request note. Each variant is concise, specific, and avoids generic openers. Writes drafts to `outreach.md` with placeholders for personalization.

**Output:** `job-search/companies/<company-slug>/positions/<role-slug>/outreach.md`

---

### ATS Application

**`/apply-ats <company> <role> [system]`**
Reads `profile.md`, `narrative.md`, `jd.md`, and `materials.md`. Generates pre-written answers for common ATS fields (work authorization, years of experience, salary expectations, short-answer questions, diversity questions) tailored to the role. If `[system]` is provided (e.g., `workday`, `greenhouse`, `lever`), uses ATS-specific field reference files (`ats-fields/<system>.md`) to match the exact field names and formats of that platform. Output is structured for easy copy-paste, with fields clearly labeled.

**Supporting files:** `ats-fields/workday.md`, `ats-fields/greenhouse.md`, `ats-fields/lever.md`

---

### Interview

**`/prep-interview <company> <role>`**
Reads all available context files for the company/position. Produces a comprehensive interview prep document: likely question categories and specific questions based on the JD and team research, STAR story suggestions mapped from `profile.md`, company-specific questions to ask, research gaps to fill before the interview, and a one-page cheat sheet of key facts about the company. Saves to `tracking.md`.

**Output:** Appends to `job-search/companies/<company-slug>/positions/<role-slug>/tracking.md`

**`/post-interview <company> <role>`**
Prompts user to share key moments from the interview (who they met, what was discussed, how it felt). Generates: a personalized thank you note for each interviewer (differentiated, references specific conversation points), a structured debrief (what went well, areas to address, open questions about the role), and a status update for `tracking.md`.

**Output:** Appends to `job-search/companies/<company-slug>/positions/<role-slug>/tracking.md`

---

### Pipeline & Decision

**`/pipeline`**
Reads all `tracking.md` files across the `job-search/companies/` tree. Generates a formatted dashboard: active opportunities by stage (researching / applied / outreach sent / interviewing / offer), overdue follow-ups, upcoming interview dates, and recommended next actions by company/role. Updates `pipeline.md`.

**Output:** `job-search/pipeline.md`

**`/analyze-offer <company> <role>`**
Reads `jd.md`, `research.md`, `tracking.md`, and all other available context. Prompts user to enter offer details (base, equity, bonus, benefits, PTO, remote policy). Produces: total comp estimate and breakdown, market benchmarking guidance (where to check and what to look for), comparison framework if evaluating multiple offers, and a negotiation positioning brief (what levers exist, what's standard to push on, how to phrase the ask).

**Output:** Appends to `job-search/companies/<company-slug>/positions/<role-slug>/tracking.md`

---

## Agent (1)

**`interview-coach`** (`agents/interview-coach.md`)

An interactive mock interview agent. On invoke, it reads `research.md`, `team.md`, `jd.md`, and `profile.md` for the specified company and role, then conducts a realistic mock interview: asks questions in sequence (behavioral, technical, situational), provides feedback on each answer, tracks patterns across responses, and at the end delivers a structured debrief with specific improvement suggestions. Saves session notes to `tracking.md`.

```
model: sonnet
maxTurns: 30
disallowedTools: Write, Edit
```

---

## Hook (1)

**`SessionStart`** (`hooks/hooks.json`)

If `job-search/pipeline.md` exists in the project directory, prints a brief pipeline summary at session start: count of active applications, any overdue follow-ups, and upcoming interviews. Fires only when pipeline data is present — zero noise for new users or non-job-search sessions.

---

## Plugin Layout

```
career-search-tools/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── setup-profile/
│   │   └── SKILL.md
│   ├── research-company/
│   │   ├── SKILL.md
│   │   └── templates/
│   │       └── research-template.md
│   ├── add-position/
│   │   └── SKILL.md
│   ├── find-hiring-team/
│   │   └── SKILL.md
│   ├── tailor-resume/
│   │   ├── SKILL.md
│   │   ├── ats-optimization.md
│   │   └── templates/
│   │       ├── classic.md
│   │       ├── modern.md
│   │       ├── executive.md
│   │       └── tech.md
│   ├── write-cover-letter/
│   │   └── SKILL.md
│   ├── optimize-linkedin/
│   │   └── SKILL.md
│   ├── build-personal-site/
│   │   └── SKILL.md
│   ├── outreach/
│   │   └── SKILL.md
│   ├── apply-ats/
│   │   ├── SKILL.md
│   │   └── ats-fields/
│   │       ├── workday.md
│   │       ├── greenhouse.md
│   │       └── lever.md
│   ├── prep-interview/
│   │   └── SKILL.md
│   ├── post-interview/
│   │   └── SKILL.md
│   ├── pipeline/
│   │   └── SKILL.md
│   └── analyze-offer/
│       └── SKILL.md
├── agents/
│   └── interview-coach.md
├── hooks/
│   └── hooks.json
├── docs/
│   ├── README.md
│   ├── installation.md
│   ├── usage-guide.md
│   └── ats-guide.md
├── LICENSE
└── CHANGELOG.md
```

---

## User Documentation

Documentation lives in `docs/` and is a first-class deliverable alongside the skills.

### `docs/README.md`
- What the plugin does (one paragraph)
- Feature list (14 skills + interview coach agent)
- Quick start (4-step path from install to first tailored resume)
- Links to `installation.md` and `usage-guide.md`

### `docs/installation.md`
Step-by-step install for both platforms:

**Claude Code:**
1. `claude plugin install career-search-tools` (marketplace), or `claude plugin install --plugin-dir ./career-search-tools` (local clone)
2. Verify: `/plugin list` shows `career-search-tools` as enabled
3. Run `/setup-profile` to initialize `job-search/`

**Claude Cowork:**
1. Open plugin marketplace, search `career-search-tools`, install
2. Grant file system access to your job search project folder when prompted
3. Run `/setup-profile` to initialize

Also covers: scope guidance (user vs. project install), troubleshooting (`claude plugin validate`, `/plugin` errors tab).

### `docs/usage-guide.md`
Full narrative walkthrough of the recommended workflow, phase by phase:

- **Phase 1 — Profile Setup** (one-time): `/setup-profile`
- **Phase 2 — Target a Company**: `/research-company`, `/add-position`, `/find-hiring-team`
- **Phase 3 — Apply**: `/tailor-resume`, `/write-cover-letter`, `/apply-ats`
- **Phase 4 — Outreach**: `/outreach` (timing tips: before vs. after applying)
- **Phase 5 — Interview**: `/prep-interview`, `interview-coach` agent, `/post-interview`
- **Phase 6 — Track and Decide**: `/pipeline` (run weekly), `/analyze-offer`

Includes: real-looking example commands with company/role slugs, example output snippets, and guidance on what to do when context files are missing.

### `docs/ats-guide.md`
The single user-facing reference for all ATS concerns — both resume safety and application form fields.

**Resume ATS safety:**
- Why ATS safety matters and how the plugin enforces it
- What makes a resume ATS-unsafe (tables, columns, graphics, non-standard headings, special characters)
- How to export: `.docx` vs. `.pdf` guidance per ATS system
- How the keyword gap analysis in `/tailor-resume` works

**Application form fields:**
- Supported systems: Workday, Greenhouse, Lever
- Common fields per system and how the plugin handles them
- Tips per platform (Workday character limits, Greenhouse screening questions, etc.)
- How to request support for a new ATS (GitHub issue template link)

---

## Verification

1. `claude plugin validate ./career-search-tools` — passes with no errors
2. `claude plugin install --plugin-dir ./career-search-tools`
3. `/setup-profile` in a fresh directory → `job-search/profile/` created with all three files
4. `/research-company acme-corp` → `job-search/companies/acme-corp/research.md` created
5. `/add-position acme-corp senior-engineer` with pasted JD → position directory created
6. `/tailor-resume acme-corp senior-engineer` → reads profile + JD, writes to `materials.md`
7. `/pipeline` → reads tracking files, writes `pipeline.md`, displays dashboard
8. `interview-coach` agent → loads role context, conducts multi-turn mock interview
9. `SessionStart` hook → fires pipeline summary when `pipeline.md` exists, silent otherwise
10. All docs render correctly in a Markdown viewer
