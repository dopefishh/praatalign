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
	if extractLine$(settingsData$, "PAU: ") = "True"
		pau = 1
	else
		pau = 0
	endif
#	tmp$ = extractLine$(settingsData$, "TMP: ")
	log$ = extractLine$(settingsData$, "LOG: ")
	if extractLine$(settingsData$, "LGC: ") = "a"
		lgc = 1
	else
		lgc = 0
	endif
	sox$ = extractLine$(settingsData$, "SOX: ")
	thr = extractNumber(settingsData$, "THR: ")
# If the settings isn't present initialize everything
else
	dictionary$ = ""
	ruleset$ = ""
	new$ = "align_phon"
	wrd$ = "align_word"
	lan = 1
	pau = 1
#	tmp$ = ""
	if windows
		log$ = "nul"
	else
		log$ = "/dev/null"
	endif
	lgc = 1
	sox$ = "sox"
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
		comment: "Current dictionary"
		sentence: "dictionary", dictionary$
	endif

	comment: "Select a ruleset file when pressing apply"
	boolean: "rul", 0
	if ruleset$ <> ""
		comment: "Current ruleset"
		sentence: "ruleset", ruleset$
	endif

	comment: "Set the length of the added length to the annotations"
	real: "thr", thr

	comment: "Pause first when aligning tier"
	boolean: "pau", pau

#	comment: "Temporary directory"
#	sentence: "tmp", tmp$

	comment: "Developer/debug options"
	sentence: "log", log$
	comment: "Append to log"
	boolean: "lgc", lgc
	comment: "Sox path"
	sentence: "sox", sox$
endPause: "Apply", 1

# Process the special options and optionally ask for filepaths
pau$ = if pau then "True" else "False" fi
lgc$ = if lgc then "a" else "w" fi
if dic
	dictionary$ = chooseReadFile$("Open the dictionary")
else
	if dictionary$ = ""
		dictionary$ = "None"
	endif
endif
if rul
	ruleset$ = chooseReadFile$("Open the ruleset")
else
	if ruleset$ = ""
		ruleset$ = "None"
	endif
endif

# Delete the original settings file and write the new one
deleteFile("settings")
writeFileLine("settings",
..."DCT: ", dictionary$, newline$,
..."LAN: ", lan$, newline$,
..."LGC: ", lgc$, newline$,
..."LOG: ", log$, newline$,
..."NEW: ", new$, newline$,
..."OUT: ", "praat_temp_out", newline$,
..."PAU: ", pau$, newline$,
..."RUL: ", ruleset$, newline$,
..."SOX: ", sox$, newline$,
..."THR: ", thr, newline$,
..."TMP: ", "", newline$,
..."WRD: ", wrd$)
