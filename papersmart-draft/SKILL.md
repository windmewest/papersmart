---
name: papersmart-draft
description: Generate or substantially revise full PaperSmart manuscripts from active project materials, including literature evidence, data analysis plans, visualization plans, claim-source mapping, tables, figures, manuscript text, references, and quality checks. Use when the user asks to draft a full paper, write a manuscript, produce Results/Discussion from data, rebuild a major section, integrate literature into a manuscript, or create a journal-ready PaperSmart draft.
---

# PaperSmart-draft

## Overview

Draft a complete, traceable, journal-aware manuscript from PaperSmart materials. The draft must be evidence-driven: read sources first, plan analysis and visualization before Results, then write.

## Critical Rule: Artifact Type Guard

Before creating or updating any output, classify the requested artifact:

- `manuscript`: formal article text only. Output to `03_output/manuscript/paper.md` or a user-specified manuscript path.
- `review_report`: reviewer-style assessment, pre-submission review, audit findings, reviewer comments, or accept/reject advice. Output to `03_output/revision/*`.
- `revision_advice`: modification advice, local revision tasks, improvement checklist, response strategy, or author action plan. Output to `03_output/revision/*`.
- `supplement_plan`: method operation steps, GIS workflow, data plan, analysis plan, visualization plan, evidence matrix, or claim-source map. Output to `03_output/supplement/*`.
- `translation`: translated manuscript or translation notes. Output to `03_output/translation/*`.

`03_output/manuscript/paper.md` is manuscript-only. Do not write audit opinions, review reports, reviewer comments, modification advice, method-operation plans, checklists, or implementation instructions into `paper.md`, even if the user has provided them as detailed prose.

Requests containing phrases such as `review`, `audit`, `reviewer report`, `review comments`, `revision advice`, `modification advice`, `method improvement`, `operations plan`, `审核`, `审稿`, `评审`, `修改意见`, `修改建议`, `改进建议`, `操作步骤`, or `方法改进步骤` are advice/review tasks by default. For these tasks, create a Markdown file under `03_output/revision` or `03_output/supplement`; do not create or overwrite `paper.md` unless the user explicitly says to implement the advice into the manuscript.

Review/advice output language should follow the manuscript's primary language unless the user specifies otherwise.

## Critical Rule: Keep Conversation Out Of The Manuscript

The manuscript is a scholarly artifact, not a record of the chat. Never place user comments, assistant plans, screenshot provenance, task instructions, or conversational replies into `03_output/manuscript/paper.md`.

Forbidden manuscript language includes:

- Direct references to the user: `the user said`, `the user provided`, `according to the user's comment`, `用户说`, `用户提供`, `用户要求`, `根据用户意见`.
- Process narration: `here I will`, `I will adopt`, `we need to`, `as requested`, `这里我会`, `接下来我将`, `我采用...而不是...`.
- Screenshot/chat provenance: `the screenshot provided by the user`, `from the chat`, `用户提供的截图`, `对话中提到`.
- Assistant self-reference: `I`, `my draft`, `this response`, `I chose this wording`, unless the target manuscript section itself requires first-person authorial language and the journal permits it.

Handle these inputs outside the manuscript:

| Input type | Use it for | Where to record it |
| --- | --- | --- |
| User comment or preference | Editorial guidance, style choice, revision priority | `03_output/revision/change_log.md` or `logs/decision_log.md` |
| Chat instruction | Task scope and constraints | Working notes or logs, not manuscript prose |
| Screenshot/file provenance | Evidence location or source tracking | Figure/table source note, data inventory, or TODO |
| Missing author confirmation | A precise placeholder | `TODO:` in the relevant output or supplement |
| Writing plan | Drafting workflow | `03_output/supplement/*_plan.md` or logs |

If a user comment contains a scientific claim, extract only the claim and verify it against `01_draft`, `02_reference`, data outputs, or literature before it can enter manuscript prose.

## Critical Rule: Evidence TODO Placeholders

Evidence that is not closed must stay visibly unresolved. Use this exact placeholder pattern:

```text
TODO: [specific missing evidence or action]
```

Apply this rule to missing citations, unverified case facts, incomplete financial or operational evidence, unresolved author confirmations, missing data, and uncertain journal requirements.

