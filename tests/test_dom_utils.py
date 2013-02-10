# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys
import unittest

from os import pardir
from os.path import dirname, abspath, join
sys.path.insert(0, join(dirname(abspath(__file__)), pardir))
from lxml import html
from justext.core import remove_comments, remove_tags


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

    def test_remove_tags_1(self):
        html_string = (
            '<html><head><title>Title</title></head><body>'
            '<h1>Header</h1>'
            '<p><span>text</span></p>'
            '<p>footer <em>like</em> a boss</p>'
            '</body></html>'
        )

        dom = html.fromstring(html_string)
        returned = html.tostring(dom)
        self.assertEqual(html_string, returned)

        remove_tags(dom, "head", "em")
        returned = html.tostring(dom)
        expected = (
            '<html><body>'
            '<h1>Header</h1>'
            '<p><span>text</span></p>'
            '<p>footer  a boss</p>'
            '</body></html>'
        )
        self.assertEqual(expected, returned)

    def test_remove_tags_2(self):
        html_string = (
            '<html><head><title>Title</title></head><body>'
            '<h1>Header</h1>'
            '<p>pre<span>text</span>post<em>emph</em>popost</p>'
            '<p>footer <em>like</em> a boss</p>'
            '</body></html>'
        )

        dom = html.fromstring(html_string)
        returned = html.tostring(dom)
        self.assertEqual(html_string, returned)

        remove_tags(dom, "span")
        returned = html.tostring(dom)
        expected = (
            '<html><head><title>Title</title></head><body>'
            '<h1>Header</h1>'
            '<p>prepost<em>emph</em>popost</p>'
            '<p>footer <em>like</em> a boss</p>'
            '</body></html>'
        )
        self.assertEqual(expected, returned)

    def test_remove_tags_3(self):
        html_string = (
            '<html><head><title>Title</title></head><body>'
            '<h1>Header</h1>'
            '<p>pre<span>text</span>post<em>emph</em>popost</p>'
            '<p>footer <em>like</em> a boss</p>'
            '</body></html>'
        )

        dom = html.fromstring(html_string)
        returned = html.tostring(dom)
        self.assertEqual(html_string, returned)

        remove_tags(dom, "em")
        returned = html.tostring(dom)
        expected = (
            '<html><head><title>Title</title></head><body>'
            '<h1>Header</h1>'
            '<p>pre<span>text</span>postpopost</p>'
            '<p>footer  a boss</p>'
            '</body></html>'
        )
        self.assertEqual(expected, returned)
