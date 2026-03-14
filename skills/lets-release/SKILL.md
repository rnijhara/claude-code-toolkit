---
name: lets-release
description: Release a new version with tag, changelog, version bumps, and STATE.md update
argument-hint: "[patch|minor|major]"
disable-model-invocation: true
---

You are guiding the user through a release. You analyze what changed, propose a version, and walk through each release step with confirmation.

## Getting Context

Before proposing anything:
- Read `.planning/PROJECT.md` for project config (version files, release workflow, deploy commands)
- Read `.planning/STATE.md` for current project state and version (if it exists)
- Run `git tag --sort=-v:refname | head -5` to see recent tags
- Run `git log --oneline $(git describe --tags --abbrev=0)..HEAD` to see all commits since last tag
- Read `CHANGELOG.md` for the existing format and style (if it exists)
- Browse `.planning/` for any plan files related to the changes (they have the best feature summaries)
- Read the relevant source code if needed to understand what was built

## Version Selection

- If the user provided an argument (`$ARGUMENTS`), use that: `patch`, `minor`, or `major`
- If no argument, analyze the commits and propose a version:
  - `patch` -- bug fixes only
  - `minor` -- new features (most common)
  - `major` -- breaking changes
- Present your recommendation and wait for confirmation before proceeding

## Release Steps

Walk through each step, showing the user what you plan to do. Get one confirmation, then execute all steps.

### 1. CHANGELOG.md

Add a new entry at the top following the existing format. Summarize the changes as concise bullet points. Reference the plan files for feature descriptions rather than writing from scratch. If no `CHANGELOG.md` exists, ask the user if they want one created.

### 2. Version Bumps

Update version in the files listed under "Version Files" in `.planning/PROJECT.md`. If `PROJECT.md` doesn't list version files, detect them from the project (e.g., `package.json`, `pyproject.toml`, `Cargo.toml`, `version.go`).

### 3. STATE.md

If `.planning/STATE.md` exists, update it:
- Bump the version in the Release section
- Update the date
- Add a new section under "What's Built" summarizing the feature
- Update test counts if changed
- Update "Next Steps" if priorities have shifted

### 4. Commit and Push

- Commit all release changes (changelog, versions, state)
- Push to origin
- Create and push the git tag

If the project uses submodules (e.g., `.planning` is a submodule), commit and push submodule changes first before the parent repo commit.

### 5. Deployment

If `.planning/PROJECT.md` has a deploy command under "Release", ask the user if they'd like to deploy. If no deploy config exists, skip this step.

## What NOT to Do

- Don't execute any git push or git tag without user confirmation
- Don't make up feature descriptions. Read the plan files and commits for accurate summaries.
- Don't assume project structure — read it from `PROJECT.md` or detect it.
