---
name: codex
description: Get a second opinion from Codex CLI (OpenAI) on plans, code, or debugging. Use this skill when the user asks to review plans with Codex, get a code review from Codex, or wants a second perspective on a bug. Also use proactively: after finishing an implementation plan, after completing a feature implementation, or when stuck debugging after 2-3 failed attempts. Trigger on phrases like "ask codex", "get a second opinion", "review with codex", "send to codex", or "/codex".
---

# Codex Second Opinion

Send work to OpenAI's Codex CLI for an independent review. Codex runs in the same repo and reads files itself -- never paste code or file contents into the prompt. Your job is to construct a focused prompt that tells Codex what to look at and what to look for.

## When to Use

**Explicitly triggered:** The user asks for a Codex review or second opinion.

**Proactively suggested:** After these events, suggest using Codex:
- After writing or updating an implementation plan
- After completing a feature implementation (before committing)
- When stuck on a bug after 2-3 failed debugging attempts

When suggesting proactively, be brief: "Want me to send this to Codex for a second opinion?"

## How Codex CLI Works

Codex is a separate AI agent (OpenAI) that runs in the terminal with full repo access. It reads files, runs commands, and returns findings. Key commands:

- `codex exec "<prompt>"` -- fresh session, new review. Note the session ID from the output (appears as `session id: <uuid>` near the top).
- `codex exec resume <session-id> "<follow-up prompt>"` -- resume a specific session by its ID. Always use the explicit session ID, not `--last`, to avoid resuming the wrong session.

Codex's output can be large. Read the full output (it may be saved to a file if too large for inline display). Extract and present the key findings to the user.

## Three Use Cases

### 1. Plan Review

Ask Codex to find real gaps in implementation plans -- broken cross-plan dependencies, missing functionality, incorrect assumptions, sequencing issues, security gaps.

**Prompt pattern:**
```
Review the implementation plan(s) at [file paths]. Find REAL GAPS ONLY -- missing functionality, broken dependencies, incorrect assumptions, sequencing issues, or security gaps. Do NOT nitpick formatting or wording. For each gap: state which file(s) are affected, what the gap is, and suggest a fix. Return a structured numbered list.
```

If there are multiple related plans, list all of them and mention their relationships. Give Codex enough context to understand the dependency chain.

For re-reviews after fixes, resume the session using the session ID from the initial run:
```
codex exec resume <session-id> "The previous N gaps have been fixed. Re-read the updated plans. Verify fixes landed. Then look for any NEW gaps. Focus on REAL blocking issues only. If clean, say so."
```

### 2. Code Implementation Review

Ask Codex to review code changes for quality, bugs, missed edge cases, and consistency with project conventions.

**Prompt pattern:**
```
Review the implementation in [file paths or description of changes]. Check for: bugs, missed edge cases, security issues, and consistency with the project's conventions (see CLAUDE.md). Focus on real issues, not style preferences. Return a structured list of findings with file paths and line references.
```

When a plan exists for the feature being reviewed, always include the plan file path(s) in the prompt so Codex can cross-reference the spec against the implementation:
```
Review the implementation of [feature name]. The plan is at [plan file path]. Read the plan, then read the implementation files listed in the plan's Files Summary. Check: does the implementation match the spec? Are there tests? Do the tests cover the spec's assertions? Return findings as a structured list.
```

### 3. Debugging

When stuck on a bug, send the error context and point Codex at the relevant code.

**Prompt pattern:**
```
I'm debugging [brief description of the issue]. The error is: [error message or behavior]. Relevant files: [paths or "look at the recent git changes"]. What I've tried: [brief list]. Find the root cause and suggest a fix.
```

## Rules

1. **Never paste code into the prompt.** Codex reads files itself. Point it at file paths.
2. **Never auto-apply fixes.** Present Codex's findings to the user and wait for their decision.
3. **Ask for structured output.** Codex's findings should be numbered lists with affected files and suggested fixes.
4. **Use session resumption for follow-ups.** If the user fixes issues and wants a re-review, use `codex exec resume <session-id>` with the explicit session ID from the initial run.
5. **Read the full output.** Codex output may be saved to a file if large. Always read and summarize the key findings.
6. **Run via Bash tool.** Execute `codex exec` commands using the Bash tool. Set a generous timeout (300-600 seconds) since Codex needs time to read files and think.

## Presenting Findings

After Codex returns:
1. Read the full output (check for persisted output files if truncated)
2. Summarize findings in a clear, structured format
3. Group by severity if applicable (blocking vs nice-to-have)
4. Note any findings you disagree with and explain why
5. Ask the user how they want to proceed

If Codex and you agree on a finding, say so -- convergence from two independent models is a strong signal. If you disagree with a Codex finding, flag it and explain your reasoning. Let the user decide.
