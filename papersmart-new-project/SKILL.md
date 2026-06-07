---
name: papersmart-new-project
description: Create a new paper-specific project folder inside an existing PaperSmart workspace, using the workspace language profile to scaffold English or Chinese folders, config/draft/reference/output/log directories, writing_samples, starter templates, and active-project memory. Use when the user starts a new manuscript, paper, article, research project, journal submission, or wants a fresh project folder without re-running full PaperSmart initialization.
---

# PaperSmart-new-project

## Overview

Create a new manuscript project without reinstalling skills or rebuilding the shared workspace. Use `PaperSmart-init` only for first-time setup; use this skill for routine new papers.

## Language And Path Mode

Read the workspace profile before creating files:

- English profile: `shared/memory/papersmart_profile.md`
- Chinese profile: `共享/记忆/papersmart_profile.md`

Use the profile's `language` and path map. In Chinese mode, create Chinese folder and template names and answer the user in Chinese.

## Preconditions

- The workspace should already contain the configured project and shared roots, for example `projects/` and `shared/` in English mode or `项目/` and `共享/` in Chinese mode.
- If those roots do not exist, use `PaperSmart-init` first.
- Do not place project-specific materials in `shared/`.
- Do not overwrite an existing project unless the user explicitly requests it.

## Inputs

Collect or infer:

- Working title or short topic.
- Optional project slug, for example `paper_03_ai_architectural_design`.
- Optional target journal, article type, manuscript language, authors, and research objective.
- Whether the new project should become the active project. Default: yes.

## Workflow

1. Read the PaperSmart profile and choose the matching path map.
2. Inspect the configured project root to find existing `paper_XX_*` folders.
3. If the user did not provide a slug, infer the next number and a lowercase slug from the title.
4. Use a stable ASCII slug: lowercase letters, digits, and underscores. Keep it short.
5. Run the script:

```bash
python shared/skills/papersmart-new-project/scripts/new_project.py --workspace . --title "Working title"
```

Use explicit fields when available:

```bash
python shared/skills/papersmart-new-project/scripts/new_project.py --workspace . --slug paper_03_short_slug --title "Working title" --target-journal "TODO" --language "English"
```

6. Confirm the created path and the active project record.
7. Tell the user where to put materials:
   - `01_draft` for original drafts, data, images, tables, and notes.
   - `02_reference` for target journal files, writing samples, literature, and style references.
   - `03_output` for generated manuscripts, tables, figures, revisions, translations, and submission packages.

## Created Structure

```text
projects/<project_slug>/
  README.md
  config/project_config.md
  logs/writing_log.md
  logs/decision_log.md
  01_draft/README.md
  01_draft/data_inventory.md
  01_draft/data/
  01_draft/figures/
  01_draft/tables/
  01_draft/notes/
  02_reference/README.md
  02_reference/style_notes.md
  02_reference/reference_index.md
  02_reference/literature/
  02_reference/target_journal/
  02_reference/writing_samples/
  03_output/README.md
  03_output/manuscript/
  03_output/tables/
  03_output/figures/
  03_output/supplement/
  03_output/revision/change_log.md
  03_output/revision/local_revision_tasks.md
  03_output/translation/
  03_output/submission/
```

## Template Rules

- Use precise `TODO:` markers for unknown project metadata.
- Record style-only samples as style-only in `02_reference/reference_index.md`.
- Keep original user files in `01_draft` and `02_reference`.
- Keep generated outputs in `03_output`.
- Update `papersmart_profile.md` so future PaperSmart skills know the active project, output language, and path map.

## Handoff

After creation, recommend the next skill based on the user's stage:

- `PaperSmart-outline` for argument architecture and section planning.
- `PaperSmart-draft` for full manuscript generation.
- `PaperSmart-figures` for figure planning or production.
- `PaperSmart-submission` when a manuscript is ready for journal packaging.
