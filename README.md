Interactive forced alignment in spontaneous speech version 0.7
==============================================================

##Table of Contents
- [Table of contents](#table-of-contents)
- [Installation](#installation)
	- [Requirements](#requirements)
	- [Installation process](#installation-process)
		- [Preparation](#preparation)
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
	- [Scriptability](#scriptability)
	- [Add language](#add-language)
		- [Phonetizer](#phonetizer)
		- [Models](#models)
		- [Adapt the Praat scripts](#adapt-the-praat-scripts)
- [TODO](#todo)
- [How to cite](#how-to-cite)
- [Version history](#version-history)
- [Authors](#authors)

##Installation
###Requirements
- [Python 2.7.3](https://www.python.org/download/)
- [SoX](http://sox.sourceforge.net/)
- [Praat 5.4](http://www.fon.hum.uva.nl/praat)
- HCopy and HVite from the HTK toolkit. Due to licencing we can't provide the
  binaries. They are for free and you can download them after registering
	[here](http://htk.eng.cam.ac.uk/register.shtml). The aligner is tested with
	the following versions on windows, linux and mac.
	- [Windows binaries](http://htk.eng.cam.ac.uk/ftp/software/htk-3.3-windows-binary.zip)
	- [Sources](http://htk.eng.cam.ac.uk/ftp/software/HTK-samples-3.4.tar.gz)

###Installation process
####Preparation
- Linux: Put ``HVite`` and ``HCopy`` in the ``bin_lin`` folder.
- Mac: Put ``HVite`` and ``HCopy`` in the ``bin_mac`` folder.
- Windows: Put ``HVite.exe`` and ``HCopy.exe`` in the ``bin_win`` folder.

####Automatic installation
- Linux: Run ``install_lin.bat``
- Mac: Run ``install_mac.bat``
- Windows: Run ``install_win.bat``

####Manual installation
Put the HVite and HCopy binaries in the bin folder and copy all the contents of
the root folder to:

- Windows: ``%USERPROFILE%\Praat\plugin_pralign``
- Linux: ``${HOME}/.praat-dir/plugin_pralign``
- Mac: ``${HOME}/Praat Prefs/plugin_pralign``

##Documentation
###General information
Presets for Spanish, Tzeltal and Dutch are included. Presets for Australian
English, English, Estonian, German, Hungarian, Italian, Newzealang English
Polish and Portuguese will be added in the future. When you want a language
from the above list implemented with priority you can always contact us.

Dictionary, ruleset and all other files are, and should be, encoded in *UTF-8*.
That's why the plugin setup also sets the praat reading and writing preferences
to *UTF-8*.

###Menu Items
**NOTE: To align you need to select a LongSound and a TextGrid. Selecting a
Sound and a TextGrid will cause the program to fail.**

####Generate dictionary from tier...
This function will prompt for a file location to write alle the missing words
from the selected tier to. Missing words are words that are either not in the
dictionary or unable to be phonetized.
Note that the *Setup forced alignment...* has to be run at least once to create
the initial settings file. If this is not the case the program will generate an
error and terminate.

####Clean selection
With clean selection all the intervals that have overlap with the current
selection of the current selected tier will be removed. This can come in handy
to clean up a previous alignment of an interval.

####Align current interval
This force alignes the current selected interval against the wavefile with the
given settings. This will clear all the annotation data in the target tiers
before aligning.

Note that the *Setup forced alignment...* has to be run at least once to create
the initial settings file. If this is not the case the program will generate an
error and terminate.

####Align current tier
This force alignes the entire tier against the wavefile with the given
settings. This will clear the target tiers before aligning.

Note that the *Setup forced alignment...* has to be run at least once to create
the initial settings file. If this is not the case the program will generate an
error and terminate.

####Setup forced alignment...
This button will generate the config file for the forced aligner to work with
and must be used at least once before doing alignment for the first time. When
the spawned form is closed a settings file will be written to disk for later
use with the alignment.

The following options can be specified in the settings menu:
* **new**, default: align

	Name of the tier where the alignment is stored, this may be an existing
	tier. If the tier exists, the annotations within the selected interval are
	removed upon alignment.
* **wrd**, default: alignw

	Name of the tier where the alignment on word level is stored. If the tier
	exists, the annotations within the selected interval are removed upon
	alignment. Note that in theory this can be the same tier as the phone level
	tier. When this is the case a warning will be spawned everytime you align.
* **lan**, default: tze

	Language to use for the forced alignment. Currently this is Spanish, Tzeltal
  and Dutch. Custom added languages will also appear in the dropdown menu when
	properly added.
* **dic**, default: False

	Flag for selecting a custom dictionary. If this is not set, the aligner will
	rely completely on the phonetizer. If this is set, then a prompt follows to
	select the dictionary.
* **dictionary**, default: 

	This option only appears when a dictionary is already set and shows the
	current dictionary, when you want to select a new one just tick the ``dic``
	box again or change the path in this textfield.
* **thr**, default: 0
	
	When the sources are aligned with to short annotations you can append a
  number of seconds to the beginning and the end of every annotation you align
  with this value. When there is an empty annotation next to the annotation to
	align, this number of seconds is added to the annotation length. It does not
	change the original annotations.
* **pau**, default: False

	Flag to export to pdf. If this is not set, the aligner will not create pdf
	files for the graphs it follows. If this is set, there will be a temp.pdf
	located in this plugin folder after the alignment.
* **log**, default: /dev/null

	Path for the logfile, if /dev/null there will be no log. The main python core
	script will log some usefull things in here, especially when the praat script
	crashes on executing the system commands.
* **lgc**, default: True
	
	Append the logfile instead of rewriting it.
* **sox**, default: sox

	When sox is the the ``$PATH`` or ``%PATH%`` variable this doesn't need to be
	changed. When this is not the case you should put the exact path of the sox
	executable here. Note that for example ``.bashrc`` is not source in the
	script so the ``$PATH`` variable is not always the same as in an interactive
	shell.

###Dictionary file
A dictionary file consists of several non-empty lines separated by a newline
character(``\n``).  Lines starting with a ``#`` will be ignored and can be used
as comments. The dictionary delivers the pronounciation and optional variants
to the phonetizer and has to be of the following format:

	word-1\tpronounciation-1[\tvariant-1a][\tvariant-1b]...
	word-2\tpronounciation-2[\tvariant-2a][\tvariant-2b]...
	...
	word-n\tpronounciation-n[\tvariant-na][\tvariant-nb]...

###Ruleset file
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


###Scriptability
The settings menu is not scriptable because it uses pause dialogs instead of
forms, because of this there is a settings script available that is scriptable.
For example if you want to setup a non interactive environment you can run this:
 
	runScript: "/home/frobnicator/.praat-dir/plugin_pralign/settings_ni.praat",
	..."custom_phone_tier", "custom_word_tier", "/some/path/to/dict",
	..."/some/path/to/ruleset", 0, "tze", "no", "/some/path/to/logfile", "a",
	..."/usr/bin/sox"

###Add language
####Phonetizer
There is a skeleton model available for writing a new phonetizer. This has to
be done in Python. Implement the phonetizer and add your phonetizer to the
dictionary as a tuple with as second value a parameter directory called:

	./par.lan
Where lan is a three letter language code

####Models
You can create your own models or use the given models(for example Sampa
models). Note that in the Python phonetizer file, the connection between models
and languages is defined in the phonetizer dictionary at the bottom of the
file.

####Adapt the Praat scripts
To add the language to the Praat scripts you have to edit ``settings.praat``
and add your language in the option menu on line ``53`` and in the big
selection statement on line ``18``

##Version history

| Version | Date | Version notes |
|--|--|--|
| | 0.7| 2014-10-29 | - Added windows support. |
| | | - Cleaned up documentation. |
| | | - Removed binaries due htk licence. |

- 0.6  - 2014-10-22 - Refactored and cleaned up the source, much more readable
  now
- 0.5a - 2014-09-08 - Added comments to source code(praat) and cleaned up
- 0.5  - 2014-09-04 - Fixed acronyms in spanish and cleaning didn't work
  correctly with extended boundaries for Align current interval, that's fixed
	too. Added rudimentary ruleset implemetation, still have to write a readme
	for this
- 0.4  - 2014-08-29 - Added option for enlargening the boundaries automatically
- 0.21 - 2014-08-13 - Settings split in non interactive and interactive so that
  the interactive one reflects the current settings
- 0.2  - 2014-08-11 - Better mac compatibility
- 0.1a - 2014-06-30 - Tier alignment fixed, dutch added
- 0.08 - 2014-04-29 - Cleaned up some stuff, added dutch and readmes to spanish
  and sampa
- 0.07 - 2014-04-28 - non interactive done and toc in readme
- 0.06 - 2014-04-25 - conversion to editor scripts. non-interactive has work to
  do
- 0.05 - 2014-04-03 - better readme and functional program for linux
- 0.04 - 2014-04-03 - pronounciation variants implemented
- 0.03 - 2014-03-31 - aligner works, praat imlementation needs work
- 0.02 - 2014-03-27 - started with aligner
- 0.01 - 2014-03-27 - phonetizer done
- 0.00 - 2014-03-27 - initial version

##TODO
- Make slf creating faster. Or at least make the advanced slf generation
  optional.
- Test more thoroughly on windows.

##How to cite
	
	Lubbers, M. (2014) Praatalign (Version 0.6) [Computer program].
	Available at https://github.com/dopefishh/praatalign (Accessed 2014-10-29)``

##Authors
- Programming: Mart Lubbers (mart@martlubbers.net)
- Supervision: Francisco Torreira (francisco.torreira@mpi.nl)
- Testing: Emma Valtersson (emma.valtersson@gmail.com)
