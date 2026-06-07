#!/usr/bin/env python3
"""Safely update an existing PaperSmart workspace structure."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import textwrap
from pathlib import Path


PROFILE_NAME = "papersmart_profile.md"

PATHS = {
    "en": {
        "projects": "projects",
        "shared": "shared",
        "docs": "docs",
        "prompts": "prompts",
        "tools": "tools",
        "skills": "skills",
        "memory": "memory",
        "config": "config",
        "logs": "logs",
        "draft": "01_draft",
        "reference": "02_reference",
        "output": "03_output",
        "data": "data",
        "figures": "figures",
        "tables": "tables",
        "notes": "notes",
        "literature": "literature",
        "target_journal": "target_journal",
        "writing_samples": "writing_samples",
        "manuscript": "manuscript",
        "supplement": "supplement",
        "revision": "revision",
        "translation": "translation",
        "submission": "submission",
        "workspace_readme": "README.md",
        "project_readme": "README.md",
        "shared_readme": "README.md",
        "draft_readme": "README.md",
        "reference_readme": "README.md",
        "output_readme": "README.md",
        "project_config": "project_config.md",
        "data_inventory": "data_inventory.md",
        "style_notes": "style_notes.md",
        "reference_index": "reference_index.md",
        "change_log": "change_log.md",
        "local_revision_tasks": "local_revision_tasks.md",
        "writing_log": "writing_log.md",
        "decision_log": "decision_log.md",
        "update_report": "papersmart_update_report.md",
    },
    "zh": {
        "projects": "项目",
        "shared": "共享",
        "docs": "文档",
        "prompts": "提示",
        "tools": "工具",
        "skills": "技能",
        "memory": "记忆",
        "config": "配置",
        "logs": "日志",
        "draft": "01_草稿",
        "reference": "02_参考",
        "output": "03_输出",
        "data": "数据",
        "figures": "图像",
        "tables": "表格",
        "notes": "笔记",
        "literature": "文献",
        "target_journal": "目标期刊",
        "writing_samples": "写作样本",
        "manuscript": "正文",
        "supplement": "补充材料",
        "revision": "修订",
        "translation": "翻译",
        "submission": "投稿",
        "workspace_readme": "说明.md",
        "project_readme": "说明.md",
        "shared_readme": "说明.md",
        "draft_readme": "说明.md",
        "reference_readme": "说明.md",
        "output_readme": "说明.md",
        "project_config": "项目配置.md",
        "data_inventory": "数据清单.md",
        "style_notes": "风格说明.md",
        "reference_index": "参考索引.md",
        "change_log": "修改记录.md",
        "local_revision_tasks": "局部修改任务.md",
        "writing_log": "写作日志.md",
        "decision_log": "决策日志.md",
        "update_report": "papersmart_更新报告.md",
    },
}


def today() -> str:
    return dt.date.today().isoformat()


class Recorder:
    def __init__(self, dry_run: bool) -> None:
        self.dry_run = dry_run
        self.dirs: list[str] = []
        self.files: list[str] = []
        self.skipped: list[str] = []
        self.notes: list[str] = []

    def rel(self, root: Path, path: Path) -> str:
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            return path.as_posix()

    def mkdir(self, root: Path, path: Path) -> None:
        label = self.rel(root, path)
        if path.exists():
            return
        self.dirs.append(label)
        if not self.dry_run:
            path.mkdir(parents=True, exist_ok=True)

    def write_missing(self, root: Path, path: Path, content: str) -> None:
        label = self.rel(root, path)
        if path.exists():
            self.skipped.append(f"preserved existing file: {label}")
            return
        self.files.append(label)
        if not self.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def profile_path(root: Path, p: dict[str, str]) -> Path:
    return root / p["shared"] / p["memory"] / PROFILE_NAME


def detect_language(root: Path, requested: str) -> str:
    if requested in {"en", "zh"}:
        return requested
    for language, p in PATHS.items():
        profile = profile_path(root, p)
        if profile.exists():
            text = profile.read_text(encoding="utf-8", errors="ignore")
            if "language: `zh`" in text:
                return "zh"
            if "language: `en`" in text:
                return "en"
    en_present = (root / PATHS["en"]["projects"]).exists() or (root / PATHS["en"]["shared"]).exists()
    zh_present = (root / PATHS["zh"]["projects"]).exists() or (root / PATHS["zh"]["shared"]).exists()
    if en_present and zh_present:
        raise SystemExit("Ambiguous workspace language. Pass --language en or --language zh.")
    if zh_present:
        return "zh"
    return "en"


def find_active_project(root: Path, language: str) -> str:
    p = PATHS[language]
    profile = profile_path(root, p)
    if profile.exists():
        text = profile.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"active_project:\s*`([^`]+)`", text)
        if match:
            return match.group(1)

    old_memory = root / "shared" / "memory" / "workspace_structure.md"
    if old_memory.exists():
        text = old_memory.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"(projects/[A-Za-z0-9_/-]+)", text)
        if match and language == "en":
            return match.group(1)

    projects_dir = root / p["projects"]
    if projects_dir.exists():
        projects = sorted(child.name for child in projects_dir.iterdir() if child.is_dir())
        if len(projects) == 1:
            return f"{p['projects']}/{projects[0]}"
    return "TODO:"


def profile_content(language: str, active_project: str) -> str:
    p = PATHS[language]
    lines = [
        "# PaperSmart profile" if language == "en" else "# PaperSmart 配置",
        "",
        f"- language: `{language}`",
        f"- output_language: `{'English' if language == 'en' else '中文'}`",
        f"- active_project: `{active_project}`",
        "",
        "## Path map" if language == "en" else "## 路径映射",
        "",
    ]
    for key in [
        "projects",
        "shared",
        "config",
        "logs",
        "draft",
        "reference",
        "writing_samples",
        "output",
        "manuscript",
        "revision",
        "translation",
        "submission",
    ]:
        lines.append(f"- {key}: `{p[key]}`")
    return "\n".join(lines)


def workspace_templates(language: str) -> dict[str, str]:
    p = PATHS[language]
    if language == "zh":
        return {
            p["workspace_readme"]: """
            # PaperSmart

            PaperSmart 工作区用于管理科研论文项目。每篇论文放在 `项目/` 下的独立文件夹中。
            跨项目复用的文档、提示、工具、技能和记忆放在 `共享/`。
            """,
            f"{p['projects']}/{p['project_readme']}": """
            # 项目

            每个文件夹对应一篇论文或一个研究项目。不要把单篇论文材料放入 `共享/`。
            """,
            f"{p['shared']}/{p['shared_readme']}": """
            # 共享

            这里只放跨项目复用资源。项目专用草稿、数据、输出、修订和投稿文件应留在项目目录内。
            """,
        }
    return {
        p["workspace_readme"]: """
        # PaperSmart

        PaperSmart is a workspace for scientific manuscript projects. Put each paper or research
        project in its own folder under `projects/`. Put reusable documentation, prompts, tools,
        skills, and memory under `shared/`.
        """,
        f"{p['projects']}/{p['project_readme']}": """
        # Projects

        Each folder here is one manuscript or research project. Do not put single-paper materials
        in `shared/`.
        """,
        f"{p['shared']}/{p['shared_readme']}": """
        # Shared

        Use this folder for reusable PaperSmart resources only. Keep project-specific drafts,
        data, outputs, revisions, and submission files inside the relevant project folder.
        """,
    }


def project_templates(language: str, title: str) -> dict[str, str]:
    p = PATHS[language]
    if language == "zh":
        return {
            p["project_readme"]: f"""
            # {title}

            原始材料放入 `{p['draft']}`，期刊格式、文献和写作样本放入 `{p['reference']}`，
            生成稿件和投稿材料写入 `{p['output']}`。
            """,
            f"{p['config']}/{p['project_config']}": f"""
            # 项目配置

            更新日期：{today()}

            - 工作题目：{title}
            - 文章类型：TODO:
            - 目标期刊：TODO:
            - 写作语言：TODO:
            - 作者和单位：TODO:
            - 研究目标：TODO:
            - 研究问题或假设：TODO:
            - 方法摘要：TODO:
            - 主要数据来源：TODO:
            - 已知主要结果：TODO:
            - 伦理声明：TODO:
            - 基金：TODO:
            - 利益冲突：TODO:
            - 致谢：TODO:
            - 缺失信息：TODO:
            """,
            f"{p['draft']}/{p['draft_readme']}": "# 草稿与原始材料\n\n这里存放原始笔记、草稿、数据、表格、图像和作者指示。",
            f"{p['draft']}/{p['data_inventory']}": """
            # 数据清单

            | 文件或文件夹 | 类型 | 字段或内容 | 单位 | 分组 | 缺失值 | 已知问题 | 预期用途 |
            | --- | --- | --- | --- | --- | --- | --- | --- |
            | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: |
            """,
            f"{p['reference']}/{p['reference_readme']}": "# 参考材料\n\n这里存放期刊指南、模板、写作样本、文献 PDF、引用文件和风格说明。",
            f"{p['reference']}/{p['style_notes']}": """
            # 风格说明

            - 目标期刊结构：TODO:
            - 标题层级：TODO:
            - 摘要长度和结构：TODO:
            - 引用格式：TODO:
            - 参考文献格式：TODO:
            - 图表题注格式：TODO:
            - 字数限制：TODO:
            - 仅作风格参考的材料：TODO:
            """,
            f"{p['reference']}/{p['reference_index']}": """
            # 参考索引

            | 文件或来源 | 类型 | 用途 | 是否进入参考文献 | 备注 |
            | --- | --- | --- | --- | --- |
            | TODO: | TODO: | TODO: | TODO: | TODO: |
            """,
            f"{p['output']}/{p['output_readme']}": "# 输出\n\n生成的正文、表格、图像、补充材料、修订记录、翻译稿和投稿包放在这里。",
            f"{p['output']}/{p['revision']}/{p['change_log']}": """
            # 修改记录

            | 日期 | 修改 | 影响文件 | 备注 |
            | --- | --- | --- | --- |
            | TODO: | TODO: | TODO: | TODO: |
            """,
            f"{p['output']}/{p['revision']}/{p['local_revision_tasks']}": "# 局部修改任务\n\n正文生成后，将局部修改要求写在这里。",
            f"{p['logs']}/{p['writing_log']}": "# 写作日志\n\n| 日期 | 动作 | 备注 |\n| --- | --- | --- |\n| TODO: | TODO: | TODO: |",
            f"{p['logs']}/{p['decision_log']}": "# 决策日志\n\n| 日期 | 决策 | 理由 | 证据 |\n| --- | --- | --- | --- |\n| TODO: | TODO: | TODO: | TODO: |",
        }
    return {
        p["project_readme"]: f"""
        # {title}

        Use `{p['draft']}` for original materials, `{p['reference']}` for journal files,
        literature, and writing samples, and `{p['output']}` for generated manuscript products.
        """,
        f"{p['config']}/{p['project_config']}": f"""
        # Project config

        Last updated: {today()}

        - Working title: {title}
        - Article type: TODO:
        - Target journal: TODO:
        - Writing language: TODO:
        - Authors and affiliations: TODO:
        - Research objective: TODO:
        - Research questions or hypotheses: TODO:
        - Methods summary: TODO:
        - Main data sources: TODO:
        - Main results known so far: TODO:
        - Ethics statement: TODO:
        - Funding: TODO:
        - Conflicts of interest: TODO:
        - Acknowledgements: TODO:
        - Missing information: TODO:
        """,
        f"{p['draft']}/{p['draft_readme']}": "# Draft source materials\n\nStore original notes, drafts, data, tables, figures, images, and author instructions here.",
        f"{p['draft']}/{p['data_inventory']}": """
        # Data inventory

        | File or folder | Type | Fields or contents | Units | Groups | Missing values | Known issues | Expected use |
        | --- | --- | --- | --- | --- | --- | --- | --- |
        | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: |
        """,
        f"{p['reference']}/{p['reference_readme']}": "# Reference materials\n\nStore journal guidelines, templates, writing samples, literature PDFs, citation files, and style notes here.",
        f"{p['reference']}/{p['style_notes']}": """
        # Style notes

        - Target journal structure: TODO:
        - Heading style: TODO:
        - Abstract length and structure: TODO:
        - Citation style: TODO:
        - Reference style: TODO:
        - Table and figure caption style: TODO:
        - Word limit: TODO:
        - Style-only reference materials: TODO:
        """,
        f"{p['reference']}/{p['reference_index']}": """
        # Reference index

        | File or source | Type | Use | Cite in manuscript? | Notes |
        | --- | --- | --- | --- | --- |
        | TODO: | TODO: | TODO: | TODO: | TODO: |
        """,
        f"{p['output']}/{p['output_readme']}": "# Output\n\nGenerated manuscripts, tables, figures, supplements, revisions, translations, and submission packages belong here.",
        f"{p['output']}/{p['revision']}/{p['change_log']}": """
        # Change log

        | Date | Change | Files affected | Notes |
        | --- | --- | --- | --- |
        | TODO: | TODO: | TODO: | TODO: |
        """,
        f"{p['output']}/{p['revision']}/{p['local_revision_tasks']}": "# Local revision tasks\n\nAdd requested local edits here after a manuscript exists.",
        f"{p['logs']}/{p['writing_log']}": "# Writing log\n\n| Date | Action | Notes |\n| --- | --- | --- |\n| TODO: | TODO: | TODO: |",
        f"{p['logs']}/{p['decision_log']}": "# Decision log\n\n| Date | Decision | Rationale | Evidence |\n| --- | --- | --- | --- |\n| TODO: | TODO: | TODO: | TODO: |",
    }


def project_title(project: Path, fallback: str) -> str:
    for config in [project / "config" / "project_config.md", project / "配置" / "项目配置.md"]:
        if config.exists():
            text = config.read_text(encoding="utf-8", errors="ignore")
            for pattern in [r"Working title:\s*(.+)", r"工作题目：\s*(.+)"]:
                match = re.search(pattern, text)
                if match and match.group(1).strip() and "TODO" not in match.group(1):
                    return match.group(1).strip()
    return fallback


def update_workspace(root: Path, language: str, recorder: Recorder) -> Path:
    p = PATHS[language]

    for relative in [
        p["projects"],
        f"{p['shared']}/{p['docs']}",
        f"{p['shared']}/{p['prompts']}",
        f"{p['shared']}/{p['tools']}",
        f"{p['shared']}/{p['skills']}",
        f"{p['shared']}/{p['memory']}",
    ]:
        recorder.mkdir(root, root / relative)

    active_project = find_active_project(root, language)
    for relative, content in workspace_templates(language).items():
        recorder.write_missing(root, root / relative, content)
    recorder.write_missing(root, profile_path(root, p), profile_content(language, active_project))

    old_memory = root / "shared" / "memory" / "workspace_structure.md"
    if old_memory.exists() and language == "en":
        recorder.notes.append("preserved old memory file: shared/memory/workspace_structure.md")

    projects_dir = root / p["projects"]
    if not projects_dir.exists() and recorder.dry_run:
        return root / p["shared"] / p["memory"] / p["update_report"]
    if projects_dir.exists():
        for project in sorted(child for child in projects_dir.iterdir() if child.is_dir()):
            update_project(root, project, language, recorder)

    report_path = root / p["shared"] / p["memory"] / p["update_report"]
    write_report(root, report_path, language, recorder)
    return report_path


def update_project(root: Path, project: Path, language: str, recorder: Recorder) -> None:
    p = PATHS[language]
    for relative in [
        p["config"],
        p["logs"],
        f"{p['draft']}/{p['data']}",
        f"{p['draft']}/{p['figures']}",
        f"{p['draft']}/{p['tables']}",
        f"{p['draft']}/{p['notes']}",
        f"{p['reference']}/{p['literature']}",
        f"{p['reference']}/{p['target_journal']}",
        f"{p['reference']}/{p['writing_samples']}",
        f"{p['output']}/{p['manuscript']}",
        f"{p['output']}/{p['tables']}",
        f"{p['output']}/{p['figures']}",
        f"{p['output']}/{p['supplement']}",
        f"{p['output']}/{p['revision']}",
        f"{p['output']}/{p['translation']}",
        f"{p['output']}/{p['submission']}",
    ]:
        recorder.mkdir(root, project / relative)

    title = project_title(project, project.name)
    for relative, content in project_templates(language, title).items():
        recorder.write_missing(root, project / relative, content)


def write_report(root: Path, report_path: Path, language: str, recorder: Recorder) -> None:
    heading = "# PaperSmart update report" if language == "en" else "# PaperSmart 更新报告"
    lines = [
        heading,
        "",
        f"- date: `{today()}`",
        f"- language: `{language}`",
        f"- dry_run: `{recorder.dry_run}`",
        f"- folders_created: `{len(recorder.dirs)}`",
        f"- files_created: `{len(recorder.files)}`",
        f"- preserved_or_skipped: `{len(recorder.skipped)}`",
        "",
        "## Created folders",
        "",
        *(f"- `{item}`" for item in recorder.dirs),
        "",
        "## Created files",
        "",
        *(f"- `{item}`" for item in recorder.files),
        "",
        "## Preserved existing files",
        "",
        *(f"- {item}" for item in recorder.skipped),
        "",
        "## Notes",
        "",
        *(f"- {item}" for item in recorder.notes),
    ]
    if not recorder.dry_run:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safely update a PaperSmart workspace.")
    parser.add_argument("--workspace", default=".", help="PaperSmart workspace root.")
    parser.add_argument("--language", choices=["auto", "en", "zh"], default="auto", help="Workspace language. Default: auto.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created without writing changes.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.workspace).resolve()
    if not root.exists():
        raise SystemExit(f"Workspace does not exist: {root}")

    language = detect_language(root, args.language)
    recorder = Recorder(dry_run=args.dry_run)
    report_path = update_workspace(root, language, recorder)

    print(f"PaperSmart workspace: {root}")
    print(f"Language mode: {language}")
    print(f"Dry run: {args.dry_run}")
    print(f"Folders to create/created: {len(recorder.dirs)}")
    print(f"Files to create/created: {len(recorder.files)}")
    print(f"Existing files preserved: {len(recorder.skipped)}")
    print(f"Update report: {report_path}")
    if args.dry_run:
        print("No files were written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
