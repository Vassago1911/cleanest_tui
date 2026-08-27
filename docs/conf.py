# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Prevent Python from creating __pycache__ directories
sys.dont_write_bytecode = True

# Setze den Pfad auf den lib-Ordner (relativ zur conf.py)
sys.path.insert(0, os.path.abspath("../lib"))
# Falls deine Ordnerstruktur direkt im Hauptverzeichnis ist:
sys.path.insert(0, os.path.abspath("../"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ifstui'
copyright = '2026, ml'
author = 'ml'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme"
]
templates_path = ['_templates']
exclude_patterns = ['_build']

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = []
