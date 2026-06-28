#!/usr/bin/env python3
"""CI eval runner for career-search-tools skills and agents.

Discovers evals.json files under skills/*/evals/ and agents/evals/,
runs each test case against the Anthropic API, grades assertions using
an LLM-as-judge, and writes results to a workspace directory.

Usage:
    python scripts/run_evals.py [--skills skill1,skill2] [--threshold 0.7] [--workspace ./eval-workspace]
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


def get_anthropic_client():
    """Return an Anthropic client, erroring early if no API key is set."""
    try:
        import anthropic  # noqa: PLC0415
    except ImportError:
        print("ERROR: anthropic package not installed. Run: pip install -r requirements.txt")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable is not set.")
        sys.exit(1)

    return anthropic.Anthropic(api_key=api_key)


def discover_skill_evals(repo_root: Path, skills_filter: list[str] | None) -> list[dict]:
    """Find all skills/*/evals/evals.json files and return a list of skill eval specs."""
    specs = []

    skills_dir = repo_root / "skills"
    for evals_json in sorted(skills_dir.glob("*/evals/evals.json")):
        skill_dir = evals_json.parent.parent
        skill_name = skill_dir.name

        if skills_filter and skill_name not in skills_filter:
            continue

        skill_md_path = skill_dir / "SKILL.md"
        skill_md = skill_md_path.read_text() if skill_md_path.exists() else ""

        data = json.loads(evals_json.read_text())
        # Evals files use either "tests" or "evals" as the array key.
        tests = data.get("tests") or data.get("evals") or []

        specs.append({
            "kind": "skill",
            "name": skill_name,
            "skill_md": skill_md,
            "tests": tests,
        })

    return specs


def discover_agent_evals(repo_root: Path, skills_filter: list[str] | None) -> list[dict]:
    """Find all agents/evals/*.json files and return a list of agent eval specs."""
    specs = []

    agents_evals_dir = repo_root / "agents" / "evals"
    if not agents_evals_dir.exists():
        return specs

    for evals_json in sorted(agents_evals_dir.glob("*.json")):
        data = json.loads(evals_json.read_text())
        agent_name = data.get("agent_name") or evals_json.stem

        if skills_filter and agent_name not in skills_filter:
            continue

        # Agents have no SKILL.md; look for a matching agents/<name>.md
        agent_md_path = repo_root / "agents" / f"{agent_name}.md"
        agent_md = agent_md_path.read_text() if agent_md_path.exists() else ""

        tests = data.get("tests") or data.get("evals") or []

        specs.append({
            "kind": "agent",
            "name": agent_name,
            "skill_md": agent_md,
            "tests": tests,
        })

    return specs


def build_system_prompt(skill_md: str) -> str:
    """Wrap a SKILL.md into the standard system prompt prefix."""
    if skill_md:
        return (
            "You are a Claude assistant with the following skill instructions:\n\n"
            f"{skill_md}\n\n"
            "---\n\n"
            "Respond to the user's task accordingly."
        )
    return "You are a helpful Claude assistant. Respond to the user's task accordingly."


def run_test(client: Any, system_prompt: str, test: dict, model: str) -> dict:
    """Send the test prompt to the API and return the response text plus token count."""
    prompt = test.get("prompt", "")

    # If the test supplies context files, prepend them to the prompt.
    context = test.get("context", {})
    if context:
        context_block = "**Context files available:**\n\n"
        for filename, content in context.items():
            context_block += f"**{filename}:**\n```\n{content}\n```\n\n"
        prompt = context_block + prompt

    start_ms = int(time.time() * 1000)

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}],
    )

    duration_ms = int(time.time() * 1000) - start_ms
    output_text = response.content[0].text if response.content else ""
    total_tokens = response.usage.input_tokens + response.usage.output_tokens

    return {
        "output": output_text,
        "total_tokens": total_tokens,
        "duration_ms": duration_ms,
    }


