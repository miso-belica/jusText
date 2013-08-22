# -*- coding: utf8 -*-

"""
Copyright (c) 2011 Jan Pomikalek

This software is licensed as described in the file LICENSE.rst.
"""

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import os
import re
import sys
import pkgutil
import lxml.etree
import lxml.html
import lxml.sax

from xml.sax.handler import ContentHandler
from .paragraph import Paragraph
from ._compat import unicode, ignored


MAX_LINK_DENSITY_DEFAULT = 0.2
LENGTH_LOW_DEFAULT = 70
LENGTH_HIGH_DEFAULT = 200
STOPWORDS_LOW_DEFAULT = 0.30
STOPWORDS_HIGH_DEFAULT = 0.32
NO_HEADINGS_DEFAULT = False
# Short and near-good headings within MAX_HEADING_DISTANCE characters before
# a good paragraph are classified as good unless --no-headings is specified.
MAX_HEADING_DISTANCE_DEFAULT = 200
PARAGRAPH_TAGS = [
    'body', 'blockquote', 'caption', 'center', 'col', 'colgroup', 'dd',
    'div', 'dl', 'dt', 'fieldset', 'form', 'legend', 'optgroup', 'option',
    'p', 'pre', 'table', 'td', 'textarea', 'tfoot', 'th', 'thead', 'tr',
    'ul', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
]
DEFAULT_ENCODING = 'utf8'
DEFAULT_ENC_ERRORS = 'replace'
CHARSET_META_TAG_PATTERN = re.compile(br"""<meta[^>]+charset=["']?([^'"/>\s]+)""",
    re.IGNORECASE)

class JustextError(Exception):
    "Base class for jusText exceptions."

class JustextInvalidOptions(JustextError):
    pass


def get_stoplists():
    """Returns a collection of built-in stop-lists."""
    path_to_stoplists = os.path.dirname(sys.modules["justext"].__file__)
    path_to_stoplists = os.path.join(path_to_stoplists, "stoplists")

    stoplist_names = []
    for filename in os.listdir(path_to_stoplists):
        name, extension = os.path.splitext(filename)
        if extension == ".txt":
            stoplist_names.append(name)

    return tuple(stoplist_names)


def get_stoplist(language):
    """Returns an built-in stop-list for the language as a set of words."""
    file_path = os.path.join("stoplists", "%s.txt" % language)
    try:
        stopwords = pkgutil.get_data("justext", file_path)
    except IOError:
        raise ValueError("Stoplist for language %s is missing. Please use function 'get_stoplists' for complete list of stoplists and feel free to contribute by your own stoplist." % language)

    return frozenset(w.decode("utf8") for w in stopwords.splitlines())


def decode_html(html_string, encoding=None, default_encoding=DEFAULT_ENCODING,
        errors=DEFAULT_ENC_ERRORS):
    """
    Converts a `html_string` containing an HTML page into Unicode.
    Tries to guess character encoding from meta tag.
    """
    if isinstance(html_string, unicode):
        return html_string

    if encoding:
        return html_string.decode(encoding, errors)

    match = CHARSET_META_TAG_PATTERN.search(html_string)
    if match:
        declared_encoding = match.group(1).decode("ASCII")
        # proceed unknown encoding as if it wasn't found at all
        with ignored(LookupError):
            return html_string.decode(declared_encoding, errors)

    # unknown encoding
    try:
        # try UTF-8 first
        return html_string.decode("utf8")
    except UnicodeDecodeError:
        # try lucky with default encoding
        try:
            return html_string.decode(default_encoding)
        except UnicodeDecodeError as e:
            raise JustextError("Unable to decode the HTML to Unicode: " + unicode(e))


def is_blank(string):
    """
    Returns `True` if string contains only white-space characters
    or is empty. Otherwise `False` is returned.
    """
    return not bool(string.lstrip())


def remove_comments(root):
    "Removes comment nodes."
    comments = []
    for node in root.iter():
        if isinstance(node, lxml.html.HtmlComment):
            comments.append(node)

    # start with inner most nodes
    for comment in reversed(comments):
        comment.drop_tree()


def remove_tags(root, *tags):
    useless_tags = tuple(n for n in root.iter() if n.tag in tags)
    # start with inner most nodes
    for node in reversed(useless_tags):
        node.drop_tree()


