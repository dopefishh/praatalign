#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import itertools
import logging
import os
import phonetizer as ph
import subprocess
import sys


def force(phonetizer, utterance, starttime, endtime, wavefile,
          soxbinary, hvitebinary, hcopybinary, parameterdir,
          basename, hdr=True, code='w'):
    """Wrapper for the _force function that writes the status to a file for
    feedback via praat module.

    statusses can be:
        done     - Alignment was successfull.
        missox   - Sox binary not found.
        mishcopy - HCopy binary not found.
        mishvite - HVite binary not found.
    """
    status = _force(
        phonetizer, utterance, starttime, endtime, wavefile,
        soxbinary, hvitebinary, hcopybinary, parameterdir,
        basename, hdr, code)
    with open('{}.status'.format(basename), 'w') as f:
        f.write(status)
    return not status


def _force(phonetizer, utterance, starttime, duration, wavefile,
           soxbinary, hvitebinary, hcopybinary, parameterdir,
           basename, hdr, code):
    """
    Force aligns the given utterance, all parameters are passed by kwarg
    """
    logging.info('Starting to align: {}'.format(code))
    logging.info('Removing old files')
    for suffix in ['dot', 'htk', 'nis', 'rec', 'slf', 'status']:
        try:
            os.remove('{}.{}'.format(basename, suffix))
        except:
            pass

    # Open the preconfig and extract the sourcerate
    sourcerate = str(1e7/625)

    # Load the phonetizer
    pron = phonetizer.phonetize(utterance) or [[['<nib>']]]

    canonical = [''.join(p[0]) for p in pron]
    logging.info('Utterance phonetized spawned')

    # Create the graph file
    dawg = phonetizer.todawg(pron)
    with open('{}.slf'.format(basename), 'w') as f:
        f.write(phonetizer.toslf(*dawg))
    with open('{}.dot'.format(basename), 'w') as f:
        f.write(phonetizer.todot(*dawg))
    logging.info('SLF file created')

    # Run the sound processing
    soxcommand = [
        soxbinary, wavefile,
        '-t', 'sph',
        '-e', 'signed-integer',
        '-b', '16', '-c', '1',
        '{}.nis'.format(basename),
        'trim', starttime, duration,
        'rate', '-s', '-a', sourcerate]
    logging.info(' '.join(soxcommand))
    proc = subprocess.Popen(soxcommand,
                            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode == 127:
        return 'Sox binary couldn\'t be found...\n'\
            'It is searched for in {}'.format(hcopybinary)
    logging.info('Sox ran({}):\n\tout: {}\n\terr: {}'.format(
        proc.returncode, out, err))

    # Run the HCopy process
    hcopycommand = [
        hcopybinary,
        '-T', '0',
        '-C', os.path.join(parameterdir, 'PRECONFIGNIST'),
        '{}.nis'.format(basename), '{}.htk'.format(basename)]

    logging.info(' '.join(hcopycommand))
    proc = subprocess.Popen(hcopycommand,
                            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode == 127:
        return 'HCopy binary couldn\'t be found...\n'\
            'It is searched for in {}'.format(hcopybinary)
    logging.info('HCopy ran({}):\n\tout: {}\n\terr: {}'.format(
        proc.returncode, out, err))

    # Run the HVite actual alignment
    hvitecommand = [
        hvitebinary,
        '-C', os.path.join(parameterdir, 'HVITECONF'),
        '-w', '-X', 'slf',
        '-H', os.path.join(parameterdir, 'MMF'),
        '-s', '7.0',
        '-p', '6.0',
        os.path.join(parameterdir, 'DICT'),
        os.path.join(parameterdir, 'MONOPHONES'),
        '{}.htk'.format(basename)]
    logging.info(' '.join(hvitecommand))
    proc = subprocess.Popen(hvitecommand,
                            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode == 127:
        return 'HVite binary couldn\'t be found...\n'\
            'It is searched for in {}'.format(hvitebinary)
    logging.info('HVite ran({}):\n\tout: {}\n\terr: {}'.format(
        proc.returncode, out, err))
    if proc.returncode != 0:
        return 'HVite failed with the following error: {}'.format(err)

    # Open the output file
    out = 'praat_temp_out'
    ortwords = utterance.replace(",", "").split(' ')
    with open(out, code) as fileio:
        logging.info('Output file selected')
        with open('{}.rec'.format(basename), 'r') as f:
            # Write if necessary the header
            if hdr != 'False':
                fileio.write('start,end,label,type\n')
                logging.info('Header written')
            word = None
            for d in itertools.imap(lambda x: x.split(), f):
                # Parse the time parameters and convert them to seconds
                start = float(starttime) + int(d[0]) / 1e7
                end = float(starttime) + int(d[1]) / 1e7

                # Detect word boundaries
                if d[2] == '<':
                    word = (end, '')
                # If the end of a word is reached write the word to file
                elif d[2] == '#':
                    fileio.write('{:f},{:f},{},w\n'.format(
                        word[0], start, word[1]))
                    fileio.write('{:f},{:f},{},c\n'.format(
                        word[0], start, canonical.pop(0)))
                    fileio.write('{:f},{:f},{},o\n'.format(
                        word[0], start, ortwords.pop(0).encode('utf-8')))
                    word = (end, '')
                # Else add the current phone to the current word
                else:
                    word = (word[0], word[1] + d[2])
                # If the length is non zero write the phone to the file
                if end - start > 0:
                    fileio.write('{:f},{:f},{},p\n'.format(
                        start, end, d[2]))
                    fileio.write('{:f},{:f},{},l\n'.format(
                        start, end, float(d[3])))
            logging.info('Datafile written')
    logging.info('Finished')
    return ''


def parsesettings(filepath):
    with open(filepath, 'r') as f:
        settings = {k: v.strip() for k, v in (x.split(': ') for x in f)}
    return settings


if __name__ == '__main__':
    # Load the sett
    sett = parsesettings('isettings')
    sett.update(parsesettings('settings'))

    # Initialize the logger
    logging.basicConfig(filename=sett['LOG'], level=20,
                        format='%(created)f: %(message)s')

    # Load the phonetizer
    try:
        phone = ph.getphonetizer(
            sett['LAN'], sett['PHO'], sett['DCT'], sett['RUL'])
    except UnicodeError:
        with open('temp.status', 'w') as f:
            f.write('Unicode error. Check if the files are utf-8')
        exit()
    except IOError as e:
        if e.filename == sett['DCT']:
            error = 'Dictionary file couldn\'t be found\n'\
                'It is searched for in {}'.format(e.filename)
        elif e.filename == sett['RUL']:
            error = 'Ruleset file couldn\'t be found\n'\
                'It is searched for in {}'.format(e.filename)
        elif e.filename == sett['PHO']:
            error = 'Universal phonetizer file couldn\'t be found\n'\
                'It is searched for in {}'.format(e.filename)
        else:
            error = 'Some io error: ' + str(e)
        with open('temp.status', 'w') as f:
            f.write(error)
        exit()

    p = 'par.{}'.format(sett['MOD'])

    if sys.argv[1] == 'tier':
        # Read the data
        with codecs.open(sett['OUT'], 'r', 'utf-8') as f:
            data = f.readlines()

        # Setup the code for writing and header sett
        first = 0
        code = 'w'
        hdr = 'True'

        # Parse the data
        data = map(lambda x: x.strip().split('\t'), data[1:])

        # Setup and align all data
        for i, (start, _, utt, end) in enumerate(data):
            if first == 0:
                first += 1

        # If neccesary unset the header and change write mode to append
            elif first == 1:
                hdr = 'False'
                code = 'a'

        # Check for empty pre and post annotations for extended bounds option
            if i > 0:
                start = max(float(start)-float(sett['THR']),
                            float(data[i-1][3]))
            if i < len(data) - 1:
                end = min(float(end) + float(sett['THR']),
                          float(data[i+1][0]))

            dur = str(float(end)-float(start))
        # Do the actual alignment
            if not force(
                    phone, utt, str(start), dur, sett['WAV'],
                    sett['SOX'], sett['HVB'], sett['HCB'], p, 'temp',
                    hdr=hdr, code=code):
                break
    elif sys.argv[1] == 'annotation':
        force(phone, sett['UTT'], sett['STA'], sett['DUR'], sett['WAV'],
              sett['SOX'], sett['HVB'], sett['HCB'], p, 'temp')
