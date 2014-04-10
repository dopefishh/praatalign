### Interactive forced alignment in spontaneous speech, version 0.06

### Installation
#### Linux
##### Requirements
- Python 2[7.3]
- SoX (has to be in path)
- Praat
- HCopy and HVite (binaries included might not work on all systems, alternatively
  put your own compiled binaries in the bin folder before installing).
- Alternatively you need dot to compile pdf's from the generated dot file. Dot is
  a binary from the GraphViz package.

##### Installation
Automatic installation:

	$ ./install\_lin
Manual installation:

Copy the binaries to the bin folder and then copy the entire content of the
directory to the following folder:

	${HOME}/.praat-dir/plugin_pralign


#### Mac
##### Requirements
Same as linux

##### Installation
Automatic installation:
	
	$ ./install\_mac
Manual installation:

Copy the binaries to the bin folder and then copy the entire content of the
directory to the following folder:

	${HOME}/Library/Preferences/Praat Prefs/plugin_pralign

#### Windows
Not implemented yet. Also not planned for the immediate future.

### Documentation
#### General information
When force aligning you need a model and a phonetizer/dictionary. When a word can't be 
phonetized the script terminates prematurely.

#### Generate dictionary
This function can generate a dictionary of missing words from a tier within a
TextGrid. Do the following to start the script:
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

	Temporary file directory, this is the directory where Praat stores the
	annotations so that the Python script can read them.

When the form is accepted the script will ask for the path to which it will write the
dictionary. Praat will then generate all the missing words and write them into the standard
dictionary format. When you want to use the dictionary later you just need to
fill in the phonetizations and select the dictionary file when force aligning.

#### Interactive forced alignment
The plugin works very straight forward, say one wants to force align a tier in
a TextGrid file with a LongSound. Then do the following to start the script:
- Read TextGrid from file
- Read LongSound from file
- Select both
- Press the button that says: *Start interactive force alignment...*

Now there will be a form so that you can specify some parameters:
* **newtier**, default: align

	Name of the tier where the alignment is stored, this may be an existing
	tier. If the tier exists, the annotations within the selected interval are
	removed upon alignment.
* **lang**, default: tze

	Language to use for the forced alignment. Currently this is Spanish and Tzeltal, in the future
	one can add custom languages.
* **dictpath**, default: False

	Flag for selecting a custom dictionary. If this is not set, the aligner will
	rely completely on the phonetizer. If this is set, then a prompt follows to
	select the dictionary.
* **ruleset**, default: False

	Flag for using a ruleset file. If this is not set, the aligner will not use a 
	ruleset. If this is set, then a prompt follows to select the ruleset file.
* **pdf**, default: False

	Flag to export to pdf. If this is not set, the aligner will not create pdf
	files for the graphs it follows. If this is set, there will be a temp.pdf located in 
	this plugin folder after the alignment(on linux ~/.praat-dir/plugin_pralign
* **tmpdir**, default: /tmp/

	Temporary file directory. This is the directory where the aligner stores
	the semi-raw results from HTK.

When the form is accepted the TextGrid editor will be opened and a pause
window is spawned. When you select an annotation and press continue it will
align the annotation using the specified options.

#### Non-interactive forced alignment
This function is also very straight forward. Do the following to start the script:
- Read TextGrid from file
- Read LongSound from file
- Select both
- Press the button that says: *Start non interactive force alignment*

Now there will also be a form with some parameter specification. All the
parameter options can be found in the interactive alignment section except the
following changes:
* **tiername**, 

	Name for the tier to align. This must contain the annotations matching the
	selected LongSound.
* **newtier**, default: align

	Name for the tier to put the aligned annotations in. If the tier exists, it
	first gets cleared out.

When the form is accepted the praat program freezes and the alignment has started 
in the background. This takes a while depending on the amount of
pronunciation variants and the amount of annotations. When it's finished it
shows a prompt. Note: you still have to save the TextGrid.

#### Dictionary file
A dictionary file consists of several non-empty lines separated by a newline character(\\n). 
Lines starting with a # will be ignored and can be used as comments. The dictionary
delivers the pronounciation and optional variants to the phonetizer and has to
be of the following format:

	word-1<TAB>pronounciation-1[<TAB>variant-1a][<TAB>variant-1b]...
	word-2<TAB>pronounciation-2[<TAB>variant-2a][<TAB>variant-2b]...
	...
	word-n<TAB>pronounciation-n[<TAB>variant-na][<TAB>variant-nb]...

#### Ruleset file
Currently only inter-word rules are possible...  A ruleset file describes
certain rules that can be on inter- and intra-word level and uses Python regular
expressions to achive this. It will tie the group named *to* to *from*, so that you
can easily describe deletion rules. A ruleset file is of the following format:

	regex-1
	regex-2
	...
	regex-n

Every regex must contain at minimum the named groups *to* and *from*.
For example the rule that will delete a *d* if it is between *a* and *o*
regardless of word boundaries:
	
	(?P<fr>a#?)d(?P<to>#?o)

#### Customize/add language
##### Phonetizer
There is a skeleton model available for writing a new phonetizer. This has to
be done in Python. Implement the phonetizer and add your phonetizer to the
dictionary as a tuple with as second value a parameter directory called:

	./par.lan
Where lan is a three letter language code

##### Models
You can create your own models or use the given models(for example Sampa
models). Note that in the Python phonetizer file, the connection between models
and languages is defined in the phonetizer dictionary.

##### Adapt the Praat scripts
To add the language to the Praat scripts you can just edit the file called

	languageselection.praat
This file is included in all the menus as the language selector, so just add
your language and note that the indentation must stay the same.

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
