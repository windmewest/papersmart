#!/usr/bin/env python3
"""Scan a manuscript for chat/commentary leakage."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PATTERNS = [
    ("user_reference_en", re.compile(r"\b(the user|user-provided|provided by the user|user said|user asked|user requested|according to the user)\b", re.I)),
    ("chat_reference_en", re.compile(r"\b(in the chat|this conversation|as requested|as discussed above|in this response)\b", re.I)),
    ("screenshot_provenance_en", re.compile(r"\b(screenshot provided by|user'?s screenshot|provided screenshot|attached screenshot)\b", re.I)),
    ("assistant_plan_en", re.compile(r"\b(here I will|I will adopt|I chose|I have chosen|we need to|this draft will|my draft)\b", re.I)),
    ("review_artifact_en", re.compile(r"\b(reviewer report|review comments|review opinion|revision advice|modification advice|audit opinion|pre-?submission review|major revision request|minor revision request|method improvement operations plan|operations plan|action plan for revision)\b", re.I)),
    ("evidence_gap_commentary_en", re.compile(r"\b(evidence can be completed later|does not affect publishability|does not weaken the paper|this treatment is more publishable|can be supplemented later|temporarily not treated as settled)\b", re.I)),
    ("inline_ai_marker", re.compile(r"\bAIGEN\b|\bAIPO\b|\bAIREF\b")),
    ("todo_without_brackets", re.compile(r"\bTODO:(?!\s*\[)")),
    ("user_reference_zh", re.compile(r"(用户|作者)(提供|指出|表示|说|认为|要求|希望|建议|强调)")),
    ("chat_reference_zh", re.compile(r"(根据用户|按照用户|回应用户|对话中|聊天中|如上所述|这里我会|接下来我将|我会采用|我将采用)")),
    ("screenshot_provenance_zh", re.compile(r"(用户提供的截图|用户截图|截图中可以看到|截图显示)")),
    ("assistant_plan_zh", re.compile(r"(这里采用|本文这里会|我在这里|我选择|我会|我将)")),
    ("review_artifact_zh", re.compile(r"(审核意见|审稿意见|评审意见|评阅意见|审稿报告|预审意见|修改意见|修改建议|改进建议|建议作者|作者应|方法改进步骤|操作步骤|审核结论|审稿人意见|正式稿中建议|需要在改进过程中)")),
    ("evidence_gap_commentary_zh", re.compile(r"(证据不足后期可以补全|不影响论文发表|不影响发表|不削弱问题意识|更可发表|暂不把|暂时不把|后续可以补全|这种处理并不削弱)")),
]


def iter_targets(paths: list[Path]) -> list[Path]:
    targets: list[Path] = []
    for path in paths:
        if path.is_dir():
            targets.extend(sorted(path.rglob("*.md")))
        else:
            targets.append(path)
    return targets


def scan(path: Path) -> list[tuple[str, int, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    findings: list[tuple[str, int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for label, pattern in PATTERNS:
            if pattern.search(line):
                findings.append((label, line_no, line.strip()))
    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit manuscript files for conversation or comment leakage.")
    parser.add_argument("--file", action="append", dest="files", required=True, help="Markdown file or directory to scan. Repeat for multiple targets.")
    parser.add_argument("--warn-only", action="store_true", help="Always exit 0 even when findings are present.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = [Path(item).resolve() for item in args.files]
    missing = [path for path in paths if not path.exists()]
    if missing:
        for path in missing:
            print(f"missing: {path}")
        return 2

    total = 0
    for path in iter_targets(paths):
        findings = scan(path)
        if not findings:
            continue
        total += len(findings)
        print(f"\n{path}")
        for label, line_no, line in findings:
            print(f"  {line_no}: [{label}] {line}")

    if total == 0:
        print("No manuscript contamination patterns found.")
        return 0

    print(f"\nFound {total} possible contamination pattern(s).")
    return 0 if args.warn_only else 1


if __name__ == "__main__":
    raise SystemExit(main())
