# Configuration file for the Sphinx documentation builder.
#
import sys
import os
import django
from pathlib import Path
# from ..personal_assistant.settings import DJANGO_SETTINGS_MODULE
#
import environ
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

sys.path.append(os.path.abspath('..'))
DJANGO_SETTINGS_MODULE = env('DJANGO_SETTINGS_MODULE')
django.setup()

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Web Personal Assistant'
copyright = '2023, Team 1 Python Web 9'
author = 'Roman, Maksym, Stanislav, Olexandr'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'agogo'
html_static_path = ['_static']
