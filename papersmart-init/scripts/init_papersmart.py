#!/usr/bin/env python3
"""Initialize a PaperSmart workspace in English or Chinese."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import tempfile
import textwrap
import urllib.request
from pathlib import Path


FIND_SKILLS_RAW = (
    "https://raw.githubusercontent.com/vercel-labs/skills/main/"
    "skills/find-skills/SKILL.md"
)
HUMANIZER_RAW = "https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md"
NATURE_REPO = "https://github.com/Yuan1z0825/nature-skills.git"
NATURE_SKILLS = [
    "nature-academic-search",
    "nature-citation",
    "nature-data",
    "nature-figure",
    "nature-paper2ppt",
    "nature-polishing",
    "nature-reader",
    "nature-response",
    "nature-reviewer",
    "nature-writing",
]

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
    },
}


def today() -> str:
    return dt.date.today().isoformat()


def assistant_skills_dir(override: str | None = None) -> Path:
    if override:
        return Path(override).expanduser().resolve()
    for name in ("PAPERSMART_SKILLS_DIR", "ASSISTANT_SKILLS_DIR", "SKILLS_DIR"):
        value = os.environ.get(name)
        if value:
            return Path(value).expanduser().resolve()
    return Path.home() / ".skills"


def write_file(path: Path, content: str, overwrite: bool) -> bool:
    if path.exists() and not overwrite:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    return True


def mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def slugify(text: str) -> str:
    ascii_text = text.lower().encode("ascii", "ignore").decode("ascii")
    ascii_text = re.sub(r"[^a-z0-9]+", "_", ascii_text)
    ascii_text = re.sub(r"_+", "_", ascii_text).strip("_")
    return ascii_text[:48].strip("_") or "new_project"


def profile_path(root: Path, p: dict[str, str]) -> Path:
    return root / p["shared"] / p["memory"] / PROFILE_NAME


def profile_content(language: str, active_project: str | None = None) -> str:
    p = PATHS[language]
    lines = [
        "# PaperSmart profile" if language == "en" else "# PaperSmart 配置",
        "",
        f"- language: `{language}`",
        f"- output_language: `{'English' if language == 'en' else '中文'}`",
        f"- active_project: `{active_project or 'TODO:'}`",
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


def workspace_files(root: Path, language: str, overwrite: bool) -> list[str]:
    p = PATHS[language]
    created: list[str] = []
    for relative in [
        p["projects"],
        f"{p['shared']}/{p['docs']}",
        f"{p['shared']}/{p['prompts']}",
        f"{p['shared']}/{p['tools']}",
        f"{p['shared']}/{p['skills']}",
        f"{p['shared']}/{p['memory']}",
    ]:
        mkdir(root / relative)

    if language == "zh":
        files = {
            p["workspace_readme"]: """
            # PaperSmart

            PaperSmart 是一个用于管理科研论文项目的工作区。每篇论文放在
            `项目/` 下的独立文件夹中；跨项目复用的文档、提示、工具、技能和记忆
            放在 `共享/`。
            """,
            f"{p['projects']}/{p['project_readme']}": """
            # 项目

            每个文件夹对应一篇论文或一个研究项目。项目专用的草稿、数据、输出、
            修订记录和投稿材料都应留在对应项目文件夹内。
            """,
            f"{p['shared']}/{p['shared_readme']}": """
            # 共享

            这里只放跨项目复用资源。不要把单篇论文的草稿、数据、生成输出或投稿
            文件放在这里。
            """,
        }
    else:
        files = {
            p["workspace_readme"]: """
            # PaperSmart

            PaperSmart is a workspace for scientific manuscript projects. Put
            each paper or research project in its own folder under `projects/`.
            Put reusable documentation, prompts, tools, skills, and memory under
            `shared/`.
            """,
            f"{p['projects']}/{p['project_readme']}": """
            # Projects

            Each folder here is one manuscript or research project. Keep
            project-specific drafts, data, outputs, revisions, and submission
            packages inside the relevant project folder.
            """,
            f"{p['shared']}/{p['shared_readme']}": """
            # Shared

            Use this folder for reusable PaperSmart resources only. Do not put
            project-specific drafts, data, generated outputs, or submission
            files here.
            """,
        }

    files[f"{p['shared']}/{p['memory']}/{PROFILE_NAME}"] = profile_content(language)
    for relative, content in files.items():
        if write_file(root / relative, content, overwrite):
            created.append(relative)
    return created


def project_files(root: Path, slug: str, title: str, language: str, overwrite: bool) -> list[str]:
    p = PATHS[language]
    project = root / p["projects"] / slug
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
        mkdir(project / relative)

    if language == "zh":
        files = {
            p["project_readme"]: f"""
            # {title}

            项目目录：`{slug}`

            原始材料放入 `{p['draft']}`，期刊格式和文献背景放入
            `{p['reference']}`，生成稿件和投稿材料写入 `{p['output']}`。
            """,
            f"{p['config']}/{p['project_config']}": f"""
            # 项目配置

            更新日期：{today()}

            - 工作题目：{title}
            - 文章类型：TODO:
            - 目标期刊：TODO:
            - 写作语言：中文
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
            f"{p['draft']}/{p['draft_readme']}": """
            # 草稿与原始材料

            这里存放原始笔记、草稿、数据、表格、图像和作者指示。除非用户明确要求，
            不要覆盖原始文件。
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
            写作样本如果只用于风格参考，必须明确标注，不要自动写入参考文献。
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

            正文生成后，将局部修改要求写在这里。每项任务应说明章节、修改要求、
            受影响的图表以及证据边界。
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
            journal and literature context, and `{p['output']}` for generated
            manuscript products.
            """,
            f"{p['config']}/{p['project_config']}": f"""
            # Project config

            Last updated: {today()}

            - Working title: {title}
            - Article type: TODO:
            - Target journal: TODO:
            - Writing language: English
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
            f"{p['draft']}/{p['draft_readme']}": """
            # Draft source materials

            Store original notes, drafts, data, tables, figures, images, and
            author instructions here. Do not overwrite originals unless the
            user explicitly asks.
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
            clearly; do not cite them as evidence unless the manuscript discusses
            their substantive claims.
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

            Add requested local edits here after a manuscript exists. Each task
            should specify the section, requested change, affected figures or
            tables, and evidence boundary.
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

    created: list[str] = []
    for relative, content in files.items():
        if write_file(project / relative, content, overwrite):
            created.append(str(Path(p["projects"]) / slug / relative))

    write_file(profile_path(root, p), profile_content(language, f"{p['projects']}/{slug}"), True)
    return created


