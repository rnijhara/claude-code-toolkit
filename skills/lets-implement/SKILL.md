---
name: lets-implement
description: Implement a plan from .planning/ phase by phase with subagents
argument-hint: "<plan-file> [phase-number]"
---

You are orchestrating the implementation of a plan file from `.planning/`. You read the plan, implement each phase using a subagent, review the output, fix issues, and commit.

## Getting Context

Before starting:
- Read the plan file provided in `$ARGUMENTS` (first argument)
- Read `.planning/PROJECT.md` for project config (quality commands, stack, structure)
- Read `.planning/STATE.md` for current project state (if it exists)
- Read project instructions file (`CLAUDE.md` or `AGENTS.md`) for conventions
- Read the source files that will be modified to understand the current code

## Arguments

- `$ARGUMENTS[0]` -- path to the plan file (required). Example: `.planning/SCHEDULED_TASKS_IMPL.md`
- `$ARGUMENTS[1]` -- phase number (optional). If provided, only implement that phase. If omitted, implement all phases iteratively.

## Implementation Cycle

For each phase (or the specified phase), repeat this cycle:

### 1. Implement (subagent)

Spawn a subagent with a clear prompt:
- Include the full plan file path so it can read it
- Specify which phase to implement
- Tell it to read the relevant existing code before making changes
- Tell it to run the quality commands from `.planning/PROJECT.md` when done (lint, typecheck, test)
- Tell it NOT to commit

The subagent prompt should be self-contained. Include enough context that it can work autonomously.

### 2. Review (you, the orchestrator)

After the subagent completes:
- Run `git diff --stat` to see what files changed
- **Read the full changed files** (not just the diff). Use the Read tool on each modified file to understand the complete code in context. Diffs can hide issues that are only visible when reading the full file (wrong imports, duplicated logic, inconsistent patterns with surrounding code).
- Check against the plan: are all items in this phase addressed?
- Check for: missing edge cases, type safety, error handling, convention violations
- Check test coverage: do the tests match what the plan specifies?

### 3. Fix

If issues are found during review, fix them directly (typos, missing types, formatting, logic errors, etc.). Do not use a subagent for fixes.

### 4. Quality Checks

Run the quality commands defined in `.planning/PROJECT.md` (lint, typecheck, test) and ensure they pass. If `PROJECT.md` doesn't specify commands, look for them in the project instructions file or detect from `package.json` / `Makefile` / `pyproject.toml`.

### 5. Commit

Create a conventional commit for this phase:
- `feat:` for new features
- `fix:` for bug fixes
- `chore:` for maintenance
- Concise message focusing on the "why"

### 6. Next Phase

Move to the next phase and repeat. Update the Implementation Order in the plan file with a checkmark for the completed phase.

## When All Phases Are Done

After the last phase is committed:
- Run a final quality check across everything
- Summarize what was implemented
- Ask the user if they'd like to proceed with UAT

## What NOT to Do

- Don't implement multiple phases in a single subagent run. One phase per cycle.
- Don't skip the review step. Every subagent output must be reviewed.
- Don't commit without passing quality checks.
- Don't modify the plan file except to add checkmarks to Implementation Order.
