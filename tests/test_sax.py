# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys
import unittest

from os import pardir
from os.path import dirname, abspath, join
sys.path.insert(0, join(dirname(abspath(__file__)), pardir))
from lxml import html
from justext.core import ParagraphMaker


class TestSax(unittest.TestCase):
    def asserParagraphsEqual(self, paragraph, **kwargs):
        for name, value in kwargs.items():
            returned_value = getattr(paragraph, name)
            msg = "%s: %r != %r" % (name, value, returned_value)
            self.assertEqual(value, returned_value, msg)

    def test_no_paragraphs(self):
        html_string = '<html><body></body></html>'
        dom = html.fromstring(html_string)

        returned = html.tostring(dom)
        self.assertEqual(html_string, returned)

        paragraphs = ParagraphMaker.make_paragraphs(dom)
        self.assertEqual(len(paragraphs), 0)

    def test_basic(self):
        html_string = (
            '<html><body>'
            '<h1>Header</h1>'
            '<p>text and some <em>other</em> words <span class="class">that I</span> have in my head now</p>'
            '<p>footer</p>'
            '</body></html>'
        )
        dom = html.fromstring(html_string)

        returned = html.tostring(dom)
        self.assertEqual(html_string, returned)

        paragraphs = ParagraphMaker.make_paragraphs(dom)
        self.assertEqual(len(paragraphs), 3)

        self.asserParagraphsEqual(paragraphs[0], text="Header", words_count=1, tags_count=0)

        text = "text and some other words that I have in my head now"
        self.asserParagraphsEqual(paragraphs[1], text=text, words_count=12, tags_count=2)

        self.asserParagraphsEqual(paragraphs[2], text="footer", words_count=1, tags_count=0)

    def test_whitespace_handling(self):
        html_string = (
            '<html><body>'
            '<p>pre<em>in</em>post \t pre  <span class="class"> in </span>  post</p>'
            '<div>pre<em> in </em>post</div>'
            '<pre>pre<em>in </em>post</pre>'
            '<blockquote>pre<em> in</em>post</blockquote>'
            '</body></html>'
        )
        dom = html.fromstring(html_string)

        returned = html.tostring(dom)
        self.assertEqual(html_string, returned)

        paragraphs = ParagraphMaker.make_paragraphs(dom)
        self.assertEqual(len(paragraphs), 4)

        self.asserParagraphsEqual(paragraphs[0], text="preinpost pre in post",
            words_count=4, tags_count=2)

        self.asserParagraphsEqual(paragraphs[1], text="pre in post",
            words_count=3, tags_count=1)

        self.asserParagraphsEqual(paragraphs[2], text="prein post",
            words_count=2, tags_count=1)

        self.asserParagraphsEqual(paragraphs[3], text="pre inpost",
            words_count=2, tags_count=1)

    def test_multiple_line_break(self):
        html_string = (
            '<html><body>'
            '  normal text   <br><br> another   text  '
            '</body></html>'
        )
        dom = html.fromstring(html_string)

        returned = html.tostring(dom)
        self.assertEqual(html_string, returned)

        paragraphs = ParagraphMaker.make_paragraphs(dom)
        self.assertEqual(len(paragraphs), 2)

        self.asserParagraphsEqual(paragraphs[0], text="normal text",
            words_count=2, tags_count=0)

        self.asserParagraphsEqual(paragraphs[1], text="another text",
            words_count=2, tags_count=0)

    def test_inline_text_in_body(self):
        """Inline text should be treated as separate paragraph."""
        html_string = (
            '<html><body>'
            '<sup>I am <strong>top</strong>-inline\n\n\n\n and I am happy \n</sup>'
            '<p>normal text</p>'
            '<code>\nvar i = -INFINITY;\n</code>'
            '<div>after text with variable <var>N</var> </div>'
            '   I am inline\n\n\n\n and I am happy \n'
            '</body></html>'
        )
        dom = html.fromstring(html_string)

        paragraphs = ParagraphMaker.make_paragraphs(dom)
        self.assertEqual(len(paragraphs), 5)

        self.asserParagraphsEqual(paragraphs[0], words_count=7, tags_count=2,
            text="I am top-inline and I am happy")

        self.asserParagraphsEqual(paragraphs[1], words_count=2, tags_count=0,
            text="normal text")

        self.asserParagraphsEqual(paragraphs[2], words_count=4, tags_count=1,
            text="var i = -INFINITY;")

        self.asserParagraphsEqual(paragraphs[3], words_count=5, tags_count=1,
            text="after text with variable N")

        self.asserParagraphsEqual(paragraphs[4], words_count=7, tags_count=0,
            text="I am inline and I am happy")

    def test_links(self):
        """Inline text should be treated as separate paragraph."""
        html_string = (
            '<html><body>'
            '<a>I am <strong>top</strong>-inline\n\n\n\n and I am happy \n</a>'
            '<p>normal text</p>'
            '<code>\nvar i = -INFINITY;\n</code>'
            '<div>after <a>text</a> with variable <var>N</var> </div>'
            '   I am inline\n\n\n\n and I am happy \n'
            '</body></html>'
        )
        dom = html.fromstring(html_string)

        paragraphs = ParagraphMaker.make_paragraphs(dom)
        self.assertEqual(len(paragraphs), 5)

        self.asserParagraphsEqual(paragraphs[0], words_count=7, tags_count=2,
            text="I am top-inline and I am happy", chars_count_in_links=31)

        self.asserParagraphsEqual(paragraphs[1], words_count=2, tags_count=0,
            text="normal text")

        self.asserParagraphsEqual(paragraphs[2], words_count=4, tags_count=1,
            text="var i = -INFINITY;")

        self.asserParagraphsEqual(paragraphs[3], words_count=5, tags_count=2,
            text="after text with variable N", chars_count_in_links=4)

        self.asserParagraphsEqual(paragraphs[4], words_count=7, tags_count=0,
            text="I am inline and I am happy")
