---
description: Resolve AIREF inline markers in a PaperSmart manuscript by verifying claims, adding suitable citations, narrowing claims when necessary, and logging the evidence decision.
---

# /papersmart-airef

Use the `PaperSmart-AIREF` skill.

## Preflight

1. Identify the active project and manuscript path.
2. Read the surrounding manuscript section, current references, claim-source map, and affected figure/table captions.
3. Locate each `*content*AIREF` marker and identify the exact claim needing support.

## Plan

For each marker, decide whether existing references support the claim. If not, search for scholarly or authoritative sources that support the claim's specific verb, scope, and context.

## Commands

Follow `PaperSmart-AIREF`. Do not invent citations, source details, DOIs, URLs, page ranges, publication years, or source claims. If adequate evidence cannot be found, use `TODO: [specific missing evidence or action]`.

## Verification

Confirm all resolved markers, added or reused references, narrowed claims, remaining TODOs, citation numbering, and change-log entries.
