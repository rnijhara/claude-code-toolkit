---
name: lets-plan
description: Discuss and create a structured implementation plan in .planning/
argument-hint: "[feature-name]"
---

You are helping the user plan a new feature or task. Your goal is to have a thorough discussion, refine ideas iteratively, and produce a structured plan file in `.planning/` when ready.

## Getting Context

Before discussing, read these to understand the project:
- `.planning/PROJECT.md` for project config (stack, quality commands, structure)
- `.planning/STATE.md` for current project state, what's built, and what's next (if it exists)
- `.planning/PRODUCT.md` for product vision and architecture (if it exists)
- Project instructions file (`CLAUDE.md` or `AGENTS.md`) for conventions and project structure
- Relevant source code for areas the feature will touch

Browse `.planning/` for completed plans in similar areas. They provide useful patterns and context for how prior features were designed.

## How We Plan

1. **Discuss first, don't write yet.** Understand what the user wants, ask clarifying questions, explore trade-offs. Do not create the plan file until you have sufficient context and alignment.
2. **Surface decisions explicitly.** When a design choice comes up, present the options with trade-offs and make a recommendation. Document the chosen option AND the rejected alternatives with reasons.
3. **Think about edge cases and UAT early.** Don't treat these as afterthoughts. Ask "what could go wrong?" and "how would we manually verify this?" during discussion, not after the plan is written.
4. **Break into phases.** Each phase should be independently implementable and testable. Consider dependencies between phases.
5. **Be specific about changes.** Name exact files, describe what changes in each, write test cases at assertion level. The plan should be detailed enough for an implementation agent to execute without ambiguity.

## Creating the Plan File

When the user is ready (they'll say so, or you'll have covered enough ground), create the plan file at `.planning/{FEATURE_NAME}.md` using the template at `template.md` bundled with this skill.

Key rules:
- **Why section is required.** Every plan needs motivation and context in one place.
- **Design Decisions is the most important section.** A plan without explicit decisions is incomplete.
- **Tests at assertion granularity** per phase, not vague "add tests for X."
- **UAT Scenarios are required.** Step-by-step manual verification. Think adversarially. Include the scenarios where the user tries something unexpected (like typing "2m" instead of "120" for an interval).
- **Edge Cases are required.** Named scenarios with how the system handles them.
- **Open Questions section** means the plan is still in discussion. Remove it entirely when the plan is implementation-ready.
- **Implementation Order** at the bottom tracks progress. Phases get checkmarks as they're completed.

## What NOT to Do

- Don't include full code blocks in the plan. Describe what changes, don't write the code.
- Don't include dependency installation commands. Those belong in Deployment Notes if anywhere.
- Don't create the plan file until the user is aligned on the approach.
- Don't skip the Why section even if the motivation seems obvious.
