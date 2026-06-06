#!/usr/bin/env python3
"""Create a new project folder in an existing PaperSmart workspace."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import textwrap
from pathlib import Path


PROJECT_RE = re.compile(r"^paper_(\d{2})_(.+)$")


def today() -> str:
    return dt.date.today().isoformat()


def slugify(text: str) -> str:
    ascii_text = text.lower().encode("ascii", "ignore").decode("ascii")
    ascii_text = re.sub(r"[^a-z0-9]+", "_", ascii_text)
    ascii_text = re.sub(r"_+", "_", ascii_text).strip("_")
    if not ascii_text:
        ascii_text = "new_project"
    return ascii_text[:48].strip("_") or "new_project"


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


def create_dirs(project: Path) -> None:
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
        (project / relative).mkdir(parents=True, exist_ok=True)


def project_templates(
    project: Path,
    slug: str,
    title: str,
    target_journal: str,
    article_type: str,
    language: str,
    objective: str,
    overwrite: bool,
) -> list[str]:
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
        - Article type: {article_type}
        - Target journal: {target_journal}
        - Writing language: {language}
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
        "01_draft/README.md": """
        # Draft source materials

        Store original notes, drafts, data, tables, figures, images, and author
        instructions here. Do not overwrite originals unless explicitly asked.

        Suggested intake:

        - Working title or topic
        - Study objective
        - Research questions or hypotheses
        - Methods notes
        - Main results
        - Data files and variable descriptions
        - Existing tables or figures
        - Literature anchors or citation files
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

    created = []
    for relative, content in files.items():
        if write_file(project / relative, content, overwrite):
            created.append(relative)
    return created


def update_active_project(root: Path, slug: str) -> None:
    memory = root / "shared" / "memory" / "workspace_structure.md"
    memory.parent.mkdir(parents=True, exist_ok=True)
    content = f"""
    # Workspace structure memory

    Last updated: {today()}

    PaperSmart uses a two-root structure:

    - `projects/` contains one complete folder per paper or research project.
    - `shared/` contains reusable cross-project resources.

    Current active project:

    - `projects/{slug}`

    Project-specific files should stay inside their project folder. Cross-project
    templates, workflow docs, reusable tools, skills, and durable memory belong
    in `shared/`.
    """
    memory.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new PaperSmart project.")
    parser.add_argument("--workspace", default=".", help="Existing PaperSmart workspace root.")
    parser.add_argument("--title", required=True, help="Working title or project topic.")
    parser.add_argument("--slug", help="Optional explicit project slug.")
    parser.add_argument("--target-journal", default="TODO:", help="Target journal.")
    parser.add_argument("--article-type", default="TODO:", help="Article type.")
    parser.add_argument("--language", default="TODO:", help="Writing language.")
    parser.add_argument("--objective", default="TODO:", help="Research objective.")
    parser.add_argument("--overwrite-templates", action="store_true", help="Overwrite template files.")
    parser.add_argument("--no-set-active", action="store_true", help="Do not update active project memory.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.workspace).resolve()
    projects_dir = root / "projects"
    shared_dir = root / "shared"

    if not projects_dir.exists() or not shared_dir.exists():
        raise SystemExit(
            "This does not look like an initialized PaperSmart workspace. "
            "Run PaperSmart-init first."
        )

    slug = args.slug or infer_slug(projects_dir, args.title)
    if not re.match(r"^[a-z0-9_]+$", slug):
        raise SystemExit("Project slug must use only lowercase letters, digits, and underscores.")
    if not slug.startswith("paper_"):
        raise SystemExit("Project slug should start with paper_, for example paper_03_short_slug.")

    project = projects_dir / slug
    if project.exists() and not args.overwrite_templates:
        raise SystemExit(f"Project already exists: {project}")

    create_dirs(project)
    created = project_templates(
        project=project,
        slug=slug,
        title=args.title,
        target_journal=args.target_journal,
        article_type=args.article_type,
        language=args.language,
        objective=args.objective,
        overwrite=args.overwrite_templates,
    )
    if not args.no_set_active:
        update_active_project(root, slug)

    print(f"Created PaperSmart project: {project}")
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
