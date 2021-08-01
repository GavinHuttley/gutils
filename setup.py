#!/usr/bin/env python
import pathlib
import sys

from setuptools import find_packages, setup

__author__ = "Gavin Huttley"
__copyright__ = "Copyright 2014, Gavin Huttley"
__credits__ = ["Gavin Huttley"]
__license__ = "BSD-3"
__version__ = "0.3"
__maintainer__ = "Gavin Huttley"
__email__ = "Gavin.Huttley@anu.edu.au"
__status__ = "Development"

# Check Python version, no point installing if unsupported version inplace
if sys.version_info < (3, 6):
    py_version = ".".join([str(n) for n in sys.version_info])
    raise RuntimeError(
        "Python-3.6 or greater is required, Python-%s used." % py_version
    )

short_description = "MutationMotif"

readme_path = pathlib.Path(__file__).parent / "README.md"
long_description = readme_path.read_text()
PROJECT_URLS = {
    "Documentation": "https://github.com/GavinHuttley/gutils",
    "Bug Tracker": "https://github.com/GavinHuttley/gutils",
    "Source Code": "https://github.com/GavinHuttley/gutils",
}

PACKAGE_DIR = "src"

setup(
    name="gutils",
    version=__version__,
    author="Gavin Huttley",
    author_email="gavin.huttley@anu.edu.au",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/md",
    url="https://github.com/GavinHuttley/gutils",
    platforms=["any"],
    license=["BSD"],
    keywords=[
        "biology",
        "genomics",
        "genetics",
        "statistics",
        "evolution",
        "bioinformatics",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
    ],
    install_requires=["click",],
    entry_points={"console_scripts": ["gutils=gutils.cli:main",],},
    packages=find_packages(where="src"),
    package_dir={"": PACKAGE_DIR},
    project_urls=PROJECT_URLS,
)
