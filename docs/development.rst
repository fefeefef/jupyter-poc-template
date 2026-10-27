Development
===========

The root ``CONTRIBUTING.md`` is the contributor guide for humans and agents.
Development uses uv and the committed lockfile:

.. code-block:: bash

   uv sync --locked --group dev --group docs
   uv run --locked pre-commit run --all-files
   uv run --locked pytest --cov --cov-report=term-missing
   uv build
   uv run --locked twine check dist/*
   uv run --locked coverage run --append scripts/check_distribution.py
   uv run --locked coverage run --append scripts/check_notebooks.py
   uv run --locked coverage report
   uv run --locked coverage xml
   uv run --locked coverage html

Build and preview this documentation
------------------------------------

.. code-block:: bash

   uv run --locked --group docs sphinx-build -b html docs docs/_build/html
   python -m http.server --directory docs/_build/html 8000

Open http://localhost:8000 in a browser. Stop the preview server with Ctrl-C.
The build imports the installed package to generate API documentation.
Documentation dependencies are separate from the package's runtime dependencies.

The ``testing`` workflow builds these pages locally on its runner; it does not
publish them. Coverage is reported without a percentage gate. Codecov uploads are
an explicit repository opt-in; publishing remains inactive.
