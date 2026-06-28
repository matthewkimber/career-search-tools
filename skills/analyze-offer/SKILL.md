---
name: analyze-offer
description: "Evaluate a job offer with total comp breakdown, market benchmarking guidance, comparison framework, and negotiation positioning. Usage: /analyze-offer <company> <role>"
---

Read:
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/research.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/jd.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/tracking.md

Ask the user for offer details one at a time in this order:

1. "What is the base salary?"
2. "What is the bonus — target percentage and is it guaranteed or performance-based?"
3. "What is the equity package — options or RSUs? Please share the grant size, vesting schedule, strike price if options, and the most recent 409A valuation if you know it."
4. "What are the benefits — specifically the employee cost for health insurance, the 401k match percentage, and any HSA contribution?"
5. "How many PTO days, and is there an unlimited PTO policy? If unlimited, does the company have a minimum or any caveats?"
6. "What is the remote / hybrid / in-office policy?"
7. "What is the proposed start date and is there a signing bonus?"

## Output

### Total Compensation Estimate

Calculate and display each component:
- Base: $X
- Bonus (expected): $X (X% of base, assuming target payout — note if guaranteed or at-risk)
- Equity (annualized): $X (grant value ÷ vesting years; note if value is unknown because the company is private and no 409A was provided)
- Benefits value: $X estimated (employer health premium contribution + 401k match; use reasonable market estimates if employee did not share exact figures)
- **Total estimated annual comp: $X**

Flag any significant unknowns in bold (e.g., "Equity value is uncertain — company is private and no 409A valuation was provided").

### Market Benchmarking Guidance

Tell the user exactly where to check market data for this role and location:
- **Levels.fyi** — best for tech / engineering roles; search by role, company, and level
- **Glassdoor** — search role title + company + city; filter to last 12 months
- **LinkedIn Salary Insights** — available under the Jobs tab; useful for cross-company comparison
- **Payscale / Comprehensive.io / Radford** — better for non-tech roles or executive compensation
- **Your network** — "Do you know anyone in a similar role at a comparable company? Ask them directly — most people will share a range."

### Offer Comparison Framework

Ask: "Are you comparing this offer against one or more other offers? If yes, share the details."

If the user has multiple offers, build a side-by-side comparison table:

| | [Company A] | [Company B] |
|---|---|---|
| Base | $X | $X |
| Bonus (expected) | $X | $X |
| Equity (annualized) | $X | $X |
| Benefits value | $X | $X |
| **Total est. annual comp** | **$X** | **$X** |
| Remote policy | | |
| PTO | | |
| Start date | | |
| Other factors | | |

Add a brief qualitative comparison below the table covering: mission fit, growth trajectory, team quality signals, and any intangibles worth weighing.

If the user has only one offer, note: "If you receive other offers, run /analyze-offer for each and share the details here to build a comparison."

### Negotiation Positioning

- **Levers available:** base salary, signing bonus, equity (grant size or accelerated vesting), start date, title, remote flexibility
- **What is almost always negotiable:** base salary and signing bonus — these are standard to push on at nearly every company
- **What is harder:** equity at late-stage or public companies is often fixed by band; title negotiation varies by org
- **What to say:** "I'm really excited about this role and [Company]. Based on my research and the scope of what I'd be taking on, I was expecting something closer to $X. Is there flexibility?"
- **What not to say:** never give the first number if you can avoid it; never accept on the spot — always ask for time to review
- **Standard ask for more time:** "Thank you so much — I'd like a few days to review the full package carefully. Can I get back to you by [date]?"

Based on the offer details and the role context from jd.md and research.md, identify which levers are most likely to move and flag any red flags (e.g., cliff-heavy vesting, exploding offer deadline, below-market base).

## Append to tracking.md

```
## Offer Analysis — [Date]

### Total Compensation Estimate
[full breakdown]

### Market Benchmarking Guidance
[sources listed]

### Comparison Framework
[table if multiple offers, or note if single offer]

### Negotiation Positioning
[levers, what to say, what not to say, red flags]
```

Update the Status line in tracking.md to: "Offer Received"
