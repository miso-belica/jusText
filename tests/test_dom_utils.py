# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys
import unittest

from os import pardir
from os.path import dirname, abspath, join
sys.path.insert(0, join(dirname(abspath(__file__)), pardir))
from lxml import html
from justext.core import remove_comments


class TestDomUtils(unittest.TestCase):
    def test_remove_comments(self):
        dom = html.fromstring(
            '<html><!-- comment --><body>'
            '<h1>Header</h1>'
            '<!-- comment --> text'
            '<p>footer'
            '</body></html>'
        )

        expected = '<html><!-- comment --><body><h1>Header</h1><!-- comment --> text<p>footer</p></body></html>'
        returned = html.tostring(dom)
        self.assertEqual(expected, returned)

        remove_comments(dom)

        expected = '<html><body><h1>Header</h1> text<p>footer</p></body></html>'
        returned = html.tostring(dom)
        self.assertEqual(expected, returned)
