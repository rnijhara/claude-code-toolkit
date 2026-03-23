# Feature Name

One paragraph summary: what this is, key scope decisions or deferrals.

## Why

Current state, what triggered this, why now. Combines motivation and context so there's one place to look when revisiting this plan later.

## Research

<!-- Skip if no external references studied. Named projects with specific findings. -->

## Design Decisions

1. **Decision name** -- chose X over Y because Z.
2. ...

## Phases

<!-- ASCII dependency graph if >2 phases -->
<!-- Phase 0 → Phase 1 → Phase 2 -->

### Phase N: Title

**Why:** Motivation for this phase specifically.

**Goal:** One sentence on what's delivered.

**Tests (the spec):**
- test description at assertion level
- ...

**Changes:**
- `path/to/file.ts` -- description of what changes
- `path/to/new-file.ts` (new) -- what it does

## Files Summary

| File | Action | Phase |
|------|--------|-------|
| `path/to/file.ts` | Modify | 1 |

## UAT Scenarios

1. Step-by-step manual verification scenario
2. ...

## Edge Cases

- **Scenario name** -- what happens, how the system handles it

## Deployment Notes

<!-- Env vars, Slack scopes, EC2 commands, etc. Skip if none. -->

## Open Questions

<!-- Remove this section entirely when plan is implementation-ready. Its presence signals "still discussing, not ready to implement." -->

## Implementation Order

1. Phase 0: description
2. Phase 1: description
