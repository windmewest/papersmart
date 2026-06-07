---
name: papersmart-figures
description: Plan, create, revise, audit, and caption PaperSmart manuscript figures, tables, workflow diagrams, data visualizations, and composite figures using project evidence and journal requirements. Use when the user asks for figure planning, visualization plans, manuscript-ready scientific diagrams, data plots, figure captions, figure QA, image orientation checks, or updates to 03_output/figures and 03_output/supplement/visualization_plan.md.
---

# PaperSmart-figures

## Overview

Make figures serve the manuscript argument. Figure work starts by defining the conclusion each figure should support, then choosing the data, visual form, caption, and manuscript placement.

Use `nature-figure` for journal-grade scientific plotting when its trigger fits. If that skill requires the user to choose Python or R, ask exactly that before plotting.

## Language And Path Mode

Before reading project files, read the PaperSmart profile:

- English mode: `shared/memory/papersmart_profile.md`
- Chinese mode: `共享/记忆/papersmart_profile.md`

Use the configured path map. If `language` is `zh`, use Chinese folder names and answer in Chinese. If no profile exists, assume English mode.

## Required Reading

Read from the active project:

1. `config/project_config.md`
2. `01_draft/data_inventory.md`
3. `02_reference/style_notes.md`
4. `02_reference/reference_index.md`
5. Relevant target-journal files and `02_reference/writing_samples`
6. Existing `03_output/supplement/data_analysis_plan.md`, if present
7. Existing `03_output/supplement/visualization_plan.md`, if present
8. Relevant source data, images, tables, figure scripts, and captions

In Chinese mode, use the equivalent configured paths.

## Workflow

1. Define the manuscript claim or result each requested figure should support.
2. Audit the relevant data or source images before plotting or composing.
3. Choose the figure type because it clarifies interpretation, not because the source file is available.
4. Create or update `03_output/supplement/visualization_plan.md` for substantial figure work.
5. Generate or revise files in `03_output/figures` using stable names such as `figure_1_methodology_flowchart.svg`.
6. Create a figure note or caption file when useful, for example `figure_1_methodology_flowchart.md`.
7. Update `03_output/supplement/claim_source_map.md` when the figure supports a major claim.
8. Update manuscript in-text citations and figure numbering when the user asks for integration.
9. Record figure generation or revision in `03_output/revision/change_log.md`.

## Figure Selection

Consider:

- Radar charts, heatmaps, paired profile plots, parallel coordinates, or slope charts for multi-attribute aesthetic profiles.
- Expert scoring heatmaps, mean/range plots, disagreement plots, ranking plots, or qualitative theme summaries.
- Traditional computer-vision metric heatmaps, scatterplots, paired-difference plots, or metric-conflict figures.
- Integrated multi-panel figures when the study depends on triangulated evidence.
- Manuscript-ready workflow diagrams for methods, data flow, model flow, evaluation design, or submission logic.
- Tables only when structured comparison is clearer than a plot.

## Figure Quality Rules

- Every figure must have a stable file name, title, complete caption, data/source note, and manuscript placement.
- Workflow figures must be finished scientific diagrams, not rough sketches.
- Use clear hierarchy, consistent typography, labeled stages, meaningful color coding, and journal-suitable resolution.
- Do not make decorative figures that do not support an argument.
- Do not use source images without checking copyright, permission, and source attribution needs.
- Preserve original image orientation in composite figures unless source evidence requires rotation.
- Verify orientation against the original files, especially photographs and user-flagged orientation-sensitive images.
- Keep figure numbering in first-citation order when integrating into the manuscript.

## Visualization Plan Shape

Use:

```markdown
# Visualization plan

| Figure/table | Claim served | Source data | Visual form | Output file | Manuscript placement | Status |
| --- | --- | --- | --- | --- | --- | --- |

## Excluded candidate figures

| Candidate | Reason excluded |
| --- | --- |

## QA notes

- Orientation checks:
- Caption checks:
- Journal format checks:
```

## Final Check

Report:

- Files created or changed.
- Data or image sources used.
- Claims each figure supports.
- Remaining permission, resolution, orientation, or caption TODOs.
