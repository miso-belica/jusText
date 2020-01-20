# -*- coding: utf-8 -*-

"""
Copyright (c) 2011 Jan Pomikalek

This software is licensed as described in the file LICENSE.rst.
"""

from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open("README.rst") as readme:
    with open("CHANGELOG.rst") as changelog:
        long_description = readme.read() + "\n\n" + changelog.read()


setup(
    name="jusText",
    version="2.2.0",
    description="Heuristic based boilerplate removal tool",
    long_description=long_description,
    author="Jan Pomikálek",
    author_email="jan.pomikalek@gmail.com",
    maintainer="Michal Belica",
    maintainer_email="miso.belica@gmail.com",
    url="https://github.com/miso-belica/jusText",
    license="The BSD 2-Clause License",
    install_requires=[
        'lxml >= 4.4.2; python_version == "2.7"',
        'lxml == 4.3.5; python_version == "3.4"',
        'lxml >= 4.4.2; python_version > "3.4"',
    ],
    tests_require=[
        "pytest",
        "pytest-cov",
        "coverage",
    ],
    packages=["justext"],
    package_data={"justext": ["stoplists/*.txt"]},
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: Markup :: HTML",
    ),
)
