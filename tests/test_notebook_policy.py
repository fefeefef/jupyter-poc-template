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
