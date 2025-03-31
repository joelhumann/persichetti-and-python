
import os
import sys
sys.path.insert(0, os.path.abspath("../persichetti"))

project = 'Persichetti and Python'
copyright = '2025, Joel Humann'
author = 'Joel Humann'

release = '0.1'

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
