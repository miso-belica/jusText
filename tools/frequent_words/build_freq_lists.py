# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import bz2
import requests

from collections import Counter
from io import open
from path import Path
from WikiExtractor import OutputSplitter, process_data

from langcodes import LANGUAGE_CODES


DECOMPRESS = False
FILE_EXT = "" if DECOMPRESS else ".bz2"


def main():
    for code in LANGUAGE_CODES:
        output_xml_file = "temp/%s-wiki-latest-pages-articles.xml%s" % (code, FILE_EXT)
        output_txt_file = "temp/%s-wiki-latest-pages-articles.txt" % (code,)

        if not Path("temp/").glob(code + "-wiki-*-pages-articles.xml" + FILE_EXT):
            download_wiki_dump(code, output_xml_file)

        if len(Path("temp/").glob(code + "-wiki-*-pages-articles.xml")) == 0:
            return 0

        extract_text(output_xml_file, output_txt_file)
        counter, total_words = count_words(output_txt_file)
        words = pick_most_frequent_words(counter, total_words, 0.5)
        print("\n".join(words))

    return 0


def download_wiki_dump(code, output_file):
    print("Downloading corpus for language %s." % code)
    response = requests.get("http://dumps.wikimedia.org/%(code)swiki/latest/%(code)swiki-latest-pages-articles.xml.bz2" % {"code": code})
    response.raise_for_status()
    print("Corpus downloaded for language %s." % code)
    with open(output_file, "wb") as file:
        print("Writing file for language %s." % code)
        file.write(bz2.decompress(response.content))
    print("File written for language %s." % code)


def extract_text(input_file, output_file):
    splitter = OutputSplitter(False, 500000, "temp/extracted", segment=True)

    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as file:
            process_data('xml', file, splitter, None, None)
    finally:
        splitter.close()


def count_words(file):
    total_words = 0
    counter = Counter()

    for line in open(file, "r", encoding="utf-8"):
        words = line.split()
        total_words += len(words)
        counter.update(words)

    return counter, total_words


def pick_most_frequent_words(counter, total_words, coverage):
    words = []
    total_relative_frequency = 0

    for word, frequency in counter.most_common():
        words.append(word)
        total_relative_frequency += frequency / total_words
        if total_relative_frequency >= coverage:
            break

    return words


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
