# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Reddit Topics Aggregator"
copyright = "2024, Dan Schaefer"
author = "Dan Schaefer"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# https://pradyunsg.me/furo/
html_theme = "furo"

html_static_path = ["_static"]
# html_logo = "_static/logo.png"

# -- Options for MyST parser -------------------------------------------------
# https://myst-parser.readthedocs.io/

extensions += ["myst_parser"]

myst_enable_extensions = [
    "attrs_block",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#block-attributes
    "attrs_inline",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#inline-attributes
    "colon_fence",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#markdown-figures
]

# -- Options for sphinx-autoapi ----------------------------------------------
# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html

extensions += [
    "sphinx.ext.napoleon",  # required to parse google-style docstrings
    "sphinx.ext.autodoc",  # required to parse typehints
]
autoapi_dirs = ["../src/reddit_topics_aggregator"]

# https://sphinx-autoapi.readthedocs.io/en/latest/how_to.html#how-to-include-type-annotations-as-types-in-rendered-docstrings
autodoc_typehints = "description"

# -- Options for sphinx-clock ----------------------------------------------
# https://sphinx-click.readthedocs.io/en/latest/usage/

extensions += [
    "sphinx_click"
]
