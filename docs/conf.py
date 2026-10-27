"""Build user documentation for the installed starter package."""

from importlib.metadata import version as _package_version

project = "TODO: Customer PoC"
author = "TODO: Responsible team"
release = _package_version("todo-jupyter-poc")
version = release
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "myst_parser"]
exclude_patterns = ["_build"]
html_theme = "alabaster"
html_show_copyright = False
