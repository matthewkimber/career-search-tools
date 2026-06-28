---
name: build-personal-site
description: "Generate copy for a personal/portfolio website organized by page and section. Drop directly into any site builder (Notion, Framer, GitHub Pages, etc.). Usage: /build-personal-site"
---

Read:
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md

Generate website copy organized by page and section. Ask the user: "Do you have a portfolio website already, or are you starting from scratch? If you have one, what platform are you using?" Tailor the copy format to their platform if known.

## Pages / Sections to Generate

**Home / Hero**
- Headline (8 words max): what you do, for whom
- Subheadline (20 words max): the outcome you deliver
- Bio short (50 words): punchy, first-person, present tense
- CTA button copy (2 options): "View My Work" / "Let's Talk"

**About Page**
- Bio long (150–200 words): your story, what drives you, what makes you different
- A "By the numbers" block: 3–4 impressive stats from profile.md (years of experience, team sizes, notable metrics)
- What I'm looking for: 2–3 sentences on target roles/companies (from narrative.md)

**Work / Experience Page**
For each role in profile.md:
- Company, title, dates
- 2–3 sentence project/role description written for a web audience (more narrative than resume bullets)
- 1–2 key outcomes

**Projects Page**
For each project in profile.md:
- Title and one-line description
- Your role and what you built
- Outcome / link (if public)
- Stack (for technical projects)

**Skills Page**
- Grouped skills list formatted for display (not comma-separated — each on its own line per group)

**Contact Page**
- Friendly invitation to connect (2 sentences)
- What you're open to (from narrative.md)
- Email and LinkedIn link copy

Write all output to: ${CLAUDE_PROJECT_DIR}/job-search/profile/personal-site-draft.md

Use clear section headers and sub-headers matching page/section names so each block can be copied independently into any site builder.

Tell the user: Personal site copy saved to job-search/profile/personal-site-draft.md.
