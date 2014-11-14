Interactive forced alignment in spontaneous speech version 0.9
==============================================================

## <a name="table-of-contents"></a>Table of Contents
- [Table of contents](#table-of-contents)
- [Installation](#installation)
	- [Requirements](#requirements)
	- [Automatic installation](#automatic-installation)
	- [Manual installation](#manual-installation)
- [Documentation](#documentation)
	- [General information](#general-information)
	- [Menu items](#menu-items)
		- [Generate dictionary from tier](#generate-dictionary-from-tier)
		- [Clean selection](#clean-selection)
		- [Align current interval](#align-current-interval)
		- [Align current tier](#align-current-tier)
		- [Setup forced alignment](#setup-forced-alignment)
	- [Dictionary file](#dictionary-file)
	- [Ruleset file](#ruleset-file)
	- [Supported languages](#supported-languages)
		- [Dutch](#sl-dutch)
		- [English](#sl-english)
		- [Spanish](#sl-spanish)
		- [Tzeltal](#sl-tzeltal)
	- [Scriptability](#scriptability)
	- [Add language](#add-language)
		- [Phonetizer](#phonetizer)
		- [Models](#models)
		- [Adapt the Praat scripts](#adapt-the-praat-scripts)
- [TODO](#todo)
- [How to cite](#how-to-cite)
- [Authors](#authors)
- [Version history](#version-history)

## <a name="installation"></a>Installation<a href="#table-of-contents">↑</a>
### <a name="requirements"></a>Requirements<a href="#table-of-contents">↑</a>
- [Python 2.7.3](https://www.python.org/download/)
- [SoX](http://sox.sourceforge.net/)
- [Praat 5.4](http://www.fon.hum.uva.nl/praat)
- HCopy and HVite from the HTK toolkit. Due to licencing we can't provide the
  binaries. They are for free and you can download them after registering
	[here](http://htk.eng.cam.ac.uk/register.shtml). The aligner is tested with
	the following versions on windows, linux and mac.
	- [Windows binaries](http://htk.eng.cam.ac.uk/ftp/software/htk-3.3-windows-binary.zip)
	- [Sources](http://htk.eng.cam.ac.uk/ftp/software/HTK-samples-3.4.tar.gz)

### <a name="automatic-installation"></a>Automatic installation<a href="#table-of-contents">↑</a>
- Linux: Run ``install_lin``
- Mac: Run ``install_mac``
- Windows: Run ``install_win.bat``

### <a name="manual-installation"></a>Manual installation<a href="#table-of-contents">↑</a>
Put the HVite and HCopy binaries in the bin folder and copy all the contents of
the root folder to:

- Windows: ``%USERPROFILE%\Praat\plugin_pralign``
- Linux: ``${HOME}/.praat-dir/plugin_pralign``
- Mac: ``${HOME}/Praat Prefs/plugin_pralign``

## <a name="documentation"></a>Documentation<a href="#table-of-contents">↑</a>
### <a name="general-information"></a>General information<a href="#table-of-contents">↑</a>
Presets for Spanish, Tzeltal, English and Dutch are included. Presets for
Australian English, Estonian, German, Hungarian, Italian, Newzealand English
Polish and Portuguese will be added in the future. When you want a language
from the above list implemented with priority you can always contact us.

Dictionary, ruleset and all other files are, and should be, encoded in *UTF-8*.
That's why the plugin setup also sets the praat reading and writing preferences
to *UTF-8*.

### <a name="menu-items"></a>Menu Items<a href="#table-of-contents">↑</a>
**NOTE: To align you need to select a LongSound and a TextGrid. Selecting a
Sound and a TextGrid will cause the program to fail.**

#### <a name="generate-dictionary-from-tier"></a>Generate dictionary from tier...<a href="#table-of-contents">↑</a>
This function will prompt for a file location to write alle the missing words
from the selected tier to. Missing words are words that are either not in the
dictionary or unable to be phonetized.
Note that the *Setup forced alignment...* has to be run at least once to create
the initial settings file. If this is not the case the program will generate an
error and terminate.

#### <a name="clean-selection"></a>Clean selection<a href="#table-of-contents">↑</a>
With clean selection all the intervals that have overlap with the current
selection of the current selected tier will be removed. This can come in handy
to clean up a previous alignment of an interval.

#### <a name="align-current-interval"></a>Align current interval<a href="#table-of-contents">↑</a>
This force alignes the current selected interval against the wavefile with the
given settings. This will clear all the annotation data in the target tiers
before aligning.

Note that the *Setup forced alignment...* has to be run at least once to create
the initial settings file. If this is not the case the program will generate an
error and terminate.

#### <a name="align-current-tier"></a>Align current tier<a href="#table-of-contents">↑</a>
This force alignes the entire tier against the wavefile with the given
settings. This will clear the target tiers before aligning.

Note that the *Setup forced alignment...* has to be run at least once to create
the initial settings file. If this is not the case the program will generate an
error and terminate.

#### <a name="setup-forced-alignment"></a>Setup forced alignment...<a href="#table-of-contents">↑</a>
This button will generate the config file for the forced aligner to work with
and must be used at least once before doing alignment for the first time. When
the spawned form is closed a settings file will be written to disk for later
use with the alignment.

The following options can be specified in the settings menu:

<table style="border-collapse: collapse; border: 1px solid #C0C0C0;">
	<tr><th>Name</th><th>default</th><th>Description</th></tr>
	<tr><td>new</td><td>align</td><td>
			Name of the tier where the phone alignment is stored.<br/>
			This may be an existing tier. If the tier exists, the annotations within
			the selected interval are	removed upon alignment.
	</td></tr><tr><td>wrd</td><td>alignw</td><td>
			Name of the tier where the word alignment is stored.<br/>
			If the tier exists, the annotations within the selected interval are
			removed upon alignment. Note that in theory this can be the same tier as
			the phone level tier. When this is the case a warning will be spawned
			everytime you align.
	</td></tr><tr><td>lan</td><td>tze</td><td>
			Language to use for the forced alignment.<br/>
			Currently this is Spanish, Tzeltal and Dutch. Custom added languages will
			also appear in the dropdown menu when properly added.
	</td></tr><tr><td>dic</td><td>False</td><td>
			Flag for selecting a custom dictionary.<br/>
			If this is not set, the aligner will rely completely on the phonetizer.
			If this is set, then a prompt follows to select the dictionary.
	</td></tr><tr><td>dictionary</td><td></td><td>
			Current dictionary location.<br/>
			This option only appears when a dictionary is already set and shows the
			current dictionary, when you want to select a new one just tick the
			<code>dic</code> box again or change the path in this textfield.
	</td></tr><tr><td>rul</td><td>False</td><td>
			Flag for selecting a custom ruleset.<br/>
			If this is set, then a prompt follows to select the ruleset.
	</td></tr><tr><td>ruleset</td><td></td><td>
			Current ruleset location.<br/>
			This option only appears when a ruleset is already set and shows the
			current ruleset, when you want to select a new one just tick the
			<code>rul</code> box again or change the path in this textfield.
	</td></tr><tr><td>thr</td><td>0</td><td>
			Extra margin for all annotations.<br/>
			When the sources are aligned with to short annotations you can append a
			number of seconds to the beginning and the end of every annotation you
			align with this value. When there is an empty annotation next to the
			annotation to align, this number of seconds is added to the annotation
			length. It does not change the original annotations.
	</td></tr><tr><td>log</td><td>/dev/null or<br/>null</td><td>
			Path for the logfile.<br/>
			If <code>/dev/null</code>(<code>nul</code> on windows) there will be no
			log. The main python core script will log some usefull things in here,
			especially when the praat script crashes on executing the system
			commands.
	</td></tr><tr><td>sox</td><td>False</td><td>
			Flag for selecting a custom <code>sox</code> location.<br/>
			If this is set, then a prompt follows to select the <code>sox</code>
			executable. When <code>sox</code> is the the <code>$PATH</code> or
			<code>%PATH%</code> variable this doesn't need to be changed.
	</td></tr><tr><td>soxex</td><td>sox</td><td>
			Current custom <code>sox</code> location.<br/>
			When sox is the the <code>$PATH</code> or <code>%PATH%</code> variable
			this doesn't need to be changed. When this is not the case you should put
			the exact path of the sox executable here. Note that for example
			<code>.bashrc</code> is not source in the script so the
			<code>$PATH</code> variable is not always the same as in an interactive
			shell.
	</td></tr><tr><td>hvite</td><td>False</td><td>
			Flag for selecting a custom <code>HVite</code> location.<br/>
			If this is set, then a prompt follows to select the <code>HVite</code>
			executable. When <code>HVite</code> is the the <code>$PATH</code> or
			<code>%PATH%</code> variable this doesn't need to be changed.
	</td></tr><tr><td>hviteex</td><td>HVite</td><td>
			Current custom <code>HVite</code> location.<br/>
			This options only appears when a custom <code>HVite</code> location is
			already set and shows the current location, when you want to select a new
			one just tick the <code>hvite</code> box again or change the path in this
			textfield.
	</td></tr><tr><td>hcopy</td><td>False</td><td>
			Flag for selecting a custom <code>HCopy</code> location.<br/>
			If this is set, then a prompt follows to select the <code>HCopy</code>
			executable. When <code>HCopy</code> is the the <code>$PATH</code> or
			<code>%PATH%</code> variable this doesn't need to be changed.
	</td></tr><tr><td>hcopyex</td><td>HCopy</td><td>
			Current custom <code>HCopy</code> location.<br/>
			This options only appears when a custom <code>HCopy</code> location is
			already set and shows the current location, when you want to select a new
			one just tick the <code>hcopy</code> box again or change the path in this
			textfield.
		</td>
	</tr>
</table>

### <a name="dictionary-file"></a>Dictionary file<a href="#table-of-contents">↑</a>
A dictionary file consists of several non-empty lines separated by a newline
character(``\n``).  Lines starting with a ``#`` will be ignored and can be used
as comments. The dictionary delivers the pronounciation and optional variants
to the phonetizer and has to be of the following format:

	word-1\tpronounciation-1[\tvariant-1a][\tvariant-1b]...
	word-2\tpronounciation-2[\tvariant-2a][\tvariant-2b]...
	...
	word-n\tpronounciation-n[\tvariant-na][\tvariant-nb]...

### <a name="ruleset-file"></a>Ruleset file<a href="#table-of-contents">↑</a>
A ruleset file consists of several non-empty lines separated by a newline
character(``\n``). Lines starting with a ``#`` will be ignored and can be used
as comments. A ruleset file can provide pronunciation variants in a rule based
manner. This will use python's regular expression functions to apply the rules.
An example ruleset that describes a deletion of ``d`` when between ``a`` and
``o`` and a deletion of ``s`` when preceeded by an ``o``(and optional word
boundary) and succeeded by two vowels.

	(?P<fr>a)d(?P<to>o)
	(?P<fr>o#?>s(?P<to>\v\v)

Possible escapes are:

- ``\v`` for vowels(``[aoeiu]``)
- ``\c`` for consonants(``[^aoeui]``)

### <a name="supported-languages"></a>Supported languages<a href="#table-of-contents">↑</a>
Different languages vary in usage because of for example phonetizing
possibilities and dictionaries. The following sections describe briefly what
you need to phonetize in that language.

####<a name="sl-dutch"></a>Dutch<a href="#table-of-contents">↑</a>
Dutch is not phonetizable and therefore you need:
- TextGrid with utterance level alignment.
- Dictionary containing all the words and their pronunciation variants. The
  possible phones can be found in ``./par.dut/readme.txt``.
- *Optional* ruleset to define pronunciation variants.

####<a name="sl-english"></a>English<a href="#table-of-contents">↑</a>
English is not phonetizable and also hard to make a dictionary. Therefore we
need:
- TextGrid with the utterance level alignment. The possible phones can be
	found in ``./par.eng/readme.txt``.
- Dictionary containing all the words and their pronunciation variants. The
	possible phones can be found in ``./par.eng/readme.txt``. A conversion script
	can be found in the ``./par.eng/`` directory to convert the 
	[cmu dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) to the
	praatalign format.
- *Optional* ruleset to define pronunciation variants.

####<a name="sl-spanish"></a>Spanish<a href="#table-of-contents">↑</a>
Spanish is almost entirely phonetizable therefore you need:
- TextGrid with utterance level alignment.
- *Optional* dictionary that contains foreign words and other unphonetizable
  words. The possible phones can be found in ``./par.spa/readme.txt``.
- *Optional* ruleset that contains pronunciation variants.

####<a name="sl-tzeltal"></a>Tzeltal<a href="#table-of-contents">↑</a>
Tzeltal is almost entirely phonetizable therefore you need:
- TextGrid with utterance level alignment.
- *Optional* dictionary that contains foreign words and other unphonetizable
  words. The possible phones can be found in ``./par.sam/readme.txt``.
- *Optional* ruleset that contains pronunciation variants.

### <a name="scriptability"></a>Scriptability<a href="#table-of-contents">↑</a>
The settings menu is not scriptable because it uses pause dialogs instead of
forms, because of this there is a settings script available that is scriptable.
For example if you want to setup a non interactive environment you can run this:
 
	runScript: "/home/frobnicator/.praat-dir/plugin_pralign/settings_ni.praat",
	..."custom_phone_tier", "custom_word_tier", "/some/path/to/dict",
	..."/some/path/to/ruleset", 0, "tze", "no", "/some/path/to/logfile",
	..."/usr/bin/sox", "/usr/bin/HVite", "/usr/bin/HCopy"

### <a name="add-language"></a>Add language<a href="#table-of-contents">↑</a>
#### <a name="phonetizer"></a>Phonetizer<a href="#table-of-contents">↑</a>
There is a skeleton model available for writing a new phonetizer. This has to
be done in Python. Implement the phonetizer and add your phonetizer to the
dictionary as a tuple with as second value a parameter directory called: 
``./par.XXX``. Where ``XXX`` is a three letter language code .

#### <a name="models"></a>Models<a href="#table-of-contents">↑</a>
You can create your own models or use the given models(for example Sampa
models). Note that in the Python phonetizer file, the connection between models
and languages is defined in the phonetizer dictionary at the bottom of the
file.

#### <a name="adapt-the-praat-scripts"></a>Adapt the Praat scripts<a href="#table-of-contents">↑</a>
To add the language to the program you have to add the entry in:
- ``phonetizer.py`` in the bottom you have to add the entry to
  ``phonetizerdict`` dictionary that maps names of languages to Phonetizer
	subclasses.
- ``settings.praat`` in the menu parsing of the options around line ``15`` you
  have to edit the entries so that the names match the indices again. Also
	within the ``beginPause`` block you have to add your language to the
	optionmenu that succeeds the comment block ``comment: "Select language"``

## <a name="todo"></a>TODO<a href="#table-of-contents">↑</a>
- Make slf creating faster. Or at least make the advanced slf generation
  optional.
- Test more thoroughly on windows.
- Make tutorials for non cs people.

## <a name="how-to-cite"></a>How to cite<a href="#table-of-contents">↑</a>
Bibtex:

	@misc{praatalign,
		author={Lubbers, Mart and Torreira, Francisco},
		title={Praatalign: an interactive Praat plug-in for performing phonetic forced alignment},
		howpublished={\url{https://github.com/dopefishh/praatalign}},
		year={2013-2014},
		note={Version 0.9}
	}

## <a name="authors"></a>Authors<a href="#table-of-contents">↑</a>
- Programming: Mart Lubbers (mart@martlubbers.net)
- Supervision: Francisco Torreira (francisco.torreira@mpi.nl)
- Testing: Emma Valtersson (emma.valtersson@gmail.com)

## <a name="version-history"></a>Version history<a href="#table-of-contents">↑</a>
- 0.9
	- Cleaned up some parts of the readme.
	- Added language specific information.
	- Added english as language. Although there is no phonetizing implemented.
	- README.html better with light background for code blocks.
	- Updated citing method with bibtex.
- 0.8 (2014-10-31)
	- Removed all the binary folders.
	- Made the binary finding interactive.
	- Made all the file chooser dialogs interactive.
- 0.7 (2014-10-29)
	- Added windows support.
	- Cleaned up documentation.
	- Removed binaries due htk licence.
- 0.6 (2014-10-22)
	- Refactored and cleaned up the source.
- 0.5a (2014-09-08)
	- Added comments to source code(praat).
	- Cleaned up source.
- 0.5 (2014-09-04)
	- Fixed acronyms in spanish.
	- Fixed cleaning with extended boundaries.
	- Added rudimentary ruleset implementatien.
- 0.4 (2014-08-29)
	- Added option for enlargening the boundaries automatically.
- 0.21 (2014-08-13)
	- Settings split in non interactive and interactive so that the interactive one reflects the current settings.
- 0.2 (2014-08-11)
	- Better mac compatibility.
- 0.1a (2014-06-30)
	- Tier alignment fixed.
	- Readme for dutch.
- 0.08 (2014-04-29)
	- Cleaned up some stuff.
	- Added dutch.
	- Readme for spanish and sampa.
- 0.07 (2014-04-28)
	- Non interactive alignment implemented.
	- Table of contents in readme.
- 0.06 (2014-04-25)
	- Conversion to editor scripts.
- 0.05 (2014-04-03)
	- Better readme.
	- Functional program for linux.
- 0.04 (2014-04-03)
	- Pronounciation variants implemented.
- 0.03 (2014-03-31)
	- Aligner works in python.
- 0.02 (2014-03-27)
	- Python script around aligner started.
	- Phonetizer skeleton done
