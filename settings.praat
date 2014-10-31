# If the settings is already present extract all the entries
if fileReadable("settings")
	settingsData$ = readFile$("settings")
	dictionary$ = extractLine$(settingsData$, "DCT: ")
	if dictionary$ = "None"
		dictionary$ = ""
	endif
	ruleset$ = extractLine$(settingsData$, "RUL: ")
	if ruleset$ = "None"
		ruleset$ = ""
	endif
	new$ = extractLine$(settingsData$, "NEW: ")
	wrd$ = extractLine$(settingsData$, "WRD: ")
	lan$ = extractLine$(settingsData$, "LAN: ")
	if lan$ = "tze"
		lan = 1
	elif lan$ = "spa"
		lan = 2
	elif lan$ = "dut"
		lan = 3
	else
		lan = 1
	endif
	log$ = extractLine$(settingsData$, "LOG: ")
	if extractLine$(settingsData$, "LGC: ") = "a"
		lgc = 1
	else
		lgc = 0
	endif
	soxex$ = extractLine$(settingsData$, "SOX: ")
	hviteex$ = extractLine$(settingsData$, "HVB: ")
	hcopyex$ = extractLine$(settingsData$, "HCB: ")
	thr = extractNumber(settingsData$, "THR: ")
# If the settings isn't present initialize everything
else
	dictionary$ = ""
	ruleset$ = ""
	new$ = "align_phon"
	wrd$ = "align_word"
	lan = 1
	if windows
		log$ = "nul"
	else
		log$ = "/dev/null"
	endif
	lgc = 1
	soxex$ = "sox"
	hviteex$ = "HVite"
	hcopyex$ = "HCopy"
	thr = 0
endif

# Spawn the option window for the user
beginPause: "Set the variables"
	comment: "Name for the output tier(may already exist)"
	sentence: "new", new$
	
	comment: "Name for the output tier used for word level alignment"
	sentence: "wrd", wrd$

	comment: "Select language"
	optionMenu: "lan", lan
		option: "tze"
		option: "spa"
		option: "dut"

	comment: "Select a dictionary when pressing apply"
	boolean: "dic", 0
	if dictionary$ <> ""
		sentence: "dictionary", dictionary$
	endif

	comment: "Select a ruleset file when pressing apply"
	boolean: "rul", 0
	if ruleset$ <> ""
		sentence: "ruleset", ruleset$
	endif

	comment: "Set the length of the added length to the annotations"
	real: "thr", thr

	comment: "Developer/debug options"
	sentence: "log", log$

	comment: "Select sox executable location when pressing apply"
	boolean: "sox", 0
	if soxex$ <> "sox"
		sentence: "soxex", soxex$
	endif

	comment: "Select HVite executable location when pressing apply"
	boolean: "hvite", 0
	if hviteex$ <> "HVite"
		sentence: "hviteex", hviteex$
	endif
	
	comment: "Select HCopy executable location when pressing apply"
	boolean: "hcopy", 0
	if hcopyex$ <> "HCopy"
		sentence: "hcopyex", hcopyex$
	endif
endPause: "Apply", 1

# Process the special options and optionally ask for filepaths
lgc$ = if lgc then "a" else "w" fi

# Ask for the dictionary
if dic
	beginPause: "Instructions"
		comment: "Please point me to the dictionary file."
		comment: "The format for such file can be found in the README.html"
		comment: "Dictionary skeletons can be generated with Generate dictionary from tier..."
	clicked = endPause: "Cancel", "Continue", 2, 1
	if clicked = 2
		dictionary$ = chooseReadFile$("Point me to the dictionary file")
	endif
endif
if dictionary$ = ""
	dictionary$ = "None"
endif

# Ask for the ruleset
if rul
	beginPause: "Instructions"
		comment: "Please point me to the ruleset file."
		comment: "The format for such file can be found in the README.html"
	clicked = endPause: "Cancel", "Continue", 2, 1
	if clicked = 2
		ruleset$ = chooseReadFile$("Point me to the ruleset file")
	endif
endif
if ruleset$ = ""
	ruleset$ = "None"
endif

pathstring$ = if windows then "%PATH%" else "$PATH" fi
messagesox$ = if windows then "C:\Program Files" else "/usr/bin" fi
messagehtk$ = if windows then
... "where you unzipped the file pointed out in README.html" else
... "where you downloaded or compiled the executables" fi
# Ask for the sox executable
if sox
	beginPause: "Instructions"
		comment: "Please point me to the sox executable."
		comment: "When sox is in your 'pathstring$' you can cancel this."
		comment: "It can usually be found in 'messagesox$'"
	clicked = endPause: "Cancel", "Continue", 2, 1
	if clicked = 2
		soxex$ = chooseReadFile$("Point me to the sox executable")
	endif
endif
if soxex$ = ""
	soxex$ = "sox"
endif

# Ask for the HVite executable
if hvite
	beginPause: "Instructions"
		comment: "Please point me to the HVite executable."
		comment: "When HVite is in your 'pathstring$' you can cancel this."
		comment: "It can be found 'messagehtk$'"
	clicked = endPause: "Cancel", "Continue", 2, 1
	if clicked = 2
		hviteex$ = chooseReadFile$("Point me to the HVite executable")
	endif
endif
if hviteex$ = ""
	hviteex$ = "HVite"
endif

# Ask for the HCopy executable
if hcopy
	beginPause: "Instructions"
		comment: "Please point me to the HCopy executable."
		comment: "When HCopy is in your 'pathstring$' you can cancel this."
		comment: "It can be found 'messagehtk$'"
	clicked = endPause: "Cancel", "Continue", 2, 1
	if clicked = 2
		hcopyex$ = chooseReadFile$("Point me to the HCopy executable")
	endif
endif
if hcopyex$ = ""
	hcopyex$ = "HCopy"
endif

# Delete the original settings file and write the new one
deleteFile("settings")
writeFileLine("settings",
..."DCT: ", dictionary$, newline$,
..."HCB: ", hcopyex$, newline$,
..."HVB: ", hviteex$, newline$,
..."LAN: ", lan$, newline$,
..."LOG: ", log$, newline$,
..."NEW: ", new$, newline$,
..."OUT: ", "praat_temp_out", newline$,
..."RUL: ", ruleset$, newline$,
..."SOX: ", soxex$, newline$,
..."THR: ", thr, newline$,
..."WRD: ", wrd$)
