#!/usr/bin/env python3
"""Initialize a PaperSmart workspace and optionally install companion skills."""

from __future__ import annotations

import argparse
import datetime as dt
import os
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


def codex_skills_dir() -> Path:
    home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return home / "skills"


def write_file(path: Path, content: str, overwrite: bool) -> bool:
    if path.exists() and not overwrite:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    return True


def mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def today() -> str:
    return dt.date.today().isoformat()


def workspace_files(root: Path, overwrite: bool) -> list[str]:
    created: list[str] = []
    for relative in [
        "projects",
        "shared/docs",
        "shared/prompts",
        "shared/tools",
        "shared/skills",
        "shared/memory",
    ]:
        mkdir(root / relative)
    files = {
        "README.md": """
        # PaperSmart

        PaperSmart is a workspace for scientific manuscript projects. Put one
        paper or research project in each folder under `projects/`. Put
        reusable documentation, prompts, tools, skills, and memory under
        `shared/`.
        """,
        "projects/README.md": """
        # Projects

        Each folder here is one manuscript or research project. Keep
        project-specific drafts, data, outputs, revisions, and submission
        packages inside the relevant project folder.
        """,
        "shared/README.md": """
        # Shared

        Use this folder for reusable PaperSmart resources only. Do not place
        project-specific drafts, data, generated outputs, or submission files
        here.
        """,
        "shared/memory/workspace_structure.md": f"""
        # Workspace structure memory

        Last updated: {today()}

        PaperSmart uses two roots:

        - `projects/` contains one complete folder per paper or research project.
        - `shared/` contains reusable cross-project resources.

        Paths such as `01_draft`, `02_reference`, `03_output`, `config`, and
        `logs` are relative to the active project root.
        """,
    }
    for relative, content in files.items():
        if write_file(root / relative, textwrap.dedent(content), overwrite):
            created.append(relative)
    return created


def project_files(root: Path, slug: str, title: str, overwrite: bool) -> list[str]:
    project = root / "projects" / slug
    for relative in [
        "config",
        "logs",
        "01_draft/data",
        "01_draft/figures",
        "01_draft/tables",
        "01_draft/notes",
        "02_reference/literature",
        "02_reference/target_journal",
        "03_output/manuscript",
        "03_output/tables",
        "03_output/figures",
        "03_output/supplement",
        "03_output/revision",
        "03_output/translation",
        "03_output/submission",
    ]:
        mkdir(project / relative)

    files = {
        "README.md": f"""
        # {title}

        Project slug: `{slug}`

        Use `01_draft` for original user materials, `02_reference` for style
        and literature context, and `03_output` for generated manuscript
        products.
        """,
        "config/project_config.md": f"""
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
        "01_draft/README.md": """
        # Draft source materials

        Store original notes, drafts, data, tables, figures, images, and author
        instructions here. Do not overwrite originals unless explicitly asked.
        """,
        "01_draft/data_inventory.md": """
        # Data inventory

        | File or folder | Type | Fields or contents | Units | Groups | Missing values | Known issues | Expected use |
        | --- | --- | --- | --- | --- | --- | --- | --- |
        | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: | TODO: |
        """,
        "02_reference/README.md": """
        # Reference materials

        Store journal guidelines, templates, writing samples, literature PDFs,
        citation files, and style notes here. Mark style-only samples clearly.
        """,
        "02_reference/style_notes.md": """
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
        "02_reference/reference_index.md": """
        # Reference index

        | File or source | Type | Use | Cite in manuscript? | Notes |
        | --- | --- | --- | --- | --- |
        | TODO: | TODO: | TODO: | TODO: | TODO: |
        """,
        "03_output/README.md": """
        # Output

        Generated manuscripts, tables, figures, supplements, revisions,
        translations, and submission packages belong here.
        """,
        "03_output/revision/change_log.md": f"""
        # Change log

        | Date | Change | Files affected | Notes |
        | --- | --- | --- | --- |
        | {today()} | Project scaffold created | Project folders | TODO: |
        """,
        "03_output/revision/local_revision_tasks.md": """
        # Local revision tasks

        Add requested local edits here after a manuscript exists. Each task
        should specify the section, requested change, affected figures/tables,
        and evidence boundary.
        """,
        "logs/writing_log.md": f"""
        # Writing log

        | Date | Action | Notes |
        | --- | --- | --- |
        | {today()} | Project initialized | TODO: |
        """,
        "logs/decision_log.md": """
        # Decision log

        | Date | Decision | Rationale | Evidence |
        | --- | --- | --- | --- |
        | TODO: | TODO: | TODO: | TODO: |
        """,
    }

    created: list[str] = []
    for relative, content in files.items():
        if write_file(project / relative, textwrap.dedent(content), overwrite):
            created.append(str(Path("projects") / slug / relative))
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
    ok = result.returncode == 0
    return ok, result.stdout.strip()


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


def manual_url(raw_url: str) -> str:
    if raw_url == FIND_SKILLS_RAW:
        return "https://github.com/vercel-labs/skills/tree/main/skills/find-skills"
    if raw_url == HUMANIZER_RAW:
        return "https://github.com/blader/humanizer"
    return raw_url


def install_companion_skills(root: Path) -> list[str]:
    dest = codex_skills_dir()
    dest.mkdir(parents=True, exist_ok=True)
    notes: list[str] = [f"Codex skills directory: {dest}"]

    for name, raw_url in [
        ("find-skills", FIND_SKILLS_RAW),
        ("humanizer", HUMANIZER_RAW),
    ]:
        ok, message = install_raw_skill(name, raw_url, dest)
        notes.append(message)
        if not ok:
            notes.append(f"Manual command: npx skills add {manual_url(raw_url)} -g -y")

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

    notes_path = root / "shared" / "memory" / "install_notes.md"
    write_file(notes_path, "# PaperSmart install notes\n\n" + "\n".join(f"- {n}" for n in notes), True)
    return notes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a PaperSmart workspace.")
    parser.add_argument("--workspace", default=".", help="Workspace root to initialize.")
    parser.add_argument("--project-slug", help="Optional project folder name under projects/.")
    parser.add_argument("--project-title", default="TODO: Working title", help="Project working title.")
    parser.add_argument("--install-skills", action="store_true", help="Install companion Codex skills.")
    parser.add_argument("--overwrite-templates", action="store_true", help="Overwrite template files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.workspace).resolve()
    root.mkdir(parents=True, exist_ok=True)

    created = workspace_files(root, args.overwrite_templates)
    if args.project_slug:
        created.extend(
            project_files(root, args.project_slug, args.project_title, args.overwrite_templates)
        )

    print(f"PaperSmart workspace: {root}")
    if created:
        print("Created or updated files:")
        for path in created:
            print(f"- {path}")
    else:
        print("No template files created; existing files were preserved.")

    if args.install_skills:
        print("\nInstalling companion skills...")
        for note in install_companion_skills(root):
            print(f"- {note}")
        print("\nRestart Codex to pick up newly installed skills.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
