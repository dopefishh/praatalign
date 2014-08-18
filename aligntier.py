#!/usr/bin/env python
# -*- coding: utf-8 -*-

from align import force
import codecs
import phonetizer

with open('isettings', 'r') as f:
    settings = {k: v.strip() for k, v in map(lambda x: x.split(': '), f)}
with open('settings', 'r') as f:
    settings.update({k: v.strip() for k, v in map(lambda x: x.split(': '), f)})

phontiz = phonetizer.getphonetizer(settings['LAN'], settings['DCT'])
p = phontiz[1]
phontiz = phontiz[0]
settings.update({
    'BN': 'temp',
    'DIC': './{}DICT'.format(p),
    'HMM': './{}HMMINVENTAR'.format(p),
    'HVI': './{}HVITECONF'.format(p),
    'MMF': './{}MMF.mmf'.format(p),
    'PRE': './{}PRECONFIGNIST'.format(p),
    'HC': './bin/HCopy',
    'HV': './bin/HVite',
    'HDR': 'False'
    })

with codecs.open(settings['OUT'], 'r', 'utf-8') as f:
    data = f.readlines()

first = 0

code = 'w'
settings['HDR'] = 'True'
for line in data[1:]:
    if first == 0:
        first += 1
    elif first == 1:
        settings['HDR'] = 'False'
        code = 'a'
    start, _, utt, end = line.strip().split('\t')
    settings['STA'] = start
    settings['DUR'] = str(float(end)-float(start))
    settings['UTT'] = utt
    force(phontiz, code=code, **settings)
