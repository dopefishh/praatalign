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
while len(data) < 4:
    data.append(None)
data = map(lambda x: x.strip().split('\t'), data[1:])
for i, (start, _, utt, end) in enumerate(data):
    if first == 0:
        first += 1
    elif first == 1:
        settings['HDR'] = 'False'
        code = 'a'
    if i > 0:
        start = max(float(start) - float(settings['THR']), float(data[i-1][3]))
    if i < len(data) - 1:
        end = min(float(end) + float(settings['THR']), float(data[i+1][0]))
    settings['STA'] = str(start)
    settings['DUR'] = str(float(end)-float(start))
    settings['UTT'] = utt
    force(phontiz, code=code, **settings)
