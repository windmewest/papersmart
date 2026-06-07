---
name: papersmart-translation
description: Translate or localize an existing PaperSmart manuscript into polished Chinese academic prose while preserving scientific meaning, evidence boundaries, citations, figure/table numbering, TODO markers, and declarations. Use when the user asks for a Chinese academic translation, Chinese journal-style version, bilingual preparation, Chinese collaborator version, or 03_output/translation/paper_zh.md.
---

# PaperSmart-translation

## Overview

Create a Chinese academic version of an existing PaperSmart manuscript. This is a translation and localization workflow, not a new drafting workflow.

## Language And Path Mode

Before reading project files, read the PaperSmart profile:

- English mode: `shared/memory/papersmart_profile.md`
- Chinese mode: `共享/记忆/papersmart_profile.md`

Use the configured path map. This skill normally writes Chinese output even if the workspace is in English mode.

## Required Reading

Read from the active project:

1. `03_output/manuscript/paper.md`
2. `03_output/tables` when table titles, captions, or terminology must match
3. `03_output/figures` when figure titles, captions, or labels must match
4. `03_output/supplement/claim_source_map.md` when claims or terminology need traceability
5. `02_reference/style_notes.md` if the Chinese version must match a journal style

In Chinese workspace mode, use the equivalent configured paths.

Do not translate from obsolete drafts unless the user explicitly selects them.

## Workflow

1. Confirm the source manuscript path. Default: `03_output/manuscript/paper.md`.
2. Extract terminology choices from the manuscript, tables, figures, and claim-source map.
3. Translate into polished Chinese academic prose suitable for Chinese scholarly readers.
4. Preserve scientific meaning, cautious claim boundaries, numeric values, citations, table/figure numbering, declarations, and all `TODO:` markers.
5. Keep stable file names unchanged while translating table and figure titles/captions.
6. Keep original English technical terms in parentheses at first mention when useful.
7. Write the Chinese manuscript to `03_output/translation/paper_zh.md` unless the user specifies another path.
8. Write `03_output/translation/translation_notes.md`.
9. Record the translation pass in `03_output/revision/change_log.md`.

## Terminology Guidance

Prefer established Chinese academic terms for:

- generative AI
- latent diffusion model
- LoRA
- image aesthetic assessment
- computational aesthetics
- computational creativity
- diachronic trajectory
- static specimen
- expert blind review
- triangulated evaluation

When a term is ambiguous or field-specific, preserve the English term at first mention and list the choice in `translation_notes.md`.

## Boundaries

- Do not add new data, citations, claims, journal requirements, author information, ethics statements, funding, conflicts, or acknowledgements.
- Do not smooth away `TODO:` markers.
- Do not change citation numbering unless the source manuscript already has an error and the user asks for citation repair.
- Do not make the Chinese text more conclusive than the English source.

## Translation Notes

Create:

```markdown
# Translation notes

Date:
Source manuscript:

## Terminology choices

| English term | Chinese term | Note |
| --- | --- | --- |

## Preserved TODOs

## Passages requiring author confirmation

## Files generated
```

## Final Check

Before finishing, check that:

- `paper_zh.md` exists.
- `translation_notes.md` lists terminology and unresolved items.
- All citations, figure/table references, declarations, and TODOs remain aligned with the source.
- The change log records the translation.
