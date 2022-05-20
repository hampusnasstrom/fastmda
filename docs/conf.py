# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------


import sys
import os

on_rtd = os.environ.get('READTHEDOCS') == 'True'
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('.'))
project = u'fastmda'
try:
    import fastmda

    project_dir = os.path.abspath(os.path.join(__file__, "..", ".."))
    build_dir = os.path.abspath(fastmda.__file__)
    if on_rtd:
        print("On Read The Docs")
        print("build_dir", build_dir)
        print("project_dir", project_dir)
    elif not build_dir.startswith(project_dir):
        raise RuntimeError(
            "%s looks to come from the system. Fix your PYTHONPATH and restart sphinx."
            % project
        )
except ImportError:
    raise RuntimeError(
        "%s is not on the path. Fix your PYTHONPATH and restart sphinx." % project
    )


# -- Project information -----------------------------------------------------

project = 'FastMDA'
copyright = '2022, Hampus Näsström'
author = 'Hampus Näsström'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
