---
description: Draft or substantially rewrite a PaperSmart manuscript from project materials.
---

# /papersmart-draft

Use the `PaperSmart-draft` skill.

## Preflight

1. Identify the active project and language mode.
2. Read required project files before writing.
3. Classify inputs as evidence, context, writing samples, user comments, or task instructions.

## Plan

Create analysis plans, visualization plans, claim-source maps, and manuscript prose from verified evidence.

## Commands

Follow `PaperSmart-draft`. Do not place chat replies, user comments, screenshot provenance, or drafting plans in manuscript prose.

## Verification

Run the contamination audit when a manuscript file exists:

```bash
python shared/skills/papersmart-draft/scripts/audit_manuscript_contamination.py --file <active_project>/03_output/manuscript/paper.md
```

Also check citation continuity, figure/table numbering, claim support, and TODO precision.

## Summary

Report generated files, evidence gaps, and any contamination audit findings.

## Next Steps

Use `/papersmart-revision` for focused edits after the full draft exists.
