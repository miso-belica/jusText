#!/usr/bin/env python

import sys

total_words = 0
freqs = {}
for line in sys.stdin:
    uline = unicode(line, 'utf-8', errors='ignore')
    for word in uline.split():
        freqs[word] = freqs.get(word, 0) + 1
        total_words+= 1
count = 0
sum_rel_freq = 0
for (word, freq) in sorted(freqs.items(), lambda x,y: cmp(y[1], x[1])):
    rel_freq = float(freq) / total_words
    sum_rel_freq+= rel_freq
    print word.encode('utf-8'), freq, rel_freq, sum_rel_freq
    count+= 1
