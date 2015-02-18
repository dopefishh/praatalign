#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import itertools
import os
import phonetizer as ph
import subprocess
import sys
import logging


HCOPY = '"{HCB}" -T 0 -C "{CWD}{SEP}{PRE}" temp.nis "{CWD}{SEP}{BN}.htk"'
HVITE = """"{HVB}" -C "{CWD}{SEP}{HVI}" -w -X slf -H "{CWD}{SEP}{MMF}" -s 7.0 \
-p 0.0 "{CWD}{SEP}{DIC}" "{CWD}{SEP}{HMM}" "{CWD}{SEP}{BN}.htk" """
SOUND = """"{SOX}" "{WAV}" -t sph -e signed-integer -b 16 -c 1 \
"{CWD}{SEP}temp.nis" trim {STA} {DUR} rate -s -a {SOU}"""


def force(*args, **kwargs):
    """Wrapper for the _force function that writes the status to a file for
    feedback via praat module.

    statusses can be:
        done     - Alignment was successfull.
        missox   - Sox binary not found.
        mishcopy - HCopy binary not found.
        mishvite - HVite binary not found.
    """
    status = _force(*args, **kwargs)
    with open(kwargs['BN'] + '.status', 'w') as f:
        f.write(status)
    return status == 'done'


def _force(phonetizer, code='w', **param):
    """
    Force aligns the given utterance, all parameters are passed by kwarg

    Necessary parameters
    BN  - basename, the name of the temp files.
    DIC - htk dict file path.
    DUR - duration in seconds.
    HCB - htk HCopy binary location.
    HVB - htk HVite binary location.
    HVI - htk hvite config.
    MMF - htk mmf file path.
    OUT - file to write the output to.
    PRE - htk preconfig.
    STA - start time in seconds.
    UTT - utterance.
    WAV - wave file path.
    LOG - log the detailed output to a file.
    SOX - sox executable path.

    Optional parameters
    HDR - also write the header to file.
    """
    logging.info('Starting to align')

    # Open the preconfig and extract the sourcerate
    with open(param['PRE'], 'r') as f:
        rate = int([a for a in f if 'SOURCERATE' in a][0].split(' ')[-1])
        param['SOU'] = 1e7/rate
    logging.info('Parameters parsed: {}'.format(param))

    # Load the phonetizer
    pron = phonetizer.phonetize(param['UTT']) or [[['<nib>']]]
    logging.info('Utterance phonetized spawned')

    # Create the graph file
    phonetizer.toslf(pron, param['BN'])
    logging.info('Graph created')

    # Extract the current directory to eliminate some PATH problems
    param['CWD'] = os.getcwd()
    param['SEP'] = os.sep

    # Run the sound processing
    proc = subprocess.Popen(SOUND.format(**param), shell=True,
                            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode == 127:
        return 'missox'
    logging.info('Sox ran({}):\n\tout: {}\n\terr: {}'.format(
        proc.returncode, out, err))

    # Run the HCopy process
    logging.info(HCOPY.format(**param))
    proc = subprocess.Popen(HCOPY.format(**param), shell=True,
                            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode == 127:
        return 'mishcopy'
    logging.info('HCopy ran({}):\n\tout: {}\n\terr: {}'.format(
        proc.returncode, out, err))

    # Run the HVite actual alignment
    logging.info(HVITE.format(**param))
    proc = subprocess.Popen(HVITE.format(**param), shell=True,
                            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode == 127:
        return 'mishvite'
    logging.info('HVite ran({}):\n\tout: {}\n\terr: {}'.format(
        proc.returncode, out, err))

    # Open the output file
    out = param['OUT']
    fileio = sys.stdout if out == '-' else open(out, code)
    logging.info('Output file selected')
    with open(param['BN'] + '.rec', 'r') as f:
        # Write if necessary the header
        if param['HDR'] != 'False':
            fileio.write('start,end,label,type\n')
            logging.info('Header written')
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
        logging.info('Datafile written')
    # Close the file again
    if out != '-':
        fileio.close()
    logging.info('Finished')
    return 'done'


def parsesettings(filepath):
    with open(filepath, 'r') as f:
        settings = {k: v.strip() for k, v in (x.split(': ') for x in f)}
    return settings

if __name__ == '__main__':
    # Load the settings
    settings = parsesettings('isettings')
    settings.update(parsesettings('settings'))

    # Initialize the logger
    logging.basicConfig(filename=settings['LOG'], level=20,
                        format='%(created)f: %(message)s')

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
        'HDR': 'True'
        })

    if sys.argv[1] == 'tier':
        # Read the data
        with codecs.open(settings['OUT'], 'r', 'utf-8') as f:
            data = f.readlines()

        # Setup the code for writing and header settings
        first = 0
        code = 'w'
        settings['HDR'] = 'True'

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
                start = max(float(start)-float(settings['THR']),
                            float(data[i-1][3]))
            if i < len(data) - 1:
                end = min(float(end) + float(settings['THR']),
                          float(data[i+1][0]))
        # Parse the times
            settings['STA'] = str(start)
            settings['DUR'] = str(float(end)-float(start))
            settings['UTT'] = utt

        # Do the actual alignment
            if not force(phone, code=code, **settings):
                break
    elif sys.argv[1] == 'annotation':
        force(phone, **settings)
