#!/bin/env python
# -*- coding: utf-8 -*-

import codecs
import phonetizer
import sys

if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) != 5:
    print 'usage:'
    print '\t%s language[spa, tze] example[True, False] input output' %\
        sys.argv[0]

phon = phonetizer.getphonetizer(sys.argv[1])[0]
mis = set()

with codecs.open(sys.argv[3], 'r', 'utf-16') as i:
    for line in i:
        words = line.split('\t')[2]
        for word in words.split():
            if phon.phonetizeword(word) is None:
                mis.add(word)

with codecs.open(sys.argv[4], 'w', 'utf-16') as o:
    if sys.argv[2] == "True":
        o.write('#THIS IS AN EXAMPLE\n')
        o.write('# So type the pronunciation after the tab\n')
        o.write('ado\ta d o\ta o\n')
    for word in mis:
        o.write('%s\t\n' % word)
