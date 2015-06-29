# The form for non interactive setup
form Set the variables
	sentence new align
	sentence wrd align_w
	sentence lan
	sentence dic
	sentence rul
	real thr
	sentence log /dev/null
	sentence sox sox
	sentence hvb hvb
	sentence hcb hcb
	sentence py py
endform

# Write the settings file
writeFileLine("settings",
..."DCT: ", dic$, newline$,
..."HVB: ", hvb$, newline$,
..."HCB: ", hcb$, newline$,
..."LAN: ", lan$, newline$,
..."LOG: ", log$, newline$,
..."NEW: ", new$, newline$,
..."OUT: ", "praat_temp_out", newline$,
..."RUL: ", rul$, newline$,
..."SOX: ", sox$, newline$,
..."THR: ", thr, newline$,
..."PY2: ", py$, newline$,
..."WRD: ", wrd$)
