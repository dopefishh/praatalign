#!/bin/env python
# -*- coding: utf-8 -*-

import codecs
import phonetizer as ph
import sys

# Load the settings
with open('settings', 'r') as f:
    settings = {k: v.strip() for k, v in map(lambda x: x.split(': '), f)}

# Load the phonetizer
phone = ph.getphonetizer(settings['LAN'], settings['DCT'], settings['RUL'])[0]

# Open the output file and put all missing words in the set
mis = set()
with codecs.open(settings['OUT'], 'r', 'utf-8') as i:
    for line in i:
        words = line.split('\t')[2]
        for word in words.split():
            if phone.phonetizeword(word) is None:
                mis.add(word)

# Write the set to the specified file
with codecs.open(' '.join(sys.argv[1:]), 'w', 'utf-8') as o:
    for word in mis:
        o.write('{}\t\n'.format(word))
