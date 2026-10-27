"""Exercise notebook schema and safety checks with temporary files."""

import json
from pathlib import Path

import pytest

from scripts.check_notebooks import check_notebook


def write_notebook(path: Path, *, outputs: list | None = None, execution_count=None) -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": execution_count,
                "id": "analysis",
                "metadata": {},
                "outputs": [] if outputs is None else outputs,
                "source": ["# TODO: Add PoC code.\n"],
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(notebook), encoding="utf-8")


def test_clean_notebook_passes(tmp_path: Path) -> None:
    path = tmp_path / "clean.ipynb"
    write_notebook(path)
    assert check_notebook(path) == []


def test_saved_output_and_execution_count_fail(tmp_path: Path) -> None:
    path = tmp_path / "executed.ipynb"
    output = {"output_type": "stream", "name": "stdout", "text": ["result"]}
    write_notebook(path, outputs=[output], execution_count=1)
    problems = check_notebook(path)
    assert any("stored outputs" in problem for problem in problems)
    assert any("execution_count" in problem for problem in problems)


def test_saved_attachment_fails(tmp_path: Path) -> None:
    path = tmp_path / "attached.ipynb"
    write_notebook(path)
    notebook = json.loads(path.read_text(encoding="utf-8"))
    notebook["cells"] = [
        {
            "cell_type": "markdown",
            "id": "image",
            "metadata": {},
            "source": ["![image](attachment:image.png)"],
            "attachments": {"image.png": {"image/png": "AAAA"}},
        }
    ]
    path.write_text(json.dumps(notebook), encoding="utf-8")
    assert any("attachments" in problem for problem in check_notebook(path))


def test_widget_field_fails_even_when_empty(tmp_path: Path) -> None:
    path = tmp_path / "widgets.ipynb"
    write_notebook(path)
    notebook = json.loads(path.read_text(encoding="utf-8"))
    notebook["metadata"]["widgets"] = {}
    path.write_text(json.dumps(notebook), encoding="utf-8")
    assert any("widget" in problem for problem in check_notebook(path))


def test_empty_attachment_field_fails(tmp_path: Path) -> None:
    path = tmp_path / "attached.ipynb"
    write_notebook(path)
    notebook = json.loads(path.read_text(encoding="utf-8"))
    notebook["cells"] = [
        {
            "cell_type": "markdown",
            "id": "note",
            "metadata": {},
            "source": ["note"],
            "attachments": {},
        }
    ]
    path.write_text(json.dumps(notebook), encoding="utf-8")
    assert any("attachments" in problem for problem in check_notebook(path))


@pytest.mark.parametrize("missing_field", ["nbformat", "cell_type"])
def test_required_schema_field_fails(tmp_path: Path, missing_field: str) -> None:
    path = tmp_path / "invalid.ipynb"
    write_notebook(path)
    notebook = json.loads(path.read_text(encoding="utf-8"))
    target = notebook["cells"][0] if missing_field == "cell_type" else notebook
    target.pop(missing_field)
    path.write_text(json.dumps(notebook), encoding="utf-8")
    assert any("invalid notebook schema" in problem for problem in check_notebook(path))


def test_output_on_non_code_cell_fails(tmp_path: Path) -> None:
    path = tmp_path / "invalid.ipynb"
    write_notebook(path)
    notebook = json.loads(path.read_text(encoding="utf-8"))
    notebook["cells"][0]["cell_type"] = "markdown"
    path.write_text(json.dumps(notebook), encoding="utf-8")
    assert any("stored outputs" in problem for problem in check_notebook(path))


def test_missing_cell_id_fails(tmp_path: Path) -> None:
    path = tmp_path / "missing-id.ipynb"
    write_notebook(path)
    notebook = json.loads(path.read_text(encoding="utf-8"))
    notebook["cells"][0].pop("id")
    path.write_text(json.dumps(notebook), encoding="utf-8")
    assert any("cell id is required" in problem for problem in check_notebook(path))


