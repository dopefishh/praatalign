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
	wrd$ = extractLine$(settingsData$, "WRD: ")
	can$ = extractLine$(settingsData$, "CAN: ")
	llh$ = extractLine$(settingsData$, "LLH: ")
	lan$ = extractLine$(settingsData$, "LAN: ")
	if lan$ = "dut"
		lan = 1
	elif lan$ = "eng"
		lan = 2
	elif lan$ = "spa"
		lan = 3
	elif lan$ = "tze"
		lan = 4
	elif lan$ = "exp"
		lan = 5
	else
		lan = 3
	endif
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
	new$ = "align_phon"
	wrd$ = ""
	can$ = ""
	llh$ = ""
	lan = 3
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
	comment: "Name for the output tier(may already exist)"
	sentence: "new", new$
	
	comment: "Name for the output tier used for word level alignment"
	sentence: "wrd", wrd$

	comment: "Name for the output tier used for canonical pronunciation"
	sentence: "can", can$

	comment: "Name for the output tier used for log likelyhood values"
	sentence: "llh", llh$

	comment: "Select language."
	comment: "dut : Dutch"
	comment: "eng : English"
	comment: "spa : Spanish"
	comment: "tze : Tzeltal"
	comment: "exp : HIGHLY EXPERIMENTAL spanish"
	optionMenu: "lan", lan
		option: "dut"
		option: "eng"
		option: "spa"
		option: "tze"
		option: "exp"

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
..."LOG: ", log$, newline$,
..."LLH: ", llh$, newline$,
..."NEW: ", new$, newline$,
..."CAN: ", can$, newline$,
..."OUT: ", "praat_temp_out", newline$,
..."RUL: ", ruleset$, newline$,
..."SOX: ", soxex$, newline$,
..."THR: ", thr, newline$,
..."PY2: ", pythonex$, newline$,
..."WRD: ", wrd$)
