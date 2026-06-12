---
description: Route a PaperSmart manuscript workflow request to the right PaperSmart skill.
---

# /papersmart

Route the user's request to the smallest suitable PaperSmart skill.

## Preflight

1. Identify whether the user wants workspace setup, workspace update, a new project, outline, draft, revision, translation, figures, or submission.
2. Read `shared/memory/papersmart_profile.md` or `共享/记忆/papersmart_profile.md` when a workspace already exists.
3. If multiple projects exist and no active project is clear, ask before writing.

## Plan

Choose one route:

| Request | Use |
| --- | --- |
| First-time setup | `PaperSmart-init` |
| Update existing workspace after a PaperSmart release | `PaperSmart-update` |
| Create a new paper project | `PaperSmart-new-project` |
| Build the argument and structure | `PaperSmart-outline` |
| Draft or major rewrite | `PaperSmart-draft` |
| Focused local edits | `PaperSmart-revision` |
| Chinese academic translation | `PaperSmart-translation` |
| Figure planning or generation | `PaperSmart-figures` |
| Journal submission package | `PaperSmart-submission` |

## Commands

Do not perform all PaperSmart actions at once. Invoke the selected skill and follow its workflow.

## Verification

Confirm the selected skill, active project, language mode, and output path before making changes.

## Summary

Report which PaperSmart skill was used and what files were created or updated.

## Next Steps

Suggest the next PaperSmart command only when it follows directly from the current result.
