# -*- coding: utf-8 -*-

import codecs
import re
import unicodedata
import itertools


class tdict(dict):
    """Dictionary with a missing value that is the normalized version
    of the input
    """
    def __missing__(self, key):
        char = unicodedata.normalize('NFKD', unicode(key))
        return str(char.encode('ascii', 'ignore')).lower()


class Phonetizer:
    """Skeleton class for a phonetizer for the praat align program"""
    reps = [(r'\v', '[aoeiu]'), (r'\c', '[^aoeui]'), ('\n', '')]

    def __init__(self, dictpath=None, ruleset=None):
        """Constructor with an optional dictionary

        filters  -- A regular expression of things to filter out of the
                    utterances
        dictpath -- Path to an optional dictonary
        ruleset  -- Path to an optional ruleset file
        """
        self.r = []
        self.dictionary = dict()
        if dictpath is not None:
            with codecs.open(dictpath, 'r', 'utf-8') as f:
                for l in f:
                    if l and l[0] != '#':
                        l = [s.strip() for s in l.split('\t')]
                        self.dictionary[l[0]] = [var.split() for var in
                                                 map(str, l[1:])]
        if ruleset is not None:
            with codecs.open(ruleset, 'r', 'utf-8') as f:
                for l in itertools.ifilter(lambda x: x[0] != '#', f):
                    if not l.startswith('\t'):
                        l = re.sub(r'([.^$*+?{}[\]\|()])', r'\\\1', l)
                    else:
                        for target, repl in self.reps:
                            l = l.replace(target, repl)
                    self.r.append(l.strip().split('\t'))

    def todawg(self, pron, experimental=False):
        """Converts the pronunciation variants and rules to a graph
        representation.

        pron     -- Pronunciation
        """
        # Make a translation for all multi character phones
        c2 = [ch for wd in pron for var in wd for ch in var if len(ch) > 1]
        if experimental:
            c2.append('sp')
        c2 = dict(zip(c2, map(chr, range(1, len(c2)+1))))

        # Create all possible combinations of pronunciation variants
        pron = ((' '.join(varnt + ['#' if not experimental else 'sp'])
                 for varnt in word) for word in pron)

        # Make strings of these variants
        pron = (' '.join(x) for x in itertools.product(*pron))
        # Create combinations of all rulesets
        rcs = [()]
        for i in range(len(self.r)):
            rcs += itertools.combinations(self.r, i+1)
        all_prons = set()
        # For every variant
        for variant in pron:
            # For every combination of rules
            for combo in rcs:
                all_prons.add(variant)
                # For every rule combination
                for pat, target in combo:
                    app = sorted(x.span() for x in re.finditer(pat, variant))
                    apporders = [()]
                    for i in range(len(app)):
                        apporders += itertools.permutations(app, i+1)
                    # For every appliance order
                    for appc in reversed(apporders):
                        wordapp = variant
                        for st, en in appc:
                            try:
                                wordapp = '{}{}{}'.format(
                                    wordapp[:st], 
                                    re.sub(pat, target, wordapp[st:en]),
                                    wordapp[en:])
                            except:
                                pass
                        all_prons.add(wordapp)

        ## Replace all the multichar phones with their appropriate byte
        for f, t in c2.iteritems():
            all_prons = {x.replace(f, t) for x in all_prons} 
        all_prons = {x.replace(' ', '') for x in all_prons} 
        c2 = {v: k for k, v in c2.iteritems()}

        # Add all the words to the DAWG
        import pyDAWG
        pyd = pyDAWG.DAWG()
        for word in sorted(all_prons):
            pyd.add_word(word)

        # Create a slf with breath first search and use a translation list to
        # map the unnumbered nodes to their numbered variants
        nodenum = 0
        final_nodes, nodes, edges, translation = [], [], [], []
        queue = [(0, pyd.q0)]
        visited = set()
        if pyd.q0.final:
            final_nodes.append(nodenum)
        else:
            nodes.append(nodenum)
        nodenum += 1
        # While we still have nodes to visit
        while queue:
            # If we have not visited the newest node
            current = queue.pop()
            if not current[0] in visited:
                # Visit the node
                visited.add(current[0])
                # Go throught all the children
                for char, child in current[1].children.iteritems():
                    # Find translation for the child
                    matches = [c for c in translation if c[0] == child]
                    curnum = -1
                    # Translate if there is a translation
                    if matches:
                        curnum = matches[-1][1]
                    # Otherwise create a translation
                    else:
                        translation.append((child, nodenum))
                        curnum = nodenum
                        nodenum += 1
                    # If the node is final, mark is as such
                    if child.final:
                        final_nodes.append(curnum)
                    else:
                        nodes.append(curnum)
                    # Append the edge to the list and append the child to the
                    # queue
                    edges.append((current[0], char, curnum))
                    queue.append((curnum, child))
        # Convert the edges to a dictionary with for every number a set of
        # connections and convert the nodes to a dictionary with for every
        # number the appropriate character. Also convert the multichar phones
        # back to their original form.
        nodes += final_nodes
        nnodes = {0: '<'} if not experimental else {0: 'sil'}
        nedges = {}
        for fr, ch, to in edges:
            nnodes[to] = c2[ch] if ch in c2 else ch
            if fr not in nedges:
                nedges[fr] = set()
            nedges[fr].add(to)
        # Find the last node and remember the position to connect the end of
        # the words to it
        finalnode = len(nnodes)
        nnodes[finalnode] = '>' if not experimental else 'sil'
        for final in final_nodes:
            if final not in nedges:
                nedges[final] = set()
            nedges[final].add(finalnode)
        return nedges, nnodes

    def todot(self, nedges, nnodes):
        dot = 'digraph {rankdir=LR;'
        dot += ''.join('q{} [label="{}"];'.format(*x) for x in nnodes.items())
        for fr, to in nedges.iteritems():
            for c in to:
                dot += 'q{} -> q{};'.format(fr, c)
        return dot + '}'

    def toslf(self, nedges, nnodes):
        slf = 'N={} L={}\n'.format(
            len(nnodes), sum(len(to) for _, to in nedges.iteritems()))
            # Write all the nodes
        slf += ''.join(
            'I={} W={}\n'.format(k, v) for k, v in nnodes.iteritems())
        # Write all the edges
        i = 0
        for fr, to in nedges.iteritems():
            for c in to:
                slf += 'J={} S={} E={}\n'.format(i, fr, c)
                i += 1
        return slf

    def permute(self, items, output):
        """Helper function that creates all possible combinations of a list

        items  -- Possible items
        output -- Results list
        """
        # Append the current combination
        output.append(items)
        # For all nodes left remove 1 and put the resulting list back in
        for i, item in enumerate(items):
            items2 = items[:]
            items2.remove(item)
            self.permute(items2, output)

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
            pron = [self.phonetizeword(unicode(word, 'utf-8')) for
                    word in utterance.split()]
        except TypeError:
            pron = [self.phonetizeword(unicode(word)) for
                    word in utterance.split()]
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
            return [[a for b in [self.acronymmap[i] for i in word] for a in b]]
        else:
            lw = word.lower()
            it = iter(enumerate(lw))
            for i, ch in it:
                if ch == 'c' and i+1 < len(lw) and\
                        lw[i+1] in 'eií'.decode('utf-8'):
                    phonemap.append('T')
                elif ch == 'c' and i+1 < len(lw) and lw[i+1] == 'h':
                    phonemap += ['t', 'S']
                    next(it, None)
                elif ch == 'g' and i+1 < len(lw) and\
                        lw[i+1] == 'ü'.decode('utf-8'):
                    phonemap += ['g', 'u']
                    next(it, None)
                elif ch == 'g' and i+2 < len(lw) and lw[i+1] == 'u' and\
                        lw[i+2] in 'ei':
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
                elif ch == 'r' and ((i is 0 or lw[i-1] in 'nlsm') or
                                    (i+1 < len(lw) and lw[i+1] == 'r')):
                    if i+1 < len(lw) and lw[i+1] == 'r':
                        next(it, None)
                    phonemap += ['rr']
                elif ch == 'y' and i+1 >= len(lw):
                    phonemap.append('i')
                elif ch == 'x':
                    phonemap += ['k', 's']
                elif ch == 'h':
                    continue
                else:
                    phonemap.append(self.trans[ch])
        self.dictionary[word] = [phonemap]
        return [phonemap]


