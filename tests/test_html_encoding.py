# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import codecs
import unittest
import pytest

from justext.core import JustextError, decode_html, html_to_dom


class TestHtmlEncoding(unittest.TestCase):

    def assert_strings_equal(self, s1, s2):
        assert type(s1) == type(s2)
        assert s1 == s2

    def assert_strict_decode_error(self, html, codec, **kwargs):
        """The error is both a JustextError and the UnicodeDecodeError of the codec."""
        with pytest.raises(UnicodeDecodeError) as expected:
            html.decode(codec)

        try:
            decode_html(html, errors='strict', **kwargs)
        except JustextError as e:
            error = e
        else:
            self.fail("JustextError not raised")

        assert isinstance(error, UnicodeDecodeError)
        for attr in ("encoding", "object", "start", "end", "reason"):
            assert getattr(error, attr) == getattr(expected.value, attr)
        assert str(error) == str(expected.value)

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

    def test_unknown_encoding_in_strict_mode_is_decode_error(self):
        self.assert_strict_decode_error(b"\xff", "ascii", default_encoding="ascii")

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

    def test_given_encoding_in_strict_mode(self):
        self.assert_strict_decode_error(b"\xff", "utf-8", encoding="utf-8")

    def test_given_wrong_encoding(self):
        html = 'ľščťžäňôě'
        decoded_html = decode_html(html.encode("iso-8859-2"), encoding="ASCII")

        self.assert_strings_equal("\ufffd" * len(html), decoded_html)

    def test_fake_encoding_in_meta(self):
        html = '<meta charset="iso-fake-2"/> ľščťžäňôě'

        with pytest.raises(JustextError):
            decode_html(html.encode("iso-8859-2"), errors='strict')

    def test_meta_encoding_in_strict_mode(self):
        self.assert_strict_decode_error(b'<meta charset="utf-8"/> \xff', "utf-8")

    def test_utf8_bom_is_not_part_of_the_text(self):
        html = '<p>ľščťžýáíéäňúô Ł€</p>'
        decoded_html = decode_html(codecs.BOM_UTF8 + html.encode("utf8"))

        self.assert_strings_equal(html, decoded_html)

    def test_utf8_bom_wins_over_meta(self):
        html = '<meta charset="iso-8859-2"/> ľščťžäňôě'
        decoded_html = decode_html(codecs.BOM_UTF8 + html.encode("utf8"))

        self.assert_strings_equal(html, decoded_html)

    def test_utf8_bom_in_strict_mode(self):
        self.assert_strict_decode_error(codecs.BOM_UTF8 + b"\xff", "utf-8-sig")

    def test_utf16_bom_le(self):
        html = '<p>ľščťžýáíéäňúô Ł€</p>'
        decoded_html = decode_html(codecs.BOM_UTF16_LE + html.encode("utf-16-le"))

        self.assert_strings_equal(html, decoded_html)

    def test_utf16_bom_in_strict_mode(self):
        # a lone high surrogate followed by a plain character
        html = codecs.BOM_UTF16_LE + b"\x00\xd8" + "a".encode("utf-16-le")
        self.assert_strict_decode_error(html, "utf-16")

    def test_utf16_bom_be(self):
        html = '<p>ľščťžýáíéäňúô Ł€</p>'
        decoded_html = decode_html(codecs.BOM_UTF16_BE + html.encode("utf-16-be"))

        self.assert_strings_equal(html, decoded_html)

    def test_utf32_bom_le(self):
        html = '<p>ľščťžýáíéäňúô Ł€</p>'
        decoded_html = decode_html(codecs.BOM_UTF32_LE + html.encode("utf-32-le"))

        self.assert_strings_equal(html, decoded_html)

    def test_utf32_bom_be(self):
        html = '<p>ľščťžýáíéäňúô Ł€</p>'
        decoded_html = decode_html(codecs.BOM_UTF32_BE + html.encode("utf-32-be"))

        self.assert_strings_equal(html, decoded_html)

    def test_utf16_le_starting_with_nul_is_read_as_utf32(self):
        # BOM + U+0000 in UTF-16 LE has the same first 4 bytes as the
        # UTF-32 LE BOM, so it is decoded as UTF-32. That is the trade-off
        # for supporting UTF-32 at all.
        html_bytes = codecs.BOM_UTF16_LE + '\x00<p>abc</p>'.encode("utf-16-le")
        decoded_html = decode_html(html_bytes)

        self.assert_strings_equal(html_bytes.decode("utf-32", "replace"), decoded_html)

    def test_given_encoding_wins_over_bom(self):
        decoded_html = decode_html(codecs.BOM_UTF8 + b"abc", encoding="iso-8859-1")

        self.assert_strings_equal("\xef\xbb\xbfabc", decoded_html)

    def test_utf16_html_to_dom(self):
        html = '<html><body><p>ľščťž</p></body></html>'
        dom = html_to_dom(codecs.BOM_UTF16_LE + html.encode("utf-16-le"))

        self.assert_strings_equal("ľščťž", dom.text_content())
