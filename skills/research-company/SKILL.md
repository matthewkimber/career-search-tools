---
name: research-company
description: "Research a target company and create a structured company profile. Run before add-position or find-hiring-team. Usage: /research-company <company-name>"
---

The user wants to research a company for their job search. The company name is provided as an argument.

## Setup

1. Convert the company name to a kebab-case slug (e.g. "Acme Corp" → "acme-corp").
2. Create directory: ${CLAUDE_PROJECT_DIR}/job-search/companies/<slug>/
3. Copy the research template from ${CLAUDE_PLUGIN_ROOT}/skills/research-company/templates/research-template.md to ${CLAUDE_PROJECT_DIR}/job-search/companies/<slug>/research.md, replacing [Company Name] with the actual name.

## Research Guidance

Tell the user exactly what to look up and where, then ask them to share what they find section by section. Guide them through each section:

1. **Overview & financials** — Ask them to visit the company website (About page), LinkedIn company page, and Crunchbase. Ask: "What does the company do? How big are they? How are they funded?"

2. **Culture** — Ask them to read Glassdoor reviews (sort by most recent). Ask: "What do employees say about the culture, management, and work-life balance? What themes come up repeatedly?"

3. **Leadership** — Ask them to find the executive team on LinkedIn or the company website. Request: name, title, and a one-line background for each C-suite and relevant VP/director.

4. **Recent news** — Ask them to Google "[company name] news" filtered to the past 6 months. Ask: "What has the company announced recently? Any layoffs, expansions, product launches, or executive changes?"

5. **Why this company** — Based on everything gathered, help them articulate 3–5 genuine reasons this company aligns with their target roles and values from narrative.md.

## Output

Fill in the research.md template with everything gathered. Write clearly and concisely — this file will be read by multiple other skills. End with a checklist of which research sources were consulted.

Tell the user:
- Research saved to job-search/companies/<slug>/research.md
- Run /add-position <company> <role> to add a specific position you're targeting
