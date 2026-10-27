Installation
============

Python 3.11 or newer is required. To preview the starter package from a checkout:

.. code-block:: bash

   python -m pip install .

After the adapted project has been published, replace ``YOUR_PACKAGE_NAME`` with
its real distribution name:

.. code-block:: bash

   pip install YOUR_PACKAGE_NAME

This template does not publish a package or reserve a name on PyPI.

Notebook extra
--------------

To use JupyterLab with the helper package from a checkout:

.. code-block:: bash

   python -m pip install ".[notebook]"
   python -m jupyterlab

Open ``notebooks/poc.ipynb``. Do not commit customer data or saved results.
