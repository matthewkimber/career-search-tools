# career-search-tools

A Claude Code + Claude Cowork plugin that turns job searching into a structured, repeatable workflow. Build your profile once — every skill compounds on it.

## Skills

| Skill | What it does |
|-------|-------------|
| `/setup-profile` | Create your professional profile and positioning narrative |
| `/research-company <company>` | Guided company research with an 8-section template |
| `/add-position <company> <role>` | Add a job posting and extract ATS keywords |
| `/find-hiring-team <company> <role>` | Research the hiring manager and panel |
| `/tailor-resume <company> <role>` | ATS-optimized resume tailored to the JD |
| `/write-cover-letter <company> <role>` | Role-specific cover letter (≤400 words) |
| `/export-resume <company> <role>` | Export to DOCX, JSON Resume v1.0.0, or PDF |
| `/optimize-linkedin` | Section-by-section LinkedIn copy |
| `/build-personal-site` | Website copy organized by page and section |
| `/outreach <person> <company> <role>` | Cold and warm outreach message variants |
| `/apply-ats <company> <role>` | Pre-written ATS field answers (Workday, Greenhouse, Lever) |
| `/prep-interview <company> <role>` | Likely questions, STAR stories, company cheat sheet |
| `/post-interview <company> <role>` | Personalized thank-you notes and structured debrief |
| `/pipeline` | Cross-company application status dashboard |
| `/analyze-offer <company> <role>` | Total comp breakdown and negotiation script |

**Agent:** `interview-coach` — multi-turn mock interview with per-answer feedback and a full debrief.

## Install

**Claude Code — from GitHub:**
```bash
# Step 1: add the marketplace (one-time)
claude plugin marketplace add matthewkimber/career-search-tools

# Step 2: install the plugin
/plugin install career-search-tools@career-search-tools
```

**Claude Code — from a local clone:**
```bash
git clone https://github.com/matthewkimber/career-search-tools
claude plugin install --plugin-dir ./career-search-tools
```

**Claude Cowork:** search for `career-search-tools` in the plugin marketplace and click Install.

Full installation instructions (prerequisites, scopes, troubleshooting) → [docs/installation.md](docs/installation.md)

## Quick Start

1. Create a dedicated folder and open it in Claude Code
2. Run `/setup-profile` — takes 10–15 minutes; creates your profile, narrative, and references template
3. Run `/research-company <company>` for your first target
4. Run `/add-position <company> <role>` and paste the job description
5. Run `/tailor-resume <company> <role>` to generate your tailored resume

All your data lives in `job-search/` in your project directory as plain Markdown — readable, editable, and yours.

## Documentation

- [Installation guide](docs/installation.md) — prerequisites, install steps, troubleshooting
- [Usage guide](docs/usage-guide.md) — full 6-phase workflow with command examples
- [ATS & export guide](docs/ats-guide.md) — formatting rules, template comparison, Workday/Greenhouse/Lever tips

## License

Apache 2.0
