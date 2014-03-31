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
        """If missing return the normalized input"""
        char = unicodedata.normalize('NFKD', unicode(key))
        return str(char.encode('ascii', 'ignore')).lower()


class Phonetizer:
    """Skeleton class for a phonetizer for the pralign program"""

    def __init__(self, filters=re.compile(''), dictpath=None, ruleset=None):
        """Constructor with an optional dictionary

        filters  -- A regular expression of things to filter out of the
                    utterances
        dictpath -- Path to an optional dictonary
        ruleset  -- Path to an optional ruleset file
        """
        if isinstance(filters, basestring):
            self.f = re.compile(filters)
        else:
            self.f = filters
        self.parseruleset(ruleset)
        if dictpath is not None:
            self.dictionary = dict()
            with codecs.open(dictpath, 'r', 'utf-8') as f:
                for l in f:
                    if l and l[0] != '#':
                        l = [s.strip() for s in l.split('\t')]
                        self.dictionary[l[0]] = unicode(l[1]).split(' ')
        else:
            self.dictionary = dict()

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

    def tomlfslf(self, pron, bn, graphviz=False):
        """Generates a mlf file and slf file regarding the ruleset

        pron     -- Pronunciation of the words
        bn       -- filename without extension for the output files
        graphviz -- Flag to make a pdf of the final graph
        """
        with open('%s.mlf' % bn, 'w') as f:
            f.write('#!MLF!\n')
            f.write('"*/%s.lab"\n' % bn)
            data = '<\n%s\n#\n>\n.' % '\n#\n'.join('\n'.join(p) for p in pron)
            f.write(data)
        with open('%s.slf' % bn, 'w') as f:
            data = data.split('\n')[:-1]
            extras = [(match.start('fr'), match.end('to')) for rule in self.r
                      for match in rule.finditer(''.join(data))]
            f.write('N=%d L=%d\n' % (len(data), len(data)-1+len(extras)))
            f.write('\n'.join('I=%d W=%s' % (i, d) for i, d in enumerate(data))
                    + '\n')
            f.write('\n'.join('J=%d S=%d E=%d' % (d, d, d+1) for d in
                    xrange(len(data)-1)))
            if extras:
                for i, e in enumerate(extras):
                    double = [d for d in enumerate(data) if len(d[1]) > 1]
                    for d in double:
                        if d[0] < e[0]:
                            e = (e[0]-(len(d[1])-1), e[1]-(len(d[1])-1))
                        else:
                            break
                    f.write('\nJ=%d S=%d E=%d' % (len(data)+i-1, e[0], e[1]-1))
        if graphviz:
            with open('%s.slf' % bn, 'r') as f:
                with open('%s.dot' % bn, 'w') as ff:
                    ff.write('digraph g{\n')
                    for line in f:
                        if line[0] == 'I':
                            nu, la = line.split()
                            ff.write('\t%s [label="%s"]\n' % (nu[2:], la[2:]))
                        if line[0] == 'J':
                            fr, to = line.split()[1:]
                            ff.write('\t%s -> %s\n' % (fr[2:], to[2:]))
                    ff.write('}')
                os.system('dot -Tpdf %s.dot -o %s.pdf' % (bn, bn))

    def phonetize(self, utterance):
        """Phonetizes one utterance

        utterance -- The utterance to phonetize
        """
        utterance = self.f.sub('', utterance)
        return [self.phonetizeword(word) for word in utterance.split()]

    def phonetizeword(self, word):
        """Returns a list of phones generated from the utterance

        word -- the word to phonetize
        """
        raise NotImplementedError("Not implemented")


class PhonetizerTzeltal(Phonetizer):
    """Phonetizer for the tzeltal language"""

    trans = tdict({'j': 'x', 'w': 'b', 'x': 'S', '\'': '?', 'y': 'j'})

    def phonetizeword(self, word):
        word = unicode(word.lower())
        if word in self.dictionary:
            return dct[word]
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

        self.dictionary[word] = phonemap
        return phonemap


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
        # Remove punctuation, truncate and generalize nib symbols
        word = ''.join(ch for ch in unicode(word) if
                       unicodedata.category(ch).startswith('L') or
                       ch in '[]<>()&')
        word = re.sub('[<>]', '&', re.sub('\(.*\)', '', word))

        uppercases = len([ch for ch in word if
                         unicodedata.category(ch).startswith('Lu')])
        if word in self.dictionary:
            return self.dictionary[word]

        # Check sounds and foreign language.
        if '&' == word[0] or '[lang' in word:
            print 'Please add manually: '
            with codecs.open('mis.txt', 'a', 'utf-8') as mis:
                mis.write(word)
                mis.write('\n')
            return ['< n i b >']

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

        self.dictionary[word] = phonemap
        return phonemap
