# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import codecs
import unittest
import pytest

from justext import core
from justext.core import JustextError, decode_html, html_to_dom


class TestHtmlEncoding(unittest.TestCase):

    def assert_strings_equal(self, s1, s2):
        assert type(s1) == type(s2)
        assert s1 == s2

    def test_unicode(self):
        html = "ľščťžýáíéäňúô Ł€"
        decoded_html = decode_html(html)

        self.assert_strings_equal(html, decoded_html)

    def test_utf8_bytes(self):
        html = "ľščťžýáíéäňúô Ł€"
        decoded_html = decode_html(html.encode("utf8"))

        self.assert_strings_equal(html, decoded_html)

    def test_meta_detection_1(self):
        html = '<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-2"/> ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"))

        self.assert_strings_equal(html, decoded_html)

    def test_meta_detection_2(self):
        html = '<meta content=text/html; charset=iso-8859-2 http-equiv="Content-Type"/> ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"))

        self.assert_strings_equal(html, decoded_html)

    def test_meta_detection_3(self):
        html = '<meta content=\'text/html; charset=iso-8859-2\' http-equiv="Content-Type"/> ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"))

        self.assert_strings_equal(html, decoded_html)

    def test_meta_detection_4(self):
        html = '<meta charset=iso-8859-2/> ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"))

        self.assert_strings_equal(html, decoded_html)

    def test_meta_detection_5(self):
        html = '<meta charset="iso-8859-2"/> ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"))

        self.assert_strings_equal(html, decoded_html)

    def test_meta_detection_6(self):
        html = '<meta charset=iso-8859-2/> ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"))

        self.assert_strings_equal(html, decoded_html)

    def test_meta_detection_7(self):
        html = '<meta charset=iso-8859-2> ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"))

        self.assert_strings_equal(html, decoded_html)

    def test_meta_detection_8(self):
        html = '<meta charset=iso-8859-2> ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"))

        self.assert_strings_equal(html, decoded_html)

    def test_meta_detection_9(self):
        html = '<meta content=text/html; charset=iso-8859-2 http-equiv="Content-Type"/> ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"))

        self.assert_strings_equal(html, decoded_html)

    def test_meta_detection_charset_outside_1(self):
        html = '<meta charset="iso-8859-2"/> charset="iso-fake-29" ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"))

        self.assert_strings_equal(html, decoded_html)

    def test_meta_detection_charset_outside_2(self):
        html = '<meta content=text/html; charset=iso-8859-2 http-equiv="Content-Type"/> charset="iso-fake-29" ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"))

        self.assert_strings_equal(html, decoded_html)

    def test_meta_detection_charset_outside_3(self):
        html = '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; CHARSET=ISO-8859-2"> charset="iso-fake-29" ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"))

        self.assert_strings_equal(html, decoded_html)

    def test_unknown_encoding_in_strict_mode(self):
        html = 'ľščťžäňôě'
        with pytest.raises(JustextError):
            decode_html(html.encode("iso-8859-2"), errors='strict')

    def test_unknown_encoding_with_default_error_handler(self):
        html = 'ľščťžäňôě'
        decoded = decode_html(html.encode("iso-8859-2"), default_encoding="iso-8859-2")
        self.assertEqual(decoded, html)

    def test_default_encoding(self):
        html = 'ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"), default_encoding="iso-8859-2")

        self.assert_strings_equal(html, decoded_html)

    def test_given_encoding(self):
        html = 'ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"), encoding="iso-8859-2")

        self.assert_strings_equal(html, decoded_html)

    def test_given_wrong_encoding(self):
        html = 'ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"), encoding="ASCII")

        self.assert_strings_equal("\ufffd" * len(html), decoded_html)

    def test_fake_encoding_in_meta(self):
        html = '<meta charset="iso-fake-2"/> ľščťžäňôě'

        with pytest.raises(JustextError):
            decode_html(html.encode("iso-8859-2"), errors='strict')

    def test_utf8_bom_is_not_part_of_the_text(self):
        html = '<p>ľščťžýáíéäňúô Ł€</p>'
        decoded_html = decode_html(codecs.BOM_UTF8 + html.encode("utf8"))

        self.assert_strings_equal(html, decoded_html)

    def test_utf8_bom_wins_over_meta(self):
        html = '<meta charset="iso-8859-2"/> ľščťžäňôě'
        decoded_html = decode_html(codecs.BOM_UTF8 + html.encode("utf8"))

        self.assert_strings_equal(html, decoded_html)

    def test_utf16_bom_le(self):
        html = '<p>ľščťžýáíéäňúô Ł€</p>'
        decoded_html = decode_html(codecs.BOM_UTF16_LE + html.encode("utf-16-le"))

        self.assert_strings_equal(html, decoded_html)

    def test_utf16_bom_be(self):
        html = '<p>ľščťžýáíéäňúô Ł€</p>'
        decoded_html = decode_html(codecs.BOM_UTF16_BE + html.encode("utf-16-be"))

        self.assert_strings_equal(html, decoded_html)

    def test_given_encoding_wins_over_bom(self):
        decoded_html = decode_html(codecs.BOM_UTF8 + b"abc", encoding="iso-8859-1")

        self.assert_strings_equal("\xef\xbb\xbfabc", decoded_html)

    def test_utf16_html_to_dom(self):
        html = '<html><body><p>ľščťž</p></body></html>'
        dom = html_to_dom(codecs.BOM_UTF16_LE + html.encode("utf-16-le"))

        self.assert_strings_equal("ľščťž", dom.text_content())

    def test_alias_targets_are_known_codecs(self):
        for codec in set(core.ENCODING_LABEL_ALIASES.values()):
            codecs.lookup(codec)


# the bytes are encoded with the codec that browsers use for the declared label
@pytest.mark.parametrize("label, text, codec", [
    # windows-1252: curly quotes and the euro sign are in 0x80-0x9f
    ("iso-8859-1", "“hi” €5", "cp1252"),
    ("ISO-8859-1", "“hi” €5", "cp1252"),
    ("latin1", "“hi” €5", "cp1252"),
    ("ascii", "“hi” €5", "cp1252"),
    ("us-ascii", "“hi” €5", "cp1252"),
    # GBK has characters that GB2312 does not
    ("gb2312", "镕", "gbk"),
    ("GB2312", "镕", "gbk"),
    ("gbk", "镕", "gbk"),
    # Shift_JIS as in browsers includes NEC row 13 (circled digits)
    ("shift_jis", "日本語 ①", "cp932"),
    ("Shift_JIS", "日本語 ①", "cp932"),
    ("shift-jis", "日本語 ①", "cp932"),
    ("x-sjis", "日本語 ①", "cp932"),
    ("sjis", "日本語 ①", "cp932"),
])
def test_whatwg_encoding_labels(label, text, codec):
    html = '<meta charset="%s"/><p>%s</p>' % (label, text)
    decoded_html = decode_html(html.encode(codec))

    assert decoded_html == html
