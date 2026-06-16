---
description: Draft or substantially rewrite a PaperSmart manuscript from project materials.
---

# /papersmart-draft

Use the `PaperSmart-draft` skill.

## Preflight

1. Identify the active project and language mode.
2. Read required project files before writing.
3. Classify the requested artifact type before writing. Use `paper.md` only for formal manuscript prose.
4. Classify inputs as evidence, context, writing samples, user comments, review/advice artifacts, or task instructions.

If the user asks for review, audit, reviewer comments, modification advice, method improvement, operation steps, `审核`, `审稿`, `修改意见`, `修改建议`, `改进建议`, or `操作步骤`, route the output to `03_output/revision` or `03_output/supplement`; do not create or overwrite `03_output/manuscript/paper.md`.

## Plan

Create analysis plans, visualization plans, claim-source maps, and manuscript prose from verified evidence.

## Commands

Follow `PaperSmart-draft`. Do not place chat replies, user comments, screenshot provenance, review reports, modification advice, method-operation plans, or drafting plans in manuscript prose.

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
