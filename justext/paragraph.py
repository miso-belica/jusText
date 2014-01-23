# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import re

from .utils import normalize_whitespace


class Paragraph(object):
    """Object representing one block of text in HTML."""
    def __init__(self, dom_path, xpath):
        self.dom_path = ".".join(dom_path)
        self.xpath = '/' + '/'.join('%s[%d]' % (x.name, x.idx) for x in xpath)
        self.text_nodes = []
        self.chars_count_in_links = 0
        self.tags_count = 0

    @property
    def is_heading(self):
        return bool(re.search(r"\bh\d\b", self.dom_path))

    @property
    def is_boilerplate(self):
        return self.class_type != "good"

    @property
    def text(self):
        text = "".join(self.text_nodes)
        return normalize_whitespace(text.strip())

    def __len__(self):
        return len(self.text)

    @property
    def words_count(self):
        return len(self.text.split())

    def contains_text(self):
        return bool(self.text_nodes)

    def append_text(self, text):
        text = normalize_whitespace(text)
        self.text_nodes.append(text)
        return text

    def stopwords_count(self, stopwords):
        count = 0

        for word in self.text.split():
            if word in stopwords:
                count += 1

        return count

    def stopwords_density(self, stopwords):
        words_count = self.words_count
        if words_count == 0:
            return 0

        return self.stopwords_count(stopwords) / words_count

    def links_density(self):
        text_lenght = len(self.text)
        if text_lenght == 0:
            return 0

        return self.chars_count_in_links / text_lenght
