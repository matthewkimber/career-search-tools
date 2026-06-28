---
name: tailor-resume
description: Generate an ATS-optimized resume tailored to a specific job. Reads your profile and the job description, selects a template, mirrors JD keywords, and runs a keyword gap analysis. Usage: /tailor-resume <company> <role> [template]
---

Read these files:
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/research.md (if exists)
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/jd.md

Also read ATS rules from: ${CLAUDE_PLUGIN_ROOT}/skills/tailor-resume/ats-optimization.md

## Step 1: Template Selection

If the user provided a template argument, use that. Otherwise, read `preferred_template:` from narrative.md. If neither exists, ask the user:
"Which resume template would you like? classic (traditional industries), modern (tech/startups), executive (senior leadership), tech (engineering/IC). Your choice will be saved as your default."

Save the selected template to narrative.md as `preferred_template: <name>`.

Read the chosen template from: ${CLAUDE_PLUGIN_ROOT}/skills/tailor-resume/templates/<name>.md

## Step 2: Content Tailoring

Using profile.md as the source of truth, produce a resume that:
1. Uses the exact section structure from the chosen template
2. Mirrors language from the JD — use the same terms, not synonyms
3. Orders experience bullets to surface the most JD-relevant accomplishments first
4. Rewrites summary/headline to reflect this specific role and company
5. Includes all "Must-Have Skills" from jd.md's Keywords section

Follow ALL rules in ats-optimization.md. No exceptions.

## Step 3: ATS Keyword Gap Analysis

After drafting, compare the "Keywords for ATS" list from jd.md against the drafted resume.

Report:
```
## ATS Keyword Analysis
Coverage: X of Y keywords present

### Missing Keywords
- [keyword] — suggested placement: [section/bullet]
- [keyword] — suggested placement: [section/bullet]

### ATS Compliance Check
- [ ] Single-column layout
- [ ] Standard section headings only
- [ ] No tables, graphics, or text boxes
- [ ] Plain hyphens for bullets
- [ ] Consistent date format
```

If any missing keywords can be naturally added, add them. Ask the user to review any that feel forced.

## Output

Append to ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/materials.md:

```
---
# Resume — [Role] at [Company]
# Template: [template name]
# Generated: [date]
---

[full resume content]

---
[ATS Keyword Analysis block]
```

Tell the user:
- Resume saved to materials.md
- Run /export-resume <company> <role> to generate a DOCX file
- Run /write-cover-letter <company> <role> to write a matching cover letter
