# Copyright (c) 2011 Jan Pomikalek
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from justext.core import justext, get_stoplists, get_stoplist, main

try:
    __version__ = __import__('pkg_resources').get_distribution('justext').version
except:
    __version__ = '?'