def test_duplicate_cell_id_fails(tmp_path: Path) -> None:
    path = tmp_path / "duplicate-id.ipynb"
    write_notebook(path)
    notebook = json.loads(path.read_text(encoding="utf-8"))
    notebook["cells"].append(dict(notebook["cells"][0]))
    path.write_text(json.dumps(notebook), encoding="utf-8")
    assert any("duplicate cell id" in problem for problem in check_notebook(path))


def test_invalid_minor_version_fails_without_crashing(tmp_path: Path) -> None:
    path = tmp_path / "invalid-version.ipynb"
    write_notebook(path)
    notebook = json.loads(path.read_text(encoding="utf-8"))
    notebook["nbformat_minor"] = "5"
    path.write_text(json.dumps(notebook), encoding="utf-8")
    assert any("invalid notebook schema" in problem for problem in check_notebook(path))


def test_unreadable_notebook_returns_safe_diagnostic(tmp_path: Path) -> None:
    problems = check_notebook(tmp_path / "missing.ipynb")
    assert problems == ["cannot read valid notebook JSON: FileNotFoundError"]


def test_invalid_json_does_not_echo_notebook_content(tmp_path: Path) -> None:
    path = tmp_path / "broken.ipynb"
    path.write_text('{"sensitive-marker":', encoding="utf-8")
    problems = check_notebook(path)
    assert problems == ["cannot read valid notebook JSON: JSONDecodeError"]
    assert "sensitive-marker" not in " ".join(problems)


@pytest.mark.parametrize(
    ("notebook", "expected"),
    [
        ([], "notebook root must be an object"),
        ({"metadata": [], "cells": []}, "notebook metadata must be an object"),
        ({"metadata": {}, "cells": {}}, "cells must be a list"),
        ({"metadata": {}, "cells": [None]}, "cell 1: cell must be an object"),
    ],
)
def test_malformed_structure_has_actionable_diagnostic(
    tmp_path: Path, notebook: object, expected: str
) -> None:
    path = tmp_path / "broken.ipynb"
    path.write_text(json.dumps(notebook), encoding="utf-8")
    assert expected in check_notebook(path)


@pytest.mark.parametrize("field", ["outputs", "execution_count"])
def test_code_cell_requires_explicit_empty_results(tmp_path: Path, field: str) -> None:
    path = tmp_path / "incomplete.ipynb"
    write_notebook(path)
    notebook = json.loads(path.read_text(encoding="utf-8"))
    notebook["cells"][0].pop(field)
    path.write_text(json.dumps(notebook), encoding="utf-8")
    assert any(field in problem for problem in check_notebook(path))


def test_main_checks_explicit_paths_and_returns_failure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from scripts.check_notebooks import main

    clean = tmp_path / "clean.ipynb"
    executed = tmp_path / "executed.ipynb"
    write_notebook(clean)
    write_notebook(executed, execution_count=1)
    assert main([str(clean), str(executed)]) == 1
    assert "execution_count must be null" in capsys.readouterr().err


def test_main_discovery_skips_local_environments_and_checkpoints(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from scripts import check_notebooks

    write_notebook(tmp_path / "clean.ipynb")
    for ignored in (".venv", ".ipynb_checkpoints", ".git"):
        folder = tmp_path / ignored
        folder.mkdir()
        (folder / "broken.ipynb").write_text("not JSON", encoding="utf-8")
    monkeypatch.setattr(check_notebooks, "ROOT", tmp_path)
    assert check_notebooks.main() == 0
    assert "Checked 1 notebook(s)" in capsys.readouterr().out


def test_main_without_notebooks_reports_existing_failure_condition(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from scripts import check_notebooks

    monkeypatch.setattr(check_notebooks, "ROOT", tmp_path)
    assert check_notebooks.main() == 1
    assert "No notebooks found." in capsys.readouterr().err
