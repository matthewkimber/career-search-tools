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
