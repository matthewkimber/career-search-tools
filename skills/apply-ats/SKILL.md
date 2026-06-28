---
name: apply-ats
description: Generate pre-written answers for ATS application fields tailored to the specific role. Usage: /apply-ats <company> <role> [workday|greenhouse|lever]
---

Read:
- ${CLAUDE_PROJECT_DIR}/job-search/profile/profile.md
- ${CLAUDE_PROJECT_DIR}/job-search/profile/narrative.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/jd.md
- ${CLAUDE_PROJECT_DIR}/job-search/companies/<company-slug>/positions/<role-slug>/materials.md

If a system argument was provided, also read:
${CLAUDE_PLUGIN_ROOT}/skills/apply-ats/ats-fields/<system>.md

## Output

Generate ready-to-paste answers for the following fields. Label each field clearly.

**Standard Fields (all systems)**
- Work authorization: [derived from profile.md — ask if not present]
- Visa sponsorship required: [Yes/No — ask if not present]
- Current/most recent title: [from profile.md]
- Years of experience in [key skill from JD]: [calculated from profile.md work history]
- Salary expectations: [ask user: "What's your target compensation range?"]
- How did you hear about this role: [ask user]
- Willing to relocate: [ask user if not in profile]
- Available start date: [ask user]

**Short-Answer Questions**
Ask the user: "Does the application have any short-answer or essay questions? Paste them here and I'll draft responses."

For each question provided, write a response using profile.md + research.md as sources. Stay within character limits from the ATS reference doc. Responses should be direct, specific, and substantive — not generic.

**System-Specific Fields**
If a system was provided, list any additional fields from the reference doc not covered above, with pre-filled answers or guidance.

Format all output clearly with field labels and character counts where relevant.

Tell the user: review each answer before pasting. Update salary expectations based on your current market research.
