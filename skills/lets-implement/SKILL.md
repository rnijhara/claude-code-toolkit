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

## Implementation Cycle (TDD: Red-Green-Refactor)

For each phase (or the specified phase), repeat this cycle:

### 1. Write Tests (subagent)

Spawn a subagent with a clear prompt:
- Include the full plan file path so it can read it
- Specify which phase to implement
- Tell it to read the relevant existing code before making changes
- Tell it to write **only the test files** for this phase -- no production code
- Tell it to follow the plan's "Tests (the spec)" section for this phase
- Tell it NOT to commit

The subagent prompt should be self-contained. Include enough context that it can work autonomously.

### 2. Review Tests (you, the orchestrator)

After the subagent completes:
- Run `git diff --stat` to see what files changed
- **Read the full test files** (not just the diff). Use the Read tool on each modified file to understand the tests in full context.
- Check against the plan: do the tests match the spec for this phase?
- Check for: missing edge cases, wrong assertions, tests that would pass trivially, tests that don't actually validate the intended behavior
- Fix issues directly if found. Do not use a subagent for test fixes.

### 3. Red -- Confirm Tests Fail

Run the tests and confirm they fail as expected. This validates that the tests are actually testing something new and won't pass without the implementation.

### 4. Implement (subagent)

Spawn a subagent with a clear prompt:
- Include the full plan file path so it can read it
- Specify which phase to implement
- Tell it to read the relevant existing code and the tests just written
- Tell it to write **only the production code** to make the tests pass
- Tell it to run the quality commands from `.planning/PROJECT.md` when done (lint, typecheck, test)
- Tell it NOT to commit

### 5. Green -- Confirm Tests Pass

Run the tests and confirm they pass. If they don't, investigate and fix directly.

### 6. Review Implementation (you, the orchestrator)

After the subagent completes:
- Run `git diff --stat` to see what files changed
- **Read the full changed files** (not just the diff). Use the Read tool on each modified file to understand the complete code in context. Diffs can hide issues that are only visible when reading the full file (wrong imports, duplicated logic, inconsistent patterns with surrounding code).
- Check against the plan: are all items in this phase addressed?
- Check for: missing edge cases, type safety, error handling, convention violations
- Fix issues directly if found. Do not use a subagent for fixes.

### 7. Quality Checks

Run the quality commands defined in `.planning/PROJECT.md` (lint, typecheck, test) and ensure they pass. If `PROJECT.md` doesn't specify commands, look for them in the project instructions file or detect from `package.json` / `Makefile` / `pyproject.toml`.

### 8. Commit

Create a conventional commit for this phase:
- `feat:` for new features
- `fix:` for bug fixes
- `chore:` for maintenance
- Concise message focusing on the "why"

### 9. Next Phase

Move to the next phase and repeat. Update the Implementation Order in the plan file with a checkmark for the completed phase.

## When All Phases Are Done

After the last phase is committed:
- Run a final quality check across everything
- Summarize what was implemented
- Ask the user if they'd like to proceed with UAT

## What NOT to Do

- Don't implement multiple phases in a single subagent run. One phase per cycle.
- Don't write tests and production code in the same subagent run. Tests come first, separately.
- Don't skip review steps. Both test and implementation subagent outputs must be reviewed.
- Don't skip the Red step. If tests pass before implementation, something is wrong -- the tests are either trivial or testing existing behavior.
- Don't commit without passing quality checks.
- Don't modify the plan file except to add checkmarks to Implementation Order.
