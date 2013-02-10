# -*- coding: utf8 -*-

"""
Copyright (c) 2011 Jan Pomikalek

This software is licensed as described in the file LICENSE.rst.
"""

from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import justext


with open("README.rst") as readme, open("CHANGELOG.rst") as changelog:
    long_description = readme.read() + "\n\n" + changelog.read()

with open("LICENSE.rst") as file:
    license = file.read()


setup(
    name="jusText",
    version=justext.__version__,
    description="Heuristic based boilerplate removal tool",
    long_description=long_description,
    author="Michal Belica",
    author_email="miso.belica@gmail.com",
    url="https://github.com/miso-belica/jusText",
    license=license,
    install_requires=["lxml>=2.2.4"],
    packages=["justext"],
    package_data={"justext": ["stoplists/*.txt"]},
    scripts=["bin/justext"],
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Text Processing :: Filters",
    ),
)
