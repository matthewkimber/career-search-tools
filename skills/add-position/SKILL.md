---
name: add-position
description: "Add a specific job position you're targeting at a company. Paste in the job description. Usage: /add-position <company> <role>"
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
