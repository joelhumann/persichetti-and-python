# Create the `docs/` directory structure for Sphinx

project_name = "Persichetti and Python"
author_name = "Joel Humann"
version = "0.1"

sphinx_conf = f"""
import os
import sys
sys.path.insert(0, os.path.abspath(".."))

project = '{project_name}'
copyright = '2025, {author_name}'
author = '{author_name}'

release = '{version}'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo'
]

napoleon_google_docstring = True
napoleon_numpy_docstring = True

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
"""

index_rst = f"""
{project_name}
{'=' * len(project_name)}

Composer's Operating System for theory, composition, and musical time.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

modules_rst = """
Modules
=======

.. automodule:: fundamentals.pitch
    :members:

.. automodule:: fundamentals.time
    :members:

.. automodule:: core.scales
    :members:

.. automodule:: core.intervals
    :members:

.. automodule:: fundamentals.melodic_motif
    :members:

(add more as needed)
"""

# File map to be written into the docs/ directory
file_map = {
    "docs/conf.py": sphinx_conf,
    "docs/index.rst": index_rst,
    "docs/modules.rst": modules_rst,
    "docs/_static/.keep": "",  # placeholder
    "docs/_templates/.keep": ""
}
