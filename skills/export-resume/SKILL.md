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

Before running pandoc, read preferred_template from narrative.md, then check whether a reference template exists:

- Look for, in this order: `${CLAUDE_PLUGIN_ROOT}/skills/export-resume/templates/<template>-reference.dotx`, then `${CLAUDE_PLUGIN_ROOT}/skills/export-resume/templates/<template>-reference.docx`.
- If neither exists (only a .placeholder file is present), tell the user:
  "The reference template for '<template>' hasn't been generated yet. Run this command once to create it:
  pandoc --print-default-data-file reference.docx > <full-path-to-templates-dir>/<template>-reference.docx
  Then open the file in Word or LibreOffice to customize the fonts, margins, and layout, and re-run /export-resume."
  Stop here — do not proceed with export.
- Otherwise, call whichever file was found the **reference doc** and proceed below. Pandoc reads `.dotx` files directly as a reference doc — no conversion needed.

Also check for `${CLAUDE_PLUGIN_ROOT}/skills/export-resume/templates/<template>-reference-example.docx` — a fully filled-out sample resume showing how content should be laid out for this template. This matters because `--reference-doc` only carries over named *styles* (fonts, colors, spacing) from the reference doc — it does not recreate custom layout such as multi-column tables, side-by-side metric callouts, or per-role title/date tables. If the template relies on that kind of layout and the source Markdown is just plain headings and bullet lists, pandoc will apply the right fonts but the wrong structure, and the export will look off.

1. If `<template>-reference-example.docx` exists:
   a. Convert it to Markdown to inspect its structure: `pandoc "<full-path>/<template>-reference-example.docx" -t markdown`.
   b. Note the structural patterns used — table shapes and column counts, which sections use tables vs. plain paragraphs, exact section heading text and casing (e.g. "leadership profile", "selected achievements"), and how repeating blocks (roles, degrees, certifications) are laid out.
   c. Extract the resume section from materials.md (content between the first `---` block and the ATS Keyword Analysis section), then rewrite it into that same structure — same tables, same column counts, same heading text/case — substituting in the real name, roles, bullets, dates, education, and certifications. Do not flatten tables into plain headings/bullets just because that's simpler; pandoc will not add the layout back for you.
   d. Write the restructured Markdown to a temp file: ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/resume-temp.md
2. If no example file exists, extract the resume section from materials.md as-is (content between the first `---` block and the ATS Keyword Analysis section) and write it to the same temp file path.
3. Run pandoc, pointing `--reference-doc` at whichever reference doc file was found above (the `.dotx` if present, otherwise the `.docx`):

```bash
pandoc "${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/resume-temp.md" \
  --reference-doc="${CLAUDE_PLUGIN_ROOT}/skills/export-resume/templates/<reference-doc-found-above>" \
  -o "${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/resume.docx"
```

4. If pandoc is not found, print:
   "Pandoc is required for DOCX export. Install it with:
   macOS: brew install pandoc
   Windows: winget install pandoc
   Linux: sudo apt install pandoc
   Then re-run /export-resume."
   Do not proceed.

5. Delete the temp file after successful conversion.
6. Tell the user: "resume.docx created. Open it in Word or LibreOffice to review formatting before submitting. To convert to PDF: File → Export as PDF."

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
