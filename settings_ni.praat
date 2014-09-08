# The form for non interactive setup
form Set the variables
	sentence new align
	sentence wrd align_w
	sentence dictionary
	sentence rul
	sentence lan
	real thr
	boolean pau 1
	sentence tmp /tmp/
	sentence log /dev/null
	sentence lgc a
	sentence sox sox
endform

# Process the pause variable
pau$ = if pau then "True" else "False" fi

# Write the settings file
writeFileLine("settings",
..."DCT: ", dictionary$, newline$,
..."LAN: ", lan$, newline$,
..."LGC: ", lgc$, newline$,
..."LOG: ", log$, newline$,
..."NEW: ", new$, newline$,
..."OUT: ", tmp$, "praat_temp_out", newline$,
..."PAU: ", pau$, newline$,
..."RUL: ", rul$, newline$,
..."SOX: ", sox$, newline$,
..."THR: ", thr, newline$,
..."TMP: ", tmp$, newline$,
..."WRD: ", wrd$)
