# AGENTS.md

This repo is a Claude plugin to help someone in their job hunt. This will include assets like:

- Skills
- Agents
- Hooks
- MCPs

## Problem

Searching for a new job is tedious, discouraging, and very time consuming. Most people spend countless hours customizing resumes and cover letters to apply for a job that they will likely never get a callback from. This leads to waning interest in finding a job because it can feel hopeless.

## Objective

Create a set of useful tools that people can use to speed up their resume development, LinkedIn optimization, personal website creation, job search, and job application.

## Development Workflow

- Always place specifications in the `./specs` folder.
- Documentation for end users should reside in the `./docs` folder.
- Use a GitHub Flow as described here: https://docs.github.com/en/get-started/using-github/github-flow

## Skill Evals (Required)

Every skill must include a structured eval suite before it is considered complete. Follow the eval framework at https://agentskills.io/skill-creation/evaluating-skills.

### Eval file structure

Each skill directory must include an `evals/` subdirectory:

```
skills/<skill-name>/
├── SKILL.md
└── evals/
    ├── evals.json          ← test cases (authored by hand)
    └── files/              ← any input files required by test cases
```

### evals.json format

```json
{
  "skill_name": "<skill-name>",
  "evals": [
    {
      "id": 1,
      "prompt": "A realistic user message — the kind of thing someone would actually type.",
      "expected_output": "Human-readable description of what success looks like.",
      "files": ["evals/files/example.md"],
      "assertions": [
        "Specific, verifiable statement about what the output must contain or achieve."
      ]
    }
  ]
}
```

### Requirements for each skill

- **Minimum 3 test cases** per skill: one happy path, one with varied/casual phrasing, one edge case.
- **Assertions added** to each test case after the first eval run (once you know what good looks like).
- **Eval workspace** lives at `<skill-name>-workspace/` alongside the skill directory (gitignored — do not commit eval run outputs).
- **Evals must pass** (or failures must be documented and understood) before a skill PR is merged.

### Eval workspace structure (gitignored)

```
<skill-name>-workspace/
└── iteration-1/
    ├── eval-<test-case-name>/
    │   ├── with_skill/
    │   │   ├── outputs/
    │   │   ├── timing.json
    │   │   └── grading.json
    │   └── without_skill/
    │       ├── outputs/
    │       ├── timing.json
    │       └── grading.json
    └── benchmark.json
```

### .gitignore

Add `*-workspace/` to `.gitignore` so eval run outputs are not committed.

### Grading

After each eval run, grade every assertion as PASS or FAIL with concrete evidence. A PASS requires explicit evidence from the output — do not give the benefit of the doubt. Record results in `grading.json` per the format at https://agentskills.io/skill-creation/evaluating-skills.

## Output

- [Claude Plugin](https://code.claude.com/docs/en/plugins-reference)
