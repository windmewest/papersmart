---
name: papersmart-submission
description: Prepare PaperSmart journal submission packages from a completed manuscript, including title page, anonymized or main manuscript files, figure captions, tables, declarations, cover letter drafts, metadata templates, submission checklists, and package QA. Use when the user asks to prepare a submission, journal package, cover letter, title page, anonymized manuscript, declarations, figure files, or 03_output/submission outputs.
---

# PaperSmart-submission

## Overview

Package a finished PaperSmart manuscript for journal submission. This skill organizes and verifies submission materials; it does not invent missing author, ethics, funding, conflict, permission, or journal metadata.

## Required Reading

Read from the active project:

1. `config/project_config.md`
2. `02_reference/style_notes.md`
3. `02_reference/reference_index.md`
4. `02_reference/target_journal` files relevant to submission
5. `03_output/manuscript/paper.md`
6. `03_output/tables`
7. `03_output/figures`
8. `03_output/supplement/claim_source_map.md`, if present
9. `03_output/revision/change_log.md`

## Workflow

1. Identify the target journal and submission type.
2. Extract verified submission requirements: manuscript structure, anonymization, title page, abstract, keywords, declarations, references, figure formats, table placement, file naming, cover letter, permissions, and supplementary files.
3. Create a package folder under `03_output/submission/<journal_or_package_slug>/`.
4. Prepare only materials supported by the manuscript and verified project metadata.
5. Use `TODO:` for missing required metadata, including author details, corresponding author, ethics, funding, conflicts, acknowledgements, data availability, image permissions, or author contributions.
6. Separate blinded and non-blinded materials when the journal requires anonymous review.
7. Copy or export figure/table files into the package only when their source, captions, and permissions are known.
8. Create a submission checklist and package README.
9. Record the package in `03_output/revision/change_log.md`.

## Typical Outputs

Use stable names such as:

```text
03_output/submission/<package_slug>/
  README.md
  title_page.md
  manuscript_main.md
  manuscript_main_anonymized.md
  figure_captions.md
  tables_for_submission.md
  declarations.md
  cover_letter.md
  submission_checklist.md
  metadata_template.md
  figures/
  supplementary/
```

Generate `.docx`, `.pdf`, `.xlsx`, or other formatted files only when the user asks or the journal requires them. Use the Documents, Spreadsheets, or Presentations skills when those formats require rendering and verification.

## Anonymization Rules

When preparing blinded materials:

- Remove author names, affiliations, acknowledgements, funding identifiers, and self-identifying file metadata when required.
- Replace self-identifying statements with `TODO: restore after review` or neutral wording only when the journal allows it.
- Keep citations to the authors' prior work if removing them would distort the scholarly record, unless journal guidance says otherwise.
- Do not anonymize generated package files by deleting source project files.

## Cover Letter Rules

Draft a cover letter only from verified information:

- Manuscript title.
- Article type.
- Target journal.
- Concise contribution.
- Confirmation statements required by the journal.
- Suggested reviewers or exclusions only if the user provides them.

Use `TODO:` for missing editorial, author, reviewer, ethics, permission, or declaration information.

## Package QA

Before finishing, check:

- Required files exist in the package folder.
- Manuscript and title page are correctly separated when needed.
- Figure and table numbering match the manuscript.
- Captions are complete and match files.
- Declarations match project metadata and do not invent missing statements.
- References are cited in text and formatted according to verified journal style as far as possible.
- Remaining `TODO:` items are listed in `submission_checklist.md`.

## Final Report

Tell the user:

- Package path.
- Files created.
- Missing metadata or permissions.
- Any journal rules that still require human confirmation.
