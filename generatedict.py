#!/bin/env python
# -*- coding: utf-8 -*-

import codecs
import phonetizer as ph
import sys
import os

# Load the settings
with open('settings', 'r') as f:
    sett = {k: v.strip() for k, v in map(lambda x: x.split(': '), f)}

try:
    os.remove('temp.status')
except:
    pass

# Load the phonetizer
try:
    phone = ph.getphonetizer(
        sett['LAN'], sett['PHO'], sett['DCT'], sett['RUL'])
except UnicodeError:
    with open('temp.status', 'w') as f:
        f.write('Unicode error. Check if the files are utf-8')
    exit()
except IOError as e:
    if e.filename == sett['DCT']:
        error = 'Dictionary file couldn\'t be found\n'\
            'It is searched for in {}'.format(e.filename)
    elif e.filename == sett['RUL']:
        error = 'Ruleset file couldn\'t be found\n'\
            'It is searched for in {}'.format(e.filename)
    elif e.filename == sett['PHO']:
        error = 'Universal phonetizer file couldn\'t be found\n'\
            'It is searched for in {}'.format(e.filename)
    else:
        error = 'Some io error: ' + str(e)
    with open('temp.status', 'w') as f:
        f.write(error)
    exit()

# Open the output file and put all missing words in the set
mis = set()
with codecs.open(sett['OUT'], 'r', 'utf-8') as i:
    for line in i:
        words = line.split('\t')[2]
        for word in words.split():
            if phone.phonetizeword(word) is None:
                mis.add(word)

# Write the set to the specified file
with codecs.open(' '.join(sys.argv[1:]), 'w', 'utf-8') as o:
    for word in mis:
        o.write(u'{}\t\n'.format(word))
