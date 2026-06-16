---
description: Apply focused local revisions to an existing PaperSmart manuscript, including AIGEN/AIPO/AIREF inline markers.
---

# /papersmart-revision

Use the `PaperSmart-revision` skill.

## Preflight

1. Identify the active project.
2. Classify whether the request is advice/report generation or implementation into the manuscript.
3. For advice-only review, audit, modification suggestions, method improvement steps, or operation steps, write a Markdown artifact under `03_output/revision` or `03_output/supplement` and do not edit `paper.md`.
4. For implementation, read `paper.md`, local revision tasks, project config, style notes, and affected artifacts.
5. Treat user comments and reviewer comments as guidance, not manuscript prose.
6. If the manuscript contains `*content*AIGEN`, `*content*AIPO`, or `*content*AIREF`, resolve those markers according to the PaperSmart marker rules.

## Plan

Apply only the requested local change and synchronize affected citations, tables, figures, captions, references, and logs.

For inline markers:

- `*content*AIGEN`: regenerate the marked span from surrounding manuscript logic and evidence.
- `*content*AIPO`: polish and repair the marked span for coherence, consistency, and repetition.
- `*content*AIREF`: verify the marked claim, add suitable citation support, and narrow the claim when evidence requires it.

## Commands

Follow `PaperSmart-revision`. Do not convert advice-only content into manuscript prose, and do not convert a local revision into a full rewrite unless the user asks.

## Verification

Confirm changed sections, affected artifacts, TODOs, citation numbering, and change-log entry.
Confirm no unresolved `AIGEN`, `AIPO`, or `AIREF` markers remain unless the user asked for a marked review copy.

## Summary

Report files changed and whether the task stayed local.

## Next Steps

Use `/papersmart-draft` only if the change requires a broader manuscript rebuild.
