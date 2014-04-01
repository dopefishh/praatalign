#!/usr/bin/env python
# -*- coding: utf-8 -*-

import phonetizer
import re
import subprocess
import sys


def forcealignutterance(pronun, starttime, endtime, wav, phontiz, ruleset,
                        pdf=True, out="-", pdir='./'):
    """Force align an utterance

    pronun    -- canonical pronunciation
    starttime -- start time
    endtime   -- end time
    wav       -- wave file
    phontiz   -- phonetizer to use
    ruleset   -- ruleset or rulesetfile to parse
    pdf       -- flag to make a pdf of the network
    out       -- output file, - for stdout
    pdir      -- prefix for the parameter files(default ./)
    """
    phonetizerdict = {
        'spa': (phonetizer.PhonetizerSpanish, 'p.spa/'),
        'tze': (phonetizer.PhonetizerTzeltal, 'p.sam/')
        }
    entry = phonetizerdict[phontiz]
    phontiz = entry[0](ruleset=ruleset)
    p = entry[1]
    starttime, endtime = map(float, (starttime, endtime))
    starttime, endtime = float(starttime), float(endtime)

    param = {
        'BN': 'temp',
        'DICT': pdir + p + 'DICT',
        'DUR': endtime-starttime,
        'HMM': pdir + p + 'HMMINVENTAR',
        'HVITECONF': pdir + p + 'HVITECONF',
        'MMF': pdir + p + 'MMF.mmf',
        'PRECONFIG': pdir + p + 'PRECONFIGNIST',
        'START': starttime,
        'WAV': wav,
        'HC': pdir + 'bin/HCopy',
        'HV': pdir + 'bin/HVite'
        }
    with open(param['PRECONFIG'], 'r') as f:
        rate = int([a for a in f if 'SOURCERATE' in a][0].split(' ')[-1])
        param['SOURCERATE'] = 1e7/rate
    pron = phontiz.phonetize(pronun)
    phontiz.tomlfslf(pron, param['BN'], pdf == "True")

    # Cut out the bit we need from the total wavefile
    snd = (
        'sox %(WAV)s -t sph -e signed-integer -b 16 -c 1 temp.nis ' +
        'trim %(START)f %(DUR)s rate -s -a %(SOURCERATE)d && ' +
        '%(HC)s -T 0 -C %(PRECONFIG)s temp.nis %(BN)s.htk && ' +
        '%(HV)s -C %(HVITECONF)s -w -X slf -H %(MMF)s -s 7.0 -p 0.0 ' +
        '%(DICT)s %(HMM)s %(BN)s.htk | grep -v \'WARNING\''
        ) % param

    subprocess.call(snd, shell=True, executable='/bin/bash')

    # Convert the rec file
    fileio = sys.stdout if out == "-" else open(out, 'w')
    with open(param['BN'] + '.rec', 'r') as f:
        fileio.write('start,end,label\n')
        for line in f:
            d = line.split()
            start = starttime + int(d[0]) / 1e7
            end = starttime + int(d[1]) / 1e7
            if end - start > 0:
                fileio.write('%f,%f,%s\n' % (start, end, d[2]))
    if out != "-":
        fileio.close()


def usage():
    print 'usage:\n\tpython aligner.py pronunciation starttime endtime wav',\
          'lang{spa, tze} [pdf{True, False}] [output]'
    print 'example:\n\tpython aligner.py "Hello World!" 0.0 5.0 hello.wav',\
          'True -'


if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        usage()
    forcealignutterance(*sys.argv[1:])
