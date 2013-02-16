# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys
import unittest

from os import pardir
from os.path import dirname, abspath, join
sys.path.insert(0, join(dirname(abspath(__file__)), pardir))
from justext.core import classify_paragraphs


class TestClassifyParagraphs(unittest.TestCase):
    def _paragraph(self, **kwargs):
        paragraph = {
            "dom_path": "body.p",
            "text": "",
            "word_count": 0,
            "linked_char_count": 0,
            "tag_count": 0,
        }

        paragraph.update(kwargs)
        return paragraph

    def test_max_link_density(self):
        paragraphs = [
            self._paragraph(text="0123456789"*2, linked_char_count=0),
            self._paragraph(text="0123456789"*2, linked_char_count=20),
            self._paragraph(text="0123456789"*8, linked_char_count=40),
            self._paragraph(text="0123456789"*8, linked_char_count=39),
            self._paragraph(text="0123456789"*8, linked_char_count=41),
        ]

        classify_paragraphs(paragraphs, (), max_link_density=0.5)

        self.assertEqual(paragraphs[0]["cfclass"], "short")
        self.assertEqual(paragraphs[1]["cfclass"], "bad")
        self.assertEqual(paragraphs[2]["cfclass"], "bad")
        self.assertEqual(paragraphs[3]["cfclass"], "bad")
        self.assertEqual(paragraphs[4]["cfclass"], "bad")

    def test_length_low(self):
        paragraphs = [
            self._paragraph(text="0 1 2 3 4 5 6 7 8 9"*2, linked_char_count=0),
            self._paragraph(text="0 1 2 3 4 5 6 7 8 9"*2, linked_char_count=20),
        ]

        classify_paragraphs(paragraphs, (), max_link_density=1, length_low=1000)

        self.assertEqual(paragraphs[0]["cfclass"], "short")
        self.assertEqual(paragraphs[1]["cfclass"], "bad")

    def test_stopwords_high(self):
        paragraphs = [
            self._paragraph(text="0 1 2 3 4 5 6 7 8 9"),
            self._paragraph(text="0 1 2 3 4 5 6 7 8 9"*2),
        ]

        classify_paragraphs(paragraphs, ("0",), max_link_density=1, length_low=0,
            stopwords_high=0, length_high=20)

        self.assertEqual(paragraphs[0]["cfclass"], "neargood")
        self.assertEqual(paragraphs[1]["cfclass"], "good")

    def test_stopwords_low(self):
        paragraphs = [
            self._paragraph(text="0 0 0 0 1 2 3 4 5 6 7 8 9", word_count=13),
            self._paragraph(text="0 1 2 3 4 5 6 7 8 9", word_count=10),
            self._paragraph(text="1 2 3 4 5 6 7 8 9", word_count=9),
        ]

        classify_paragraphs(paragraphs, ("0", "1",), max_link_density=1,
            length_low=0, stopwords_high=1000, stopwords_low=0.2)

        self.assertEqual(paragraphs[0]["cfclass"], "neargood")
        self.assertEqual(paragraphs[1]["cfclass"], "neargood")
        self.assertEqual(paragraphs[2]["cfclass"], "bad")
