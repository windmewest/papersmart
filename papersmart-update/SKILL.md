---
name: papersmart-update
description: Safely update an existing PaperSmart workspace to the current folder and template structure without overwriting project files, shared resources, memory, drafts, references, outputs, revision records, or submission packages. Use when PaperSmart has been upgraded, a workspace is missing newer folders such as writing_samples, a profile needs to be rebuilt, or older projects need non-destructive structure migration.
---

# PaperSmart-update

## Overview

Use this skill after PaperSmart itself changes. It brings an existing workspace up to the current directory contract while preserving user work.

The update is conservative by default:

- Create missing folders.
- Create missing template files.
- Rebuild `papersmart_profile.md` if it is missing.
- Copy useful details from older memory files when possible.
- Never overwrite non-empty files unless the user explicitly asks.
- Never delete, rename, or move project files automatically.

## Language And Path Mode

Read the workspace profile first:

- English: `shared/memory/papersmart_profile.md`
- Chinese: `共享/记忆/papersmart_profile.md`

If no profile exists, infer the mode from the workspace roots:

- `projects/` and `shared/` means English mode.
- `项目/` and `共享/` means Chinese mode.
- If both are absent or both modes appear ambiguous, ask before applying changes.

When the profile says `language: zh`, answer the user in Chinese and use Chinese folder/template names.

## Safe Update Rules

1. Start with a dry run unless the user has clearly asked to apply the update.
2. Do not modify files in `01_draft`/`01_草稿` or `02_reference`/`02_参考` except to add missing README, inventory, index, style note, or `writing_samples`/`写作样本` folders.
3. Do not overwrite manuscript outputs, figure files, tables, supplements, translations, revision logs, submission files, memory files, shared docs, prompts, tools, or skills.
4. If an old file needs migration, copy information into a new file and keep the old file in place.
5. Record every created file, created folder, preserved conflict, and migration note in the update report.

## Workflow

Run a dry run:

```bash
python shared/skills/papersmart-update/scripts/update_papersmart.py --workspace . --dry-run
```

Apply the update:

```bash
python shared/skills/papersmart-update/scripts/update_papersmart.py --workspace .
```

Force a known language mode only when the user confirms it:

```bash
python shared/skills/papersmart-update/scripts/update_papersmart.py --workspace . --language zh
```

## What The Script Updates

- Workspace roots: `projects/shared` or `项目/共享`.
- Shared folders: docs, prompts, tools, skills, memory.
- Project folders: config, logs, draft, reference, output.
- Reference folders: literature, target journal, writing samples.
- Output folders: manuscript, tables, figures, supplement, revision, translation, submission.
- Missing templates: project config, data inventory, style notes, reference index, output README, change log, local revision tasks, writing log, decision log.
- Profile: `papersmart_profile.md`, including language, active project, and path map.

## Handoff

After running, report:

- Detected language mode.
- Number of folders created.
- Number of files created.
- Any preserved conflicts or skipped non-empty files.
- Update report path.
- Whether the workspace is now ready for later PaperSmart skills.
