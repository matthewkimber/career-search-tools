---
name: optimize-linkedin
description: Generate optimized LinkedIn profile copy from your profile and narrative. Produces ready-to-paste copy for every section. Usage: /optimize-linkedin
---

Read:
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md

Generate optimized copy for each LinkedIn section. Use the positioning statement and unique value prop from narrative.md as the guiding voice.

## Sections to Produce

**Headline** (220 char max)
Lead with your primary value, not your job title. Format: "[What you do] | [Differentiator] | [Industry/type of company]"
Write 3 variants ranked by strength.

**About Section** (2,600 char max)
- Hook sentence (first 2 lines show before "see more")
- 2 paragraphs on what you do and the impact you drive
- Bullet list of 3–5 core competencies
- Call to action (what you're open to / how to reach you)

**Experience Bullets**
For each role in profile.md, rewrite 3–5 bullets for LinkedIn style:
- Lead with the outcome, then how
- Quantify everything possible
- Use rich media hooks: "Led team of X to deliver Y in Z weeks"

**Skills Section**
List the top 50 skills to add, grouped by: Technical, Domain, Leadership, Industry

**Featured Section Ideas**
Suggest 3–5 items to feature: portfolio links, articles, case studies, presentations.

**Open to Work / Headline Tips**
When to use #OpenToWork. How to set visibility for recruiters only.

Write all output to: ${CLAUDE_PROJECT_DIR}/job-search/profile/linkedin-draft.md

Structure the file with clear section headers so each block can be copied independently.

Tell the user: LinkedIn draft saved to job-search/profile/linkedin-draft.md. Copy each section directly into LinkedIn.
