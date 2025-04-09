import os
import sys
import sphinx_rtd_theme
sys.path.insert(0, os.path.abspath('..'))  # So Sphinx can find persichetti/

# -- Project Information -----------------------------------------------------
project = 'Persichetti and Python'
author = 'Joel Humann'
copyright = '2025, Joel Humann'
release = '0.1'

# -- General Configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML Output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']
html_theme_options = {
    'navigation_depth': 4,
}

exclude_patterns = ['**/setup.py']

locale_dirs = []  # prevents looking for locales
gettext_compact = False
