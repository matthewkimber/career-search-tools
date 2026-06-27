# Career Search Tools — Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a distributable Claude Code + Claude Cowork plugin with 15 skills, 1 agent, and 1 hook that helps job seekers from profile setup through offer analysis.

**Architecture:** A prompt-driven plugin — the implementation is SKILL.md files that instruct Claude to read and write structured Markdown files in a `job-search/` directory in the user's project. No MCP server required. One exception: `/export-resume` shells out to pandoc for DOCX generation via Claude's Bash tool.

**Tech Stack:** Claude plugin format (SKILL.md, agent .md, hooks.json, plugin.json), Pandoc ≥ 3.0 (DOCX/PDF export), JSON Resume v1.0.0 schema (portability export).

## Global Constraints

- Plugin format: Claude Code / Claude Cowork (identical)
- All skills read/write `${CLAUDE_PROJECT_DIR}/job-search/`
- Plugin assets referenced via `${CLAUDE_PLUGIN_ROOT}`
- Directory slugs: kebab-case only (e.g. `acme-corp`, `senior-software-engineer`)
- All resume output must be ATS-safe: standard headings, single-column, no tables, no graphics, no special Unicode chars
- Resume markdown templates must mirror JSON Resume v1.0.0 section hierarchy
- Export requires Pandoc ≥ 3.0 (DOCX); PDF engine optional (LaTeX or wkhtmltopdf)
- Git workflow: GitHub Flow — feature branch per phase, PR to main before next phase
- Specs: `./specs/` | User docs: `./docs/` | Plans: `./docs/superpowers/plans/`

---

## Phase 1 — Plugin Scaffold
*Deliverable: a valid, installable plugin with no skills yet. Every subsequent phase builds on this.*

---

### Task 1: Directory structure + plugin.json

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `skills/` (empty, populated in later tasks)
- Create: `agents/` (empty)
- Create: `hooks/` (empty)
- Create: `docs/` (empty, populated in Phase 9)

**Interfaces:**
- Produces: an installable plugin skeleton that passes `claude plugin validate`

- [ ] **Step 1: Create the directory skeleton**

```bash
mkdir -p .claude-plugin skills agents hooks docs
```

- [ ] **Step 2: Write plugin.json**

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "career-search-tools",
  "displayName": "Career Search Tools",
  "version": "0.1.0",
  "description": "A structured toolkit to help job seekers build materials, research companies, prepare for interviews, and track applications.",
  "author": {
    "name": "Matthew Kimber",
    "url": "https://github.com/matthewkimber/career-search-tools"
  },
  "repository": "https://github.com/matthewkimber/career-search-tools",
  "license": "Apache-2.0",
  "keywords": ["career", "job-search", "resume", "interview", "outreach"]
}
```

- [ ] **Step 3: Validate the plugin**

```bash
claude plugin validate .
```

Expected output: no errors. Warnings about empty component directories are acceptable.

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/ skills/ agents/ hooks/ docs/
git commit -m "feat: scaffold plugin structure and manifest"
```

---

## Phase 2 — Foundation
*Deliverable: users can run `/setup-profile` to create their job-search profile. Standalone useful.*

---

### Task 2: setup-profile skill

**Files:**
- Create: `skills/setup-profile/SKILL.md`

**Interfaces:**
- Produces:
  - `${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md`
  - `${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md`
  - `${CLAUDE_PROJECT_DIR}/job-search/profile/references.md`
  - Full `job-search/` directory tree

- [ ] **Step 1: Create skill directory**

```bash
mkdir -p skills/setup-profile
```

- [ ] **Step 2: Write SKILL.md**

```markdown
---
name: setup-profile
description: First-time job search profile setup. Run this before any other skill. Creates your professional profile, positioning narrative, and references template in job-search/profile/.
---

You are helping the user set up their job search profile. Work through the following two phases in order. If job-search/ already exists, ask the user whether they want to update Phase 1, Phase 2, or both.

## Setup

Create the following directory structure if it does not exist:
- ${CLAUDE_PROJECT_DIR}/job-search/profile/
- ${CLAUDE_PROJECT_DIR}/job-search/companies/

## Phase 1: Professional Facts

Ask the user for the following, one section at a time. Do not ask all at once.

1. **Full name and contact info** (email, phone, LinkedIn URL, location — city/state only)
2. **Professional summary** (ask them to describe their background in 2–3 sentences; you will refine it)
3. **Work history** (company, title, dates, 3–5 bullet accomplishments each — most recent first)
4. **Education** (institution, degree, field, year)
5. **Skills** (technical skills, tools, languages, methodologies — ask them to list freely)
6. **Certifications and awards** (if any)
7. **Notable projects** (name, description, your role, outcome)

After collecting all sections, write the following file:

**${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md**

Use this structure exactly:
```
# Professional Profile

## Contact
[name, email, phone, LinkedIn, location]

## Summary
[2–3 sentence refined summary]

## Work Experience
### [Title] — [Company] ([Start]–[End])
- [Accomplishment bullet]
- [Accomplishment bullet]
- [Accomplishment bullet]

## Education
### [Degree] in [Field] — [Institution] ([Year])

## Skills
### Technical
[comma-separated list]
### Methodologies
[comma-separated list]

## Certifications & Awards
- [item]

## Projects
### [Project Name]
[Description | Role | Outcome]
```

## Phase 2: Professional Narrative

Now help the user articulate their positioning. Ask:
1. **Target roles** — What job titles are they pursuing? What level (IC, manager, director)?
2. **Target industries** — Are there specific sectors they prefer or want to avoid?
3. **Unique value** — What do they do better than most people with similar backgrounds?
4. **Career story** — What is the through-line of their career? What problem do they keep solving?
5. **Preferred template** — Show them the four resume templates and ask which style fits their industry: `classic` (traditional), `modern` (contemporary), `executive` (senior leadership), `tech` (engineering). Save their answer as `preferred_template: <name>` in the narrative file.

After collecting answers, write:

**${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md**

Use this structure exactly:
```
# Professional Narrative

## Target Roles
[titles and level]

## Target Industries
[sectors]

## Positioning Statement
[1–2 sentences: who you are, what you uniquely offer, who you serve]

## Unique Value Proposition
[3–5 bullet points of differentiators]

## Career Story
[3–5 sentence through-line narrative]

## Preferred Resume Template
preferred_template: [classic|modern|executive|tech]
```

## Phase 3: References Template

Write an empty template:

**${CLAUDE_PROJECT_DIR}/job-search/profile/references.md**

```
# References

| Name | Title | Company | Relationship | Contact | Primed For |
|------|-------|---------|--------------|---------|------------|
|      |       |         |              |         |            |
```

## Completion

Tell the user:
- Profile created at job-search/profile/
- Run /research-company <company> to start targeting a company
- Run /optimize-linkedin to optimize your LinkedIn profile using this data
```

- [ ] **Step 3: Install and validate**

```bash
claude plugin validate .
claude plugin install --plugin-dir .
```

Expected: plugin installs, `/setup-profile` appears in skill list.

- [ ] **Step 4: Smoke test**

Start Claude Code in a temp directory and run `/setup-profile`. Verify:
- It asks questions in phases, not all at once
- `job-search/profile/profile.md` is created with correct structure
- `job-search/profile/narrative.md` is created with `preferred_template:` line
- `job-search/profile/references.md` is created with the table template

- [ ] **Step 5: Commit**

```bash
git add skills/setup-profile/
git commit -m "feat: add setup-profile skill"
```

---

## Phase 3 — Research
*Deliverable: users can research a company and set up a position. Requires Phase 2 profile.*

---

### Task 3: research-company skill + research template

**Files:**
- Create: `skills/research-company/SKILL.md`
- Create: `skills/research-company/templates/research-template.md`

**Interfaces:**
- Consumes: `${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md` (target industries)
- Produces: `${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/research.md`

- [ ] **Step 1: Create directories**

```bash
mkdir -p skills/research-company/templates
```

- [ ] **Step 2: Write research-template.md**

```markdown
# Company Research: [Company Name]

## Overview
**Industry:** 
**Founded:** 
**Size:** 
**HQ:** 
**Business Model:** 

## Products & Services
[What they make/do]

## Financial Health
**Revenue / Funding:** 
**Recent news:** 

## Culture & Values
**Stated values:** 
**Glassdoor themes:** 
**Work style (remote/hybrid/in-office):** 

## Key Leadership
| Name | Title | Background |
|------|-------|------------|
|      |       |            |

## Competitive Landscape
**Main competitors:** 
**Differentiators:** 

## Why This Company
[Genuine reasons this company aligns with your targets — fill after research]

## Research Sources
- [ ] Company website (About, Blog, Careers)
- [ ] LinkedIn company page
- [ ] Crunchbase / PitchBook
- [ ] Glassdoor reviews
- [ ] Recent press (Google News)
- [ ] Earnings calls / investor relations (if public)
```

