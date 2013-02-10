# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys
import unittest

from os import pardir
from os.path import dirname, abspath, join
sys.path.insert(0, join(dirname(abspath(__file__)), pardir))
from justext.core import is_blank, normalize_whitespace


class TestUtils(unittest.TestCase):
    def test_empty_string_is_blank(self):
        self.assertTrue(is_blank(""))

    def test_string_with_space_is_blank(self):
        self.assertTrue(is_blank(" "))

    def test_string_with_nobreak_space_is_blank(self):
        self.assertTrue(is_blank("\u00A0\t "))

    def test_string_with_narrow_nobreak_space_is_blank(self):
        self.assertTrue(is_blank("\u202F \t"))

    def test_string_with_spaces_is_blank(self):
        self.assertTrue(is_blank("    "))

    def test_string_with_newline_is_blank(self):
        self.assertTrue(is_blank("\n"))

    def test_string_with_tab_is_blank(self):
        self.assertTrue(is_blank("\t"))

    def test_string_with_whitespace_is_blank(self):
        self.assertTrue(is_blank("\t\n "))

    def test_string_with_chars_is_not_blank(self):
        self.assertFalse(is_blank("  #  "))

    def test_normalize_no_change(self):
        string = "a b c d e f g h i j k l m n o p q r s ..."
        self.assertEqual(string, normalize_whitespace(string))

    def test_normalize_dont_trim(self):
        string = "  a b c d e f g h i j k l m n o p q r s ...  "
        expected = " a b c d e f g h i j k l m n o p q r s ... "
        self.assertEqual(expected, normalize_whitespace(string))

    def test_normalize_newline_and_tab(self):
        string = "123 \n456\t\n"
        expected = "123 456 "
        self.assertEqual(expected, normalize_whitespace(string))

    def test_normalize_non_break_spaces(self):
        string = "\u00A0\t €\u202F \t"
        expected = " € "
        self.assertEqual(expected, normalize_whitespace(string))
