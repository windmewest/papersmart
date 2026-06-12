---
description: Apply focused local revisions to an existing PaperSmart manuscript, including AIGEN/AIPO inline markers.
---

# /papersmart-revision

Use the `PaperSmart-revision` skill.

## Preflight

1. Identify the active project.
2. Read `paper.md`, local revision tasks, project config, style notes, and affected artifacts.
3. Treat user comments and reviewer comments as guidance, not manuscript prose.
4. If the manuscript contains `*content*AIGEN` or `*content*AIPO`, resolve those markers according to the PaperSmart-revision marker rules.

## Plan

Apply only the requested local change and synchronize affected citations, tables, figures, captions, references, and logs.

For inline markers:

- `*content*AIGEN`: regenerate the marked span from surrounding manuscript logic and evidence.
- `*content*AIPO`: polish and repair the marked span for coherence, consistency, and repetition.

## Commands

Follow `PaperSmart-revision`. Do not convert a local revision into a full rewrite unless the user asks.

## Verification

Confirm changed sections, affected artifacts, TODOs, citation numbering, and change-log entry.
Confirm no unresolved `AIGEN` or `AIPO` markers remain unless the user asked for a marked review copy.

## Summary

Report files changed and whether the task stayed local.

## Next Steps

Use `/papersmart-draft` only if the change requires a broader manuscript rebuild.