def preprocess(html_text, encoding=None, default_encoding=DEFAULT_ENCODING,
        enc_errors=DEFAULT_ENC_ERRORS):
    "Converts HTML to DOM and removes unwanted parts."
    if isinstance(html_text, unicode):
        decoded_html = html_text
        # encode HTML for case it's XML with encoding declaration
        encoding_type = encoding if encoding else default_encoding
        html_text = html_text.encode(encoding_type, enc_errors)
    else:
        decoded_html = decode_html(html_text, encoding, default_encoding, enc_errors)

    try:
        root = lxml.html.fromstring(decoded_html)
    except ValueError: # Unicode strings with encoding declaration are not supported.
        # for XHTML files with encoding declaration, use the declared encoding
        root = lxml.html.fromstring(html_text)

    # clean DOM from useless tags
    remove_comments(root)
    remove_tags(root, "head", "script", "style")

    return root


class ParagraphMaker(ContentHandler):
    """
    A class for converting a HTML page represented as a DOM object into a list
    of paragraphs.
    """

    @classmethod
    def make_paragraphs(cls, root):
        """Converts DOM into paragraphs."""
        handler = cls()
        lxml.sax.saxify(root, handler)
        return handler.paragraphs

    def __init__(self):
        self.dom = []
        self.paragraphs = []
        self.paragraph = None
        self.link = False
        self.br = False
        self._start_new_pragraph()

    def _start_new_pragraph(self):
        if self.paragraph and self.paragraph.contains_text():
            self.paragraphs.append(self.paragraph)

        self.paragraph = Paragraph(self.dom)

    def startElementNS(self, name, qname, attrs):
        name = name[1]
        self.dom.append(name)
        if name in PARAGRAPH_TAGS or (name == "br" and self.br):
            if name == "br":
                # the <br><br> is a paragraph separator and should
                # not be included in the number of tags within the
                # paragraph
                self.paragraph.tags_count -= 1
            self._start_new_pragraph()
        else:
            self.br = bool(name == "br")
            if name == 'a':
                self.link = True
            self.paragraph.tags_count += 1

    def endElementNS(self, name, qname):
        name = name[1]
        self.dom.pop()
        if name in PARAGRAPH_TAGS:
            self._start_new_pragraph()
        if name == 'a':
            self.link = False

    def endDocument(self):
        self._start_new_pragraph()

    def characters(self, content):
        if is_blank(content):
            return

        text = self.paragraph.append_text(content)

        if self.link:
            self.paragraph.chars_count_in_links += len(text)
        self.br = False


def classify_paragraphs(paragraphs, stoplist, length_low=LENGTH_LOW_DEFAULT,
        length_high=LENGTH_HIGH_DEFAULT, stopwords_low=STOPWORDS_LOW_DEFAULT,
        stopwords_high=STOPWORDS_HIGH_DEFAULT, max_link_density=MAX_LINK_DENSITY_DEFAULT,
        no_headings=NO_HEADINGS_DEFAULT):
    "Context-free paragraph classification."
    for paragraph in paragraphs:
        length = len(paragraph)
        stopword_density = paragraph.stopwords_density(stoplist)
        link_density = paragraph.links_density()
        paragraph.heading = bool(not no_headings and paragraph.is_heading)

        if link_density > max_link_density:
            paragraph.cf_class = 'bad'
        elif ('\xa9' in paragraph.text) or ('&copy' in paragraph.text):
            paragraph.cf_class = 'bad'
        elif re.search('^select|\.select', paragraph.dom_path):
            paragraph.cf_class = 'bad'
        elif length < length_low:
            if paragraph.chars_count_in_links > 0:
                paragraph.cf_class = 'bad'
            else:
                paragraph.cf_class = 'short'
        elif stopword_density >= stopwords_high:
            if length > length_high:
                paragraph.cf_class = 'good'
            else:
                paragraph.cf_class = 'neargood'
        elif stopword_density >= stopwords_low:
            paragraph.cf_class = 'neargood'
        else:
            paragraph.cf_class = 'bad'

def _get_neighbour(i, paragraphs, ignore_neargood, inc, boundary):
    while i + inc != boundary:
        i += inc
        c = paragraphs[i].class_type
        if c in ['good', 'bad']:
            return c
        if c == 'neargood' and not ignore_neargood:
            return c
    return 'bad'

def get_prev_neighbour(i, paragraphs, ignore_neargood):
    """
    Return the class of the paragraph at the top end of the short/neargood
    paragraphs block. If ignore_neargood is True, than only 'bad' or 'good'
    can be returned, otherwise 'neargood' can be returned, too.
    """
    return _get_neighbour(i, paragraphs, ignore_neargood, -1, -1)

def get_next_neighbour(i, paragraphs, ignore_neargood):
    """
    Return the class of the paragraph at the bottom end of the short/neargood
    paragraphs block. If ignore_neargood is True, than only 'bad' or 'good'
    can be returned, otherwise 'neargood' can be returned, too.
    """
    return _get_neighbour(i, paragraphs, ignore_neargood, 1, len(paragraphs))

