#!/usr/bin/env python
# -*- coding: utf-8 -*-

from align import force
import codecs
import phonetizer
import sys
import os

with open('isettings', 'r') as f:
    settings = {k: v.strip() for k, v in map(lambda x: x.split(': '), f)}
with open('settings', 'r') as f:
    settings.update({k: v.strip() for k, v in map(lambda x: x.split(': '), f)})

phontiz = phonetizer.getphonetizer(settings['LAN'], settings['DCT'],
                                   settings['RUL'])
p = phontiz[1]
phontiz = phontiz[0]
settings.update({
    'BN': 'temp',
    'DIC': './%s/DICT' % p,
    'HMM': './%sHMMINVENTAR' % p,
    'HVI': './%sHVITECONF' % p,
    'MMF': './%s/MMF.mmf' % p,
    'PRE': './%sPRECONFIGNIST' % p,
    'HC': './bin/HCopy',
    'HV': './bin/HVite',
    'HDR': 'False'
    })

with codecs.open(settings['OUT'], 'r', 'utf-8') as f:
    data = f.readlines()

#os.remove(settings['OUT'])
first = 0

for line in data[1:]:
    if first == 0:
        settings['HDR'] = 'True'
        first += 1
    elif first == 1:
        settings['HDR'] = 'False'
    start, _, utt, end = line.strip().split('\t')
    settings['STA'] = start
    settings['DUR'] = str(float(end)-float(start))
    settings['UTT'] = utt
    force(phontiz, code='a', **settings)
