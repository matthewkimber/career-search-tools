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
