# Scripts

## run_evals.py

Runs the skill eval suite against the Anthropic API.

**Prerequisites:**
- Python 3.11+
- `pip install -r requirements.txt`
- `ANTHROPIC_API_KEY` environment variable set

**Usage:**
```bash
# Run all skill evals
python scripts/run_evals.py

# Run specific skills only
python scripts/run_evals.py --skills setup-profile,tailor-resume

# Adjust pass threshold (default: 0.7)
python scripts/run_evals.py --threshold 0.8
```

Results are written to `eval-workspace/` (gitignored).
