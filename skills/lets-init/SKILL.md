---
name: lets-init
description: Initialize .planning/ directory and PROJECT.md with auto-detected project config
argument-hint: ""
---

You are initializing a project for use with the lets-plan, lets-implement, and lets-release skills. Your goal is to auto-detect as much as possible from the codebase, confirm with the user, and write `.planning/PROJECT.md`.

## What to Detect

Scan the project root for these signals:

1. **Language & Framework** — look for `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`, `pom.xml`, `build.gradle`, `Makefile`, etc.
2. **Package manager** — npm, pnpm, yarn, bun, pip, poetry, cargo, go, maven, gradle, etc.
3. **Monorepo vs single package** — check for workspaces config, `packages/`, `apps/`, `services/` directories.
4. **Quality commands** — look for scripts in `package.json`, `Makefile` targets, `pyproject.toml` scripts, CI config (`.github/workflows/`, `.gitlab-ci.yml`). Identify lint, typecheck, test, and build commands.
5. **Version files** — files containing a version string that should be bumped during releases (e.g., `package.json`, `pyproject.toml`, `version.go`, `Cargo.toml`).
6. **Git branching** — check the default branch name, whether there's a `develop` branch, and look at recent branch naming patterns.
7. **Deploy workflow** — look for deploy scripts, Dockerfiles, CI/CD deploy stages, infrastructure config.
8. **Existing project docs** — check for `CLAUDE.md`, `AGENTS.md`, `README.md`, `.planning/` to avoid duplicating what's already documented.

## How to Interact

1. **Show what you detected.** Present findings grouped by category. Be specific — show the actual commands you found, not just "found lint command."
2. **Ask the user to confirm or correct.** Some things can't be auto-detected (e.g., which deploy command to use, whether there are manual release steps).
3. **Don't assume.** If you can't detect something, ask. Don't fill in placeholder values.

## Writing PROJECT.md

After confirmation, create `.planning/PROJECT.md` using this structure:

```markdown
# Project Configuration

## Stack
- **Language:** e.g., TypeScript
- **Framework:** e.g., Next.js, FastAPI, Go stdlib
- **Package manager:** e.g., pnpm
- **Structure:** e.g., monorepo with packages/server, packages/web, packages/shared

## Quality Commands
- **Lint:** e.g., `pnpm biome check --write`
- **Typecheck:** e.g., `pnpm exec tsc --noEmit`
- **Test:** e.g., `pnpm test`
- **Build:** e.g., `pnpm build`

## Version Files
- `package.json`
- `packages/server/package.json`

## Git
- **Default branch:** main
- **Branch convention:** e.g., feature/*, fix/*, chore/*

## Release
- **Versioning:** semver
- **Changelog:** CHANGELOG.md
- **Deploy:** e.g., `ssh deploy@prod 'cd /app && git pull && pm2 restart all'`

## Notes
Any project-specific notes the user mentioned during init.
```

Omit sections where no information was found or provided. Don't include placeholder values like "TBD" — if it's unknown, leave the section out entirely.

## What NOT to Do

- Don't overwrite an existing `.planning/PROJECT.md` without asking.
- Don't create plan files — that's what `/lets-plan` is for.
- Don't make up commands or paths you didn't find in the codebase.
- Don't include information already in `CLAUDE.md` or `AGENTS.md` — reference those files instead.
