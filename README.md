# Interactive forced alignment in spontineous speech, version 0.05

# installation
## linux
### requirements
- Python 2[7.3]
- SoX (has to be in path)
- Praat
- HCopy and HVite (binaries included might not work on all systems, optionally
  put your own compiled binaries in the bin folder before installing).

### installation
```./install_lin```

## mac
Not implemented yet.

## windows
Not implemented yet.

# documentation
## plugin
The plugin works very straight forward, say one wants to force align a tier in
a TextGrid file with a LongSound. To start the script do:
- Read TextGrid from file
- Read LongSound from file
- Select both
- Press the new button that says: *Start interactive force alignment...*

Now there will be a form so that you can specify some parameters:
* newtier
	Name for the tier where the alignment is stored, this may be an existing
	tier, if the tier exists the annotations within the selected interval are
	removed upon alignment.
	default: align
* lang
	Language to align in. Currently this is spanish and tzeltal, in the future
	one can add custom languages.
	default: tze
* dictpath
	Flag for selecting a custom dictionary, if this is not set the aligner wil
	rely completely on the phonetizer, if this is set then a prompt follows to
	select the dictionary.
	default: False
* ruleset
	Flag for using a ruleset file, if this is not set the aligner will uss no
	ruleset, if this is set then a prompt follows to select the ruleset file.
	default: False
* pdf
	Flag for export to pdf, if this is not set the aligner will not create pdf
	files for the graphs it follows, if this is set after the alignment there
	will be a temp.pdf located in this plugin folder(on linux
	~/.praat-dir/plugin_pralign
	default: False
* tmpdir
	Temporary file directory, this is the directory where the aligner stores
	the semi-raw results from HTK.
	default: /tmp/

When the form is accepted the TextGrid editor will be opened and a pause
window is spawned. When you select an annotation and press continue it will
align the annotation using the specified options.

## scripts

## customize/add language

# version history
* 0.05 - 2014-04-03 - better readme and functional program for linux
* 0.04 - 2014-04-03 - pronounciation variants implemented
* 0.03 - 2014-03-31 - aligner works, praat imlementation needs work
* 0.02 - 2014-03-27 - started with aligner
* 0.01 - 2014-03-27 - phonetizer done
* 0.00 - 2014-03-27 - initial version
# authors
mart@martlubbers.net
emma.valtersson@gmail.com

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
```mart\tm a r t\tm a r```

version history
===============

authors
=======
