include procs.praat

pythonexecutablename$ = if windows then "python.exe" else "python" fi
hcopyexecutablename$ = if windows then "HCopy.exe" else "HCopy" fi
hviteexecutablename$ = if windows then "HVite.exe" else "HVite" fi
soxexecutablename$ = if windows then "sox.exe" else "sox" fi
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
	ort$ = extractLine$(settingsData$, "ORT: ")
	wrd$ = extractLine$(settingsData$, "WRD: ")
	can$ = extractLine$(settingsData$, "CAN: ")
	llh$ = extractLine$(settingsData$, "LLH: ")
	phonetizer$ = extractLine$(settingsData$, "PHO: ")
	if phonetizer$ = "None"
		phonetizer$ = ""
	endif
	pho = 0
	lan$ = extractLine$(settingsData$, "LAN: ")
	if lan$ = "spanish"
		lan = 1
	elif lan$ = "tzeltal"
		lan = 2
	elif lan$ = "universal"
		lan = 3
	elif lan$ = "none"
		lan = 4
	else
		lan = 1
	endif
	model$ = extractLine$(settingsData$, "MOD: ")
	if model$ = "spanish"
		model = 1
	elif model$ = "dutch"
		model = 2
	elif model$ = "english"
		model = 3
	elif model$ = "sampa"
		model = 4
	else
		model = 1
	endif
	pho = 0
	log$ = extractLine$(settingsData$, "LOG: ")
	soxex$ = extractLine$(settingsData$, "SOX: ")
	hviteex$ = extractLine$(settingsData$, "HVB: ")
	hcopyex$ = extractLine$(settingsData$, "HCB: ")
	pythonex$ = extractLine$(settingsData$, "PY2: ")
	thr = extractNumber(settingsData$, "THR: ")
# If the settings isn't present initialize everything
else
	dictionary$ = ""
	ruleset$ = ""
	new$ = "phon"
	ort$ = ""
	wrd$ = ""
	can$ = ""
	llh$ = ""
	lan = 1
	phonetizer$ = ""
	pho = 0
	model = 1
	if windows
		log$ = "nul"
	else
		log$ = "/dev/null"
	endif
	soxex$ = soxexecutablename$
	hviteex$ = hviteexecutablename$
	hcopyex$ = hcopyexecutablename$
	pythonex$ = pythonexecutablename$
	thr = 0
endif

# Spawn the option window for the user
beginPause: "Basic options"
	comment: "Praatalign version 2.0a"
	comment: "Name for the output tier(may already exist)"
	sentence: "new", new$

	comment: "Name for the output tier used for orthographic word level alignment"
	sentence: "ort", ort$
	
	comment: "Name for the output tier used for word level alignment"
	sentence: "wrd", wrd$

	comment: "Name for the output tier used for canonical pronunciation"
	sentence: "can", can$

	comment: "Name for the output tier used for log likelyhood values"
	sentence: "llh", llh$

	comment: "Select model"
	optionMenu: "model", model
		option: "spanish"
		option: "dutch"
		option: "english"
		option: "sampa"

	comment: "Select phonetizer"
	optionMenu: "lan", lan
		option: "spanish"
		option: "tzeltal"
		option: "universal"
		option: "none"

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

	if phonetizer$ <> ""
		comment: "Select a phonetizer file when pressing apply"
		comment: "This always happens if you use the universal phonetizer"
		boolean: "pho", 0
		sentence: "phonetizer", phonetizer$
	endif

	comment: "Set the length of the added length to the annotations"
	real: "thr", thr
endPause: "Apply", 1

beginPause: "Advanced options"
	comment: "Developer/debug options"
	sentence: "log", log$

	comment: "Select sox executable location when pressing apply"
	boolean: "sox", 0
	if soxex$ <> soxexecutablename$
		sentence: "soxex", soxex$
	endif

	comment: "Select HVite executable location when pressing apply"
	boolean: "hvite", 0
	if hviteex$ <> hviteexecutablename$
		sentence: "hviteex", hviteex$
	endif
	
	comment: "Select HCopy executable location when pressing apply"
	boolean: "hcopy", 0
	if hcopyex$ <> hcopyexecutablename$
		sentence: "hcopyex", hcopyex$
	endif

	comment: "Select python executable location when pressing apply"
	boolean: "python", 0
	if pythonex$ <> pythonexecutablename$
		sentence: "pythonex", pythonex$
	endif
endPause: "Apply", 1

if (phonetizer$ == "" and lan$ == "universal") or pho
	beginPause: "Instructions"
		comment: "Please point me to the universal phonetizer file."
		comment: "The format for such file can be found in the manual"
	clicked = endPause: "Cancel", "Continue", 2, 1
	if clicked = 2
		phonetizer$ = chooseReadFile$("Point me to the phonetizer file")
	endif
	if phonetizer$ = ""
		pause The plugin will probably malfunction since you didn't select a file.
	endif
endif
if phonetizer$ = ""
	phonetizer$ = "None"
endif

# Ask for the dictionary
if dic
	beginPause: "Instructions"
		comment: "Please point me to the dictionary file."
		comment: "The format for such file can be found in the manual"
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
		comment: "The format for such file can be found in the manual"
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
messagepy$ = if windows then "C:\Python27\" else "/usr/bin" fi
messagehtk$ = if windows then
... "where you unzipped the file pointed out in README.html" else
... "where you downloaded or compiled the executables" fi

@getBinary: messagesox$, pathstring$, soxexecutablename$, sox
soxex$ = if getBinary.ex$ <> "" then getBinary.ex$ else soxex$ fi

@getBinary: messagehtk$, pathstring$, hviteexecutablename$, hvite
hviteex$ = if getBinary.ex$ <> "" then getBinary.ex$ else hviteex$ fi

@getBinary: messagehtk$, pathstring$, hcopyexecutablename$, hcopy
hcopyex$ = if getBinary.ex$ <> "" then getBinary.ex$ else hcopyex$ fi

@getBinary: messagepy$, pathstring$, pythonexecutablename$, python
pythonex$ = if getBinary.ex$ <> "" then getBinary.ex$ else pythonex$ fi

# Delete the original settings file and write the new one
deleteFile("settings")
writeFileLine("settings",
..."DCT: ", dictionary$, newline$,
..."HCB: ", hcopyex$, newline$,
..."HVB: ", hviteex$, newline$,
..."LAN: ", lan$, newline$,
..."MOD: ", model$, newline$,
..."PHO: ", phonetizer$, newline$,
..."LOG: ", log$, newline$,
..."LLH: ", llh$, newline$,
..."NEW: ", new$, newline$,
..."CAN: ", can$, newline$,
..."ORT: ", ort$, newline$,
..."OUT: ", "praat_temp_out", newline$,
..."RUL: ", ruleset$, newline$,
..."SOX: ", soxex$, newline$,
..."THR: ", thr, newline$,
..."PY2: ", pythonex$, newline$,
..."WRD: ", wrd$)
