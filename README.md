### Interactive forced alignment in spontineous speech, version 0.05

### installation
#### linux
##### requirements
- Python 2[7.3]
- SoX (has to be in path)
- Praat
- HCopy and HVite (binaries included might not work on all systems, optionally
  put your own compiled binaries in the bin folder before installing).

##### installation
run install\_lin

#### mac
Not implemented yet.

#### windows
Not implemented yet.

### documentation
#### plugin
The plugin works very straight forward, say one wants to force align a tier in
a TextGrid file with a LongSound. To start the script do:
- Read TextGrid from file
- Read LongSound from file
- Select both
- Press the new button that says: *Start interactive force alignment...*

Now there will be a form so that you can specify some parameters:
* **newtier**, default: align

	Name for the tier where the alignment is stored, this may be an existing
	tier, if the tier exists the annotations within the selected interval are
	removed upon alignment.
* **lang**, default: tze

	Language to align in. Currently this is spanish and tzeltal, in the future
	one can add custom languages.
* **dictpath**, default: False

	Flag for selecting a custom dictionary, if this is not set the aligner wil
	rely completely on the phonetizer, if this is set then a prompt follows to
	select the dictionary.
* **ruleset**, default: False

	Flag for using a ruleset file, if this is not set the aligner will uss no
	ruleset, if this is set then a prompt follows to select the ruleset file.
* **pdf**, default: False

	Flag for export to pdf, if this is not set the aligner will not create pdf
	files for the graphs it follows, if this is set after the alignment there
	will be a temp.pdf located in this plugin folder(on linux
	~/.praat-dir/plugin_pralign
* **tmpdir**, default: /tmp/

	Temporary file directory, this is the directory where the aligner stores
	the semi-raw results from HTK.

When the form is accepted the TextGrid editor will be opened and a pause
window is spawned. When you select an annotation and press continue it will
align the annotation using the specified options.

#### dictionary file
A dictionary file consists of several non emptylines character(\\n), lines
starting with a # will be ignored and can be used as comments. The dictionary
delivers the pronounciation and optional variants to the phonetizer and has to
be of the following format:
```
word-1<TAB>pronounciation-1[<TAB>variant-1a][<TAB>variant-1b]...
word-2<TAB>pronounciation-2[<TAB>variant-2a][<TAB>variant-2b]...
...
word-n<TAB>pronounciation-n[<TAB>variant-na][<TAB>variant-nb]...
```

#### ruleset file
Pronounciation rules are not implemented anymore but will be back very soon. A
ruleset file describes certain rules that can be on inter and intraword level
and uses python regular expressions to achive this. It will tie the group named
*to* to *from* so you can easily describe deletion rules. A ruleset file is of
the following format:
```
regex-1
regex-2
...
regex-n
```

Every regex must contain at minimal the named groups *to* and *from*.
For example the rule that will delete a *d* if it is between *a* and *o*
regardless of word boundaries:
```
(?P<fr>a#?)d(?P<to>#?o)
```

#### customize/add language
todo

### version history
* 0.05 - 2014-04-03 - better readme and functional program for linux
* 0.04 - 2014-04-03 - pronounciation variants implemented
* 0.03 - 2014-03-31 - aligner works, praat imlementation needs work
* 0.02 - 2014-03-27 - started with aligner
* 0.01 - 2014-03-27 - phonetizer done
* 0.00 - 2014-03-27 - initial version

### authors
mart@martlubbers.net
emma.valtersson@gmail.com