def install_raw_skill(name: str, raw_url: str, dest: Path) -> tuple[bool, str]:
    skill_dir = dest / name
    skill_file = skill_dir / "SKILL.md"
    if skill_file.exists():
        return True, f"{name}: already installed"
    try:
        with urllib.request.urlopen(raw_url, timeout=30) as response:
            content = response.read().decode("utf-8")
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file.write_text(content, encoding="utf-8")
        return True, f"{name}: installed from {raw_url}"
    except Exception as exc:
        return False, f"{name}: failed raw install: {exc}"


def run_command(args: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            args,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=240,
            check=False,
        )
    except Exception as exc:
        return False, f"{' '.join(args)} failed to start: {exc}"
    return result.returncode == 0, result.stdout.strip()


def copy_nature_from_clone(dest: Path) -> tuple[bool, str]:
    if all((dest / name / "SKILL.md").exists() for name in NATURE_SKILLS):
        return True, "nature skills: already installed"
    git = shutil.which("git")
    if not git:
        return False, "nature skills: git not found"
    with tempfile.TemporaryDirectory(prefix="papersmart-nature-") as tmp:
        repo_dir = Path(tmp) / "nature-skills"
        ok, output = run_command([git, "clone", "--depth", "1", NATURE_REPO, str(repo_dir)])
        if not ok:
            return False, f"nature skills: git clone failed: {output}"
        source_root = repo_dir / "skills"
        if not source_root.exists():
            return False, "nature skills: cloned repo has no skills directory"
        installed = []
        for source in source_root.iterdir():
            if not source.is_dir() or not source.name.startswith("nature-"):
                continue
            target = dest / source.name
            if target.exists():
                continue
            shutil.copytree(source, target)
            installed.append(source.name)
        if installed:
            return True, "nature skills: installed " + ", ".join(installed)
        return True, "nature skills: no missing nature skills found"


