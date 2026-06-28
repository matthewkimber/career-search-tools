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
