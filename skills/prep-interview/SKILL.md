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