Do not convert evidence gaps into manuscript commentary. In `paper.md`, avoid statements such as "this evidence can be completed later", "this does not affect publishability", "the cautious treatment is better", or "the claim is temporarily not treated as settled". Put decision rationale in `03_output/revision`, `03_output/supplement`, `logs/writing_log.md`, or `logs/decision_log.md`.

Unsupported examples and unresolved cases must not be written as settled findings. Either remove them from the core argument or keep a precise `TODO: [specific missing evidence or action]` at the point where the claim would need support.

## AI Assistance And Evidence Labels

Use inline labels only as editing instructions, not as final manuscript prose:

- `AIGEN`: regenerate the marked span from context as substantive manuscript prose. Use it when the marked content needs a new argument sentence, transition, synthesis, or paragraph-level repair.
- `AIPO`: polish the marked span while preserving meaning. Use it for clarity, academic restraint, terminology consistency, flow, and local style repair.
- `AIREF`: verify the marked claim, find suitable scholarly or authoritative evidence, add citation markers, and narrow the claim when evidence requires it.

For inline markers such as `*content*AIGEN`, `*content*AIPO`, or `*content*AIREF`, replace the full marked pattern with clean prose before final delivery unless the user explicitly asks for a marked review copy. These markers never replace citations, evidence checks, or TODO placeholders. If evidence is missing, leave `TODO: [specific missing evidence or action]`.

If a journal, institution, or publisher requires AI disclosure, convert the workflow labels into a formal AI assistance statement in the manuscript declarations or cover materials; do not leave workflow labels scattered through the article body.

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

Read in this order before generating or revising a full manuscript:

1. `config/project_config.md`
2. `01_draft/README.md`
3. `01_draft/data_inventory.md`
4. `02_reference/style_notes.md`
5. `02_reference/reference_index.md`
6. Specific drafts, outlines, notes, data files, tables, figures, images, target-journal materials, writing samples, citation files, and reference PDFs needed for the task

In Chinese mode, use the equivalent configured paths such as `配置/项目配置.md`, `01_草稿/数据清单.md`, `02_参考/风格说明.md`, `02_参考/参考索引.md`, and `02_参考/写作样本`.

For local revisions after a full manuscript already exists, prefer `PaperSmart-revision`. Use this skill only when the requested change is a major rewrite, a new Results/Discussion pass, or a full draft-level revision.

## Full Draft Workflow

1. Classify the artifact type first. Continue this workflow only for a manuscript or major manuscript rewrite. Route review reports, revision advice, method-operation steps, and checklists to `03_output/revision` or `03_output/supplement`.
2. Define the task boundary: full manuscript, major section rewrite, Results/Discussion generation, literature integration, or journal adaptation.
3. Extract project constraints: title, article type, target journal, language, authors, research questions, methods, data sources, declarations, and missing information.
4. Classify all available input as evidence, context, writing sample, user instruction, user comment, review/advice artifact, or missing-information prompt. Only evidence and verified literature can directly support manuscript claims.
5. Extract journal style from `02_reference/target_journal` when available. Respect heading style, abstract length, figure/table captions, citation style, reference style, and declaration order.
6. Build a one-sentence manuscript argument: `In [system/problem], this study shows [advance] using [approach], supported by [evidence], with [boundary].`
7. Map the full paper before drafting: field-scale need, unresolved bottleneck, proposed move, decisive evidence, implication, and boundary.
8. Perform a structured literature search for full manuscript generation, major revisions, introductions, discussions, and literature reviews unless the user explicitly says not to. Derive constraints first: research goal, core concepts, definitions, methods needing support, disciplinary scope, date range, inclusion/exclusion rules, and source priorities.
9. Save 8-12 key literature conclusions to `03_output/supplement/literature_evidence_matrix.md`. Each conclusion must include evidence strength, high-quality citations, manuscript placement, and caveats.
10. Audit all available datasets, scoring files, tables, images, statistical outputs, and generated figures before writing Results.
11. Save `03_output/supplement/data_analysis_plan.md`. State which data are used, which are excluded, what each analysis tests or illustrates, derived quantities to compute, and how each analysis supports the manuscript argument.
12. Save `03_output/supplement/visualization_plan.md` when data or diagrams are useful. Choose figures because they clarify interpretation, not because files happen to exist.
13. Generate or update tables in `03_output/tables` and figures in `03_output/figures`. Every table and figure needs a stable file name, concise title, complete caption, data source, and in-text citation.
14. Create or update `03_output/supplement/claim_source_map.md`, mapping major claims to user materials, data, figures/tables, literature, or `TODO: [specific missing evidence or action]`.
15. Draft `03_output/manuscript/paper.md`, following target journal structure when known. Use manuscript voice only. Do not include meta-comments about the user, the assistant, the chat, screenshots, review comments, revision advice, method-operation steps, drafting choices, or explanations that evidence gaps can be filled later.
16. Update `03_output/revision/change_log.md`; update `logs/writing_log.md` and `logs/decision_log.md` for major writing or evidence decisions.
17. Run a quality pass and contamination audit before delivery.

