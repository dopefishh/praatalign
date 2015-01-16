# -*- coding: utf-8 -*-

import codecs
import re
import unicodedata


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
        self.slfwordthing = True
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

    def toslf(self, pron, bn='temp', graphviz=True):
        """Converts the pronunciation variants and rules to a graph
        representation

        pron     -- Pronunciation
        bn       -- Basename for the output
        graphviz -- If set, this function also produces a .dot file
        """
        # Make a translation for all multi character phones
        c2 = [ch for wd in pron for var in wd for ch in var if len(ch) > 1]
        c2 = dict(zip(c2, map(chr, range(1, len(c2)+1))))

        # Create all possible combinations of pronunciation variants
        possibles = []
        var_is = [0]*len(pron)
        stop = False
        while not stop:
            # Add the current word
            current = [word[var_is[i]]+['#'] for i, word in enumerate(pron)]\
                if self.slfwordthing else\
                [word[var_is[i]] for i, word in enumerate(pron)]
            possibles.append(current)
            # Increment the indices
            for i in xrange(0, len(pron)):
                # If the index can be incremented, do so and break
                if var_is[i] < len(pron[i])-1:
                    var_is[i] += 1
                    break
                # else make it zero and go to the next one
                else:
                    # If this is the last one, stop...
                    if i == len(var_is)-1:
                        stop = True
                    var_is[i] = 0

        # Create all the possible combinations of ruleset combos and applied
        # rules. Duplicates will occur so a set is used
        all_pos = set()
        # Loop over all the words, but now in plain strings
        for word in [''.join(a for p in pp for a in p) for pp in possibles]:
            # Get all the combinations of rules present in the ruleset
            ruleset_combos = []
            self.permute(self.r, ruleset_combos)
            # Loop over all possible combinations
            for ruleset_combo in ruleset_combos:
                # When the combination is empty we can just add the word
                if not ruleset_combo:
                    all_pos.add(word)
                    break
                # Otherwise we have to add for every combination of rules
                for rule in ruleset_combo:
                    # Find all rule matches and find all combinations of these
                    mo = list(rule.finditer(word))
                    possible_replace_combos = []
                    self.permute(mo, possible_replace_combos)
                    # For every combinations, apply them and add it to the set
                    for combi in possible_replace_combos:
                        nword = word
                        for r in reversed(combi):
                            nword = nword[:r.end('fr')]+nword[r.start('to'):]
                        all_pos.add(nword)
        # Replace all the multichar phones with their appropriate byte
        chain_rep = lambda x, (f, t): x.replace(f, t)
        all_pos = {reduce(chain_rep, c2.iteritems(), v) for v in all_pos}

        # Reverse the dictionary so that we later can change it back
        c2 = {v: k for k, v in c2.iteritems()}

        # Add all the words to the DAWG
        import pyDAWG
        pyd = pyDAWG.DAWG()
        for word in sorted(all_pos):
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
        nnodes = {0: '<'}
        nedges = {}
        for fr, ch, to in edges:
            nnodes[to] = c2[ch] if ch in c2 else ch
            if fr not in nedges:
                nedges[fr] = set()
            nedges[fr].add(to)
        # Find the last node and remember the position to connect the end of
        # the words to it
        finalnode = len(nnodes)
        nnodes[finalnode] = '>'
        for final in final_nodes:
            if final not in nedges:
                nedges[final] = set()
            nedges[final].add(finalnode)

        # Open the slf for writing
        with open('{}.slf'.format(bn), 'w') as out:
            # Write statistics about the number of nodes and edges
            out.write('N={} L={}\n'.format(
                len(nnodes), sum(len(to) for _, to in nedges.iteritems())))
            # Write all the nodes
            out.write(''.join(
                'I={} W={}\n'.format(k, v) for k, v in nnodes.iteritems()))
            # Write all the edges
            i = 0
            for fr, to in nedges.iteritems():
                for c in to:
                    out.write('J={} S={} E={}\n'.format(i, fr, c))
                    i += 1
        # If specified create graphviz file
        if graphviz:
            with open('{}.dot'.format(bn), 'w') as out:
                out.write('digraph dawg {\n')
                for number, label in nnodes.iteritems():
                    out.write('\t{} [shape = circle, label = "{}"];\n'.format(
                        number, label))
                for fr, to in nedges.iteritems():
                    for c in to:
                        out.write('\t{} -> {};\n'.format(fr, c))
                out.write('}\n')

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

#    def toslf(self, pron, bn, graphviz=False):
#        """Generates a mlf file and slf file regarding the ruleset
#
#        pron     -- pronunciation in the form of [word1, word2, ..., wordn]
#                        where wordi = [var1, var2, ..., varn]
#                        where vari  = [char1, char2, ..., charn]
#        bn       -- filename without extension for the output files
#        graphviz -- Flag to make a dotfile
#        """
#        nit, eit = 0, 0
#        nodebase = 'I={:d} W={}\n'
#        edgebase = 'J={:d} S={:d} E={:d}\n'
#        wordb = 0
#        nodestr = nodebase.format(0, '<')
#        nit += 1
#        edgestr = ''
#        for word in pron:
#            toadd = []
#            for var in word:
#                edgestr += edgebase.format(eit, wordb, nit)
#                eit += 1
#                for num, char in enumerate(var):
#                    if num > 0:
#                        edgestr += edgebase.format(eit, nit-1, nit)
#                        eit += 1
#                    nodestr += nodebase.format(nit, char)
#                    nit += 1
#                toadd.append(nit-1)
#            nodestr += nodebase.format(nit, '#')
#            wordb = nit
#            nit += 1
#            for to in toadd:
#                edgestr += edgebase.format(eit, to, wordb)
#                eit += 1
#        nodestr += nodebase.format(nit, '>')
#        edgestr += edgebase.format(eit, nit-1, nit)
#        slfstr = 'N={:d} L={:d}\n{}{}'.format(nit+1, eit+1, nodestr, edgestr)
#        with open('{}.slf'.format(bn), 'w') as ff:
#            ff.writelines(slfstr)
#        if graphviz:
#            with open('{}.dot'.format(bn), 'w') as ff:
#                ff.write('digraph g{\n')
#                for li in filter(None,
#                                 [l.split() for l in slfstr.split('\n')]):
#                    if li[0][0] == 'I':
#                        ff.write('\t{} [label="{}"]\n'.format(
#                            li[0][2:], li[1][2:]))
#                    if li[0][0] == 'J':
#                        ff.write('\t{} -> {}\n'.format(li[1][2:], li[2][2:]))
#                ff.write('}')

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
                    phonemap += 'rr'
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


class PhonetizerLoopback(Phonetizer):
    """Dummy phonetizer that uses direct loopback to generate phonetic
    transcription, therefore allowing the user to use his own phonetic
    transcription"""

    def __init__(self, *args, **kwargs):
        Phonetizer.__init__(self, *args, **kwargs)
        self.slfwordthing = False

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
    'spa': (PhonetizerSpanish, 'par.spa'),
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