def grade_assertion(client: Any, assertion: str, output: str, model: str) -> dict:
    """Ask the LLM judge whether the output satisfies the assertion.

    Returns {"passed": bool, "evidence": str}.
    """
    judge_prompt = (
        f"You are grading an AI assistant's output. "
        f"Assertion: '{assertion}'. "
        f"Output to evaluate:\n\n{output}\n\n"
        "Reply with exactly: PASS: <evidence> or FAIL: <evidence>"
    )

    response = client.messages.create(
        model=model,
        max_tokens=512,
        messages=[{"role": "user", "content": judge_prompt}],
    )

    verdict_text = response.content[0].text.strip() if response.content else "FAIL: no response"

    if verdict_text.upper().startswith("PASS"):
        passed = True
        evidence = verdict_text[5:].lstrip(": ").strip() if len(verdict_text) > 4 else ""
    else:
        passed = False
        evidence = verdict_text[5:].lstrip(": ").strip() if len(verdict_text) > 4 else verdict_text

    return {"passed": passed, "evidence": evidence}


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def run_skill_evals(
    client: Any,
    spec: dict,
    workspace: Path,
    model: str,
) -> dict:
    """Run all tests for one skill/agent and return per-skill summary stats."""
    name = spec["name"]
    system_prompt = build_system_prompt(spec["skill_md"])
    tests = spec["tests"]

    total_passed = 0
    total_failed = 0
    total_tokens_all = 0

    for test in tests:
        test_id = str(test.get("id", "unknown"))
        assertions = test.get("assertions", [])

        # Run the test
        result = run_test(client, system_prompt, test, model)
        output = result["output"]
        total_tokens = result["total_tokens"]
        duration_ms = result["duration_ms"]

        total_tokens_all += total_tokens

        # Grade each assertion
        assertion_results = []
        for assertion in assertions:
            grade = grade_assertion(client, assertion, output, model)
            assertion_results.append({
                "text": assertion,
                "passed": grade["passed"],
                "evidence": grade["evidence"],
            })
            if grade["passed"]:
                total_passed += 1
            else:
                total_failed += 1

        n_pass = sum(1 for r in assertion_results if r["passed"])
        n_fail = len(assertion_results) - n_pass
        pass_rate = n_pass / len(assertion_results) if assertion_results else 1.0

        grading_data = {
            "assertion_results": assertion_results,
            "summary": {
                "passed": n_pass,
                "failed": n_fail,
                "total": len(assertion_results),
                "pass_rate": round(pass_rate, 4),
            },
        }

        timing_data = {
            "total_tokens": total_tokens,
            "duration_ms": duration_ms,
        }

        eval_dir = workspace / f"{name}-workspace" / "iteration-1" / f"eval-{test_id}" / "with_skill"
        write_json(eval_dir / "grading.json", grading_data)
        write_json(eval_dir / "timing.json", timing_data)

    total_assertions = total_passed + total_failed
    skill_pass_rate = total_passed / total_assertions if total_assertions > 0 else 1.0

    return {
        "name": name,
        "evals": len(tests),
        "assertions": total_assertions,
        "passed": total_passed,
        "failed": total_failed,
        "pass_rate": round(skill_pass_rate, 4),
        "total_tokens": total_tokens_all,
    }


def write_benchmark(workspace: Path, skill_summaries: list[dict]) -> None:
    """Write the top-level benchmark.json aggregating pass rates per skill."""
    if not skill_summaries:
        mean_pass_rate = 0.0
        mean_tokens = 0
    else:
        mean_pass_rate = sum(s["pass_rate"] for s in skill_summaries) / len(skill_summaries)
        mean_tokens = sum(s["total_tokens"] for s in skill_summaries) // len(skill_summaries)

    benchmark = {
        "run_summary": {
            "with_skill": {
                "pass_rate": {"mean": round(mean_pass_rate, 4)},
                "tokens": {"mean": mean_tokens},
            }
        },
        "skills": {
            s["name"]: {
                "evals": s["evals"],
                "passed": s["passed"],
                "failed": s["failed"],
                "pass_rate": s["pass_rate"],
            }
            for s in skill_summaries
        },
    }

    workspace.mkdir(parents=True, exist_ok=True)
    write_json(workspace / "benchmark.json", benchmark)


