# Installation Guide

## Prerequisites

- Claude Code v2.1.0 or later, or Claude Cowork
- [Pandoc](https://pandoc.org/installing.html) (required for DOCX/PDF export only)

**Install Pandoc:**
- macOS: `brew install pandoc`
- Windows: `winget install pandoc`
- Linux: `sudo apt install pandoc`

Verify: `pandoc --version` should show 3.0 or later.

## Install on Claude Code

**From the marketplace:**
```bash
claude plugin install career-search-tools
```

**From a local clone:**
```bash
git clone https://github.com/matthewkimber/career-search-tools
claude plugin install --plugin-dir ./career-search-tools
```

**Verify installation:**
```bash
claude plugin list
```
You should see `career-search-tools` listed as enabled.

**Installation scope:**
- `user` (default) — available in all your projects
- `project` — available only in the current project, shared with teammates via `.claude/settings.json`

```bash
# Project scope:
claude plugin install career-search-tools --scope project
```

## Install on Claude Cowork

1. Open the plugin marketplace from the Cowork interface
2. Search for `career-search-tools`
3. Click Install
4. When prompted, grant file system access to your job search project folder
5. Start a task and run `/setup-profile` to initialize

## First Run

After installing, create a dedicated folder for your job search:

```bash
mkdir my-job-search
cd my-job-search
claude  # or open in Cowork
```

Then run `/setup-profile` to initialize the `job-search/` directory.

## Troubleshooting

**Plugin not appearing:**
```bash
claude plugin validate /path/to/career-search-tools
```
Check the `/plugin` errors tab in Claude Code.

**Skills not found after install:**
Run `/reload-plugins` in your Claude Code session.

**Pandoc not found when running /export-resume:**
Install pandoc (see Prerequisites above), then retry.

**Skills reading wrong directory:**
Make sure Claude Code is launched from your job search project folder — `${CLAUDE_PROJECT_DIR}` is set to the directory where Claude Code starts.
