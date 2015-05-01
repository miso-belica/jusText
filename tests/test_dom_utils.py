# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import unittest

from nose import tools
from lxml import html
from justext.core import preprocessor, html_to_dom


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
        returned = html.tostring(dom).decode("utf8")
        tools.assert_equal(expected, returned)

        dom = preprocessor(dom)

        expected = '<html><body><h1>Header</h1> text<p>footer</p></body></html>'
        returned = html.tostring(dom).decode("utf8")
        tools.assert_equal(expected, returned)

    def test_remove_head_tag(self):
        html_string = (
            '<html><head><title>Title</title></head><body>'
            '<h1>Header</h1>'
            '<p><span>text</span></p>'
            '<p>footer <em>like</em> a boss</p>'
            '</body></html>'
        )

        dom = html.fromstring(html_string)
        returned = html.tostring(dom).decode("utf8")
        tools.assert_equal(html_string, returned)

        dom = preprocessor(dom)
        returned = html.tostring(dom).decode("utf8")
        expected = (
            '<html><body>'
            '<h1>Header</h1>'
            '<p><span>text</span></p>'
            '<p>footer <em>like</em> a boss</p>'
            '</body></html>'
        )
        tools.assert_equal(expected, returned)

    def test_preprocess_simple_unicode_string(self):
        html_string = (
            '<html><head><title>Title</title></head><body>'
            '<h1>Header</h1>'
            '<p>pre<span>text</span>post<em>emph</em>popost</p>'
            '<p>footer <em>like</em> a boss</p>'
            '</body></html>'
        )

        dom = preprocessor(html_to_dom(html_string))
        returned = html.tostring(dom).decode("utf8")
        expected = (
            '<html><body>'
            '<h1>Header</h1>'
            '<p>pre<span>text</span>post<em>emph</em>popost</p>'
            '<p>footer <em>like</em> a boss</p>'
            '</body></html>'
        )
        tools.assert_equal(expected, returned)

    def test_preprocess_simple_bytes_string(self):
        html_string = (
            b'<html><head><title>Title</title></head><body>'
            b'<h1>Header</h1>'
            b'<p>pre<span>text</span>post<em>emph</em>popost</p>'
            b'<p>footer <em>like</em> a boss</p>'
            b'  <!-- abcdefgh -->\n'
            b'</body></html>'
        )

        dom = preprocessor(html_to_dom(html_string))
        returned = html.tostring(dom).decode("utf8")
        expected = (
            '<html><body>'
            '<h1>Header</h1>'
            '<p>pre<span>text</span>post<em>emph</em>popost</p>'
            '<p>footer <em>like</em> a boss</p>'
            '  \n'
            '</body></html>'
        )
        tools.assert_equal(expected, returned)

    def test_preprocess_simple_unicode_xhtml_string_with_declaration(self):
        html_string = (
            '<?xml version="1.0" encoding="windows-1250"?>'
            '<!DOCTYPE html>'
            '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="sk" lang="sk">'
            '<head>'
            '<title>Hello World</title>'
            '<meta http-equiv="imagetoolbar" content="no" />'
            '<meta http-equiv="Content-Type" content="text/html; charset=windows-1250" />'
            '</head>'
            '<body id="index">'
            '</body>'
            '</html>'
        )

        dom = preprocessor(html_to_dom(html_string))
        returned = html.tostring(dom).decode("utf8")
        expected = (
            '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="sk" lang="sk">'
            '<body id="index">'
            '</body>'
            '</html>'
        )
        tools.assert_equal(expected, returned)

    def test_preprocess_simple_bytes_xhtml_string_with_declaration(self):
        html_string = (
            b'<?xml version="1.0" encoding="windows-1250"?>'
            b'<!DOCTYPE html>'
            b'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="sk" lang="sk">'
            b'<head>'
            b'<title>Hello World</title>'
            b'<meta http-equiv="imagetoolbar" content="no" />'
            b'<meta http-equiv="Content-Type" content="text/html; charset=windows-1250" />'
            b'</head>'
            b'<body id="index">'
            b'</body>'
            b'</html>'
        )

        dom = preprocessor(html_to_dom(html_string))
        returned = html.tostring(dom).decode("utf8")
        expected = (
            '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="sk" lang="sk">'
            '<body id="index">'
            '</body>'
            '</html>'
        )
        tools.assert_equal(expected, returned)
