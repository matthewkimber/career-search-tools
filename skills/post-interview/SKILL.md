---
name: post-interview
description: "Generate personalized thank-you notes for each interviewer and log a structured debrief. Run within 24 hours of an interview. Usage: /post-interview <company> <role>"
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
