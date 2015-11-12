#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2
import re

url = 'http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict.0.7a'
tdict = {
    'AA': 'A:',
    'AE': '{',
    'AH': 'V',
    'AO': 'O:',
    'AW': 'aU',
    'AY': 'aI',
    'B': 'b',
    'CH': 'tS',
    'D': 'd',
    'DH': 'D',
    'EH': 'E',
    'ER': '3:',
    'EY': 'eI',
    'F': 'f',
    'G': 'g',
    'HH': 'h',
    'IH': 'I',
    'IY': 'i',
    'JH': 'dZ',
    'K': 'k',
    'L': 'l',
    'M': 'm',
    'N': 'n',
    'NG': 'N',
    'OW': '@U',  # Not sure about this one TODO
    'OY': 'OI',
    'P': 'p',
    'R': 'r',
    'S': 's',
    'SH': 'S',
    'T': 't',
    'TH': 'T',
    'UH': 'U',
    'UW': 'u',
    'V': 'v',
    'W': 'w',
    'Y': 'j',
    'Z': 'z',
    'ZH': '3'
    }

if len(sys.argv) <= 1:
    print 'you have not selected input file, downloading the latest version...'
    inputdata = urllib2.urlopen(url).read()
else:
    with open(sys.argv[1], 'r') as f:
        inputdata = f.read()

prons = {}
phones = set()
for line in inputdata.split('\n'):
    if line.startswith(';;;') or not line:
        continue
    word, pron = line.split('  ')
    word = word.lower().strip()
    word = re.sub('\(\d+\)$', '', word)
    pron = re.sub('\d', '', pron)
    pron = [tdict[p] for p in pron.strip().split(' ')]
    if word not in prons:
        prons[word] = []
    prons[word].append(pron)

try:
    output = open('dict.eng', 'w') if len(sys.argv) <= 2 else\
        sys.stdout if sys.argv[2] == '-' else open(sys.argv[2], 'w')
    for w, p in sorted(prons.iteritems()):
        output.write('{}\t{}\n'.format(w, '\t'.join(' '.join(x) for x in p)))
finally:
    if output != sys.stdout:
        output.close()
