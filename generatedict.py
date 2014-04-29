#!/bin/env python
# -*- coding: utf-8 -*-

import codecs
import phonetizer
import sys

with open('settings', 'r') as f:
    settings = {k: v.strip() for k, v in map(lambda x: x.split(': '), f)}

phontiz = phonetizer.getphonetizer(settings['LAN'], settings['DCT'],
                                   settings['RUL'])[0]

mis = set()
with codecs.open(settings['OUT'], 'r', 'utf-8') as i:
    for line in i:
        words = line.split('\t')[2]
        for word in words.split():
            if phontiz.phonetizeword(word) is None:
                mis.add(word)

with codecs.open(' '.join(sys.argv[1:]), 'w', 'utf-8') as o:
    for word in mis:
        o.write('%s\t\n' % word)
