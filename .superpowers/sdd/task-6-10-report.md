# Tasks 6–10 Implementation Report

**Branch:** `feature/phase-4-materials`
**Date:** 2026-06-27

---

## Task 6: tailor-resume

### Files Created
- `skills/tailor-resume/SKILL.md`
- `skills/tailor-resume/ats-optimization.md`
- `skills/tailor-resume/templates/classic.md`
- `skills/tailor-resume/templates/modern.md`
- `skills/tailor-resume/templates/executive.md`
- `skills/tailor-resume/templates/tech.md`

### Commit
`c9017b3` — feat: add tailor-resume skill with ATS optimization and templates

### Self-review
- SKILL.md faithfully implements all three steps from the brief: template selection (with fallback to narrative.md and interactive prompt if absent), content tailoring, and ATS keyword gap analysis.
- All four templates carry the `# ATS Compliance: PASS` header and the JSON Resume section mapping comment.
- ats-optimization.md is the canonical ATS rules file shared with export-resume per the design doc.
- The output format (materials.md append with `---` separator blocks) matches the design doc schema.
- `preferred_template` is both read from and written back to narrative.md.

### Evals Rationale
4 tests covering: (1) template from narrative.md, (2) explicit classic template for executive role, (3) no template set — prompts user and saves choice, (4) template arg overrides narrative.md preference. Together these exercise the template selection precedence logic and the ATS output block.

---

## Task 7: write-cover-letter

### Files Created
- `skills/write-cover-letter/SKILL.md`

### Commit
`895153f` — feat: add write-cover-letter skill

### Self-review
- 5-point writing structure (strong open, company-specific paragraph, experience paragraph, narrative thread, close) matches the brief exactly.
- Hiring manager name sourced from team.md if present, falls back to "Hiring Team".
- 400-word cap and no-filler-phrases rule both stated as hard constraints.
- Output appended to materials.md using the standard separator format.

### Evals Rationale
3 tests covering: (1) team.md present — addressed to named hiring manager, (2) team.md absent — addressed to Hiring Team, (3) startup context — verifies company-specific reference from research.md.

---

## Task 8: export-resume

### Files Created
- `skills/export-resume/SKILL.md`
- `skills/export-resume/templates/classic-reference.docx.placeholder`
- `skills/export-resume/templates/modern-reference.docx.placeholder`
- `skills/export-resume/templates/executive-reference.docx.placeholder`
- `skills/export-resume/templates/tech-reference.docx.placeholder`

### Commit
`ac8493d` — feat: add export-resume skill with reference DOCX templates

### Pandoc Note
Pandoc was not installed in the build environment (`command not found: pandoc`). Per the task instructions, placeholder text files were created instead of real DOCX files. Each placeholder contains the exact `pandoc --print-default-data-file reference.docx` command to generate the real file. **Users should run that command and customize the output in Word** (set fonts, heading styles, and margins as described in the task brief) before relying on the DOCX export format. The SKILL.md itself handles the missing-pandoc case gracefully with install instructions at runtime.

### Self-review
- DOCX, JSON, and PDF export paths all implemented.
- Pandoc presence check precedes DOCX export; graceful fallback message with platform-specific install commands.
- JSON export maps all sections to JSON Resume v1.0.0 schema (basics, work, education, skills, projects, certificates).
- PDF export checks for pdflatex/wkhtmltopdf/weasyprint; falls back with two clear options.
- Temp file (`resume-temp.md`) is deleted after successful conversion.

### Evals Rationale
4 tests covering: (1) DOCX export with pandoc missing — verifies graceful fallback and no temp file left, (2) JSON export — verifies valid JSON Resume structure, (3) PDF export with no PDF engine — verifies fallback message, (4) DOCX export with pandoc available — verifies template selection and cleanup.

---

## Task 9: optimize-linkedin

### Files Created
- `skills/optimize-linkedin/SKILL.md`

### Commit
`d908ed4` — feat: add optimize-linkedin skill

### Self-review
- All 6 required sections specified: Headline (3 variants, 220-char limit), About (2,600-char limit with hook + paragraphs + competencies + CTA), Experience Bullets (outcome-first, quantified), Skills (50 skills, 4 groups), Featured Section Ideas (3–5 items), Open to Work tips.
- Output file path (`linkedin-draft.md`) uses the canonical profile directory per design doc.
- Section headers in the output are designed for independent copy-paste into LinkedIn.

### Evals Rationale
3 tests covering: (1) IC / data engineer persona — verifies headline variants, character limits, grouped skills, (2) executive / CTO persona — verifies leadership-skewed headlines and org-scale metrics, (3) PM persona — verifies headline doesn't lead with title and About hook is prominent.

---

## Task 10: build-personal-site

### Files Created
- `skills/build-personal-site/SKILL.md`

### Commit
`e7a162e` — feat: add build-personal-site skill

### Self-review
- Skill opens with a platform question before generating (Notion / Framer / GitHub Pages / etc.) and tailors copy format to the platform when known.
- All 6 page sections specified: Home/Hero, About, Work/Experience, Projects, Skills, Contact.
- Word limits enforced per section (headline 8 words, subheadline 20 words, short bio 50 words, long bio 150–200 words).
- Skills page uses one-per-line grouping (explicitly not comma-separated) for display suitability.
- Output file path (`personal-site-draft.md`) uses the canonical profile directory.

### Evals Rationale
3 tests covering: (1) IC engineer with projects — verifies all 6 sections and project details, (2) Framer platform response — verifies platform-aware formatting, (3) executive persona — verifies leadership-appropriate hero and By the numbers content.

---

## Evals File

- `evals/evals.json` — 17 total test cases (4 for tailor-resume, 3 for write-cover-letter, 4 for export-resume, 3 for optimize-linkedin, 3 for build-personal-site)
- Evals commit: `7d05b73`
- Execution: CI-only. Each test case has `id`, `prompt`, `context`, `expected_output`, and `assertions` array.

---

## Commit Summary

| Task | Skill | Commit |
|------|-------|--------|
| 6 | tailor-resume | `c9017b3` |
| 7 | write-cover-letter | `895153f` |
| 8 | export-resume | `ac8493d` |
| 9 | optimize-linkedin | `d908ed4` |
| 10 | build-personal-site | `e7a162e` |
| — | evals | `7d05b73` |
