### Interactive forced alignment in spontineous speech, version 0.06

### installation
#### linux
##### requirements
- Python 2[7.3]
- SoX (has to be in path)
- Praat
- HCopy and HVite (binaries included might not work on all systems, optionally
  put your own compiled binaries in the bin folder before installing).
- Optionally you need dot to compile pdf's from the generated dot file. Dot is
  a binary from the GraphViz package.

##### installation
Automatic installation:

	$ ./install\_lin
Manual installation:

copy the binaries to the bin folder and then copy all the contents of the
directory to the exact folder:

	${HOME}/.praat-dir/plugin_pralign


#### mac
##### requirements
same as linux

##### installation
Automatic installation:
	
	$ ./install\_mac
Manual installation:

copy the binaries to the bin folder and then copy all the contents of the
directy to the exact folder:

	${HOME}/Library/Preferences/Praat Prefs/plugin_pralign

#### windows
Not implemented yet. Also not planned for the very near future

### documentation
#### general information
When force aligning you need a model and a phonetizer/dictionary. Words that
can't be found in the dictionary and can't be phonetized will be put in a file
located at the plugin directory and is called 

	mis.txt

#### generate dictionary
This function can generate a missing words dictionary from a tier within a
TextGrid. To start the script do:
- Read TextGrid from file
- Select the TextGrid
- Press the button that says: *Generate dictionary*

Now there will be a form so that you can specify some parameters:
* **tiername**,

	Name for the tier to get the annotations from.
* **lang**, default: tze
	
	Language to phonetize in.
* **example**, default: False

	Create an example entry in the output dictionary.
* **tmp**, default: /tmp/

	Temporary file directory, this is the directory where praat stores the
	annotations so that the python script can read them.

When the form is accepted the script will ask for the path to write the
dictionary to, generate all the missing words and write them in the standard
dictionary format. When you want to use the dictionary later you just need to
fill in the phonetizations and select the dictionary file when force aligning.

#### interactive forced alignment
The plugin works very straight forward, say one wants to force align a tier in
a TextGrid file with a LongSound. To start the script do:
- Read TextGrid from file
- Read LongSound from file
- Select both
- Press the button that says: *Start interactive force alignment...*

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

#### non interactive forced alignment
This function is also very straight forword, to start the script do:
- Read TextGrid from file
- Read LongSound from file
- Select both
- Press the button that says: *Start non interactive force alignment*

Now there will also be a form with some parameter specification, all the
parameter options can be found in the interactive alignment section except the
following changes:
* **tiername**, 

	Name for the tier to align, this must contain the annotations matching the
	selected LongSound.
* **newtier**, default: align

	Name for the tier to put the aligned annotations in, if the tier exists it
	gets cleared out first.

When the form is accepted the praat program freezes and in the background the
alignment has started. This takes a while depending on the amount of
pronunciation variants and the amount of annotations. When it's finished it
shows a prompt. Note: you still have to save the TextGrid.

#### dictionary file
A dictionary file consists of several non emptylines character(\\n), lines
starting with a # will be ignored and can be used as comments. The dictionary
delivers the pronounciation and optional variants to the phonetizer and has to
be of the following format:

	word-1<TAB>pronounciation-1[<TAB>variant-1a][<TAB>variant-1b]...
	word-2<TAB>pronounciation-2[<TAB>variant-2a][<TAB>variant-2b]...
	...
	word-n<TAB>pronounciation-n[<TAB>variant-na][<TAB>variant-nb]...

#### ruleset file
Currently only interword rules are possible...  A ruleset file describes
certain rules that can be on inter and intraword level and uses python regular
expressions to achive this. It will tie the group named *to* to *from* so you
can easily describe deletion rules. A ruleset file is of the following format:

	regex-1
	regex-2
	...
	regex-n

Every regex must contain at minimal the named groups *to* and *from*.
For example the rule that will delete a *d* if it is between *a* and *o*
regardless of word boundaries:
	
	(?P<fr>a#?)d(?P<to>#?o)

#### customize/add language
##### Phonetizer
There is a skeleton model available for writing a new phonetizer, this has to
be done in python, implement the phonetizer and add your phonetizer to the
dictionary as a tuple with as second value a parameter directory called:

	./par.lan
Where lan is a three letter language code

##### Models
You can create your own models or use the given models(for example sampa
models). Note that in the phonetizer python file the connection between models
and languages is defined in the phonetizer dictionary.

##### Adapt the praat scripts
To add the language to the praat scripts you can just edit the file called

	languageselection.praat
This file is included in all the menus as the language selector, so just add
your language and note that the indentation must stay the same.

### todo
fix when the first alignment starts at time 0


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