- [ ] **Step 3: Write SKILL.md**

```markdown
---
name: research-company
description: Research a target company and create a structured company profile. Run before add-position or find-hiring-team. Usage: /research-company <company-name>
---

The user wants to research a company for their job search. The company name is provided as an argument.

## Setup

1. Convert the company name to a kebab-case slug (e.g. "Acme Corp" → "acme-corp").
2. Create directory: ${CLAUDE_PROJECT_DIR}/job-search/companies/<slug>/
3. Copy the research template from ${CLAUDE_PLUGIN_ROOT}/skills/research-company/templates/research-template.md to ${CLAUDE_PROJECT_DIR}/job-search/companies/<slug>/research.md, replacing [Company Name] with the actual name.

## Research Guidance

Tell the user exactly what to look up and where, then ask them to share what they find section by section. Guide them through each section:

1. **Overview & financials** — Ask them to visit the company website (About page), LinkedIn company page, and Crunchbase. Ask: "What does the company do? How big are they? How are they funded?"

2. **Culture** — Ask them to read Glassdoor reviews (sort by most recent). Ask: "What do employees say about the culture, management, and work-life balance? What themes come up repeatedly?"

3. **Leadership** — Ask them to find the executive team on LinkedIn or the company website. Request: name, title, and a one-line background for each C-suite and relevant VP/director.

4. **Recent news** — Ask them to Google "[company name] news" filtered to the past 6 months. Ask: "What has the company announced recently? Any layoffs, expansions, product launches, or executive changes?"

5. **Why this company** — Based on everything gathered, help them articulate 3–5 genuine reasons this company aligns with their target roles and values from narrative.md.

## Output

Fill in the research.md template with everything gathered. Write clearly and concisely — this file will be read by multiple other skills. End with a checklist of which research sources were consulted.

Tell the user:
- Research saved to job-search/companies/<slug>/research.md
- Run /add-position <company> <role> to add a specific position you're targeting
```

- [ ] **Step 4: Install, validate, smoke test**

```bash
claude plugin validate .
```

Run `/research-company acme-corp` in a test session. Verify:
- Directory `job-search/companies/acme-corp/` is created
- `research.md` is populated from the template with company name substituted
- Skill asks for info section by section, not all at once

- [ ] **Step 5: Commit**

```bash
git add skills/research-company/
git commit -m "feat: add research-company skill with guided template"
```

---

### Task 4: add-position skill

**Files:**
- Create: `skills/add-position/SKILL.md`

**Interfaces:**
- Consumes: `${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/research.md` (optional, for context)
- Produces: `${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/jd.md`

- [ ] **Step 1: Create directory**

```bash
mkdir -p skills/add-position
```

- [ ] **Step 2: Write SKILL.md**

```markdown
---
name: add-position
description: Add a specific job position you're targeting at a company. Paste in the job description. Usage: /add-position <company> <role>
---

The user wants to add a position they're targeting. Arguments: company name, role title.

## Setup

1. Convert both arguments to kebab-case slugs.
2. Create directory: ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/
3. Also create empty placeholder files for later skills:
   - team.md (empty)
   - materials.md (empty)
   - outreach.md (empty)
   - tracking.md with initial status header (see below)

## Job Description

Ask the user to paste the full job description. Do not truncate it.

After they paste it, extract and structure the following into jd.md:

**${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/jd.md**

```
# Job Description: [Role Title] at [Company]