## Nature-Style Drafting Pattern

Use these nature-writing principles for every major section, especially when the target journal is Nature-family or high-impact interdisciplinary:

- Author evidence comes first. Do not write around missing evidence.
- Write the argument before writing sentences.
- Use ambitious but bounded claims. Prefer `show`, `demonstrate`, `suggest`, `indicate`, `enable`, `may`, and `could` according to evidence strength.
- Each paragraph has one job: context, gap, approach, result, comparison, mechanism, implication, or limitation.
- Each paragraph should have one message, a clear opening sentence, and explicit sentence-to-sentence relations.
- Results should follow an evidence ladder: system/workflow, validation, main result, baseline comparison, diagnostic analysis, and application or generalization when supported.
- Discussion should widen from finding to meaning: central advance, evidence meaning, relation to prior work, constraints, and future use.
- Conclusions introduce no new data, citations, mechanisms, or promises.

For Chinese or mixed Chinese-English author notes, translate intent rather than syntax. Split notes into claim, evidence, condition, comparison, implication, and limitation before drafting English.

## Writing Standards

- Do not invent data, results, statistics, citations, author details, journal requirements, ethics, funding, conflicts, or acknowledgements.
- Use precise `TODO: [specific missing evidence or action]` markers for missing required information.
- Do not write unsupported examples, unresolved cases, or uncertain financial or operational claims as settled findings.
- Do not use manuscript prose to justify why an evidence gap remains open. Record that reasoning in revision notes, supplement files, or logs.
- Keep comments, author instructions, chat context, screenshots, and writing plans out of the manuscript body unless they are transformed into verified scientific content.
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

## Manuscript Contamination Audit

Before handoff, scan `03_output/manuscript/paper.md` for conversation leakage. Use the bundled script when a local manuscript file exists:

```bash
python shared/skills/papersmart-draft/scripts/audit_manuscript_contamination.py --file <active_project>/03_output/manuscript/paper.md
```

In Chinese mode, use the configured manuscript path. If the script reports high-risk matches, remove them from the manuscript and move any useful decision rationale, review comments, modification advice, or method-operation steps to logs, `03_output/revision`, or `03_output/supplement`.

## Quality Pass

Before considering the manuscript ready for human review, check:

- Source integrity and `TODO:` precision.
- No open evidence gap has been turned into explanatory manuscript commentary.
- No `AIGEN`, `AIPO`, or `AIREF` labels remain in the final manuscript unless the user explicitly requested a marked review copy or a formal AI disclosure section.
- No conversation leakage: no `用户说`, `用户提供`, `the user`, `screenshot provided`, `here I will`, `as requested`, assistant self-reference, or drafting-plan language in manuscript prose.
- Literature evidence quality and citation consistency.
- Structure against the target journal.
- Data analysis plan and visualization plan completeness.
- Table and figure numbering by first citation order.
- Claim support for background, methods, results, and discussion claims.
- Paragraph flow: one paragraph, one message, clear topic sentence, evidence linked to the section thesis.
- Reviewer-style risk check: unsupported claims, vague contribution, missing method detail, weak comparison, incomplete evaluation, and overbroad conclusion.
- Reference list consistency.
- Logs and change records.

Report any unverified citation details, missing materials, or remaining author confirmations clearly.
