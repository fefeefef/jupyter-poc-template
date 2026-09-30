"""Reject invalid notebooks and saved results without executing cells."""

import json
import sys
import warnings
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".ipynb_checkpoints", ".venv"}


def check_notebook(path: Path) -> list[str]:
    """Return schema and safety-policy violations for one notebook."""
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"cannot read valid notebook JSON: {exc.__class__.__name__}"]

    if not isinstance(notebook, dict):
        return ["notebook root must be an object"]

    problems = []
    metadata = notebook.get("metadata")
    if not isinstance(metadata, dict):
        problems.append("notebook metadata must be an object")
    elif "widgets" in metadata:
        problems.append("saved widget state is forbidden")

    cells = notebook.get("cells")
    if not isinstance(cells, list):
        return problems + ["cells must be a list"]

    minor_version = notebook.get("nbformat_minor")
    require_cell_ids = (
        notebook.get("nbformat") == 4 and isinstance(minor_version, int) and minor_version >= 5
    )
    seen_ids = set()
    for index, cell in enumerate(cells, start=1):
        if not isinstance(cell, dict):
            problems.append(f"cell {index}: cell must be an object")
            continue
        if require_cell_ids:
            cell_id = cell.get("id")
            if not isinstance(cell_id, str) or not cell_id:
                problems.append(f"cell {index}: cell id is required")
            elif cell_id in seen_ids:
                problems.append(f"cell {index}: duplicate cell id")
            else:
                seen_ids.add(cell_id)
        if "attachments" in cell:
            problems.append(f"cell {index}: saved attachments are forbidden")
        if "outputs" in cell:
            if cell.get("cell_type") != "code" or cell["outputs"] != []:
                problems.append(f"cell {index}: stored outputs are forbidden")
        elif cell.get("cell_type") == "code":
            problems.append(f"cell {index}: outputs must be an empty list")
        if "execution_count" in cell:
            if cell.get("cell_type") != "code" or cell["execution_count"] is not None:
                problems.append(f"cell {index}: execution_count must be null")
        elif cell.get("cell_type") == "code":
            problems.append(f"cell {index}: execution_count must be null")

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            nbformat.validate(notebook)
    except Exception as exc:
        # Validation exceptions can include full cell contents; keep diagnostics data-safe.
        problems.append(f"invalid notebook schema: {exc.__class__.__name__}")
    return problems


def main(paths: list[str] | None = None) -> int:
    """Check given notebooks, or discover notebooks under the template root."""
    if paths:
        notebooks = [Path(path) for path in paths]
    else:
        notebooks = sorted(
            path for path in ROOT.rglob("*.ipynb") if not SKIP_PARTS.intersection(path.parts)
        )

    if not notebooks:
        print("No notebooks found.", file=sys.stderr)
        return 1

    failed = False
    for path in notebooks:
        problems = check_notebook(path)
        for problem in problems:
            print(f"{path}: {problem}", file=sys.stderr)
            failed = True

    if not failed:
        print(f"Checked {len(notebooks)} notebook(s): no saved results.")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
