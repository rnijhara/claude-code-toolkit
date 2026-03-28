# Claude Code Toolkit

Personal utilities, configs, and reusable skills for AI coding agents.

Works with [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex CLI](https://developers.openai.com/codex/cli/), and [OpenCode](https://opencode.ai/) — all three support the `SKILL.md` format.

## What's Inside

### `/statusline` — Custom Statusline for Claude Code

A Python script that displays model name, directory, git branch, and a context usage bar with auto-compact awareness. See [statusline/README.md](statusline/README.md) for setup.

### `/skills` — Reusable Development Workflow Skills

#### Development Workflow

A four-skill workflow for planning, implementing, and releasing features:

| Skill | Description |
|-------|-------------|
| `/lets-init` | One-time project setup. Auto-detects stack, quality commands, version files, and writes `.planning/PROJECT.md`. |
| `/lets-plan` | Discussion-first planning. Iterates with you on design decisions, edge cases, and UAT before writing a structured plan in `.planning/`. |
| `/lets-implement` | Phase-by-phase execution. Spawns a subagent per phase, reviews the output, fixes issues, runs quality checks, and commits. |
| `/lets-release` | Guided release. Analyzes commits, proposes semver bump, updates changelog, bumps versions, tags, and optionally deploys. |

The intended workflow:

```
/lets-init           →  one-time: creates .planning/PROJECT.md
/lets-plan feature   →  per feature: creates .planning/FEATURE.md
/lets-implement .planning/FEATURE.md  →  executes the plan phase by phase
/lets-release minor  →  cuts a release
```

#### Second Opinion & Research

| Skill | Description |
|-------|-------------|
| `/codex` | Get a second opinion from OpenAI's Codex CLI on plans, code, or debugging. Reviews plans for gaps, code for bugs, and helps when you're stuck. |
| `/grok` | Query xAI's Grok with native X/Twitter search. Fetch tweets, search discussions, check reactions -- anything that needs real-time X data. Requires an `XAI_API_KEY` in `~/.config/grok/.env`. |

## Installation

### Claude Code

Copy the skills to your global skills directory:

```sh
cp -r skills/* ~/.claude/skills/
```

### Codex CLI

Copy to the Codex skills directory:

```sh
mkdir -p ~/.agents/skills
cp -r skills/* ~/.agents/skills/
```

### OpenCode

Copy to the OpenCode skills directory:

```sh
mkdir -p ~/.config/opencode/skills
cp -r skills/* ~/.config/opencode/skills/
```

OpenCode also reads from `~/.claude/skills/` and `~/.agents/skills/` as fallbacks.

### Per-project installation

To scope skills to a specific project instead of installing globally, copy them into the project:

```sh
# Claude Code
cp -r skills/* .claude/skills/

# Codex CLI
cp -r skills/* .agents/skills/

# OpenCode
cp -r skills/* .opencode/skills/
```

## How It Works

### The `.planning/` directory

Running `/lets-init` creates a `.planning/` directory in your project with a `PROJECT.md` that captures:

- **Stack** — language, framework, package manager, project structure
- **Quality commands** — lint, typecheck, test, build commands
- **Version files** — which files contain version strings to bump
- **Git conventions** — default branch, branch naming
- **Release/deploy** — deploy commands, release workflow

The other skills read from `PROJECT.md` so they adapt to any project without modification.

### Plan files

`/lets-plan` creates plan files like `.planning/FEATURE_NAME.md` with phases, design decisions, tests at assertion level, UAT scenarios, and edge cases. `/lets-implement` reads these and executes them phase by phase.

## Requirements

- Python 3 (for statusline)
- One of: Claude Code, Codex CLI, or OpenCode
