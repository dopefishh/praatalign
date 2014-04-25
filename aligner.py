#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import phonetizer
import re
import subprocess
import sys


def forcealigntier(txtpath, wav, lang, ruleset, pdir, dictpath=None,
                   sendpraat=None):
    dictpath = dictpath if dictpath != "None" else None
    phontiz = phonetizer.getphonetizer(lang, dictpath, ruleset)
    p = phontiz[1]
    phontiz = phontiz[0]

    param = {
        'BN': 'temp',
        'DICT': pdir + p + 'DICT',
        'HMM': pdir + p + 'HMMINVENTAR',
        'HVITECONF': pdir + p + 'HVITECONF',
        'MMF': pdir + p + 'MMF.mmf',
        'PRECONFIG': pdir + p + 'PRECONFIGNIST',
        'WAV': wav,
        'HC': pdir + 'bin/HCopy',
        'HV': pdir + 'bin/HVite'
        }
    f = codecs.open(txtpath, 'r', 'utf-8')
    f.readline()
    sys.stdout.write('start,end,label\n')
    for line in f:
        start, utt, end = line.split('\t')
        param['START'] = float(start)
        param['DUR'] = float(end) - param['START']
        force(utt, wav, phontiz, param, "-", header=False)
        if sendpraat is not None:
            subprocess.call('%s 0 praat "printline %s"' % (sendpraat,
                            param['START']), shell=True)
    f.close()
    subprocess.call('%s 0 praat "printline done"', shell=True)


def force(utt, wav, phonetizer, param, out="-", header=True, pdf=False, log="/tmp/fa_log.txt"):
    logfile = open(log, 'a')
    logfile.write('started a new log\n')
    with open(param['PRECONFIG'], 'r') as f:
        rate = int([a for a in f if 'SOURCERATE' in a][0].split(' ')[-1])
        param['SOURCERATE'] = 1e7/rate
    logfile.write('sourcerate parsed\n')
    pron = phonetizer.phonetize(utt) or [[['<nib>']]]
    logfile.write('phonetizer initialized\n')
    phonetizer.toslf(pron, param['BN'], pdf)
    logfile.write('slf created\n')
    snd = (
        'sox %(WAV)s -t sph -e signed-integer -b 16 -c 1 temp.nis ' +
        'trim %(START)f %(DUR)s rate -s -a %(SOURCERATE)d && ' +
        '%(HC)s -T 0 -C %(PRECONFIG)s temp.nis %(BN)s.htk && ' +
        '%(HV)s -C %(HVITECONF)s -w -X slf -H %(MMF)s -s 7.0 -p 0.0 ' +
        '%(DICT)s %(HMM)s %(BN)s.htk | grep -v \'WARNING\''
        ) % param
    logfile.write('command created\n%s\n' % snd)

    subprocess.call(snd, shell=True, executable='/bin/bash')
    logfile.write('subprocess done\n')

    # Convert the rec file
    fileio = sys.stdout if out == "-" else open(out, 'w')
    with open(param['BN'] + '.rec', 'r') as f:
        if header:
            fileio.write('start,end,label\n')
        for line in f:
            d = line.split()
            start = param['START'] + int(d[0]) / 1e7
            end = param['START'] + int(d[1]) / 1e7
            if end - start > 0:
                fileio.write('%f,%f,%s\n' % (start, end, d[2]))
    if out != "-":
        fileio.close()
    logfile.write('recfile created\n')
    logfile.close()


def forcealignutterance(pronun, starttime, endtime, wav, lang, ruleset=None,
                        pdf=True, out="-", pdir='./', dictpath=None):
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
    phontiz = phonetizer.getphonetizer(lang)
    p = phontiz[1]
    phontiz = phontiz[0]
    starttime, endtime = map(float, (starttime, endtime))
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
    force(pronun, wav, phontiz, param, out, True, pdf == "True")


def usage():
    print 'usage:\n\tpython aligner.py pronunciation starttime endtime wav',\
          'lang{spa, tze} [pdf{True, False}] [output]'
    print 'example:\n\tpython aligner.py "Hello World!" 0.0 5.0 hello.wav',\
          'True -'
    print '\nor in tier mode'
    print 'usage:'
    print '\tpython aligner.py tier txtpath wav lang dictpath ruleset pdir'


if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        usage()
    if sys.argv[1] != 'tier':
        forcealignutterance(*sys.argv[1:])
    else:
        forcealigntier(*sys.argv[2:])