class PhonetizerDictionary(Phonetizer):
    """Dummy phonetizer for dictionary only phonetizers"""

    def phonetizeword(self, word):
       # word = word.lower()
        if word in self.dictionary:
            return self.dictionary[word]
        else:
            return None


class PhonetizerLoopback(Phonetizer):
    """Dummy phonetizer that uses direct loopback to generate phonetic
    transcription, therefore allowing the user to use his own phonetic
    transcription"""

    def __init__(self, *args, **kwargs):
        Phonetizer.__init__(self, *args, **kwargs)

    def phonetize(self, utterance):
        """Phonetizes one utterance

        utterance -- The utterance to phonetize
        """
        return [[[a]] for a in utterance.split(' ')]


class PhonetizerSkeleton(Phonetizer):
    """Skeleton to create your own phonetizer"""

    def phonetizeword(self, word):
        #  Substitute all transcription specific useless markings and lowercase
        # word
        # word = re.sub('[.,\-]', '', word.lower())
        # If the word already exists in the dictionary return it immediatly
        # if word in self.dictionary:
        #     return self.dictionary[word]
        # If some condition is not met and the word is unphonetizable you
        # should return None
        # if some_condition:
        #     return None
        # Do the magic phonetizing here
        # Add the phontization to the dictionary
        # self.dictionary[word] = [phonemap]
        # Return the map
        # return [phonemap]
        pass

phonetizerdict = {
    'dut': (PhonetizerDictionary, 'par.dut'),
    'eng': (PhonetizerDictionary, 'par.eng'),
    'sam': (PhonetizerDictionary, 'par.sam'),
    'spa': (PhonetizerSpanish, 'par.spa'),
    'exp': (PhonetizerSpanish, 'par.exp'),
    'tze': (PhonetizerTzeltal, 'par.sam')
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
