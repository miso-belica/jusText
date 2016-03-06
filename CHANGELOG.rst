.. :changelog:

Changelog for jusText
=====================

2.2.0 (2016-03-06)
------------------
- *INCOMPATIBLE CHANGE:* Stop words are case insensitive.
- *INCOMPATIBLE CHANGE:* Dropped support for Python 3.2
- *BUG FIX:* Preserve new lines from original text in paragraphs.

2.1.1 (2014-05-27)
------------------
- *BUG FIX:* Function ``decode_html`` now respects parameter ``errors`` when falling to ``default_encoding`` `#9 <https://github.com/miso-belica/jusText/issues/9>`_.

2.1.0 (2014-01-25)
------------------
- *FEATURE:* Added XPath selector to the paragrahs. XPath selector is also available in detailed output as ``xpath`` attribute of ``<p>`` tag `#5 <https://github.com/miso-belica/jusText/pull/5>`_.

2.0.0 (2013-08-26)
------------------
- *FEATURE:* Added pluggable DOM preprocessor.
- *FEATURE:* Added support for Python 3.2+.
- *INCOMPATIBLE CHANGE:* Paragraphs are instances of
  ``justext.paragraph.Paragraph``.
- *INCOMPATIBLE CHANGE:* Script 'justext' removed in favour of
  command ``python -m justext``.
- *FEATURE:* It's possible to enter an URI as input document in CLI.
- *FEATURE:* It is possible to pass unicode string directly.

1.2.0 (2011-08-08)
------------------
- *FEATURE:* Character counts used instead of word counts where possible in
  order to make the algorithm work well in the language independent
  mode (without a stoplist) for languages where counting words is
  not easy (Japanese, Chinese, Thai, etc).
- *BUG FIX:* More robust parsing of meta tags containing the information about
  used charset.
- *BUG FIX:* Corrected decoding of HTML entities &#128; to &#159;

1.1.0 (2011-03-09)
------------------
- First public release.
