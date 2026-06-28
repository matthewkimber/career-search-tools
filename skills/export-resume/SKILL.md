---
name: export-resume
description: "Export your tailored resume to DOCX (default), JSON Resume v1.0.0, or PDF. Requires Pandoc for DOCX/PDF. Usage: /export-resume <company> <role> [docx|json|pdf]"
---

Read:
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/materials.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md (for preferred_template)
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md (for JSON export)

The format argument defaults to `docx` if not provided.

## DOCX Export

Before running pandoc, check whether the reference DOCX exists:
- Look for: ${CLAUDE_PLUGIN_ROOT}/skills/export-resume/templates/<template>-reference.docx
- If it does NOT exist (only a .placeholder file is present), tell the user:
  "The reference DOCX template for '<template>' hasn't been generated yet. Run this command once to create it:
  pandoc --print-default-data-file reference.docx > <full-path-to-templates-dir>/<template>-reference.docx
  Then open the file in Word or LibreOffice to customize the fonts and margins, and re-run /export-resume."
  Stop here — do not proceed with export.
- If the file exists, proceed with pandoc as described below.

1. Extract the resume section from materials.md (content between the first `---` block and the ATS Keyword Analysis section).
2. Write it to a temp file: ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/resume-temp.md
3. Read preferred_template from narrative.md to determine the reference DOCX.
4. Run pandoc:

```bash
pandoc "${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/resume-temp.md" \
  --reference-doc="${CLAUDE_PLUGIN_ROOT}/skills/export-resume/templates/<template>-reference.docx" \
  -o "${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/resume.docx"
```

5. If pandoc is not found, print:
   "Pandoc is required for DOCX export. Install it with:
   macOS: brew install pandoc
   Windows: winget install pandoc
   Linux: sudo apt install pandoc
   Then re-run /export-resume."
   Do not proceed.

6. Delete the temp file after successful conversion.
7. Tell the user: "resume.docx created. Open it in Word or LibreOffice to review formatting before submitting. To convert to PDF: File → Export as PDF."

## JSON Export

Convert the resume from materials.md into a JSON Resume v1.0.0 object. Map sections as follows:
- Summary → basics.summary (also extract name/email/phone/LinkedIn/location into basics)
- Work Experience → work[] (each role: name, position, startDate, endDate, highlights[])
- Education → education[] (institution, area, studyType, endDate)
- Skills → skills[] (group by category if present, otherwise single entry)
- Projects → projects[] (name, description)
- Certifications → certificates[] (name, issuer, date)

Write to: ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/resume.json

The output must validate against: https://jsonresume.org/schema

Tell the user: "resume.json created. Compatible with resume-cli: npm install -g resume-cli && resume serve"

## PDF Export

1. Check if a PDF engine is available:
```bash
which pdflatex || which wkhtmltopdf || which weasyprint
```

2. If found, run:
```bash
pandoc "${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/resume-temp.md" \
  -o "${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/resume.pdf"
```

3. If no PDF engine found, tell the user:
   "No PDF engine found. Options:
   - Convert resume.docx to PDF in Word (File → Export as PDF) — recommended
   - Install wkhtmltopdf: brew install wkhtmltopdf, then re-run /export-resume <company> <role> pdf"
