#!/usr/bin/env python3
"""Create a new PaperSmart project using the workspace language profile."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import textwrap
from pathlib import Path


PROJECT_RE = re.compile(r"^paper_(\d{2})_(.+)$")
PROFILE_NAME = "papersmart_profile.md"

PATHS = {
    "en": {
        "projects": "projects",
        "shared": "shared",
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
        "project_readme": "README.md",
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
    },
    "zh": {
        "projects": "项目",
        "shared": "共享",
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
        "project_readme": "说明.md",
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
    },
}


def today() -> str:
    return dt.date.today().isoformat()


def slugify(text: str) -> str:
    ascii_text = text.lower().encode("ascii", "ignore").decode("ascii")
    ascii_text = re.sub(r"[^a-z0-9]+", "_", ascii_text)
    ascii_text = re.sub(r"_+", "_", ascii_text).strip("_")
    return ascii_text[:48].strip("_") or "new_project"


def read_language(root: Path, requested: str) -> str:
    if requested in {"en", "zh"}:
        return requested
    for language, p in PATHS.items():
        profile = root / p["shared"] / p["memory"] / PROFILE_NAME
        if profile.exists():
            text = profile.read_text(encoding="utf-8", errors="ignore")
            if "language: `zh`" in text:
                return "zh"
            if "language: `en`" in text:
                return "en"
    if (root / "项目").exists() and (root / "共享").exists():
        return "zh"
    return "en"


def next_project_number(projects_dir: Path) -> int:
    numbers = []
    for child in projects_dir.iterdir():
        if not child.is_dir():
            continue
        match = PROJECT_RE.match(child.name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def infer_slug(projects_dir: Path, title: str) -> str:
    number = next_project_number(projects_dir)
    return f"paper_{number:02d}_{slugify(title)}"


def write_file(path: Path, content: str, overwrite: bool) -> bool:
    if path.exists() and not overwrite:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    return True


def create_dirs(project: Path, p: dict[str, str]) -> None:
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
        (project / relative).mkdir(parents=True, exist_ok=True)


def project_templates(
    project: Path,
    slug: str,
    title: str,
    target_journal: str,
    article_type: str,
    writing_language: str,
    objective: str,
    workspace_language: str,
    overwrite: bool,
) -> list[str]:
    p = PATHS[workspace_language]
    if workspace_language == "zh":
        files = {
            p["project_readme"]: f"""
            # {title}

            项目目录：`{slug}`

            原始材料放入 `{p['draft']}`，期刊格式、文献和写作样本放入
            `{p['reference']}`，生成稿件和投稿材料写入 `{p['output']}`。
            """,
            f"{p['config']}/{p['project_config']}": f"""
            # 项目配置

            更新日期：{today()}

            - 工作题目：{title}
            - 文章类型：{article_type}
            - 目标期刊：{target_journal}
            - 写作语言：{writing_language}
            - 作者和单位：TODO:
            - 研究目标：{objective}
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
            f"{p['draft']}/{p['draft_readme']}": """
            # 草稿与原始材料

            这里存放原始笔记、草稿、数据、表格、图像和作者指示。
            """,
            f"{p['draft']}/{p['data_inventory']}": """
            # 数据清单

            | 文件或文件夹 | 类型 | 字段或内容 | 单位 | 分组 | 缺失值 | 已知问题 | 预期用途 |
            | --- | --- | --- | --- | --- | --- | --- | --- |
            | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: |
            """,
            f"{p['reference']}/{p['reference_readme']}": """
            # 参考材料

            这里存放期刊指南、模板、写作样本、文献 PDF、引用文件和风格说明。
            写作样本只作风格参考时，不要自动写入参考文献。
            """,
            f"{p['reference']}/{p['style_notes']}": """
            # 风格说明

            - 目标期刊结构：TODO:
            - 标题层级：TODO:
            - 摘要长度和结构：TODO:
            - 引用格式：TODO:
            - 参考文献格式：TODO:
            - 图表题注格式：TODO:
            - 字数限制：TODO:
            - 声明顺序：TODO:
            - 仅作风格参考的材料：TODO:
            """,
            f"{p['reference']}/{p['reference_index']}": """
            # 参考索引

            | 文件或来源 | 类型 | 用途 | 是否进入参考文献 | 备注 |
            | --- | --- | --- | --- | --- |
            | TODO: | TODO: | TODO: | TODO: | TODO: |
            """,
            f"{p['output']}/{p['output_readme']}": """
            # 输出

            生成的正文、表格、图像、补充材料、修订记录、翻译稿和投稿包放在这里。
            """,
            f"{p['output']}/{p['revision']}/{p['change_log']}": f"""
            # 修改记录

            | 日期 | 修改 | 影响文件 | 备注 |
            | --- | --- | --- | --- |
            | {today()} | 创建项目模板 | 项目目录 | TODO: |
            """,
            f"{p['output']}/{p['revision']}/{p['local_revision_tasks']}": """
            # 局部修改任务

            正文生成后，将局部修改要求写在这里。
            """,
            f"{p['logs']}/{p['writing_log']}": f"""
            # 写作日志

            | 日期 | 动作 | 备注 |
            | --- | --- | --- |
            | {today()} | 初始化项目 | TODO: |
            """,
            f"{p['logs']}/{p['decision_log']}": """
            # 决策日志

            | 日期 | 决策 | 理由 | 证据 |
            | --- | --- | --- | --- |
            | TODO: | TODO: | TODO: | TODO: |
            """,
        }
    else:
        files = {
            p["project_readme"]: f"""
            # {title}

            Project slug: `{slug}`

            Use `{p['draft']}` for original materials, `{p['reference']}` for
            journal files, literature, and writing samples, and `{p['output']}`
            for generated manuscript products.
            """,
            f"{p['config']}/{p['project_config']}": f"""
            # Project config

            Last updated: {today()}

            - Working title: {title}
            - Article type: {article_type}
            - Target journal: {target_journal}
            - Writing language: {writing_language}
            - Authors and affiliations: TODO:
            - Research objective: {objective}
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
            f"{p['draft']}/{p['draft_readme']}": """
            # Draft source materials

            Store original notes, drafts, data, tables, figures, images, and
            author instructions here.
            """,
            f"{p['draft']}/{p['data_inventory']}": """
            # Data inventory

            | File or folder | Type | Fields or contents | Units | Groups | Missing values | Known issues | Expected use |
            | --- | --- | --- | --- | --- | --- | --- | --- |
            | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: |
            """,
            f"{p['reference']}/{p['reference_readme']}": """
            # Reference materials

            Store journal guidelines, templates, writing samples, literature
            PDFs, citation files, and style notes here. Mark style-only samples
            clearly.
            """,
            f"{p['reference']}/{p['style_notes']}": """
            # Style notes

            - Target journal structure: TODO:
            - Heading style: TODO:
            - Abstract length and structure: TODO:
            - Citation style: TODO:
            - Reference style: TODO:
            - Table and figure caption style: TODO:
            - Word limit: TODO:
            - Declaration order: TODO:
            - Style-only reference materials: TODO:
            """,
            f"{p['reference']}/{p['reference_index']}": """
            # Reference index

            | File or source | Type | Use | Cite in manuscript? | Notes |
            | --- | --- | --- | --- | --- |
            | TODO: | TODO: | TODO: | TODO: | TODO: |
            """,
            f"{p['output']}/{p['output_readme']}": """
            # Output

            Generated manuscripts, tables, figures, supplements, revisions,
            translations, and submission packages belong here.
            """,
            f"{p['output']}/{p['revision']}/{p['change_log']}": f"""
            # Change log

            | Date | Change | Files affected | Notes |
            | --- | --- | --- | --- |
            | {today()} | Project scaffold created | Project folders | TODO: |
            """,
            f"{p['output']}/{p['revision']}/{p['local_revision_tasks']}": """
            # Local revision tasks

            Add requested local edits here after a manuscript exists.
            """,
            f"{p['logs']}/{p['writing_log']}": f"""
            # Writing log

            | Date | Action | Notes |
            | --- | --- | --- |
            | {today()} | Project initialized | TODO: |
            """,
            f"{p['logs']}/{p['decision_log']}": """
            # Decision log

            | Date | Decision | Rationale | Evidence |
            | --- | --- | --- | --- |
            | TODO: | TODO: | TODO: | TODO: |
            """,
        }

    created = []
    for relative, content in files.items():
        if write_file(project / relative, content, overwrite):
            created.append(relative)
    return created


def update_active_project(root: Path, slug: str, language: str) -> None:
    p = PATHS[language]
    memory = root / p["shared"] / p["memory"] / PROFILE_NAME
    memory.parent.mkdir(parents=True, exist_ok=True)
    content = (
        "# PaperSmart profile\n\n"
        if language == "en"
        else "# PaperSmart 配置\n\n"
    )
    content += (
        f"- language: `{language}`\n"
        f"- output_language: `{'English' if language == 'en' else '中文'}`\n"
        f"- active_project: `{p['projects']}/{slug}`\n\n"
    )
    content += "## Path map\n\n" if language == "en" else "## 路径映射\n\n"
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
        content += f"- {key}: `{p[key]}`\n"
    memory.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new PaperSmart project.")
    parser.add_argument("--workspace", default=".", help="Existing PaperSmart workspace root.")
    parser.add_argument("--title", required=True, help="Working title or project topic.")
    parser.add_argument("--slug", help="Optional explicit project slug.")
    parser.add_argument("--workspace-language", choices=["auto", "en", "zh"], default="auto", help="Folder/template language. Default: auto from profile.")
    parser.add_argument("--target-journal", default="TODO:", help="Target journal.")
    parser.add_argument("--article-type", default="TODO:", help="Article type.")
    parser.add_argument("--language", default="TODO:", help="Manuscript writing language.")
    parser.add_argument("--objective", default="TODO:", help="Research objective.")
    parser.add_argument("--overwrite-templates", action="store_true", help="Overwrite template files.")
    parser.add_argument("--no-set-active", action="store_true", help="Do not update active project memory.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.workspace).resolve()
    workspace_language = read_language(root, args.workspace_language)
    p = PATHS[workspace_language]
    projects_dir = root / p["projects"]
    shared_dir = root / p["shared"]

    if not projects_dir.exists() or not shared_dir.exists():
        raise SystemExit("This does not look like an initialized PaperSmart workspace. Run PaperSmart-init first.")

    slug = args.slug or infer_slug(projects_dir, args.title)
    if not re.match(r"^[a-z0-9_]+$", slug):
        raise SystemExit("Project slug must use only lowercase letters, digits, and underscores.")
    if not slug.startswith("paper_"):
        raise SystemExit("Project slug should start with paper_, for example paper_03_short_slug.")

    project = projects_dir / slug
    if project.exists() and not args.overwrite_templates:
        raise SystemExit(f"Project already exists: {project}")

    create_dirs(project, p)
    created = project_templates(
        project=project,
        slug=slug,
        title=args.title,
        target_journal=args.target_journal,
        article_type=args.article_type,
        writing_language=args.language,
        objective=args.objective,
        workspace_language=workspace_language,
        overwrite=args.overwrite_templates,
    )
    if not args.no_set_active:
        update_active_project(root, slug, workspace_language)

    print(f"Created PaperSmart project: {project}")
    print(f"Workspace language: {workspace_language}")
    print(f"Active project updated: {'no' if args.no_set_active else 'yes'}")
    if created:
        print("Created template files:")
        for path in created:
            print(f"- {path}")
    else:
        print("No template files created; existing files were preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
