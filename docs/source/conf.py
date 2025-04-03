import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  # So Sphinx can find persichetti/

# -- Project Information -----------------------------------------------------
project = 'Persichetti and Python'
author = 'Joel Humann'
copyright = '2025, Joel Humann'
release = '0.1'

# -- General Configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML Output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'navigation_depth': 4,
}
