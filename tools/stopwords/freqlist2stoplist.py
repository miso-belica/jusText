#!/usr/bin/env python

import sys
import re

CORPUS_COVERAGE = 0.5

#non_alphabetical = re.compile('(?!\s)(?:\W|\d|_)', re.U)
alphabetical = re.compile('(?![0-9_])\w', re.U)
sum_rel_freq = 0
for line in sys.stdin:
    uline = unicode(line, 'utf-8', errors='ignore')
    word, dummy_freq, rel_freq, dummy_sum_rel_freq = uline.strip().split()
    if alphabetical.search(word):
        rel_freq = float(rel_freq)
        sum_rel_freq+= rel_freq
        print word.encode('utf-8')
        if sum_rel_freq >= CORPUS_COVERAGE:
            break