def revise_paragraph_classification(paragraphs, max_heading_distance=MAX_HEADING_DISTANCE_DEFAULT):
    """
    Context-sensitive paragraph classification. Assumes that classify_pragraphs
    has already been called.
    """
    # copy classes
    for paragraph in paragraphs:
        paragraph.class_type = paragraph.cf_class

    # good headings
    for i, paragraph in enumerate(paragraphs):
        if not (paragraph.heading and paragraph.class_type == 'short'):
            continue
        j = i + 1
        distance = 0
        while j < len(paragraphs) and distance <= max_heading_distance:
            if paragraphs[j].class_type == 'good':
                paragraph.class_type = 'neargood'
                break
            distance += len(paragraphs[j].text)
            j += 1

    # classify short
    new_classes = {}
    for i, paragraph in enumerate(paragraphs):
        if paragraph.class_type != 'short':
            continue
        prev_neighbour = get_prev_neighbour(i, paragraphs, ignore_neargood=True)
        next_neighbour = get_next_neighbour(i, paragraphs, ignore_neargood=True)
        neighbours = set((prev_neighbour, next_neighbour))
        if neighbours == set(['good']):
            new_classes[i] = 'good'
        elif neighbours == set(['bad']):
            new_classes[i] = 'bad'
        # it must be set(['good', 'bad'])
        elif (prev_neighbour == 'bad' and get_prev_neighbour(i, paragraphs, ignore_neargood=False) == 'neargood') or \
             (next_neighbour == 'bad' and get_next_neighbour(i, paragraphs, ignore_neargood=False) == 'neargood'):
            new_classes[i] = 'good'
        else:
            new_classes[i] = 'bad'

    for i, c in new_classes.items():
        paragraphs[i].class_type = c

    # revise neargood
    for i, paragraph in enumerate(paragraphs):
        if paragraph.class_type != 'neargood':
            continue
        prev_neighbour = get_prev_neighbour(i, paragraphs, ignore_neargood=True)
        next_neighbour = get_next_neighbour(i, paragraphs, ignore_neargood=True)
        if (prev_neighbour, next_neighbour) == ('bad', 'bad'):
            paragraph.class_type = 'bad'
        else:
            paragraph.class_type = 'good'

    # more good headings
    for i, paragraph in enumerate(paragraphs):
        if not (paragraph.heading and paragraph.class_type == 'bad' and paragraph.cf_class != 'bad'):
            continue
        j = i + 1
        distance = 0
        while j < len(paragraphs) and distance <= max_heading_distance:
            if paragraphs[j].class_type == 'good':
                paragraph.class_type = 'good'
                break
            distance += len(paragraphs[j].text)
            j += 1

def justext(html_text, stoplist, length_low=LENGTH_LOW_DEFAULT,
        length_high=LENGTH_HIGH_DEFAULT, stopwords_low=STOPWORDS_LOW_DEFAULT,
        stopwords_high=STOPWORDS_HIGH_DEFAULT, max_link_density=MAX_LINK_DENSITY_DEFAULT,
        max_heading_distance=MAX_HEADING_DISTANCE_DEFAULT, no_headings=NO_HEADINGS_DEFAULT,
        encoding=None, default_encoding=DEFAULT_ENCODING,
        enc_errors=DEFAULT_ENC_ERRORS):
    """
    Converts an HTML page into a list of classified paragraphs. Each paragraph
    is represented as a dictionary with the following attributes:

    text:
      Plain text content.

    cfclass:
      The context-free class -- class assigned by the context-free
      classification: 'good', 'bad', 'neargood' or 'short'.

    class:
      The final class: 'good' or 'bad'.

    heading:
      Set to True of the paragraph contains a heading, False otherwise.

    word_count:
      Number of words.

    linked_char_count:
      Number of characters inside links.

    link_density:
      linked_char_count / len(text)

    stopword_count:
      Number of stop-words in stop-list.

    stopword_density:
      stopword_count / word_count

    dom_path:
      A dom path to the paragraph in the original HTML page.
    """
    root = preprocess(html_text, encoding=encoding,
        default_encoding=default_encoding, enc_errors=enc_errors)
    paragraphs = ParagraphMaker.make_paragraphs(root)
    classify_paragraphs(paragraphs, stoplist, length_low, length_high,
        stopwords_low, stopwords_high, max_link_density, no_headings)
    revise_paragraph_classification(paragraphs, max_heading_distance)
    return paragraphs
