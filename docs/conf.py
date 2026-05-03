# Configuration file for the Sphinx documentation builder.
# See the documentation for a complete list of options.

import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath('..'))

project = 'FeatEx'
copyright = '2024, FeatEx Contributors'
author = 'FeatEx Contributors'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = []

# Configure autodoc
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
}
