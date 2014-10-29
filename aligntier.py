#!/usr/bin/env python
# -*- coding: utf-8 -*-

from align import force
import codecs
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
    'HC': os.path.join('bin', 'HCopy'),
    'HV': os.path.join('bin', 'HVite'),
    'HDR': 'False'
    })

# Read the data
with codecs.open(settings['OUT'], 'r', 'utf-8') as f:
    data = f.readlines()

# Setup the code for writing and header settings
first = 0
code = 'w'
settings['HDR'] = 'True'

# Create dummy values if there are less then 4 values
while len(data) < 4:
    data.append(None)

# Parse the data
data = map(lambda x: x.strip().split('\t'), data[1:])

# Setup and align all data
for i, (start, _, utt, end) in enumerate(data):
    if first == 0:
        first += 1

# If neccesary unset the header and change write mode to append
    elif first == 1:
        settings['HDR'] = 'False'
        code = 'a'

# Check for empty pre and post annotations for extended bounds option
    if i > 0:
        start = max(float(start) - float(settings['THR']), float(data[i-1][3]))
    if i < len(data) - 1:
        end = min(float(end) + float(settings['THR']), float(data[i+1][0]))
# Parse the times
    settings['STA'] = str(start)
    settings['DUR'] = str(float(end)-float(start))
    settings['UTT'] = utt

# Do the actual alignment
    force(phone, code=code, **settings)
