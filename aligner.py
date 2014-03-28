#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import phonetizer
import re
import subprocess
import sys


def forcealignutterance(pronun, starttime, endtime, wav, phontiz):
    """Force align an utterance

    pronun    -- canonical pronunciation
    starttime -- start time
    endtime   -- end time
    wav       -- wave file
    phontiz   -- phonetizer to use
    """
    param = {'PRECONFIG': './p/PRECONFIGNIST', 'HVITECONF': './p/HVITECONF',
             'MMF': './p/MMF.mmf', 'DICT': './p/DICT', 'BN': 'temp',
             'HMMINVENTAR': './p/HMMINVENTAR'}
    with open(param['PRECONFIG'], 'r') as f:
        rate = int([a for a in f if 'SOURCERATE' in a][0].split(' ')[-1])
        param['SOURCERATE'] = 1e7/rate
    phontiz.tomlfslf(phontiz.phonetize(pronun), param['BN'])

    # Cut out the bit we need from the total wavefile
    subprocess.call('sox -G %s %s.wav trim %f %f 2>&1 1>/dev/null' % (wav,
                    param['BN'], starttime, endtime-starttime), shell=True)
    # Convert to nis and resample
    subprocess.call(
        'sox %(BN)s.wav -t sph -e signed-integer -b 16 -c 1 %(BN)s.nis' %
        param, shell=True
        )
    subprocess.call(
        'sox %(BN)s.nis -t sph %(BN)s.re.nis rate -s -a %(SOURCERATE)d' %
        param, shell=True
        )
    # Create HTK file
    subprocess.call(
        './HCopy -T 0 -C %(PRECONFIG)s %(BN)s.re.nis %(BN)s.htk' %
        param, shell=True
        )
    # Force align the file
    subprocess.call(
        ('./HVite -C %(HVITECONF)s -w -X slf -H %(MMF)s -s 7.0 -p 0.0 ' +
         '%(DICT)s %(HMMINVENTAR)s %(BN)s.htk | grep -v \'WARNING\'') %
        param, shell=True
        )
    # Convert the rec file
    with open(param['BN']+'.rec', 'r') as f:
        data = [d.split(' ') for d in f]
    # Parse the alignments and print them
    data = [(int(d[0])/1e7, int(d[1])/1e7, d[2], d[3]) for d in data]
    for ann in data:
        print ann[0]+starttime[0], ann[1]+starttime, pronun


def usage():
    print 'usage: python aligner.py pronunciation starttime endtime wav',\
          'lang{spa, tze}'
    print 'example: python aligner.py "Hello World!" 0.0 5.0 hello.wav spa'


if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        usage()
    try:
        forcealignutterance(*sys.argv[1:])
    except TypeError:
        usage()
