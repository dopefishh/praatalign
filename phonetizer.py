# -*- coding: utf-8 -*-

import codecs
import re
import unicodedata

class tdict(dict):
	"""Dictionary with a missing value that is the normalized version
	of the input
	"""
	def __missing__(self, key):
		"""If missing return the normalized input"""
		return str(unicodedata.normalize('NFKD', unicode(key)).	encode('ascii',	
			'ignore')).lower()

class Phonetizer:
	"""Skeleton class for a phonetizer for the pralign program"""

	def __init__(self, filters=re.compile(''), dictpath=None):
		"""Constructor with an optional dictionary"""
		self.f = re.compile(filters) if isinstance(filters, basestring)	else filters
		if dictpath is not None:
			self.dictionary = dict()
			with codecs.open(dictpath, 'r', 'utf-8') as f:
				for l in f:
					if l and l[0]!='#':
						l = [s.strip() for s in l.split('\t')]
						self.dictionary[l[0]] = unicode(l[1]).split(' ')
		else:
			self.dictionary = dict()

	def tomlf(self, pron, mlf):
		with open(mlf, 'w') as f:
			f.write('#!MLF!\n')
			f.write('"*/%s.lab"\n' % mlf[:-4])
			f.write('<\n%s\n#\n>\n.' % '\n#\n'.join('\n'.join(p) for p in pron))

	def phonetize(self, utterance):
		utterance = self.f.sub('', utterance)
		return [self.phonetizeword(word) for word in utterance.split()]
	
	def phonetizeword(self, word):
		"""Returns a list of phones generated from the utterance"""
		raise NotImplementedError("Not implemented")


class PhonetizerTzeltal(Phonetizer):
	"""Phonetizer for the tzeltal language"""
	trans = tdict({'j':'x', 'w':'b', 'x':'S', '\'':'?', 'y':'j'})

	def phonetizeword(self, word):
		"""Phonetizes one word by optionally looking it up in the dictionary"""
		word = unicode(word.lower())
		if word in self.dictionary:
			return dct[word]

		phonemap = list()
		it = iter(enumerate(word))
		for i, character in it:
			if character == 'c' and i+1<len(word) and word[i+1]=='h':
				if i+2<len(word) and word[i+2]=='\'':
					next(it, None)
				phonemap.append('ts_j')
				next(it, None)
			elif character == 'k' and i+1<len(word) and word[i+1]=='\'':
				phonemap.append('k')
				next(it, None)
			elif character == 't' and i+1<len(word) and word[i+1]=='\'':
				phonemap.append('t')
				next(it, None)
			elif character == 't' and i+1<len(word) and word[i+1]=='z':
				if i+2<len(word) and word[i+2]=='\'':
					next(it, None)
				phonemap.append('ts_j')
				next(it, None)
			else:
				phonemap.append(self.trans[character])

		self.dictionary[word] = phonemap
		return phonemap

class PhonetizerSpanish(Phonetizer):
	"""Phonetizer for the spanish language"""

	acronymmap = tdict({'B':['b', 'e'], 'C':['T', 'e'], 'D':['d', 'e'],
		'F':['e', 'f', 'e'], 'G':['x', 'e'], 'H':['a', 't', 'S', 'e'],
		'J':['x', 'o', 't', 'a'], 'K':['k', 'a'], 'L':['e', 'l', 'e'],
		'M':['e', 'm', 'e'], 'N':['e', 'n', 'e'], 'Q':['k', 'u'], 
		'R':['e', 'r', 'r', 'e'], 'S':['e', 's', 'e'], 'T':['t', 'e'], 
		'V':['u', 'b', 'u'], 'W':['u', 'b', 'u', 'd', 'o', 'b', 'l', 'e'], 
		'X':['e', 'k', 'i', 's'], 'Y':['i', 'g', 'r', 'i', 'e', 'g', 'a'],
		'Z':['T', 'e', 't', 'a']})

	trans = tdict({'ñ'.decode('utf-8'):'J', 'ç'.decode('utf-8'):'T', 'j':'x',
		'c':'k', 'v':'b', 'w':'b', 'z':'T', 'y':'j'})
	
	def phonetizeword(self, word):
		"""Spanish word to phoneme mapping the word should be in Unicode ex. u'sabes', the dictionary is optional it could be used for fast lookup"""
		#Remove punctuation, truncate and generalize nib symbols
		word = ''.join(ch for ch in unicode(word) if unicodedata.category(ch).startswith('L') or ch in '[]<>()&')
		word = re.sub('[<>]', '&', re.sub('\(.*\)', '', word))
	
		uppercases = len([ch for ch in word if unicodedata.category(ch).startswith('Lu')])
		if word in self.dictionary:
			return self.dictionary[word]
	
		#Check sounds and foreign language.
		if '&' == word[0] or  '[lang' in word:
			print 'non word character or foreign language, please add manually: '
			with codecs.open('mis.txt', 'a', 'utf-8') as mis:
				mis.write(word)
				mis.write('\n')
			return ['< n i b >']
		
		#Remove optional laughter and breathing and try again to look it up
		if '[' in word or ']' in word:
			return self.phonetizeword(re.sub('\[.*\]', '', word))
	
		#Allocate the map
		phonemap = list()
		if uppercases==len(word):
			return  [a for b in [self.acronymmap[i] for i in word] for a in b]
		else:
			lowerword = word.lower()
			it = iter(enumerate(lowerword))
			for i, ch in it:
				if ch=='c' and i+1<len(lowerword) and lowerword[i+1] in 'ei':
					phonemap.append('T')
				elif ch=='c' and  i+1<len(lowerword) and lowerword[i+1]=='h':
					phonemap += ['t', 'S']
					next(it, None)
				elif ch=='g' and i+1<len(lowerword) and lowerword[i+1]=='ü'.decode('utf-8'):
					phonemap += ['g', 'u']
					next(it, None)
				elif ch=='g' and i+1<len(lowerword) and lowerword[i+1]=='u':
					phonemap.append('g')
					next(it, None)
				elif ch=='g' and i+1<len(lowerword) and lowerword[i+1] in 'ei':
					phonemap.append('x')
				elif ch=='l' and i+1<len(lowerword) and lowerword[i+1]=='l':
					phonemap.append('jj')
					next(it, None)
				elif ch=='q':
					phonemap.append('k')
					if i+1<len(lowerword) and lowerword[i+1]=='u':
						next(it, None)
				elif ch=='r' and (i is 0 or lowerword[i-1] in 'nlsm'):
					phonemap += ['r', 'r']
				elif ch=='y' and i+1>=len(lowerword):
					phonemap.append('i')
				elif ch=='h':
					continue
				else:
					phonemap.append(self.trans[ch])
		
		self.dictionary[word] = phonemap
		return phonemap
