---
name: papersmart-init
description: Initialize a PaperSmart scientific-manuscript workspace or a new PaperSmart project folder, including the projects/shared directory model, required draft/reference/output/config/log templates, and companion Codex skills. Use when the user asks to set up PaperSmart, create the base file system, scaffold a new manuscript project, install PaperSmart dependencies, or prepare a reusable PaperSmart workspace for other users.
---

# PaperSmart-init

## Overview

Set up the PaperSmart working environment before any manuscript writing. Preserve the separation between paper-specific project files under `projects/` and reusable resources under `shared/`.

Use `scripts/init_papersmart.py` for first-time filesystem setup. Install companion skills when network access and user approval are available; otherwise leave clear install commands. For routine new papers after the workspace exists, use `PaperSmart-new-project`.

## Inputs

- Workspace root, defaulting to the current directory.
- Optional project slug, for example `paper_01_digital_doppelganger`.
- Optional working title, target journal, language, and short research objective.
- Optional instruction to install companion skills immediately.

## Directory Contract

Create this workspace shape:

```text
projects/
  README.md
shared/
  README.md
  docs/
  prompts/
  tools/
  skills/
  memory/
```

When a project slug is provided, create:

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

Do not put project-specific drafts, data, outputs, revision records, or submission packages in `shared/`.

## Workflow

1. Identify whether the task is workspace initialization or new-project scaffolding. If the user only asks for base setup, create `projects/` and `shared/` without a project folder.
2. If creating a project and multiple naming choices are possible, choose a short lowercase slug from the title. Use `paper_XX_short_slug` when the user has not specified a naming convention.
3. Run the script:

```bash
python shared/skills/papersmart-init/scripts/init_papersmart.py --workspace . --project-slug paper_01_short_slug --project-title "Working title"
```

Add `--install-skills` when the user asks for dependency installation and network access is allowed:

```bash
python shared/skills/papersmart-init/scripts/init_papersmart.py --workspace . --install-skills
```

4. Confirm that the script did not overwrite original user materials. Existing files should be preserved unless the user explicitly requested replacement.
5. If companion skill installation fails, write the exact manual commands to `shared/memory/install_notes.md` and tell the user to restart Codex after installation.

## Companion Skills

PaperSmart expects these skills to be available:

- `find-skills`, used to choose the smallest useful skill set for a manuscript task.
- `humanizer`, used when the user wants writing to sound less machine-generated.
- Nature-family academic skills, especially `nature-academic-search`, `nature-writing`, `nature-polishing`, `nature-figure`, `nature-citation`, `nature-response`, `nature-data`, `nature-reader`, and `nature-paper2ppt`.

Installation sources used by the script:

- `find-skills`: `https://github.com/vercel-labs/skills/tree/main/skills/find-skills`
- `humanizer`: `https://github.com/blader/humanizer`
- Nature skills: `https://github.com/Yuan1z0825/nature-skills`

The script first checks whether those skill folders already exist under `$CODEX_HOME/skills` or `~/.codex/skills`. Skip installation for skills that are already present.

## Project Templates

Use precise `TODO:` markers instead of guessing missing details. Template files should capture:

- Working title, article type, target journal, language, authors, study objective, research questions, methods, data sources, ethics, funding, conflicts, acknowledgements, and missing information in `config/project_config.md`.
- Source materials, known datasets, table/figure inventories, known data-quality issues, and expected comparisons in `01_draft/data_inventory.md`.
- Journal format, writing style, heading style, abstract length, citation style, table/figure rules, and submission constraints in `02_reference/style_notes.md`.
- Literature anchors, target-journal files, writing samples, PDFs, citation files, and "style only, do not cite" notes in `02_reference/reference_index.md`.

## Handoff

After initialization, tell the user:

- The workspace or project path created.
- Which companion skills are installed, already present, or still missing.
- Where to place original materials: `01_draft` for user materials and `02_reference` for style/literature context.
- That generated outputs must go to `03_output`.
- To use `PaperSmart-new-project` for future papers instead of rerunning full initialization.