def print_summary_table(skill_summaries: list[dict], threshold: float) -> None:
    """Print a summary table to stdout."""
    col_w = [24, 8, 8, 8, 10]
    header = f"{'Skill':<{col_w[0]}} {'Evals':>{col_w[1]}} {'Passed':>{col_w[2]}} {'Failed':>{col_w[3]}} {'Pass Rate':>{col_w[4]}}"
    sep = "-" * sum(col_w + [len(col_w) - 1])

    print()
    print("Eval Results")
    print(sep)
    print(header)
    print(sep)

    for s in skill_summaries:
        flag = "" if s["pass_rate"] >= threshold else " [BELOW THRESHOLD]"
        print(
            f"{s['name']:<{col_w[0]}} "
            f"{s['evals']:>{col_w[1]}} "
            f"{s['passed']:>{col_w[2]}} "
            f"{s['failed']:>{col_w[3]}} "
            f"{s['pass_rate']:>{col_w[4]}.1%}"
            f"{flag}"
        )

    print(sep)

    if skill_summaries:
        overall_pass = sum(s["passed"] for s in skill_summaries)
        overall_total = sum(s["assertions"] for s in skill_summaries)
        overall_rate = overall_pass / overall_total if overall_total else 1.0
        print(
            f"{'OVERALL':<{col_w[0]}} "
            f"{'':>{col_w[1]}} "
            f"{overall_pass:>{col_w[2]}} "
            f"{overall_total - overall_pass:>{col_w[3]}} "
            f"{overall_rate:>{col_w[4]}.1%}"
        )

    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run career-search-tools skill evals against the Anthropic API."
    )
    parser.add_argument(
        "--skills",
        default="",
        help="Comma-separated list of skill/agent names to run (default: all)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        help="Minimum pass rate to pass CI (default: 0.7)",
    )
    parser.add_argument(
        "--workspace",
        default="./eval-workspace",
        help="Directory to write results into (default: ./eval-workspace)",
    )
    args = parser.parse_args()

    skills_filter = [s.strip() for s in args.skills.split(",") if s.strip()] or None
    threshold = args.threshold
    workspace = Path(args.workspace)
    model = "claude-haiku-4-5-20251001"

    # Locate repo root (the directory containing the skills/ folder)
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    client = get_anthropic_client()

    # Discover evals
    skill_specs = discover_skill_evals(repo_root, skills_filter)
    agent_specs = discover_agent_evals(repo_root, skills_filter)
    all_specs = skill_specs + agent_specs

    if not all_specs:
        print("No evals found matching the given filter.")
        return 0

    print(f"Discovered {len(all_specs)} skill/agent eval suite(s).")
    print(f"Model: {model}")
    print(f"Threshold: {threshold:.0%}")
    print(f"Workspace: {workspace}")

    skill_summaries = []
    for spec in all_specs:
        name = spec["name"]
        n_tests = len(spec["tests"])
        print(f"\nRunning {name} ({n_tests} test(s))...")
        summary = run_skill_evals(client, spec, workspace, model)
        skill_summaries.append(summary)
        print(f"  {summary['passed']}/{summary['assertions']} assertions passed ({summary['pass_rate']:.1%})")

    write_benchmark(workspace, skill_summaries)

    print_summary_table(skill_summaries, threshold)

    # Exit non-zero if any skill falls below threshold
    failing = [s for s in skill_summaries if s["pass_rate"] < threshold]
    if failing:
        names = ", ".join(s["name"] for s in failing)
        print(f"FAIL: {len(failing)} skill(s) below threshold ({threshold:.0%}): {names}")
        return 1

    print(f"PASS: All skills at or above threshold ({threshold:.0%}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
