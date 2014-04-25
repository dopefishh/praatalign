#!/bin/env python
# -*- coding: utf-8 -*-

from align import force
import phonetizer

with open('isettings', 'r') as f:
    settings = {k: v.strip() for k, v in map(lambda x: x.split(': '), f)}
with open('settings', 'r') as f:
    settings.update({k: v.strip() for k, v in map(lambda x: x.split(': '), f)})

phontiz = phonetizer.getphonetizer(settings['LAN'],
                                   settings['DCT'],
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
    'HDR': '1'
    })

force(phontiz, **settings)
