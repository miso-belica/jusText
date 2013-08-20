.. :changelog:

Changelog for jusText
=====================
- *INCOMPATIBLE CHANGE:* Paragraphs are instances of
  ``justext.paragraph.Paragraph``.
- *INCOMPATIBLE CHANGE:* Script 'justext' removed in favour of
  command `python -m justext`.
- *FEATURE:* It's possible to enter an URI as input document in CLI.
- *FEATURE:* It is possible to pass unicode string directly.

1.2 (2011-08-08)
-----------------
- *FEATURE:* Character counts used instead of word counts where possible in
  order to make the algorithm work well in the language independent
  mode (without a stoplist) for languages where counting words is
  not easy (Japanese, Chinese, Thai, etc).
- *BUG FIX:* More robust parsing of meta tags containing the information about
  used charset.
- *BUG FIX:* Corrected decoding of HTML entities &#128; to &#159;

1.1 (2011-03-09)
----------------
- First public release.
