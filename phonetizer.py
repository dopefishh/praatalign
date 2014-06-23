# -*- coding: utf-8 -*-

import codecs
import re
import unicodedata
import os


class tdict(dict):
    """Dictionary with a missing value that is the normalized version
    of the input
    """
    def __missing__(self, key):
        char = unicodedata.normalize('NFKD', unicode(key))
        return str(char.encode('ascii', 'ignore')).lower()


class Phonetizer:
    """Skeleton class for a phonetizer for the praat align program"""

    def __init__(self, dictpath=None, ruleset=None):
        """Constructor with an optional dictionary

        filters  -- A regular expression of things to filter out of the
                    utterances
        dictpath -- Path to an optional dictonary
        ruleset  -- Path to an optional ruleset file
        """
        self.parseruleset(ruleset)
        self.dictionary = dict()
        if dictpath is not None:
            with codecs.open(dictpath, 'r', 'utf-8') as f:
                for l in f:
                    if l and l[0] != '#':
                        l = [s.strip() for s in l.split('\t')]
                        self.dictionary[l[0]] = [var.split() for var in
                                                 map(str, l[1:])]

    def parseruleset(self, path):
        """Parses the ruleset from a file

        path -- The path of the ruleset file, if None then there will be an
                empty ruleset
        """
        self.r = list()
        if path is not None:
            reps = [(r'\v', '[aoeiu]'), (r'\c', '[^aoeui]'), ('\n', '')]
            with open(path, 'r') as f:
                lines = [re.compile(reduce(lambda x, (o, n): x.replace(o, n),
                         reps, l)) for l in f if l and l[0] != '"']
                self.r += lines

    def toslf(self, pron, bn, graphviz=False):
        """Generates a mlf file and slf file regarding the ruleset

        pron     -- pronunciation in the form of [word1, word2, ..., wordn]
                        where wordi = [var1, var2, ..., varn]
                        where vari  = [char1, char2, ..., charn]
        bn       -- filename without extension for the output files
        graphviz -- Flag to make a pdf of the final graph
        """
        nit, eit = 0, 0
        nodebase = 'I=%d W=%s\n'
        edgebase = 'J=%d S=%d E=%d\n'
        wordb = 0
        nodestr = nodebase % (0, '<')
        nit += 1
        edgestr = ''
        for word in pron:
            toadd = []
            for var in word:
                edgestr += edgebase % (eit, wordb, nit)
                eit += 1
                for num, char in enumerate(var):
                    if num > 0:
                        edgestr += edgebase % (eit, nit-1, nit)
                        eit += 1
                    nodestr += nodebase % (nit, char)
                    nit += 1
                toadd.append(nit-1)
            nodestr += nodebase % (nit, '#')
            wordb = nit
            nit += 1
            for to in toadd:
                edgestr += edgebase % (eit, to, wordb)
                eit += 1
        nodestr += nodebase % (nit, '>')
        edgestr += edgebase % (eit, nit-1, nit)
        slfstr = 'N=%d L=%d\n%s%s' % (nit+1, eit+1, nodestr, edgestr)
        with open('%s.slf' % bn, 'w') as ff:
            ff.writelines(slfstr)
        if graphviz:
            with open('%s.dot' % bn, 'w') as ff:
                ff.write('digraph g{\n')
                for li in filter(None,
                                 [l.split() for l in slfstr.split('\n')]):
                    if li[0][0] == 'I':
                        ff.write('\t%s [label="%s"]\n'
                                 % (li[0][2:], li[1][2:]))
                    if li[0][0] == 'J':
                        ff.write('\t%s -> %s\n' % (li[1][2:], li[2][2:]))
                ff.write('}')
            os.system('dot -Tpdf %s.dot -o %s.pdf' % (bn, bn))

    def applyrules(self, phon):
        """Apply the rules specified in the ruleset

        phon - phonetization of the utterance
        """
        if phon is not None and len(phon) == 1:
            word = ''.join(phon[0])
            for rule in self.r:
                mo = rule.search(word)
                if mo is not None:
                    wordafter = word[:mo.end('fr')]+word[mo.start('to'):]
                    phon.append(list(wordafter))
        return phon

    def phonetize(self, utterance):
        """Phonetizes one utterance

        utterance -- The utterance to phonetize
        """
        try:
            pron = [self.applyrules(self.phonetizeword(
                unicode(word, 'utf-8'))) for word in utterance.split()]
        except TypeError:
            pron = [self.applyrules(self.phonetizeword(
                unicode(word))) for word in utterance.split()]
        pron = filter(None, pron)
        return pron

    def phonetizeword(self, word):
        """Returns a list of phones generated from the utterance and should
        return None when unable to phonetize

        word -- the word to phonetize
        """
        if word in self.dictionary:
            return self.dictionary[word]
        else:
            return None


class PhonetizerTzeltal(Phonetizer):
    """Phonetizer for the tzeltal language"""

    trans = tdict({'j': 'x', 'w': 'b', 'x': 'S', '\'': '?', 'y': 'j'})

    def phonetizeword(self, word):
        word = re.sub('[.,\-]', '', word.lower())
        if word in self.dictionary:
            return self.dictionary[word]
        phonemap = list()
        it = iter(enumerate(word))
        for i, character in it:
            if character == 'c' and i+1 < len(word) and word[i+1] == 'h':
                if i+2 < len(word) and word[i+2] == '\'':
                    next(it, None)
                phonemap.append('ts_j')
                next(it, None)
            elif character == 't' and i+1 < len(word) and word[i+1] == '\'':
                phonemap.append('t')
                next(it, None)
            elif character == 't' and i+1 < len(word) and word[i+1] == 'z':
                if i+2 < len(word) and word[i+2] == '\'':
                    next(it, None)
                phonemap.append('ts_j')
                next(it, None)
            else:
                phonemap.append(self.trans[character])
        self.dictionary[word] = [phonemap]
        return [phonemap]


