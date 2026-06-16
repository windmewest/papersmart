---
name: papersmart-airef
description: Resolve PaperSmart inline AIREF markers by finding suitable scholarly or authoritative evidence, adding citation markers, revising the marked claim when needed, and logging the citation decision. Use when a manuscript contains markers such as *content*AIREF or when the user asks to support marked claims with literature or evidence.
---

# PaperSmart-AIREF

Use this skill for inline evidence-support markers in PaperSmart manuscripts.

## Marker Meaning

`*content*AIREF` means: verify the marked claim, find appropriate support, add citation markers, and remove the marker. The marked content may be edited if the evidence supports a narrower or more precise claim.

## Workflow

1. Read the surrounding paragraph, section thesis, current references, figure/table captions, and existing claim-source map if available.
2. Decide whether current references already support the claim.
3. If current references are insufficient, search scholarly databases, reference indexes, publisher pages, institutional reports, or the web, prioritizing:
   - peer-reviewed reviews and systematic reviews;
   - seminal books or classic theory sources;
   - transparent empirical studies;
   - official institutional or professional reports for adoption/regulation/practice claims.
4. Do not add a source merely because it sounds related. The citation must support the marked claim's specific verb and scope.
5. If evidence supports only part of the claim, revise the claim to match the evidence.
6. In numbered-reference manuscripts, keep citation numbers continuous and ordered by first appearance.
7. Replace the entire marked pattern, including asterisks and `AIREF`, with clean manuscript prose and citation markers.
8. Update the reference list, figure/table source statements, and change logs when sources or figure claims change.

## Boundaries

- Do not invent citations, DOIs, URLs, page ranges, publication years, or source claims.
- Prefer existing verified references when they are adequate.
- New sources should be necessary, reliable, and proportionate to the manuscript length.
- Keep unsupported claims as `TODO: [specific missing evidence or action]` only when no adequate evidence can be found.
- Do not leave `AIREF` markers in the final manuscript unless explicitly requested.

## Logging

For each resolved marker, record:

- marked claim summary;
- evidence used or search result;
- manuscript change;
- whether the claim was narrowed;
- any rejected or unused evidence and reason.
