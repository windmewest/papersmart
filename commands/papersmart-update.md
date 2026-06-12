---
description: Safely update an existing PaperSmart workspace to the current structure.
---

# /papersmart-update

Use the `PaperSmart-update` skill.

## Preflight

1. Detect the workspace language from `papersmart_profile.md` or existing roots.
2. Start with a dry run unless the user clearly asked to apply changes.
3. Confirm no project-specific files should be overwritten.

## Plan

Create missing folders and missing templates while preserving projects, shared resources, memory, drafts, references, outputs, revisions, translations, and submissions.

## Commands

Run the updater script when appropriate:

```bash
python shared/skills/papersmart-update/scripts/update_papersmart.py --workspace . --dry-run
```

Apply changes only after the user accepts the dry-run plan or explicitly asks to apply the update.

## Verification

Read the generated update report and confirm preserved files.

## Summary

Report created folders, created files, skipped existing files, and update report path.

## Next Steps

Use the relevant PaperSmart workflow command after the workspace structure is current.
