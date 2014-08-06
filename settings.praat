form Set the variables
	comment Name for the output tier(may already exist)
	sentence new align

	comment Name for the output tier used for word level alignment
	sentence wrd align_w

include languageselection.praat

	comment Custom dictionary path
	boolean dic 0
	sentence dictionary
	
	comment Use ruleset
	boolean rul 0
	sentence ruleset

	comment Pause first when aligning tier
	boolean pau 1

	comment Export the graph to pdf
	boolean pdf 0

	comment Temporary directory
	sentence tmp /tmp/
endform
pdf$ = if pdf then "True" else "False" fi
pau$ = if pau then "True" else "False" fi
dic$ = if dic then chooseReadFile$("Open the dictionary") else "None" fi
rul$ = if rul then chooseReadFile$("Open the ruleset file") else "None" fi
if dictionary$ <> ""
	dic$ = dictionary$
endif
if ruleset$ <> ""
	rul$ = ruleset$
endif

deleteFile("settings")
writeFileLine("settings",
..."NEW: ", new$, newline$,
..."LAN: ", lan$, newline$,
..."DCT: ", dic$, newline$,
..."RUL: ", rul$, newline$,
..."PDF: ", pdf$, newline$,
..."TMP: ", tmp$, newline$,
..."WRD: ", wrd$, newline$,
..."PAU: ", pau$, newline$,
..."OUT: ", tmp$, "praat_temp_out")
