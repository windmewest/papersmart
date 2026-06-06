---
name: papersmart-draft
description: Generate or substantially revise full PaperSmart manuscripts from active project materials, including literature evidence, data analysis plans, visualization plans, claim-source mapping, tables, figures, manuscript text, references, and quality checks. Use when the user asks to draft a full paper, write a manuscript, produce Results/Discussion from data, rebuild a major section, integrate literature into a manuscript, or create a journal-ready PaperSmart draft.
---

# PaperSmart-draft

## Overview

Draft a complete, traceable, journal-aware manuscript from PaperSmart materials. The draft must be evidence-driven: read sources first, plan analysis and visualization before Results, then write.

## Project Selection

1. Identify the active project under `projects/`.
2. If the user names a project, use it.
3. If only one project exists, use it.
4. If multiple projects exist and the intended project is unclear, ask before writing.

## Required Reading

Read in this order before generating or revising a full manuscript:

1. `config/project_config.md`
2. `01_draft/README.md`
3. `01_draft/data_inventory.md`
4. `02_reference/style_notes.md`
5. `02_reference/reference_index.md`
6. Specific drafts, outlines, notes, data files, tables, figures, images, target-journal materials, citation files, and reference PDFs needed for the task

For local revisions after a full manuscript already exists, prefer `PaperSmart-revision`. Use this skill only when the requested change is a major rewrite, a new Results/Discussion pass, or a full draft-level revision.

## Full Draft Workflow

1. Define the task boundary: full manuscript, major section rewrite, Results/Discussion generation, literature integration, or journal adaptation.
2. Extract project constraints: title, article type, target journal, language, authors, research questions, methods, data sources, declarations, and missing information.
3. Extract journal style from `02_reference/target_journal` when available. Respect heading style, abstract length, figure/table captions, citation style, reference style, and declaration order.
4. Perform a structured literature search for full manuscript generation, major revisions, introductions, discussions, and literature reviews unless the user explicitly says not to. Derive constraints first: research goal, core concepts, definitions, methods needing support, disciplinary scope, date range, inclusion/exclusion rules, and source priorities.
5. Save 8-12 key literature conclusions to `03_output/supplement/literature_evidence_matrix.md`. Each conclusion must include evidence strength, high-quality citations, manuscript placement, and caveats.
6. Audit all available datasets, scoring files, tables, images, statistical outputs, and generated figures before writing Results.
7. Save `03_output/supplement/data_analysis_plan.md`. State which data are used, which are excluded, what each analysis tests or illustrates, derived quantities to compute, and how each analysis supports the manuscript argument.
8. Save `03_output/supplement/visualization_plan.md` when data or diagrams are useful. Choose figures because they clarify interpretation, not because files happen to exist.
9. Generate or update tables in `03_output/tables` and figures in `03_output/figures`. Every table and figure needs a stable file name, concise title, complete caption, data source, and in-text citation.
10. Create or update `03_output/supplement/claim_source_map.md`, mapping major claims to user materials, data, figures/tables, literature, or TODOs.
11. Draft `03_output/manuscript/paper.md`, following target journal structure when known.
12. Update `03_output/revision/change_log.md`; update `logs/writing_log.md` and `logs/decision_log.md` for major writing or evidence decisions.
13. Run a quality pass before delivery.

## Writing Standards

- Do not invent data, results, statistics, citations, author details, journal requirements, ethics, funding, conflicts, or acknowledgements.
- Use precise `TODO:` markers for missing required information.
- Introduction must integrate literature logic and research gaps, not merely introduce the study.
- Methods must explain materials, data, models, evaluation methods, analysis boundaries, and reproducibility limits.
- Results must interpret evidence through findings. Do not merely walk through tables.
- Discussion must connect findings to literature, disagreements, theory, limitations, and future work.
- Keep claims traceable to `01_draft`, `02_reference`, verified literature, generated analysis outputs, or explicit user instructions.
- If using numbered citations, keep numbers continuous and ordered by first appearance. Every reference-list item must be cited, and every in-text citation must have a matching reference.
- If the target journal uses unnumbered headings, remove chapter-style or decimal heading numbers from the final manuscript.

## Data And Figure Expectations

For data-driven manuscripts, inspect agreement and disagreement rather than only displaying available values. Use derived quantities where justified:

- Group comparisons
- Means, ranges, standard deviations, differences, rankings, disagreement scores, correlations, or conflict indicators
- Qualitative codes or comment themes
- Outlier and counterexample analysis
- Small-sample descriptive interpretation, avoiding unsupported significance claims

Use richer visualizations when they serve the argument:

- Radar charts, heatmaps, paired profile plots, parallel coordinates, or slope charts for multi-attribute aesthetic profiles.
- Expert scoring heatmaps, mean/range plots, disagreement plots, ranking plots, or qualitative keyword/theme summaries.
- Traditional computer-vision metric heatmaps, scatterplots, paired-difference plots, or metric-conflict figures.
- Integrated multi-panel figures for triangulated evidence.
- Manuscript-ready workflow diagrams with clear hierarchy, consistent typography, labeled stages, meaningful color coding, and journal-suitable resolution.

When creating composite figures from source images, preserve original orientation unless source evidence requires rotation. Verify orientation against the original files.

## Skill Coordination

Use companion skills when their trigger fits:

- Use `find-skills` to choose the smallest useful skill set for a complex request.
- Use `PaperSmart-new-project` for routine new project folders after the workspace exists.
- Use `PaperSmart-revision` for focused edits after `03_output/manuscript/paper.md` exists.
- Use `PaperSmart-translation` for Chinese academic translation.
- Use `PaperSmart-figures` for figure planning, generation, and QA.
- Use `PaperSmart-submission` for journal submission packages.
- Use `nature-academic-search` for structured literature retrieval and citation verification.
- Use `nature-writing` or `nature-polishing` for Nature-leaning academic structure or prose quality when the user asks for that style.
- Use `nature-figure` for manuscript-grade scientific figures when the user selects Python or R.
- Use `nature-citation` when the user asks to add strict Nature/CNS-style citations to claims.
- Use `humanizer` only when the user asks to remove AI-like writing patterns or make prose sound more natural; preserve scientific caution.

## Quality Pass

Before considering the manuscript ready for human review, check:

- Source integrity and `TODO:` precision.
- Literature evidence quality and citation consistency.
- Structure against the target journal.
- Data analysis plan and visualization plan completeness.
- Table and figure numbering by first citation order.
- Claim support for background, methods, results, and discussion claims.
- Reference list consistency.
- Logs and change records.

Report any unverified citation details, missing materials, or remaining author confirmations clearly.
