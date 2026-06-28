---
name: pipeline
description: "Generate a status dashboard of all active job search opportunities across companies and roles. Updates pipeline.md. Usage: /pipeline"
---

Use the Bash tool to find all tracking files:

```bash
find "${CLAUDE_PROJECT_DIR}/job-search/companies" -name "tracking.md" 2>/dev/null
```

Read each tracking.md found. From the file path, extract:
- Company name: the directory segment immediately under `companies/` (e.g. `acme-corp`)
- Role name: the directory segment immediately under `positions/` (e.g. `senior-engineer`)

From the file contents, extract:
- Current Stage (from the "Current Stage:" or "Status:" line)
- Last Updated (from the "Last Updated:" line, or fall back to the most recent dated section heading)
- Next action or follow-up date (from a Timeline section, Notes, or any "Follow up by:" line)

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
[List any overdue follow-ups or upcoming deadlines with specific next steps. If a follow-up date has passed, flag it explicitly. If no deadlines are imminent, say "No urgent actions at this time."]

## Summary
- Total active: [N]
- In interview stage: [N]
- Offers pending: [N]
```

Place each opportunity in the table matching its current stage. Use the company slug and role slug as display names unless a human-readable name is available in the tracking.md header. Leave table cells blank (—) when data is not present in the tracking.md.

Tell the user: pipeline updated at job-search/pipeline.md. Run /pipeline weekly to stay current.
