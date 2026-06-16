---
name: papersmart-outline
description: Create or revise PaperSmart manuscript outlines, argument maps, article structures, section plans, figure/table plans, and evidence plans from an active project. Use when the user asks for a paper outline, research-paper structure, manuscript plan, argument framework, journal-specific outline, literature-backed outline, or conceptual architecture before full drafting.
---

# PaperSmart-outline

## Overview

Turn rough research materials into a journal-aware, evidence-grounded manuscript outline. The output should be a usable writing blueprint, not a generic section list.

## Language And Path Mode

Before reading project files, read the PaperSmart profile:

- English mode: `shared/memory/papersmart_profile.md`
- Chinese mode: `共享/记忆/papersmart_profile.md`

Use the configured path map. If `language` is `zh`, use Chinese folder names and answer in Chinese. If no profile exists, assume English mode.

## Project Selection

1. Identify the active project under the configured project root.
2. If the user names a project, use it.
3. If only one project exists, use it.
4. If multiple projects exist and the intended project is unclear, ask before writing.

## Required Reading

Read these files, relative to the active project root, before generating or revising an outline:

1. `config/project_config.md`
2. `01_draft/README.md`
3. `01_draft/data_inventory.md`
4. `02_reference/style_notes.md`
5. `02_reference/reference_index.md`
6. Relevant drafts, notes, tables, datasets, figures, target-journal files, and `02_reference/writing_samples`

In Chinese mode, use the equivalent configured paths such as `配置/项目配置.md`, `01_草稿/数据清单.md`, `02_参考/风格说明.md`, `02_参考/参考索引.md`, and `02_参考/写作样本`.

Do not overwrite original files in `01_draft` or `02_reference`.

## Workflow

1. Extract constraints: working title, article type, target journal, language, research object, core question, study scope, available evidence, missing information, and forbidden assumptions.
2. Extract journal style: heading depth, abstract shape, reference style, table/figure expectations, declaration order, word limits, and whether headings should be numbered.
3. Build the central claim. State the paper's one-sentence thesis and the main argumentative turn that distinguishes it from a descriptive report.
4. Audit evidence at outline level. Separate user-provided materials, data/figures/tables, literature anchors, style-only references, and unsupported claims.
5. Derive literature-search constraints for major outlines, introductions, discussions, reviews, or full-paper preparation unless the user explicitly says not to search. Save a search frame when useful.
6. Create the section plan. Each section should have a function, central claim, evidence to use, likely citations, figure/table needs, and TODOs.
7. Create a figure/table plan if visual evidence or conceptual diagrams are central to the paper. Figures must serve the argument, not decorate it.
8. Mark unsupported or missing material with precise `TODO: [specific missing evidence or action]` notes.
9. Save the outline to `03_output/manuscript/paper_outline.md` unless the user specifies another path.

## Outline Shape

Use a structure like this, adapting it to the target journal:

```markdown
# Paper outline: <title>

Date: <date>
Active project: <path>
Target journal: <journal or TODO>
Article type: <type or TODO>

## Core thesis

<One-sentence thesis>

## Research questions

1. <question>

## Argument chain

<Step-by-step logic>

## Proposed manuscript structure

### <section title>

Function:
Central claim:
Evidence:
Literature needed:
Figure/table role:
TODO:

## Figure and table plan

| Item | Function | Source material | Form | Manuscript placement | Status |
| --- | --- | --- | --- | --- | --- |

## Literature search frame

Core concepts:
Date range:
Inclusion rules:
Exclusion rules:
Source priority:

## Evidence gaps and TODOs
```

## Evidence Rules

- Do not invent data, methods, results, citations, author details, journal requirements, ethics, funding, conflicts, or acknowledgements.
- Treat target-journal files and writing samples as style references unless the manuscript explicitly discusses their substantive claims.
- Do not cite style-only samples as scholarly evidence.
- Keep claims traceable to `01_draft`, `02_reference`, verified literature, generated analysis outputs, or explicit user instructions.
- Use cautious language when the outline is conceptual and evidence remains to be gathered.
- Do not treat unresolved examples, cases, financial claims, operational claims, or literature gaps as settled outline claims. Either remove them from the core argument or mark the exact missing source with `TODO: [specific missing evidence or action]`.

## Output Updates

When the outline materially affects later drafting, also create or update:

- `03_output/supplement/literature_search_frame.md`
- `03_output/supplement/claim_source_map.md`
- `03_output/revision/change_log.md`
- `logs/writing_log.md` for major writing decisions
