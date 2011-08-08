#!/usr/bin/env python
#
# Copyright (c) 2011 Jan Pomikalek
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from distutils.core import setup

setup(
    name='justext',
    version='1.2',
    description='Heuristic based boilerplate removal tool',
    long_description='''jusText is a tool for removing boilerplate content,
    such as navigation links, headers, and footers from HTML pages. It is
    designed to preserve mainly text containing full sentences and it is
    therefore well suited for creating linguistic resources such as Web
    corpora.''',
    author='Jan Pomikalek',
    author_email='jan.pomikalek@gmail.com',
    url='http://code.google.com/p/justext/',
    license='BSD',
    requires=['lxml (>=2.2.4)'],
    packages=['justext'],
    package_data={'justext': ['stoplists/*.txt']},
    scripts=['bin/justext'],
)
