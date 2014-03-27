#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import PhonetizerSpanish as Phonetizer
import tzeltal_phonetizer as tz
import subprocess
import codecs
import re
from pympi.Elan import Eaf
from pympi.Praat import TextGrid

def parseRuleset(path):
	"""Parses the rulset from the path and returns a list of substitution tuples"""
	#Make vowel and consonant set and remove newlines
	reps = [('\\v', '[aoeiu]'),
			('\\c', '[^aoeui]'),
			('\n', '')]
	with open(path, 'r') as f:
		lines = [re.compile(reduce(lambda x, (o, n): x.replace(o, n), reps, l)) for l in f if l and l[0]!='"']
	return lines

def loadDict(path):
	"""Loads a dictionary from a path into the memory"""
	dictionary = dict()
	with codecs.open(path, 'r', 'utf-8') as f:
		for l in f:
			#Filter out comments
			if not l or l[0]=='#':
				continue
			else:
				l = [s.strip() for s in l.split('\t')]
				dictionary[l[0]] = unicode(l[1].decode('utf-8')).split(' ')
	return dictionary

def mlf2slf(bn, ruleset=None):
	"""Converts a mlf file to a slf file"""
	with open(bn+'.mlf', 'r') as f:
		#Read the mlf and strip the header off
		data = [d.strip() for d in f.readlines()[2:-1]]
	with open(bn+'.slf', 'w') as f:
		#Find all the truncation rules in the string
		extras = []
		if ruleset is not None and ruleset:
			extras = [match.span() for rule in ruleset for match in rule.finditer(''.join(data))]
		#Number of edges is the linpath plus the extra truncation rules
		f.write('N=%d L=%d\n' % (len(data), len(data)-1+len(extras)))
		#Write the basic linear path and the nodes
		f.write('\n'.join('I=%d W=%s' % (i, d) for i,d in enumerate(data)) + '\n')
		f.write('\n'.join('J=%d S=%d E=%d' % (d, d, d+1) for d in range(len(data)-1)))
		#Write the extras
		if extras:
			for i, e in enumerate(extras):
				double = [d for d in enumerate(data) if len(d[1])>1]
				for d in double:
					if d[0]<e[0]:
						e = (e[0]-(len(d[1])-1), e[1]-(len(d[1])-1))
					else:
						break
				f.write('\nJ=%d S=%d E=%d' % (len(data)+i-1, e[0], e[1]-1))

def forceAlignTier(tgin, wav, tiername, tgout='new.TextGrid',  dictpath='./dict', ruleset=None):
	"""Aligns a wave file with a TextGrid tier and writes it to a new TextGrid file and uses an optional dictionary"""
	#Load parameters
	param = {	'PRECONFIG':'./p/PRECONFIGNIST',
				'HVITECONF':'./p/HVITECONF',
				'MMF':'./p/MMF.mmf',
				'DICT':'./p/DICT',
				'HMMINVENTAR':'./p/HMMINVENTAR', 
				'BN':'temp'}
	#Load the sourcerate
	with open(param['PRECONFIG'], 'r') as f:
		param['SOURCERATE'] = 10000000/int([a for a in f if 'SOURCERATE' in a][0].split(' ')[-1])
		
	#Load the file and dictionary and create the tiers and mark the starting time
	a = TextGrid(tgin, 'utf-16')
	newtier = a.addTier('%s_align' % tiername)
	dictionary = loadDict(dictpath)
	allanns = len(a.getTier(tiername).getIntervals())
	#Iterate over all the annotations
	for i, an in enumerate(sorted(a.getTier(tiername).getIntervals())):
		if not an[2].strip():
			continue
		an = (int(an[0]*1000), int(an[1]*1000), an[2])
		#Create the mlf file for htk but skip if the utterance is empty
		pron = ['\n'.join(w) for w in tz.phonetizeSentence(an[2])]
		if not pron:
			continue
		with open(param['BN']+'.mlf', 'w') as f:
			f.write('#!MLF!\n"*/%s.lab"\n<\n%s\n#\n>\n.' % (param['BN'], '\n#\n'.join(pron)))
		#Cut the corresponding wave file with sox
		subprocess.call('sox -G %s %s.wav trim %f %f 2>&1 1>/dev/null' % (wav, param['BN'], an[0]/1000.0, (an[1]-an[0])/1000.0), shell=True)
		#Convert to nis and resample
		subprocess.call('sox %(BN)s.wav -t sph -e signed-integer -b 16 -c 1 %(BN)s.nis 2>&1 1>/dev/null' % param, shell=True)
		subprocess.call('sox %(BN)s.nis -t sph %(BN)s.re.nis rate -s -a %(SOURCERATE)d 2>&1 1>/dev/null' % param, shell=True)
		#Create HTK file
		subprocess.call('./HCopy -T 0 -C %(PRECONFIG)s %(BN)s.re.nis %(BN)s.htk' % param, shell=True)

		#Create SLF
		mlf2slf(param['BN'], ruleset)
		#Force align the file
		subprocess.call('./HVite -C %(HVITECONF)s -w -X slf -H %(MMF)s -s 7.0 -p 0.0 %(DICT)s %(HMMINVENTAR)s %(BN)s.htk | grep -v \'WARNING\'' % param, shell=True)
		#Convert the rec file
		with open(param['BN']+'.rec', 'r') as f:
			data = [d.split(' ') for d in f]
		#Add the aligments to the eaf after converting
		for ann in [(int(d[0])/10000000.0, int(d[1])/10000000.0, d[2], d[3]) for d in data]:
			newtier.addInterval(ann[0]+an[0]/1000.0, ann[1]+an[0]/1000.0, ' '.join(ann[2]), check=False)
			
		#Print the progress
		print '%d/%d done' % (i, allanns)

	#Remove the temporary files and write the elan file
	a.tofile(tgout)
	print 'done...'
	subprocess.call('rm -fv ./temp*', shell=True)

if __name__ == '__main__':
	forceAlignTier('2013March27_PaseroKunerolBartolo.TextGrid', '2013March27_PaseroKunerolBartolo_L.wav', '1_ANTUN')
	forceAlignTier('new.TextGrid', '2013March27_PaseroKunerolBartolo_R.wav', '1_PASERO')
