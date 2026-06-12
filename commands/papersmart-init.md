---
description: Initialize a PaperSmart workspace in English or Chinese.
---

# /papersmart-init

Use the `PaperSmart-init` skill.

## Preflight

1. Ask which workspace language to use. Default to English.
2. Confirm the workspace root.
3. Ask whether to install companion skills only if the user requested installation.

## Plan

Create the PaperSmart workspace roots, language profile, optional first project, and starter templates.

## Commands

Follow `PaperSmart-init`. Use `papersmart-init/scripts/init_papersmart.py` when file-system setup is needed.

## Verification

Confirm the profile file, project/shared roots, and generated template paths.

## Summary

Report the language mode, workspace path, and next command for new paper projects.

## Next Steps

Use `/papersmart-new-project` for future paper projects instead of rerunning full initialization.
