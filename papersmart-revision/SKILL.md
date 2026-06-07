---
name: papersmart-revision
description: Apply focused local revisions to an existing PaperSmart manuscript while preserving source integrity, evidence traceability, figure/table numbering, citations, and change logs. Use when the user asks for local edits, reviewer-style fixes, section polishing, targeted restructuring, citation cleanup, caption updates, or specific changes after 03_output/manuscript/paper.md already exists.
---

# PaperSmart-revision

## Overview

Handle local manuscript changes after a draft exists. Keep the change scoped to the user's request, and synchronize any affected tables, figures, captions, citations, references, and logs.

Use `PaperSmart-draft` instead when the user asks for a full manuscript, a major rewrite of the argument, or new Results based on unaudited data.

## Language And Path Mode

Before reading project files, read the PaperSmart profile:

- English mode: `shared/memory/papersmart_profile.md`
- Chinese mode: `共享/记忆/papersmart_profile.md`

Use the configured path map. If `language` is `zh`, use Chinese folder names and answer in Chinese. If no profile exists, assume English mode.

## Required Reading

Read from the active project:

1. `03_output/manuscript/paper.md`
2. `03_output/revision/local_revision_tasks.md`
3. `config/project_config.md`
4. `02_reference/style_notes.md`
5. Any affected table, figure, caption, data, literature, or reference file

In Chinese mode, use the equivalent configured paths.

If the task references reviewer comments or an editor decision letter, read those files before editing.

## Workflow

1. Identify the exact requested change and the affected manuscript sections.
2. Check whether the requested change requires evidence from `01_draft`, `02_reference`, `03_output/tables`, `03_output/figures`, or verified literature.
3. Apply only the requested local change. Do not opportunistically rewrite unrelated sections.
4. If the revision affects a table, figure, caption, in-text citation, reference entry, declaration, or numbering sequence, update the linked artifacts in the same pass.
5. Preserve all unsupported or missing information as precise `TODO:` markers.
6. Keep citation numbers continuous and ordered by first appearance when using a numbered style.
7. Update `03_output/revision/change_log.md`.
8. If the change is substantial, update `logs/writing_log.md` or `logs/decision_log.md`.

## Revision Types

Use these patterns:

- Text polish: improve clarity, academic restraint, tense, transitions, and terminology without adding new claims.
- Local restructure: reorganize only the requested section and preserve claim support.
- Citation repair: add, remove, or renumber citations only when sources are verified.
- Figure/table sync: revise captions, in-text citations, numbering, or references to generated files.
- Reviewer response preparation: preserve a trace from each reviewer request to the manuscript change and change log.
- Journal adaptation: adjust headings, abstract shape, captions, or declarations only according to verified journal guidance.

## Boundaries

- Do not invent data, results, citations, author details, ethics, funding, conflicts, acknowledgements, or journal requirements.
- Do not overwrite original files in `01_draft` or `02_reference`.
- Do not convert a local revision into a full rewrite unless the user asks.
- Do not cite style-only target-journal samples as scholarly evidence.
- Use `humanizer` only when the user asks to reduce AI-like prose; preserve scientific caution and citation precision.

## Change Log Entry

Append a concise entry like this:

```markdown
| YYYY-MM-DD | Local revision: <short label> | <files changed> | <evidence or TODO notes> |
```

## Final Check

Before finishing, report:

- Sections changed.
- Tables, figures, citations, or references updated.
- Any remaining `TODO:` or author-confirmation item.
- Whether the task stayed local or should trigger a broader `PaperSmart-draft` pass later.
