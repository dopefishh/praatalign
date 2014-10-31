# The form for non interactive setup
form Set the variables
	sentence new align
	sentence wrd align_w
	sentence dictionary
	sentence rul
	sentence lan
	real thr
	sentence log /dev/null
	sentence sox sox
	sentence hvb hvb
	sentence hcb hcb
endform

# Process the pause variable
pau$ = if pau then "True" else "False" fi

# Write the settings file
writeFileLine("settings",
..."DCT: ", dictionary$, newline$,
..."HVB: ", hvb$, newline$,
..."HCB: ", hcb$, newline$,
..."LAN: ", lan$, newline$,
..."LOG: ", log$, newline$,
..."NEW: ", new$, newline$,
..."OUT: ", "praat_temp_out", newline$,
..."RUL: ", rul$, newline$,
..."SOX: ", sox$, newline$,
..."THR: ", thr, newline$,
..."WRD: ", wrd$)
