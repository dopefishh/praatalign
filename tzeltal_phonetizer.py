#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pympi.Elan import Eaf
import codecs
import glob
import re

trans = {'j':'x', 'w':'b', 'x':'S', '\'':'?'}

def phonetize(word, dct=None):
	if dct:
		return dct[word]
	#Make a list
	phonList = list()
	#Loop through all characters
	it = iter(enumerate(word))
	for i, character in it:
		if character == 'c' and i+1<len(word) and word[i+1]=='h':
			if i+2<len(word) and word[i+2]=='\'':
				next(it, None)
			phonList.append('ts_j')
			next(it, None)
		elif character == 'k' and i+1<len(word) and word[i+1]=='\'':
			phonList.append('k')
			next(it, None)
		elif character == 't' and i+1<len(word) and word[i+1]=='\'':
			phonList.append('t')
			next(it, None)
		elif character == 't' and i+1<len(word) and word[i+1]=='z':
			if i+2<len(word) and word[i+2]=='\'':
				next(it, None)
			phonList.append('ts_j') #check character!!
			next(it, None)
		elif character in trans:
			phonList.append(trans[character])		
		else:
			phonList.append(character)
	return phonList

def phonetizeSentence(sent, dct=None):
	sent = re.sub(r'(\(.*?\)|[,.\-()])', '', sent).strip().lower()
	return [phonetize(word, dct) for word in sent.split()]

if __name__ == '__main__':
	allwords = set()
	for elanFile in glob.glob('../*.eaf'):
		#Load the elan file
		eaf = Eaf(elanFile)
		#Filter the tiernames to only match annotated tiers
		wordTiers = [i for i in eaf.getTierNames() if i.startswith('1_')]
		for wordTier in wordTiers:
			for annotation in eaf.getAnnotationDataForTier(wordTier):
				#print annotation
				#exclude annotations that are blank
				#strippedann = annotation[2].strip().replace(',', '').replace('-', '').replace('..', '')
				strippedann = re.sub(r'(\(.*?\)|[,.\-()])', '', annotation[2]).strip()
				#divide annotation into words by using the split-function
				for word in strippedann.split():
					allwords.add(word.lower())
					
	worddict = dict()
	for word in allwords:
		if word in worddict:
			continue
		else:
			pronunciation = phonetize(word)
			worddict[word] = pronunciation
			
	outputfile = 'tzeltaldict.txt'
	with codecs.open(outputfile, 'w', 'utf-8') as f:
		for item in sorted(worddict.items()):
			f.write('%s\t%s\n' % (item[0], ' '.join(item[1])))