**URL:** [ask user for the job posting URL]
**Date Added:** [today's date]
**Status:** Researching

## Full Job Description
[paste verbatim]

## Extracted Requirements

### Must-Have Skills
[bullet list extracted from JD — be specific, use JD's exact language]

### Nice-to-Have Skills
[bullet list]

### Key Responsibilities
[bullet list of the 5–7 most important duties]

### Keywords for ATS
[comma-separated list of all high-signal technical terms, tools, methodologies from the JD — these are used by /tailor-resume for keyword gap analysis]
```

## Initialize tracking.md

Write the following to tracking.md:
```
# Tracking: [Role Title] at [Company]

## Status
Current Stage: Researching
Last Updated: [today's date]

## Timeline
| Date | Event |
|------|-------|
| [today] | Position added |

## Notes

## Interview Notes

## Offer Details
```

## Completion

Tell the user:
- Position added at job-search/companies/<company-slug>/positions/<role-slug>/
- Run /find-hiring-team <company> <role> to research who's hiring
- Run /tailor-resume <company> <role> when ready to apply
```

- [ ] **Step 3: Install, validate, smoke test**

Run `/add-position acme-corp senior-engineer`. Verify:
- Position directory created with all placeholder files
- `jd.md` contains full JD, extracted requirements, and Keywords section
- `tracking.md` initialized with correct structure

- [ ] **Step 4: Commit**

```bash
git add skills/add-position/
git commit -m "feat: add add-position skill"
```

---

### Task 5: find-hiring-team skill

**Files:**
- Create: `skills/find-hiring-team/SKILL.md`

**Interfaces:**
- Consumes: `jd.md`, `research.md`
- Produces: `team.md`

- [ ] **Step 1: Create directory**

```bash
mkdir -p skills/find-hiring-team
```

- [ ] **Step 2: Write SKILL.md**

```markdown
---
name: find-hiring-team
description: Research and document the hiring team for a specific position. Guides you to find the hiring manager, likely panel, and key contacts. Usage: /find-hiring-team <company> <role>
---

Read the following files:
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/research.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/jd.md

## Research Guidance

Guide the user to find the hiring team using these specific strategies, in order:

1. **Hiring manager search**
   - Search LinkedIn: "[role title] [company name]" — look for the person who would manage this role
   - Look at the JD: does it name a team or manager?
   - Check the company's team page or org chart if public
   - Ask: "Did you find a likely hiring manager? If so, share their name, title, and LinkedIn URL."

2. **Panel / interviewers**
   - Search LinkedIn for people at the company with titles that suggest they'd interview for this role (peers, tech leads, senior members of the team)
   - Ask: "Who else do you think might be on the interview panel based on the team page or LinkedIn?"

3. **Recruiter**
   - Search LinkedIn: people at [company] with "recruiter" or "talent" in their title, filtered by recent activity
   - Check if the job posting lists a recruiter name
   - Ask: "Did you find a recruiter or sourcer associated with this role?"

4. **Key adjacent contacts**
   - Who is the skip-level manager (hiring manager's boss)?
   - Are there respected ICs on the team worth knowing?

## Output

Write to ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/team.md:

```
# Hiring Team: [Role] at [Company]

## Hiring Manager
**Name:** 
**Title:** 
**LinkedIn:** 
**Background:** 
**Notes:** 

## Likely Panel
| Name | Title | LinkedIn | Notes |
|------|-------|----------|-------|
|      |       |          |       |

## Recruiter
**Name:** 
**Title:** 
**LinkedIn:** 

## Key Contacts
| Name | Title | Why They Matter |
|------|-------|-----------------|
|      |       |                 |

## Research Notes
[how confident is this info? what couldn't be found?]
```

Tell the user:
- Team info saved. Run /outreach <person> <company> <role> to draft outreach.
- Run /tailor-resume <company> <role> to create application materials.
```

- [ ] **Step 3: Smoke test**

Run `/find-hiring-team acme-corp senior-engineer`. Verify `team.md` is written with correct structure.

- [ ] **Step 4: Commit**

```bash
git add skills/find-hiring-team/
git commit -m "feat: add find-hiring-team skill"
```

---

## Phase 4 — Application Materials
*Deliverable: users can generate tailored resumes, cover letters, exported DOCX, LinkedIn copy, and personal site copy.*

---

### Task 6: tailor-resume skill + ATS reference + markdown templates

**Files:**
- Create: `skills/tailor-resume/SKILL.md`
- Create: `skills/tailor-resume/ats-optimization.md`
- Create: `skills/tailor-resume/templates/classic.md`
- Create: `skills/tailor-resume/templates/modern.md`
- Create: `skills/tailor-resume/templates/executive.md`
- Create: `skills/tailor-resume/templates/tech.md`

**Interfaces:**
- Consumes: `profile.md`, `narrative.md`, `research.md`, `jd.md`
- Produces: appends tailored resume to `materials.md`; updates `preferred_template` in `narrative.md`

- [ ] **Step 1: Create directories**

```bash
mkdir -p skills/tailor-resume/templates
```

- [ ] **Step 2: Write ats-optimization.md**

This is the canonical ATS rules file referenced by tailor-resume and export-resume.

```markdown
# ATS Optimization Rules

## Approved Section Headings (use these exactly)
- Work Experience (not "Professional History", "Career", etc.)
- Education
- Skills
- Summary (or Professional Summary)
- Certifications
- Projects
- Volunteer Experience
- Publications
- Awards

## Formatting Constraints
- Single-column layout only — no multi-column, no sidebars
- No tables inside the resume body
- No text boxes, graphics, logos, or images
- No headers or footers (contact info goes in the body)
- Use plain hyphens (-) for bullets, not •, ◆, or other Unicode symbols
- Dates: "Jan 2022 – Present" format (en-dash, spelled month)
- No special characters: avoid em-dashes (—) in bullet text; use commas or semicolons

## Keyword Strategy
- Mirror the exact language from the JD — if the JD says "stakeholder management", use that phrase, not "managing stakeholders"
- Place high-signal keywords in the first bullet of each role where natural
- Ensure all "Must-Have Skills" from jd.md appear at least once in the resume
- Do not keyword-stuff — one natural mention is enough for ATS; the human reader matters too

## File Export Guidance
- DOCX (.docx) is preferred over PDF for most ATS systems — ATS parsers handle Word documents more reliably
- If a company explicitly requests PDF, convert from DOCX in Word or LibreOffice (File → Export as PDF)
- Never submit a resume scanned as an image PDF — ATS cannot parse it
- Pandoc command for DOCX export: see /export-resume skill
```

- [ ] **Step 3: Write the four markdown templates**

All four templates must follow ATS rules above. Section names must match JSON Resume v1.0.0 field names (basics → Summary, work → Work Experience, education → Education, skills → Skills, projects → Projects).

**skills/tailor-resume/templates/classic.md**
```markdown
# ATS Compliance: PASS
# Template: Classic Chronological
# Best for: Traditional industries (finance, law, consulting, government, most corporate roles)
# JSON Resume mapping: basics→Summary, work→Work Experience, education→Education, skills→Skills, projects→Projects

---

[FULL NAME]
[Email] | [Phone] | [LinkedIn] | [City, State]

## Summary
[2–3 sentence professional summary emphasizing years of experience and core strengths]

## Work Experience

### [Job Title] — [Company], [City, State]
*[Month Year] – [Month Year]*
- [Accomplishment starting with strong verb, quantified where possible]
- [Accomplishment]
- [Accomplishment]

### [Job Title] — [Company], [City, State]
*[Month Year] – [Month Year]*
- [Accomplishment]

## Education

### [Degree] in [Field] — [Institution]
*[Year]*

## Skills
[Comma-separated list of technical and soft skills — single paragraph, no sub-sections]

## Certifications
- [Certification Name] — [Issuing Body], [Year]
```

**skills/tailor-resume/templates/modern.md**
```markdown
# ATS Compliance: PASS
# Template: Modern Single-Column
# Best for: Tech-adjacent roles, startups, creative industries, product management
# JSON Resume mapping: basics→Summary, work→Work Experience, education→Education, skills→Skills, projects→Projects

---

[FULL NAME]
[Email] · [Phone] · [LinkedIn] · [City, State]

## Summary
[2–3 sentences: bold opening statement about what you do and what impact you drive]

## Skills
### Technical
[comma-separated]
### Domain
[comma-separated]

## Work Experience

### [Job Title]
**[Company]** · [City, State] · [Month Year] – [Month Year]
- [Impact-first bullet: outcome → how you achieved it]
- [Bullet]
- [Bullet]

## Projects
### [Project Name]
*[Tech stack / tools]*
[1–2 sentence description of project and your contribution]

## Education
[Degree] in [Field] — [Institution], [Year]

## Certifications
[Name] — [Issuer], [Year]
```

**skills/tailor-resume/templates/executive.md**
```markdown
# ATS Compliance: PASS
# Template: Executive / Senior Leadership
# Best for: Director, VP, C-suite, and senior manager roles
# JSON Resume mapping: basics→Summary, work→Work Experience, education→Education, skills→Skills

---

[FULL NAME]
[Email] | [Phone] | [LinkedIn] | [City, State]

## Summary
[3–4 sentences: leadership philosophy, scale of impact (team size, budget, revenue), and unique expertise]

## Core Competencies
[12–16 comma-separated leadership competencies — drawn from JD language]

## Professional Experience

### [Job Title] — [Company]
*[Month Year] – [Month Year] | [Location]*

**Scope:** [Team size] direct reports | [$X] budget | [Context/scale]

- [Bullet: strategic outcome — quantify at org/business level]
- [Bullet: team/people impact]
- [Bullet: process or transformation achievement]
- [Bullet]

## Education
[Degree] in [Field] — [Institution], [Year]
[Additional credentials if relevant]

## Board & Advisory
- [Organization] — [Role], [Years] (if applicable)
```

**skills/tailor-resume/templates/tech.md**
```markdown
# ATS Compliance: PASS
# Template: Technical / Engineering
# Best for: Software engineering, data science, DevOps, security, and other IC technical roles
# JSON Resume mapping: basics→Summary, skills→Skills, work→Work Experience, projects→Projects, education→Education

---

[FULL NAME]
[Email] | [Phone] | [LinkedIn] | [GitHub] | [City, State]

## Summary
[2 sentences: technical stack + type of problems you solve + scale]

## Technical Skills
**Languages:** [list]
**Frameworks & Libraries:** [list]
**Infrastructure & Tools:** [list]
**Methodologies:** [list]

## Work Experience

### [Job Title] — [Company]
*[Month Year] – [Month Year]*
- [Technical accomplishment: what you built/fixed, what stack, what scale/impact]
- [Bullet]
- [Bullet]

## Projects
### [Project Name] — [github.com/link or "private"]
*[Stack: language, framework, infra]*
[2–3 sentences: what it does, your role, any metrics]

## Education
[Degree] in [Field] — [Institution], [Year]

## Certifications
[Name] — [Issuer], [Year]
```

- [ ] **Step 4: Write SKILL.md**

```markdown
---
name: tailor-resume
description: Generate an ATS-optimized resume tailored to a specific job. Reads your profile and the job description, selects a template, mirrors JD keywords, and runs a keyword gap analysis. Usage: /tailor-resume <company> <role> [template]
---

Read these files:
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/research.md (if exists)
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/jd.md

Also read ATS rules from: ${CLAUDE_PLUGIN_ROOT}/skills/tailor-resume/ats-optimization.md

## Step 1: Template Selection

If the user provided a template argument, use that. Otherwise, read `preferred_template:` from narrative.md. If neither exists, ask the user:
"Which resume template would you like? classic (traditional industries), modern (tech/startups), executive (senior leadership), tech (engineering/IC). Your choice will be saved as your default."

Save the selected template to narrative.md as `preferred_template: <name>`.

Read the chosen template from: ${CLAUDE_PLUGIN_ROOT}/skills/tailor-resume/templates/<name>.md

## Step 2: Content Tailoring

Using profile.md as the source of truth, produce a resume that:
1. Uses the exact section structure from the chosen template
2. Mirrors language from the JD — use the same terms, not synonyms
3. Orders experience bullets to surface the most JD-relevant accomplishments first
4. Rewrites summary/headline to reflect this specific role and company
5. Includes all "Must-Have Skills" from jd.md's Keywords section

Follow ALL rules in ats-optimization.md. No exceptions.

## Step 3: ATS Keyword Gap Analysis

After drafting, compare the "Keywords for ATS" list from jd.md against the drafted resume.

Report:
```
## ATS Keyword Analysis
Coverage: X of Y keywords present

### Missing Keywords
- [keyword] — suggested placement: [section/bullet]
- [keyword] — suggested placement: [section/bullet]

### ATS Compliance Check
- [ ] Single-column layout
- [ ] Standard section headings only
- [ ] No tables, graphics, or text boxes
- [ ] Plain hyphens for bullets
- [ ] Consistent date format
```

If any missing keywords can be naturally added, add them. Ask the user to review any that feel forced.

## Output

Append to ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/materials.md:

```
---
# Resume — [Role] at [Company]
# Template: [template name]
# Generated: [date]
---

[full resume content]

---
[ATS Keyword Analysis block]
```

Tell the user:
- Resume saved to materials.md
- Run /export-resume <company> <role> to generate a DOCX file
- Run /write-cover-letter <company> <role> to write a matching cover letter
```

- [ ] **Step 5: Install, validate, smoke test**

```bash
claude plugin validate .
```

Run `/tailor-resume acme-corp senior-engineer` after seeding profile.md and jd.md. Verify:
- Template selection works (defaults to narrative.md preference)
- ATS keyword analysis block appears in output
- materials.md is created with resume content
- Output uses only approved section headings from ats-optimization.md

- [ ] **Step 6: Commit**

```bash
git add skills/tailor-resume/
git commit -m "feat: add tailor-resume skill with ATS optimization and template selection"
```

---

### Task 7: write-cover-letter skill

**Files:**
- Create: `skills/write-cover-letter/SKILL.md`

**Interfaces:**
- Consumes: `profile.md`, `narrative.md`, `research.md`, `jd.md`, `team.md` (optional)
- Produces: appends cover letter to `materials.md`

- [ ] **Step 1: Create directory and write SKILL.md**

```bash
mkdir -p skills/write-cover-letter
```

```markdown
---
name: write-cover-letter
description: Write a tailored cover letter for a specific position using your profile and company research. Usage: /write-cover-letter <company> <role>
---

Read:
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/research.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/jd.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/team.md (if exists)

## Writing Instructions

Write a cover letter that:
1. **Opens strong** — first sentence names the specific role and one compelling reason you're the right fit (not "I am writing to apply…")
2. **Paragraph 1** — Why this company, specifically. Reference something from research.md: a product, a mission statement, a recent announcement. Show you did the work.
3. **Paragraph 2** — Your most relevant experience mapped to the role's top 2–3 requirements. Use specific accomplishments from profile.md, quantified.
4. **Paragraph 3** — Your narrative thread: the through-line from narrative.md and why this role is the natural next step.
5. **Close** — Specific ask (looking forward to discussing / available for a call this week). Name the hiring manager if known from team.md.

Format:
- 3–4 paragraphs, no more than 400 words total
- Addressed to hiring manager by name if available, otherwise "Hiring Team"
- No filler phrases: "I am a passionate…", "I would be a great fit…", "I am excited to…"

Append to ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/materials.md:
```
---
# Cover Letter — [Role] at [Company]
# Generated: [date]
---

[date]
[Hiring Manager Name or "Hiring Team"]
[Company Name]

Dear [Name / Hiring Team],

[cover letter body]

Sincerely,
[User's full name]
[Email] | [Phone]
```

Tell the user: cover letter appended to materials.md. Review and personalize before sending.
```

- [ ] **Step 2: Smoke test and commit**

Run `/write-cover-letter acme-corp senior-engineer`. Verify cover letter appended correctly to materials.md with date and greeting.

```bash
git add skills/write-cover-letter/
git commit -m "feat: add write-cover-letter skill"
```

---

### Task 8: export-resume skill + reference DOCX templates

**Files:**
- Create: `skills/export-resume/SKILL.md`
- Create: `skills/export-resume/templates/classic-reference.docx`
- Create: `skills/export-resume/templates/modern-reference.docx`
- Create: `skills/export-resume/templates/executive-reference.docx`
- Create: `skills/export-resume/templates/tech-reference.docx`

**Interfaces:**
- Consumes: `materials.md` (resume section), `narrative.md` (preferred_template), `profile.md`
- Produces: `resume.docx` and/or `resume.json` and/or `resume.pdf`

- [ ] **Step 1: Create directory**

```bash
mkdir -p skills/export-resume/templates
```

- [ ] **Step 2: Create reference DOCX templates**

Each reference DOCX defines Word styles that pandoc applies during conversion. Create them manually:

For each of the four templates (classic, modern, executive, tech):

1. Run: `pandoc --print-default-data-file reference.docx > skills/export-resume/templates/<name>-reference.docx`
2. Open the file in Word or LibreOffice Writer
3. Modify the following styles (Format → Styles):
   - **Normal** (body text): Times New Roman 11pt / Calibri 11pt (classic), Calibri 11pt (modern), Georgia 11pt (executive), Consolas/Calibri 11pt (tech)
   - **Heading 1** (name): 18pt bold, no space before
   - **Heading 2** (section headings): 12pt bold, border-bottom, 6pt space before
   - **Heading 3** (job titles): 11pt bold, italic
4. Set page margins: 1 inch all sides (classic/executive), 0.75 inch (modern/tech)
5. Save and close

**Verification:** Run `pandoc --version` to confirm pandoc ≥ 3.0 is installed. If not: `brew install pandoc` (macOS), `winget install pandoc` (Windows), `apt install pandoc` (Linux).

After creating all four reference DOCX files, commit them as binary files:
```bash
git add skills/export-resume/templates/*.docx
git commit -m "feat: add reference DOCX templates for pandoc export"
```
No git-lfs required — reference DOCX files are typically under 100KB.

- [ ] **Step 3: Write SKILL.md**

```markdown
---
name: export-resume
description: Export your tailored resume to DOCX (default), JSON Resume v1.0.0, or PDF. Requires Pandoc for DOCX/PDF. Usage: /export-resume <company> <role> [docx|json|pdf]
---

Read:
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/materials.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md (for preferred_template)
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md (for JSON export)

The format argument defaults to `docx` if not provided.

## DOCX Export

1. Extract the resume section from materials.md (content between the first `---` block and the ATS Keyword Analysis section).
2. Write it to a temp file: ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/resume-temp.md
3. Read preferred_template from narrative.md to determine the reference DOCX.
4. Run pandoc:

```bash
pandoc "${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/resume-temp.md" \
  --reference-doc="${CLAUDE_PLUGIN_ROOT}/skills/export-resume/templates/<template>-reference.docx" \
  -o "${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/resume.docx"
```

5. If pandoc is not found, print:
   "Pandoc is required for DOCX export. Install it with:
   macOS: brew install pandoc
   Windows: winget install pandoc
   Linux: sudo apt install pandoc
   Then re-run /export-resume."
   Do not proceed.

6. Delete the temp file after successful conversion.
7. Tell the user: "resume.docx created. Open it in Word or LibreOffice to review formatting before submitting. To convert to PDF: File → Export as PDF."

## JSON Export

Convert the resume from materials.md into a JSON Resume v1.0.0 object. Map sections as follows:
- Summary → basics.summary (also extract name/email/phone/LinkedIn/location into basics)
- Work Experience → work[] (each role: name, position, startDate, endDate, highlights[])
- Education → education[] (institution, area, studyType, endDate)
- Skills → skills[] (group by category if present, otherwise single entry)
- Projects → projects[] (name, description)
- Certifications → certificates[] (name, issuer, date)

Write to: ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/resume.json

The output must validate against: https://jsonresume.org/schema

Tell the user: "resume.json created. Compatible with resume-cli: npm install -g resume-cli && resume serve"

## PDF Export

1. Check if a PDF engine is available:
```bash
which pdflatex || which wkhtmltopdf || which weasyprint
```

2. If found, run:
```bash
pandoc "${CLAUDE_PROJECT_DIR}/job-search/.../resume-temp.md" \
  -o "${CLAUDE_PROJECT_DIR}/job-search/.../resume.pdf"
```

3. If no PDF engine found, tell the user:
   "No PDF engine found. Options:
   - Convert resume.docx to PDF in Word (File → Export as PDF) — recommended
   - Install wkhtmltopdf: brew install wkhtmltopdf, then re-run /export-resume <company> <role> pdf"
```

- [ ] **Step 4: Install, validate, smoke test**

```bash
claude plugin validate .
```

Test sequence:
1. Run `/export-resume acme-corp senior-engineer` — verify `resume.docx` is created
2. Open `resume.docx` in Word — verify styles match the template (headings, fonts, margins)
3. Run `/export-resume acme-corp senior-engineer json` — verify `resume.json` is valid JSON Resume
4. Validate JSON: `cat resume.json | python3 -c "import json,sys; json.load(sys.stdin); print('valid JSON')"`
5. Run `/export-resume acme-corp senior-engineer pdf` without PDF engine — verify graceful fallback message

- [ ] **Step 5: Commit**

```bash
git add skills/export-resume/
git commit -m "feat: add export-resume skill with pandoc DOCX and JSON Resume export"
```

---

### Task 9: optimize-linkedin skill

**Files:**
- Create: `skills/optimize-linkedin/SKILL.md`

**Interfaces:**
- Consumes: `profile.md`, `narrative.md`
- Produces: `${CLAUDE_PROJECT_DIR}/job-search/profile/linkedin-draft.md`

- [ ] **Step 1: Write SKILL.md**

```bash
mkdir -p skills/optimize-linkedin
```

```markdown
---
name: optimize-linkedin
description: Generate optimized LinkedIn profile copy from your profile and narrative. Produces ready-to-paste copy for every section. Usage: /optimize-linkedin
---

Read:
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md

Generate optimized copy for each LinkedIn section. Use the positioning statement and unique value prop from narrative.md as the guiding voice.

## Sections to Produce

**Headline** (220 char max)
Lead with your primary value, not your job title. Format: "[What you do] | [Differentiator] | [Industry/type of company]"
Write 3 variants ranked by strength.

**About Section** (2,600 char max)
- Hook sentence (first 2 lines show before "see more")
- 2 paragraphs on what you do and the impact you drive
- Bullet list of 3–5 core competencies
- Call to action (what you're open to / how to reach you)

**Experience Bullets**
For each role in profile.md, rewrite 3–5 bullets for LinkedIn style:
- Lead with the outcome, then how
- Quantify everything possible
- Use rich media hooks: "Led team of X to deliver Y in Z weeks"

**Skills Section**
List the top 50 skills to add, grouped by: Technical, Domain, Leadership, Industry

**Featured Section Ideas**
Suggest 3–5 items to feature: portfolio links, articles, case studies, presentations.

**Open to Work / Headline Tips**
When to use #OpenToWork. How to set visibility for recruiters only.

Write all output to: ${CLAUDE_PROJECT_DIR}/job-search/profile/linkedin-draft.md

Structure the file with clear section headers so each block can be copied independently.

Tell the user: LinkedIn draft saved to job-search/profile/linkedin-draft.md. Copy each section directly into LinkedIn.
```

- [ ] **Step 2: Smoke test and commit**

Run `/optimize-linkedin`. Verify `linkedin-draft.md` is created with all sections, headline has 3 variants, skills section has grouped list.

```bash
git add skills/optimize-linkedin/
git commit -m "feat: add optimize-linkedin skill"
```

---

### Task 10: build-personal-site skill

**Files:**
- Create: `skills/build-personal-site/SKILL.md`

**Interfaces:**
- Consumes: `profile.md`, `narrative.md`
- Produces: `${CLAUDE_PROJECT_DIR}/job-search/profile/personal-site-draft.md`

- [ ] **Step 1: Write SKILL.md**

```bash
mkdir -p skills/build-personal-site
```

```markdown
---
name: build-personal-site
description: Generate copy for a personal/portfolio website organized by page and section. Drop directly into any site builder (Notion, Framer, GitHub Pages, etc.). Usage: /build-personal-site
---

Read:
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md

Generate website copy organized by page and section. Ask the user: "Do you have a portfolio website already, or are you starting from scratch? If you have one, what platform are you using?" Tailor the copy format to their platform if known.

## Pages / Sections to Generate

**Home / Hero**
- Headline (8 words max): what you do, for whom
- Subheadline (20 words max): the outcome you deliver
- Bio short (50 words): punchy, first-person, present tense
- CTA button copy (2 options): "View My Work" / "Let's Talk"

**About Page**
- Bio long (150–200 words): your story, what drives you, what makes you different
- A "By the numbers" block: 3–4 impressive stats from profile.md (years of experience, team sizes, notable metrics)
- What I'm looking for: 2–3 sentences on target roles/companies (from narrative.md)

**Work / Experience Page**
For each role in profile.md:
- Company, title, dates
- 2–3 sentence project/role description written for a web audience (more narrative than resume bullets)
- 1–2 key outcomes

**Projects Page**
For each project in profile.md:
- Title and one-line description
- Your role and what you built
- Outcome / link (if public)
- Stack (for technical projects)

**Skills Page**
- Grouped skills list formatted for display (not comma-separated — each on its own line per group)

**Contact Page**
- Friendly invitation to connect (2 sentences)
- What you're open to (from narrative.md)
- Email and LinkedIn link copy

Write all output to: ${CLAUDE_PROJECT_DIR}/job-search/profile/personal-site-draft.md

Use clear section headers and sub-headers matching page/section names so each block can be copied independently into any site builder.

Tell the user: Personal site copy saved to job-search/profile/personal-site-draft.md.
```

- [ ] **Step 2: Smoke test and commit**

Run `/build-personal-site`. Verify output is organized by page/section and each section is self-contained.

```bash
git add skills/build-personal-site/
git commit -m "feat: add build-personal-site skill"
```

---

## Phase 5 — Outreach & ATS
*Deliverable: users can draft outreach messages and generate ATS application answers.*

---

### Task 11: outreach skill

**Files:**
- Create: `skills/outreach/SKILL.md`

**Interfaces:**
- Consumes: `profile.md`, `narrative.md`, `research.md`, `team.md`
- Produces: `outreach.md`

- [ ] **Step 1: Write SKILL.md**

```bash
mkdir -p skills/outreach
```

```markdown
---
name: outreach
description: Draft cold or warm outreach messages to a recruiter, hiring manager, or connection. Generates multiple variants. Usage: /outreach <person> <company> <role>
---

Arguments: person name or description, company, role.

Read:
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/research.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/team.md (if exists)

Ask the user:
1. "Is this a cold contact (you don't know them) or a warm contact (mutual connection or previous interaction)?"
2. "What is their role — recruiter, hiring manager, peer/IC, executive, or mutual connection?"
3. If warm: "What's your connection? (e.g., met at a conference, connected on LinkedIn, mutual contact named [X])"

## Generate Four Variants

**Variant A: LinkedIn Connection Request (300 char max)**
No opener like "Hi [name], I came across your profile." Lead with a specific reason you're reaching out tied to the company or their background.

**Variant B: LinkedIn Message / InMail (short)**
2–3 sentences. Specific hook (mention something real from their background or company), one line on who you are and why relevant, soft ask (happy to share more / open to a quick chat).

**Variant C: Email (if applicable)**
Subject line + 3-paragraph email:
- Para 1: specific hook — why them, why now
- Para 2: who you are and the most relevant thing you've done
- Para 3: soft ask — 15-minute call, happy to share resume, etc.
No generic openers. No "I hope this email finds you well."

**Variant D: Warm Outreach (if warm contact)**
Reference the mutual connection or prior interaction directly in the first sentence. Leverage the relationship without over-explaining it.

## Output

Write to ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/outreach.md:
```
# Outreach: [Person] — [Role] at [Company]
Date: [today]

## Variant A: LinkedIn Connection Request
[text]

## Variant B: LinkedIn Message
[text]

## Variant C: Email
Subject: [subject]
[body]

## Variant D: Warm Outreach
[text or "N/A — cold contact"]

## Sent Log
| Date | Channel | Variant | Response |
|------|---------|---------|----------|
|      |         |         |          |
```

Tell the user: outreach drafts saved. Personalize [PLACEHOLDER] text before sending. Log sends in the Sent Log table.
```

- [ ] **Step 2: Smoke test and commit**

Run `/outreach "Jane Smith, recruiter" acme-corp senior-engineer`. Verify all four variants generated and written to `outreach.md`.

```bash
git add skills/outreach/
git commit -m "feat: add outreach skill with cold/warm variants"
```

---

### Task 12: apply-ats skill + ATS field reference docs

**Files:**
- Create: `skills/apply-ats/SKILL.md`
- Create: `skills/apply-ats/ats-fields/workday.md`
- Create: `skills/apply-ats/ats-fields/greenhouse.md`
- Create: `skills/apply-ats/ats-fields/lever.md`

**Interfaces:**
- Consumes: `profile.md`, `narrative.md`, `jd.md`, `materials.md`
- Produces: printed answers ready to copy-paste (no file written — user copies directly into ATS)

- [ ] **Step 1: Create directories**

```bash
mkdir -p skills/apply-ats/ats-fields
```

- [ ] **Step 2: Write ATS field reference docs**

**skills/apply-ats/ats-fields/workday.md**
```markdown
# Workday Common Fields

## Application Fields
- **Legal First Name / Last Name** — use legal name exactly
- **Address** — city, state, zip required; street optional
- **Phone** — format: (555) 555-5555
- **LinkedIn Profile URL** — paste full URL
- **Resume Upload** — upload resume.docx (Workday parses DOCX reliably)
- **Cover Letter** — optional upload or text field; 5,000 char limit

## Screening Questions (common)
- **Authorized to work in [country]?** — Yes / No
- **Require visa sponsorship now or in future?** — Yes / No
- **Years of experience in [skill]?** — integer field
- **Salary expectations** — range or single number; research market first
- **How did you hear about this role?** — LinkedIn / Company website / Referral / Job board
- **Willing to relocate?** — Yes / No / Open to discussion
- **Available start date** — format: MM/DD/YYYY

## Character Limits
- Work experience descriptions: 4,000 characters per role
- Cover letter text field: 5,000 characters
- Short-answer questions: typically 500–1,000 characters

## Tips
- Workday auto-parses resume — verify parsed data matches your resume after upload
- If parsing fails, re-upload as .docx (not .pdf)
- Save application progress frequently — sessions time out after ~30 minutes
```

**skills/apply-ats/ats-fields/greenhouse.md**
```markdown
# Greenhouse Common Fields

## Application Fields
- **Full Name** — first and last
- **Email** — use a professional address
- **Phone** — any format accepted
- **Resume** — upload DOCX or PDF; Greenhouse parses both well
- **Cover Letter** — separate upload or text field
- **LinkedIn URL** — optional but recommended
- **Website / Portfolio** — include if relevant
- **Location** — city, state / remote

## Screening Questions (common)
- **Work authorization** — dropdown: US Citizen / Green Card / Visa / Other
- **Sponsorship required?** — Yes / No
- **Years of relevant experience** — dropdown ranges (0-2, 3-5, 5-10, 10+)
- **Compensation expectations** — text field; enter a range
- **Source** — how you found the role

## Short-Answer / Essay Questions
Greenhouse frequently includes role-specific questions. Common examples:
- "Tell us about a project you're proud of" (500 char)
- "Why [Company]?" (500 char)
- "Describe your experience with [skill]" (1,000 char)

## Tips
- Greenhouse supports both DOCX and PDF — DOCX preferred for parsing accuracy
- Short-answer questions are often scored; answer completely, not briefly
- Application is usually submitted in one session — prepare answers in advance
```

**skills/apply-ats/ats-fields/lever.md**
```markdown
# Lever Common Fields

## Application Fields
- **Full Name**
- **Email**
- **Phone**
- **Current Company** — if employed; "Job Searching" if not
- **Current Title**
- **Resume** — upload; Lever parses PDF and DOCX
- **LinkedIn / Twitter / GitHub** — optional profile links
- **Portfolio / Website**
- **Location**

## Screening Questions (common)
- **Work authorization** — free text or dropdown
- **Sponsorship required?** — Yes / No
- **Years of experience** — numeric
- **Salary expectations** — range acceptable

## Additional Info Fields
Lever often has a free-text "Additional Information" field (2,000 chars). Use it to:
- Add context the resume doesn't capture
- Name a referral
- Address a potential concern proactively

## Tips
- Lever is recruiter-forward — the recruiter sees your profile card before your resume
- Fill all optional fields; they appear on the recruiter's card
- Referrals entered in the source field are flagged prominently to recruiters
```

- [ ] **Step 3: Write SKILL.md**

```markdown
---
name: apply-ats
description: Generate pre-written answers for ATS application fields tailored to the specific role. Usage: /apply-ats <company> <role> [workday|greenhouse|lever]
---

Read:
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/jd.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/materials.md

If a system argument was provided, also read:
${CLAUDE_PLUGIN_ROOT}/skills/apply-ats/ats-fields/<system>.md

## Output

Generate ready-to-paste answers for the following fields. Label each field clearly.

**Standard Fields (all systems)**
- Work authorization: [derived from profile.md — ask if not present]
- Visa sponsorship required: [Yes/No — ask if not present]
- Current/most recent title: [from profile.md]
- Years of experience in [key skill from JD]: [calculated from profile.md work history]
- Salary expectations: [ask user: "What's your target compensation range?"]
- How did you hear about this role: [ask user]
- Willing to relocate: [ask user if not in profile]
- Available start date: [ask user]

**Short-Answer Questions**
Ask the user: "Does the application have any short-answer or essay questions? Paste them here and I'll draft responses."

For each question provided, write a response using profile.md + research.md as sources. Stay within character limits from the ATS reference doc. Responses should be direct, specific, and substantive — not generic.

**System-Specific Fields**
If a system was provided, list any additional fields from the reference doc not covered above, with pre-filled answers or guidance.

Format all output clearly with field labels and character counts where relevant.

Tell the user: review each answer before pasting. Update salary expectations based on your current market research.
```

- [ ] **Step 4: Smoke test and commit**

Run `/apply-ats acme-corp senior-engineer workday`. Verify all standard fields are addressed and Workday-specific tips are included.

```bash
git add skills/apply-ats/
git commit -m "feat: add apply-ats skill with Workday, Greenhouse, and Lever reference docs"
```

---

## Phase 6 — Interview
*Deliverable: users can prep for interviews, run mock sessions, and send post-interview follow-ups.*

---

### Task 13: prep-interview skill

**Files:**
- Create: `skills/prep-interview/SKILL.md`

**Interfaces:**
- Consumes: all context files for the company/position
- Produces: appends prep guide to `tracking.md`

- [ ] **Step 1: Write SKILL.md**

```bash
mkdir -p skills/prep-interview
```

```markdown
---
name: prep-interview
description: Generate a comprehensive interview prep guide for a specific role. Covers likely questions, STAR stories, company research, and a cheat sheet. Usage: /prep-interview <company> <role>
---

Read all available files:
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/research.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/jd.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/team.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/tracking.md

Ask the user: "What round is this interview? (Recruiter screen / Hiring manager / Technical / Panel / Final / Other)"

## Generate Prep Guide

**1. Company Cheat Sheet (1 page)**
From research.md: company in one sentence, 3 key facts, recent news to reference, 2 things about the culture.

**2. Role Alignment**
From jd.md: top 3 requirements and your strongest proof point for each (from profile.md).

**3. Likely Questions by Category**

*Behavioral (STAR format expected):*
Generate 8 likely behavioral questions based on the JD and round. For each, suggest the best story from profile.md with STAR outline: Situation → Task → Action → Result.

*Role-Specific / Technical:*
Generate 5 likely technical or domain questions based on the role type and JD requirements.

*Company / Cultural:*
Generate 3 questions the interviewer may ask about fit, motivation, and culture.

**4. Questions to Ask**
Generate 5 strong questions for the user to ask, tailored to the round:
- For recruiter screens: process, team culture, timeline
- For hiring manager: what success looks like, team dynamics, challenges
- For technical/panel: technical decisions, how the team works, growth areas

**5. Research Gaps**
List anything the user should verify or research before the interview (e.g., "Look up [interviewer name] on LinkedIn — their background may signal what they care about").

Append all of the above to ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/tracking.md under a new section:
```
## Interview Prep — [Round] — [Date]
[full prep guide]
```

Tell the user: prep guide saved to tracking.md. For mock interview practice, use the interview-coach agent.
```

- [ ] **Step 2: Smoke test and commit**

Run `/prep-interview acme-corp senior-engineer`. Verify prep guide appended to tracking.md with all sections.

```bash
git add skills/prep-interview/
git commit -m "feat: add prep-interview skill"
```

---

### Task 14: post-interview skill

**Files:**
- Create: `skills/post-interview/SKILL.md`

**Interfaces:**
- Consumes: `team.md`, `tracking.md`, user's debrief input
- Produces: appends thank-you notes and debrief to `tracking.md`

- [ ] **Step 1: Write SKILL.md**

```bash
mkdir -p skills/post-interview
```

```markdown
---
name: post-interview
description: Generate personalized thank-you notes for each interviewer and log a structured debrief. Run within 24 hours of an interview. Usage: /post-interview <company> <role>
---

Read:
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/team.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/tracking.md

Ask the user (one question at a time):
1. "Who did you interview with today? List names and titles (or paste from your calendar invite)."
2. "For each interviewer, what's one specific thing you discussed or that stood out?"
3. "How did the interview feel overall? Any topics that came up unexpectedly?"
4. "Was anything unclear about the role or company that you'd want to address?"
5. "What's your excitement level about this role right now, 1–10?"

## Generate Thank-You Notes

For each interviewer mentioned, write a distinct thank-you note:
- Subject: "Thank you — [Role Title] interview" (email) or no subject (LinkedIn)
- Para 1: Thank them and reference the specific conversation point they shared
- Para 2: One sentence connecting something discussed to your experience/enthusiasm
- Para 3: Brief close — looking forward to next steps

Each note should be different. Do not reuse the same sentences across interviewers.
Length: 100–150 words per note.

## Structured Debrief

Write a debrief section:
```
### What went well
- [specific moment]

### What to improve
- [specific moment]

### Open questions about the role
- [question]

### Excitement level: [X/10]
### Next step expected: [what recruiter said]
### Follow up if no response by: [date — 5 business days from today]
```

Append everything to tracking.md:
```
## Post-Interview — [Date]

### Thank-You Notes
#### [Interviewer Name] — [Title]
[note text]

### Debrief
[debrief block]
```

Update Status in tracking.md: "Interviewed — [round]"
```

- [ ] **Step 2: Smoke test and commit**

Run `/post-interview acme-corp senior-engineer`. Verify distinct thank-you notes per interviewer and debrief appended to tracking.md.

```bash
git add skills/post-interview/
git commit -m "feat: add post-interview skill"
```

---

### Task 15: interview-coach agent

**Files:**
- Create: `agents/interview-coach.md`

**Interfaces:**
- Consumes: `research.md`, `team.md`, `jd.md`, `profile.md`
- Produces: interview feedback and session notes appended to `tracking.md`

- [ ] **Step 1: Write agent definition**

```markdown
---
name: interview-coach
description: Conducts a realistic mock interview for a specific role, gives structured per-answer feedback, and delivers a full debrief at the end. Invoke with company and role: "interview-coach for acme-corp senior-engineer"
model: sonnet
effort: high
maxTurns: 30
disallowedTools: Edit
---

You are an expert interview coach conducting a realistic mock interview. The user will tell you the company and role they're preparing for.

## Setup

Read these files before starting:
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/research.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/jd.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/team.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md

Ask the user: "What round are we practicing? (Recruiter screen / Hiring manager / Technical / Panel)"

## Interview Conduct

1. Tell the user: "I'll play the interviewer. Answer as you would in the real interview. I'll ask one question at a time, give you feedback after each answer, then move to the next question. Ready?"

2. Ask questions appropriate to the round type. Draw from:
   - JD requirements and Must-Have Skills for technical/role questions
   - Standard behavioral questions (STAR format expected)
   - Company-specific questions based on research.md

3. After each answer, provide structured feedback:
   ```
   **Feedback:**
   ✓ Strong: [what worked]
   ✗ Improve: [what to sharpen]
   💡 Tip: [specific suggestion]
   ```

4. Continue for 8–10 questions, then close the mock interview.

## Debrief

After the mock interview, provide a full debrief:

```
## Mock Interview Debrief — [Date]

### Overall Assessment
[2–3 sentence honest assessment]

### Strengths
- [specific strength with example from the session]

### Development Areas
- [specific area with concrete suggestion]

### Top 3 Answers to Polish Before Real Interview
1. [question + what to fix]

### Recommended Practice
[specific exercises or topics to work on]
```

Ask: "Would you like me to save these notes to your tracking file?" If yes, write the debrief to tracking.md.
```

- [ ] **Step 2: Validate and smoke test**

```bash
claude plugin validate .
```

Start the interview-coach agent in a test session. Verify it:
- Reads context files before starting
- Asks questions one at a time
- Gives structured feedback after each answer
- Delivers a full debrief at the end

- [ ] **Step 3: Commit**

```bash
git add agents/interview-coach.md
git commit -m "feat: add interview-coach agent"
```

---

## Phase 7 — Pipeline & Decision
*Deliverable: users can track all active applications and evaluate offers.*

---

### Task 16: pipeline skill

**Files:**
- Create: `skills/pipeline/SKILL.md`

**Interfaces:**
- Consumes: all `tracking.md` files across `job-search/companies/`
- Produces: `${CLAUDE_PROJECT_DIR}/job-search/pipeline.md`

- [ ] **Step 1: Write SKILL.md**

```bash
mkdir -p skills/pipeline
```

```markdown
---
name: pipeline
description: Generate a status dashboard of all active job search opportunities across companies and roles. Updates pipeline.md. Usage: /pipeline
---

Use the Bash tool to find all tracking files:
```bash
find "${CLAUDE_PROJECT_DIR}/job-search/companies" -name "tracking.md" 2>/dev/null
```

Read each tracking.md found. Extract:
- Company name (from directory path)
- Role name (from directory path)
- Current Stage (from "Current Stage:" line)
- Last Updated (from "Last Updated:" line)
- Next step / follow-up date (from Timeline or Notes)

## Generate Dashboard

Write to ${CLAUDE_PROJECT_DIR}/job-search/pipeline.md:

```
# Job Search Pipeline
Last Updated: [today's date]

## Active Opportunities

### Researching
| Company | Role | Added | Next Action |
|---------|------|-------|-------------|

### Applied
| Company | Role | Applied | Follow Up By |
|---------|------|---------|--------------|

### Outreach Sent
| Company | Role | Sent | Contact | Response? |
|---------|------|------|---------|-----------|

### Interviewing
| Company | Role | Round | Next Interview |
|---------|------|-------|----------------|

### Offer
| Company | Role | Offer Details | Deadline |
|---------|------|---------------|----------|

### Closed / Declined
| Company | Role | Outcome |
|---------|------|---------|

## Recommended Actions
[List any overdue follow-ups or upcoming deadlines with specific next steps]

## Summary
- Total active: [N]
- In interview stage: [N]
- Offers pending: [N]
```

Tell the user: pipeline updated. Run /pipeline weekly to stay current.
```

- [ ] **Step 2: Smoke test and commit**

Seed test data with 2–3 tracking.md files in different stages. Run `/pipeline`. Verify all opportunities appear in the correct stage table.

```bash
git add skills/pipeline/
git commit -m "feat: add pipeline skill"
```

---

### Task 17: analyze-offer skill

**Files:**
- Create: `skills/analyze-offer/SKILL.md`

**Interfaces:**
- Consumes: `jd.md`, `research.md`, `tracking.md`
- Produces: appends offer analysis to `tracking.md`

- [ ] **Step 1: Write SKILL.md**

```bash
mkdir -p skills/analyze-offer
```

```markdown
---
name: analyze-offer
description: Evaluate a job offer with total comp breakdown, market benchmarking guidance, comparison framework, and negotiation positioning. Usage: /analyze-offer <company> <role>
---

Read:
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/research.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/jd.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/tracking.md

Ask the user for offer details (one at a time):
1. Base salary
2. Bonus (target % and structure: guaranteed / performance-based)
3. Equity (options or RSUs — grant size, vesting schedule, strike price if options, last 409A if known)
4. Benefits (health insurance cost to employee, 401k match %, HSA contribution)
5. PTO (days + any unlimited caveats)
6. Remote / hybrid / in-office policy
7. Start date and any signing bonus

## Output

**Total Compensation Estimate**
Calculate and display:
- Base: $X
- Bonus (expected): $X (X% of base, assuming target payout)
- Equity (annualized): $X (based on grant ÷ vest years; note assumptions)
- Benefits value: $X (estimate health premium employer contribution + 401k match)
- **Total estimated annual comp: $X**
- **Note any significant unknowns** (e.g., equity value uncertain without knowing company valuation)

**Market Benchmarking Guidance**
Tell the user exactly where to check:
- Levels.fyi (for tech roles)
- Glassdoor (role + company + location)
- LinkedIn Salary Insights
- Payscale / Comprehensive.io / Radford (for non-tech)
- Ask your network: "Do you know anyone in a similar role at a similar-stage company?"

**Offer Comparison Framework** (if evaluating multiple offers)
Ask: "Are you comparing this to other offers? If so, share the details."
Build a side-by-side table if multiple offers present.

**Negotiation Positioning**
- What levers exist: base, sign-on, equity refresh, start date, title, remote flexibility
- What's standard to push on: base and sign-on are almost always negotiable; equity is harder at late-stage companies
- What to say: "I'm very excited about this opportunity. Based on my research, I was expecting something closer to $X. Is there flexibility?"
- What not to say: never give the first number; never accept on the spot

Append to tracking.md:
```
## Offer Analysis — [Date]
[full analysis]
```

Update Status: "Offer Received"
```

- [ ] **Step 2: Smoke test and commit**

Run `/analyze-offer acme-corp senior-engineer` with sample offer data. Verify total comp is calculated, benchmarking sources are listed, and negotiation script is included.

```bash
git add skills/analyze-offer/
git commit -m "feat: add analyze-offer skill"
```

---

## Phase 8 — Infrastructure
*Deliverable: the SessionStart hook shows pipeline context at session start.*

---

### Task 18: SessionStart hook

**Files:**
- Create: `hooks/hooks.json`

**Interfaces:**
- Consumes: `${CLAUDE_PROJECT_DIR}/job-search/pipeline.md` (if exists)
- Produces: session-start notification with pipeline summary

- [ ] **Step 1: Write hooks.json**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'PIPELINE=\"${CLAUDE_PROJECT_DIR}/job-search/pipeline.md\"; if [ -f \"$PIPELINE\" ]; then echo \"--- Job Search Pipeline ---\"; grep -E \"^- Total active:|^- In interview|^- Offers pending\" \"$PIPELINE\" 2>/dev/null || head -20 \"$PIPELINE\"; echo \"---------------------------\"; fi'"
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 2: Validate and smoke test**

```bash
claude plugin validate .
```

Start a new Claude Code session in a directory containing `job-search/pipeline.md`. Verify the summary prints at session start. Start a session in a directory without `pipeline.md` — verify nothing prints.

- [ ] **Step 3: Commit**

```bash
git add hooks/hooks.json
git commit -m "feat: add SessionStart hook for pipeline summary"
```

---

## Phase 9 — Documentation
*Deliverable: complete user-facing documentation in docs/.*

---

### Task 19: README + installation guide

**Files:**
- Create: `docs/README.md`
- Create: `docs/installation.md`

- [ ] **Step 1: Write docs/README.md**

```markdown
# Career Search Tools

A Claude Code + Claude Cowork plugin that turns job searching into a structured, repeatable workflow. Build your profile once — every skill compounds on it.

## What's Included

**15 skills:**
- `/setup-profile` — Create your professional profile and positioning narrative
- `/research-company` — Structured company research guide
- `/add-position` — Add a job posting and extract requirements
- `/find-hiring-team` — Research the hiring manager and panel
- `/tailor-resume` — ATS-optimized resume tailored to the JD
- `/write-cover-letter` — Role-specific cover letter
- `/export-resume` — Export to DOCX (default), JSON Resume, or PDF
- `/optimize-linkedin` — Section-by-section LinkedIn optimization
- `/build-personal-site` — Website copy organized by page/section
- `/outreach` — Cold and warm outreach message variants
- `/apply-ats` — Pre-written ATS field answers (Workday, Greenhouse, Lever)
- `/prep-interview` — Likely questions, STAR stories, company cheat sheet
- `/post-interview` — Personalized thank-you notes and debrief
- `/pipeline` — Cross-company application status dashboard
- `/analyze-offer` — Total comp breakdown and negotiation positioning

**1 agent:**
- `interview-coach` — Multi-turn mock interview with per-answer feedback

## Quick Start

1. Install the plugin (see [Installation](installation.md))
2. Run `/setup-profile` — create your profile and narrative (10–15 min)
3. Run `/research-company <company>` — research your first target company
4. Run `/add-position <company> <role>` — paste the job description
5. Run `/tailor-resume <company> <role>` — generate your tailored resume

## Data

All your data lives in `job-search/` in your project directory. It's plain Markdown — readable, editable, and yours.

## Documentation
- [Installation guide](installation.md)
- [Usage guide](usage-guide.md)
- [ATS & export guide](ats-guide.md)
```

- [ ] **Step 2: Write docs/installation.md**

```markdown
# Installation Guide

## Prerequisites

- Claude Code v2.1.0 or later, or Claude Cowork
- [Pandoc](https://pandoc.org/installing.html) (required for DOCX/PDF export only)

**Install Pandoc:**
- macOS: `brew install pandoc`
- Windows: `winget install pandoc`
- Linux: `sudo apt install pandoc`

Verify: `pandoc --version` should show 3.0 or later.

## Install on Claude Code

**From the marketplace:**
```bash
claude plugin install career-search-tools
```

**From a local clone:**
```bash
git clone https://github.com/matthewkimber/career-search-tools
claude plugin install --plugin-dir ./career-search-tools
```

**Verify installation:**
```bash
claude plugin list
```
You should see `career-search-tools` listed as enabled.

**Installation scope:**
- `user` (default) — available in all your projects
- `project` — available only in the current project, shared with teammates via `.claude/settings.json`

```bash
# Project scope:
claude plugin install career-search-tools --scope project
```

## Install on Claude Cowork

1. Open the plugin marketplace from the Cowork interface
2. Search for `career-search-tools`
3. Click Install
4. When prompted, grant file system access to your job search project folder
5. Start a task and run `/setup-profile` to initialize

## First Run

After installing, create a dedicated folder for your job search:

```bash
mkdir my-job-search
cd my-job-search
claude  # or open in Cowork
```

Then run `/setup-profile` to initialize the `job-search/` directory.

## Troubleshooting

**Plugin not appearing:**
```bash
claude plugin validate /path/to/career-search-tools
```
Check the `/plugin` errors tab in Claude Code.

**Skills not found after install:**
Run `/reload-plugins` in your Claude Code session.

**Pandoc not found when running /export-resume:**
Install pandoc (see Prerequisites above), then retry.

**Skills reading wrong directory:**
Make sure Claude Code is launched from your job search project folder — `${CLAUDE_PROJECT_DIR}` is set to the directory where Claude Code starts.
```

- [ ] **Step 3: Commit**

```bash
git add docs/README.md docs/installation.md
git commit -m "docs: add README and installation guide"
```

---

### Task 20: Usage guide

**Files:**
- Create: `docs/usage-guide.md`

- [ ] **Step 1: Write docs/usage-guide.md**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add docs/usage-guide.md
git commit -m "docs: add usage guide"
```

---

### Task 21: ATS & export guide

**Files:**
- Create: `docs/ats-guide.md`

- [ ] **Step 1: Write docs/ats-guide.md**

```markdown
# ATS & Export Guide

## Why ATS Safety Matters

Most large companies use Applicant Tracking Systems (ATS) to parse resumes before a human sees them. An ATS-unsafe resume can score zero for keyword matching even if the candidate is qualified — simply because the parser couldn't read it. All resumes generated by this plugin are ATS-safe by design.

## What Makes a Resume ATS-Unsafe

- **Tables** — many parsers can't read table cells correctly
- **Multi-column layouts** — text reads out of order
- **Headers and footers** — content is often ignored by parsers
- **Text boxes** — treated as images, not text
- **Non-standard section headings** — "My Journey" instead of "Work Experience"
- **Special characters** — Unicode bullets (•, ◆) may not parse; use plain hyphens
- **Image or scanned PDFs** — no text layer to parse

The plugin uses only: single-column layout, plain hyphens, standard headings, and body-level contact info.

## Resume Templates

Four templates are included, all ATS-safe:

| Template | Best For | Key Feature |
|----------|----------|-------------|
| `classic` | Traditional industries | Chronological, conservative formatting |
| `modern` | Tech-adjacent, startups | Clean, contemporary, skills near top |
| `executive` | Senior leadership | Scope/scale emphasis, competencies block |
| `tech` | Engineering / IC roles | Skills section first, projects prominent |

Set your preferred template during `/setup-profile` or per-export with `/tailor-resume <company> <role> <template>`.

## Exporting Your Resume

### DOCX (Recommended)

```
/export-resume acme-corp senior-engineer
```

Requires Pandoc ≥ 3.0. Install: `brew install pandoc` (macOS), `winget install pandoc` (Windows), `sudo apt install pandoc` (Linux).

Produces `resume.docx` styled with your chosen template. Open in Word or LibreOffice to review before submitting.

**When to use DOCX:** for most ATS submissions. DOCX parses more reliably than PDF across Workday, Greenhouse, and Lever.

### PDF

```
/export-resume acme-corp senior-engineer pdf
```

Requires a PDF engine (LaTeX or wkhtmltopdf). If not installed, the skill will tell you.

**Easier option:** open `resume.docx` → File → Export as PDF. This produces a cleaner PDF than pandoc in most cases.

**When to use PDF:** when the company explicitly requests it, or for human-only submissions (portfolio, email).

### JSON Resume

```
/export-resume acme-corp senior-engineer json
```

Exports to [JSON Resume v1.0.0](https://jsonresume.org/schema) format. Use this to:
- Import into compatible resume builders
- Render with any JSON Resume theme: `npm install -g resume-cli && resume serve`
- Feed into other job search tools

## ATS Systems

### Workday
- Upload `resume.docx` (DOCX parses more reliably than PDF in Workday)
- Workday auto-parses your resume into fields — verify parsed data after upload
- Session timeout: ~30 min; save progress frequently
- Character limit per role: ~4,000 characters

### Greenhouse
- Accepts both DOCX and PDF
- Short-answer questions are often scored — answer fully, not briefly
- Prepare answers in advance; Greenhouse applications are usually one-session

### Lever
- Fill all optional fields — they appear on the recruiter's profile card
- Include a referral name in the source field if you have one — it's flagged prominently
- Use the Additional Information field to add context the resume doesn't capture

## Request Support for a New ATS

[Open an issue](https://github.com/matthewkimber/career-search-tools/issues) with the label `ats-support` and include: the ATS name, which company uses it, and any field names or quirks you've noticed.
```

- [ ] **Step 2: Commit**

```bash
git add docs/ats-guide.md
git commit -m "docs: add ATS and export guide"
```

---

## Phase 10 — Integration & Validation

---

### Task 22: Full plugin validation and integration test

**Files:**
- No new files. Validates the complete plugin.

- [ ] **Step 1: Run plugin validation**

```bash
claude plugin validate .
```

Expected: no errors. Acceptable warnings: empty optional directories.

- [ ] **Step 2: Install and run full smoke test sequence**

Create a clean test directory:
```bash
mkdir /tmp/job-search-test && cd /tmp/job-search-test
claude plugin install --plugin-dir /path/to/career-search-tools
```

Run in sequence:
1. `/setup-profile` → verify `job-search/profile/` created with 3 files
2. `/research-company acme-corp` → verify `job-search/companies/acme-corp/research.md` created
3. `/add-position acme-corp senior-engineer` → verify position directory and all placeholder files
4. `/find-hiring-team acme-corp senior-engineer` → verify `team.md` written
5. `/tailor-resume acme-corp senior-engineer` → verify `materials.md` written with ATS analysis block
6. `/write-cover-letter acme-corp senior-engineer` → verify cover letter appended to `materials.md`
7. `/export-resume acme-corp senior-engineer` → verify `resume.docx` created; open and check styling
8. `/export-resume acme-corp senior-engineer json` → verify valid JSON; check against JSON Resume schema
9. `/optimize-linkedin` → verify `linkedin-draft.md` created with all sections
10. `/build-personal-site` → verify `personal-site-draft.md` created organized by page
11. `/outreach "Jane Smith" acme-corp senior-engineer` → verify `outreach.md` with 4 variants
12. `/apply-ats acme-corp senior-engineer workday` → verify all standard fields addressed
13. `/prep-interview acme-corp senior-engineer` → verify prep guide appended to `tracking.md`
14. Start `interview-coach` agent → verify it reads context, asks questions, gives feedback
15. `/post-interview acme-corp senior-engineer` → verify thank-you notes and debrief in `tracking.md`
16. `/pipeline` → verify `pipeline.md` dashboard created
17. `/analyze-offer acme-corp senior-engineer` → verify total comp and negotiation brief in `tracking.md`
18. Start new session with `pipeline.md` present → verify `SessionStart` hook prints summary

- [ ] **Step 3: Open PR**

```bash
git push origin HEAD
gh pr create --title "feat: complete career-search-tools plugin implementation" \
  --body "Implements all 15 skills, 1 agent, 1 hook, and 4 documentation files per the approved design spec."
```

---

*End of plan. 22 tasks across 10 phases. Each phase is independently deployable.*
