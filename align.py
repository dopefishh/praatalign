#!/usr/bin/env python
# -*- coding: utf-8 -*-

import phonetizer
import subprocess
import sys

def force(phonetizer, **param):
    with open(param['PRE'], 'r') as f:
        rate = int([a for a in f if 'SOURCERATE' in a][0].split(' ')[-1])
        param['SOU'] = 1e7/rate
    pron = phonetizer.phonetize(param['UTT']) or [[['<nib>']]]
    phonetizer.toslf(pron, param['BN'], param['PDF']=='True')
    snd = (
        'sox %(WAV)s -t sph -e signed-integer -b 16 -c 1 temp.nis ' +
        'trim %(STA)s %(DUR)s rate -s -a %(SOU)d && ' +
        '%(HC)s -T 0 -C %(PRE)s temp.nis %(BN)s.htk && ' +
        '%(HV)s -C %(HVI)s -w -X slf -H %(MMF)s -s 7.0 -p 0.0 ' +
        '%(DIC)s %(HMM)s %(BN)s.htk | grep -v \'WARNING\''
        ) % param

    subprocess.call(snd, shell=True, executable='/bin/bash')

    # Convert the rec file
    out = param['OUT']
    fileio = sys.stdout if out == "-" else open(out, 'w')
    with open(param['BN'] + '.rec', 'r') as f:
        if param['HDR']:
            fileio.write('start,end,label\n')
        for line in f:
            d = line.split()
            start = float(param['STA']) + int(d[0]) / 1e7
            end = float(param['STA']) + int(d[1]) / 1e7
            if end - start > 0:
                fileio.write('%f,%f,%s\n' % (start, end, d[2]))
    if out != "-":
        fileio.close()
