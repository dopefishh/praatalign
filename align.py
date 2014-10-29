#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import os
import subprocess
import sys
import time
import datetime

HCOPY = ('"{CWD}{SEP}{HC}" -T 0 '
         '-C "{CWD}{SEP}{PRE}" temp.nis "{CWD}{SEP}{BN}.htk" || true')
HVITE = ('"{CWD}{SEP}{HV}" '
         '-C "{CWD}{SEP}{HVI}" -w -X slf '
         '-H "{CWD}{SEP}{MMF}" '
         '-s 7.0 -p 0.0 '
         '"{CWD}{SEP}{DIC}" "{CWD}{SEP}{HMM}" "{CWD}{SEP}{BN}.htk" || true')
SOUND = ('"{SOX}" "{WAV}" '
         '-t sph -e signed-integer -b 16 -c 1 '
         '"{CWD}{SEP}temp.nis" trim {STA} {DUR} rate -s -a {SOU} || true')


def current_millis():
    c = datetime.datetime.now()
    return (c.hour*3600 + c.minute*60 + c.second) * 1000 + c.microsecond/1000


def force(phonetizer, code='w', **param):
    """
    Force aligns the given utterance, all parameters are passed by kwarg

    Necessary parameters
    BN  - basename, the name of the temp files.
    DIC - htk dict file path.
    DUR - duration in seconds.
    HC  - htk HCopy binary location.
    HV  - htk HVite binary location.
    HVI - htk hvite config.
    MMF - htk mmf file path.
    OUT - file to write the output to.
    PDF - {True, False}, the option to leave a pdf file on site with the graph.
    PRE - htk preconfig.
    STA - start time in seconds.
    UTT - utterance.
    WAV - wave file path.
    LOG - log the detailed output to a file.
    LGC - log code, a for append, w for write.
    SOX - sox executable path.

    Optional parameters
    HDR - also write the header to file.
    """
    # Open the log file
    with open(param['LOG'], param['LGC']) as lg:
        ltime = current_millis()
        lg.write('Starting to align: {}\n'.format(
            time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())))

        # Open the preconfig and extract the sourcerate
        with open(param['PRE'], 'r') as f:
            rate = int([a for a in f if 'SOURCERATE' in a][0].split(' ')[-1])
            param['SOU'] = 1e7/rate
        ctime = current_millis()
        lg.write('({})Parameters parsed: {}\n'.format(ctime-ltime, param))
        ltime = ctime

        # Load the phonetizer
        pron = phonetizer.phonetize(param['UTT']) or [[['<nib>']]]
        ctime = current_millis()
        lg.write('({})Utterance phonetized spawned\n'.format(ctime-ltime))
        ltime = ctime

        # Create the graph file
        phonetizer.toslf(pron, param['BN'])
        ctime = current_millis()
        lg.write('({})Graph created\n'.format(ctime-ltime))
        ltime = ctime

        # Extract the current directory to eliminate some PATH problems
        param['CWD'] = os.getcwd()
        param['SEP'] = os.sep

        # Run the sound processing
        proc = subprocess.Popen(SOUND.format(**param), shell=True,
                                env={'PATH': os.environ['PATH']},
                                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        ctime = current_millis()
        lg.write('({})Sox ran:\n\tout: {}\n\terr: {}\n'.format(
            ctime-ltime, out, err))
        ltime = ctime

        # Run the HCopy process
        proc = subprocess.Popen(HCOPY.format(**param), shell=True,
                                env={'PATH': os.environ['PATH']},
                                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        ctime = current_millis()
        lg.write('({})HCopy ran:\n\tout: {}\n\terr: {}\n'.format(
            ctime-ltime, out, err))
        ltime = ctime

        # Run the HVite actual alignment
        proc = subprocess.Popen(HVITE.format(**param), shell=True,
                                env={'PATH': os.environ['PATH']},
                                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        ctime = current_millis()
        lg.write('({})HVite ran:\n\tout: {}\n\terr: {}\n'.format(
            ctime-ltime, out, err))
        ltime = ctime

        # Open the output file
        out = param['OUT']
        fileio = sys.stdout if out == '-' else open(out, code)
        lg.write('Output file selected\n')
        with open(param['BN'] + '.rec', 'r') as f:
            # Write if necessary the header
            if param['HDR'] != 'False':
                fileio.write('start,end,label,type\n')
                lg.write('Header written\n')
            for d in itertools.imap(lambda x: x.split(), f):
                # Parse the time parameters and convert them to seconds
                start = float(param['STA']) + int(d[0]) / 1e7
                end = float(param['STA']) + int(d[1]) / 1e7

                # Detect word boundaries
                if d[2] == '<':
                    word = (end, '')
                # If the end of a word is reached write the word to file
                elif d[2] == '#':
                    fileio.write('{:f},{:f},{},w\n'.format(
                        word[0], start, word[1]))
                    word = (end, '')
                # Else add the current phone to the current word
                else:
                    word = (word[0], word[1] + d[2])
                # If the length is non zero write the phone to the file
                if end - start > 0:
                    fileio.write('{:f},{:f},{},p\n'.format(
                        start, end, d[2]))
            lg.write('Datafile written\n')
        # Close the file again
        if out != '-':
            fileio.close()
        ctime = current_millis()
        lg.write('({})Finished'.format(ctime-ltime))
