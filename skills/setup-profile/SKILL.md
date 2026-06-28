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
