version 0.03
============
- phonetizer.py
	- Phonetizer skeleton class, tzeltal and spanish phonetizer and tools to
	  export to slf, mlf and even graphviz pdf(if dot is installed and in PATH)
- aligner.py
	- This file will be used in the praat integration in the future, currently
	  it can align utterances.
- praat.praat
	- This file is the interface to praat, note that it's not yet modular so
	  the paths should be adapted to make it work

installation
============
Requirements:
	- Python 2
	- SoX
	- Praat
Run the installation script that is included
note. the script for mac is not yet working

rules
=====
Rules for truncation can be defined in ruleset files and specified per
language. The way of specifying is through python regular expressions with two 
named groups called 'to' and 'fr'.
For example if you want to truncate 'ado' to 'ao' you write:
```
" a d o -> a o
(?P<fr>a#?)d(?P<to>#?o)
```
Lines starting with double quotes are ignored and can serve as comments.
To make certain things more easy a couple of groups are predefined, namely:
- \v for vowels
- \c for consonants
- # is used for word boundaries
- < is used for the start of the chunk
- > is used for the end of the chunk

dictionary format
=================
Lines separated by \n and of the following format
word<TAB>pronounciation[<TAB>pronounciation variant]*

So for example let's say the word mart is pronounced as 'm a r t' or 'm a r',
then you will add this entry:
```mart	m a r t	m a r```

version history
===============
* 0.04 - 2014-04-03 - pronounciation variants implemented
* 0.03 - 2014-03-31 - aligner works, praat imlementation needs work
* 0.02 - 2014-03-27 - started with aligner
* 0.01 - 2014-03-27 - phonetizer done
* 0.00 - 2014-03-27 - initial version

authors
=======
mart@martlubbers.net
emma.valtersson@gmail.com
