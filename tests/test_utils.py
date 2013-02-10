# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys
import unittest

from os import pardir
from os.path import dirname, abspath, join
sys.path.insert(0, join(dirname(abspath(__file__)), pardir))
from justext.core import is_blank


class TestUtils(unittest.TestCase):
    def test_empty_string(self):
        self.assertTrue(is_blank(""))

    def test_string_with_space(self):
        self.assertTrue(is_blank(" "))

    def test_string_with_nobreak_space(self):
        self.assertTrue(is_blank("\u00A0\t "))

    def test_string_with_narrow_nobreak_space(self):
        self.assertTrue(is_blank("\u202F \t"))

    def test_string_with_spaces(self):
        self.assertTrue(is_blank("    "))

    def test_string_with_newline(self):
        self.assertTrue(is_blank("\n"))

    def test_string_with_tab(self):
        self.assertTrue(is_blank("\t"))

    def test_string_with_whitespace(self):
        self.assertTrue(is_blank("\t\n "))

    def test_string_with_chars(self):
        self.assertFalse(is_blank("  #  "))
