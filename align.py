#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import itertools


def force(phonetizer, code='w', **param):
    """
    Force aligns the given utterance, all parameters are passed by kwarg

    Necessary parameters
    BN  - basename, the name of the temp files
    DIC - htk dict file path
    DUR - duration in seconds
    HC  - htk HCopy binary location
    HV  - htk HVite binary location
    HVI - htk hvite config
    MMF - htk mmf file path
    OUT - file to write the output to
    PDF - {True, False}, the option to leave a pdf file on site with the graph
    PRE - htk preconfig
    STA - start time in seconds
    UTT - utterance
    WAV - wave file path

    Optional parameters
    HDR - also write the header to file
    """
    with open(param['PRE'], 'r') as f:
        rate = int([a for a in f if 'SOURCERATE' in a][0].split(' ')[-1])
        param['SOU'] = 1e7/rate
    pron = phonetizer.phonetize(param['UTT']) or [[['<nib>']]]
    phonetizer.toslf(pron, param['BN'], param['PDF'] == 'True')
    param['CWD'] = os.getcwd()
    subprocess.call(('sox {WAV} -t sph -e signed-integer -b 16 -c 1 {CWD}/temp'
                     '.nis trim {STA} {DUR} rate -s -a {SOU}').format(**param),
                    shell=True)
    subprocess.call('{CWD}/{HC} -T 0 -C {CWD}/{PRE} temp.nis {CWD}/{BN}.htk'.
                    format(**param), shell=True)
    subprocess.call(('{CWD}/{HV} -C {CWD}/{HVI} -w -X slf -H {CWD}/{MMF} -s 7.'
                     '0 -p 0.0 {CWD}/{DIC} {CWD}/{HMM} {CWD}/{BN}.htk').
                    format(**param), shell=True)
    out = param['OUT']
    fileio = sys.stdout if out == "-" else open(out, code)
    with open(param['BN'] + '.rec', 'r') as f:
        if param['HDR'] != 'False':
            fileio.write('start,end,label,type\n')
        for d in itertools.imap(lambda x: x.split(), f):
            start = float(param['STA']) + int(d[0]) / 1e7
            end = float(param['STA']) + int(d[1]) / 1e7
            if d[2] == '<':
                word = (end, '')
            elif d[2] == '#':
                fileio.write('%f,%f,%s,w\n' % (word[0], start, word[1]))
                word = (end, '')
            else:
                word = (word[0], word[1] + d[2])
            if end - start > 0:
                fileio.write('%f,%f,%s,p\n' % (start, end, d[2]))
    if out != "-":
        fileio.close()
