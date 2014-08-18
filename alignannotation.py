#!/bin/env python
# -*- coding: utf-8 -*-

from align import force
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
    'DIC': './{}/DICT'.format(p),
    'HMM': './{}HMMINVENTAR'.format(p),
    'HVI': './{}HVITECONF'.format(p),
    'MMF': './{}MMF.mmf'.format(p),
    'PRE': './{}PRECONFIGNIST'.format(p),
    'HC': './bin/HCopy',
    'HV': './bin/HVite',
    'HDR': '1'
    })

force(phontiz, **settings)
