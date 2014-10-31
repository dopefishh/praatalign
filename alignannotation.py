#!/bin/env python
# -*- coding: utf-8 -*-

from align import force
import os
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
    'DIC': os.path.join(p, 'DICT'),
    'HMM': os.path.join(p, 'HMMINVENTAR'),
    'HVI': os.path.join(p, 'HVITECONF'),
    'MMF': os.path.join(p, 'MMF.mmf'),
    'PRE': os.path.join(p, 'PRECONFIGNIST'),
    'HDR': '1'
    })

# Do the actual alignment
force(phone, **settings)
