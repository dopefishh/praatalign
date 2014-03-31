version 0.02
============
- phonetizer.py
	- Phonetizer skeleton class, tzeltal and spanish phonetizer and tools to
	  export to slf, mlf and even graphviz pdf(if dot is installed and in PATH)
- aligner.py
	- This file will be used in the praat integration in the future, currently
	  it can align utterances.
- praat.praat
	- This file is the interface to praat

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
- \# is used for word boundaries
- < is used for the start of the chunk
- \> is used for the end of the chunk

version history
===============
* 0.02 - 2014-03-27 - started with aligner
* 0.01 - 2014-03-27 - phonetizer done
* 0.00 - 2014-03-27 - initial version

authors
=======
mart@martlubbers.net
emma.valtersson@gmail.com