class PhonetizerSpanish(Phonetizer):
    """Phonetizer for the spanish language"""

    acronymmap = tdict({
        'B': ['b', 'e'], 'C': ['T', 'e'], 'D': ['d', 'e'],
        'F': ['e', 'f', 'e'], 'G': ['x', 'e'], 'H': ['a', 't', 'S', 'e'],
        'J': ['x', 'o', 't', 'a'], 'K': ['k', 'a'], 'L': ['e', 'l', 'e'],
        'M': ['e', 'm', 'e'], 'N': ['e', 'n', 'e'], 'Q': ['k', 'u'],
        'R': ['e', 'r', 'r', 'e'], 'S': ['e', 's', 'e'], 'T': ['t', 'e'],
        'V': ['u', 'b', 'u'], 'W': ['u', 'b', 'u', 'd', 'o', 'b', 'l', 'e'],
        'X': ['e', 'k', 'i', 's'], 'Y': ['i', 'g', 'r', 'i', 'e', 'g', 'a'],
        'Z': ['T', 'e', 't', 'a']
        })

    trans = tdict({'ñ'.decode('utf-8'): 'J', 'ç'.decode('utf-8'): 'T',
                   'j': 'x', 'c': 'k', 'v': 'b', 'w': 'b', 'z': 'T', 'y': 'j'})

    def phonetizeword(self, word):
        word = ''.join(ch for ch in word if
                       unicodedata.category(ch).startswith('L') or
                       ch in '[]<>()&')
        word = re.sub('[<>]', '&', re.sub('\(.*\)', '', word))
        uppercases = len([ch for ch in word if
                         unicodedata.category(ch).startswith('Lu')])
        if word in self.dictionary:
            return self.dictionary[word]
        # Check sounds and foreign language.
        if word and '&' == word[0] or '[lang' in word:
            return None
        # Remove optional laughter and breathing and try again to look it up
        if '[' in word or ']' in word:
            return self.phonetizeword(re.sub('\[.*\]', '', word))
        # Allocate the map
        phonemap = list()
        if uppercases == len(word):
            return [a for b in [self.acronymmap[i] for i in word] for a in b]
        else:
            lw = word.lower()
            it = iter(enumerate(lw))
            for i, ch in it:
                if ch == 'c' and i+1 < len(lw) and lw[i+1] in 'ei':
                    phonemap.append('T')
                elif ch == 'c' and i+1 < len(lw) and lw[i+1] == 'h':
                    phonemap += ['t', 'S']
                    next(it, None)
                elif ch == 'g' and i+1 < len(lw) and\
                        lw[i+1] == 'ü'.decode('utf-8'):
                    phonemap += ['g', 'u']
                    next(it, None)
                elif ch == 'g' and i+1 < len(lw) and lw[i+1] == 'u':
                    phonemap.append('g')
                    next(it, None)
                elif ch == 'g' and i+1 < len(lw) and lw[i+1] in 'ei':
                    phonemap.append('x')
                elif ch == 'l' and i+1 < len(lw) and lw[i+1] == 'l':
                    phonemap.append('jj')
                    next(it, None)
                elif ch == 'q':
                    phonemap.append('k')
                    if i+1 < len(lw) and lw[i+1] == 'u':
                        next(it, None)
                elif ch == 'r' and (i is 0 or lw[i-1] in 'nlsm'):
                    phonemap += ['r', 'r']
                elif ch == 'y' and i+1 >= len(lw):
                    phonemap.append('i')
                elif ch == 'h':
                    continue
                else:
                    phonemap.append(self.trans[ch])
        self.dictionary[word] = [phonemap]
        return [phonemap]


class PhonetizerDictionary(Phonetizer):
    """Dummy phonetizer for dictionary only phonetizers"""

    def phonetizeword(self, word):
        word = word.lower()
        if word in self.dictionary:
            return self.dictionary[word]
        else:
            return None


class PhonetizerSkeleton(Phonetizer):
    """Skeleton to create your own phonetizer"""

    def phonetizeword(self, word):
        # Substitute all transcription specific useless markings and lowercase
        # word
        word = re.sub('[.,\-]', '', word.lower())
        # If the word already exists in the dictionary return it immediatly
        if word in self.dictionary:
            return self.dictionary[word]
        # If some condition is not met and the word is unphonetizable you
        # should return None
        if some_condition:
            return None
        # De the magic phonetizing here

        # Add the phontization to the dictionary
        self.dictionary[word] = [phonemap]
        # Return the map
        return [phonemap]

phonetizerdict = {
    'spa': (PhonetizerSpanish, 'par.spa/'),
    'tze': (PhonetizerTzeltal, 'par.sam/'),
    'dut': (PhonetizerDictionary, 'par.dut/')
    }


def getphonetizer(lang, dictpath=None, ruleset=None):
    """
    Gives a phonetizer by language code

    lang - language code, has to be present in phonetizerdict
    dictpath - optional dictionary file
    ruleset  - optional ruleset file
    """
    dictpath = None if dictpath == "None" else dictpath
    ruleset = None if ruleset == "None" else ruleset
    phonetizer = phonetizerdict[lang]
    return (phonetizer[0](dictpath, ruleset), phonetizer[1])
