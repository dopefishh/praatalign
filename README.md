version 0.01
============
- phonetizer.py
	- Phonetizer skeleton class, tzeltal and spanish phonetizer and tools to
	  export to slf, mlf and even graphviz pdf(if dot is installed and in PATH)

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
\v for vowels
\c for consonants
\# is used for word boundaries
< is used for the start of the chunk
\> is used for the end of the chunk

version history
===============
* 0.01 - 2014-03-27 - phonetizer done
* 0.00 - 2014-03-27 - initial version

authors
=======
mart@martlubbers.net
emma.valtersson@gmail.com
