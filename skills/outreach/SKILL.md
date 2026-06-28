---
name: outreach
description: "Draft cold or warm outreach messages to a recruiter, hiring manager, or connection. Generates multiple variants. Usage: /outreach <person> <company> <role>"
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