def install_companion_skills(root: Path, language: str, skills_dir: str | None = None) -> list[str]:
    dest = assistant_skills_dir(skills_dir)
    dest.mkdir(parents=True, exist_ok=True)
    notes = [f"Skills directory: {dest}"]

    for name, raw_url in [("find-skills", FIND_SKILLS_RAW), ("humanizer", HUMANIZER_RAW)]:
        ok, message = install_raw_skill(name, raw_url, dest)
        notes.append(message)
        if not ok:
            notes.append(f"Manual command: npx skills add {raw_url} -g -y")

    missing_nature = [name for name in NATURE_SKILLS if not (dest / name / "SKILL.md").exists()]
    if missing_nature:
        ok, output = run_command(["npx", "skills", "add", "Yuan1z0825/nature-skills", "-g", "-y"])
        notes.append("nature skills via npx: " + ("ok" if ok else "failed"))
        if output:
            notes.append(output)
    missing_nature = [name for name in NATURE_SKILLS if not (dest / name / "SKILL.md").exists()]
    if missing_nature:
        ok, message = copy_nature_from_clone(dest)
        notes.append(message)
    missing_nature = [name for name in NATURE_SKILLS if not (dest / name / "SKILL.md").exists()]
    if missing_nature:
        notes.append("Missing nature skills after install attempt: " + ", ".join(missing_nature))
        notes.append("Manual command: npx skills add Yuan1z0825/nature-skills -g -y")

    p = PATHS[language]
    notes_name = "install_notes.md" if language == "en" else "安装说明.md"
    write_file(
        root / p["shared"] / p["memory"] / notes_name,
        "# PaperSmart install notes\n\n" + "\n".join(f"- {note}" for note in notes),
        True,
    )
    return notes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a PaperSmart workspace.")
    parser.add_argument("--workspace", default=".", help="Workspace root to initialize.")
    parser.add_argument("--language", choices=["en", "zh"], default="en", help="Workspace language. Default: en.")
    parser.add_argument("--project-slug", help="Optional project folder name.")
    parser.add_argument("--project-title", default="TODO: Working title", help="Project working title.")
    parser.add_argument("--install-skills", action="store_true", help="Install companion skills.")
    parser.add_argument("--skills-dir", help="Local assistant skills directory. Defaults to PAPERSMART_SKILLS_DIR, ASSISTANT_SKILLS_DIR, SKILLS_DIR, or ~/.skills.")
    parser.add_argument("--overwrite-templates", action="store_true", help="Overwrite template files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.workspace).resolve()
    root.mkdir(parents=True, exist_ok=True)

    slug = args.project_slug
    if slug is None and args.project_title != "TODO: Working title":
        slug = f"paper_01_{slugify(args.project_title)}"

    created = workspace_files(root, args.language, args.overwrite_templates)
    if slug:
        created.extend(project_files(root, slug, args.project_title, args.language, args.overwrite_templates))

    print(f"PaperSmart workspace: {root}")
    print(f"Language mode: {args.language}")
    if created:
        print("Created or updated files:")
        for path in created:
            print(f"- {path}")
    else:
        print("No template files created; existing files were preserved.")

    if args.install_skills:
        print("\nInstalling companion skills...")
        for note in install_companion_skills(root, args.language, args.skills_dir):
            print(f"- {note}")
        print("\nRestart your assistant environment to pick up newly installed skills.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
