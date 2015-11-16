# The form for non interactive setup
form Set the variables
	sentence new align
	sentence wrd align_w
	sentence can align_c
	sentence llh align_l
	sentence lan
	sentence model
	sentence pho
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
..."MOD: ", model$, newline$,
..."PHO: ", pho$, newline$,
..."LOG: ", log$, newline$,
..."LLH: ", llh$, newline$,
..."NEW: ", new$, newline$,
..."CAN: ", can$, newline$,
..."OUT: ", "praat_temp_out", newline$,
..."RUL: ", rul$, newline$,
..."SOX: ", sox$, newline$,
..."THR: ", thr, newline$,
..."PY2: ", py$, newline$,
..."WRD: ", wrd$)
