#!/bin/env python
# -*- coding: utf-8 -*-

from align import force
import phonetizer as ph

# Load the settings
with open('isettings', 'r') as f:
    settings = {k: v.strip() for k, v in map(lambda x: x.split(': '), f)}
with open('settings', 'r') as f:
    settings.update({k: v.strip() for k, v in map(lambda x: x.split(': '), f)})

# Load the phonetizer
phone = ph.getphonetizer(settings['LAN'], settings['DCT'], settings['RUL'])
p = phone[1]
phone = phone[0]

# Update the settings
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

# Do the actual alignment
force(phone, **settings)
