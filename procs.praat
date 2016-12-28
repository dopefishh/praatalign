procedure loadSettings: 
	if not fileReadable("settings")
		exitScript("No settings file found, please run the setup first")
	endif
	settings$ = readFile$("settings")
	phonetier_name$ = extractLine$(settings$, "NEW: ")
	wordtier_name$ = extractLine$(settings$, "WRD: ")
	cantier_name$ = extractLine$(settings$, "CAN: ")
	llhtier_name$ = extractLine$(settings$, "LLH: ")
	orttier_name$ = extractLine$(settings$, "ORT: ")
	tmpfile$ = extractLine$(settings$, "OUT: ")
	pythonex$ = extractLine$(settings$, "PY2: ")
	boundary_margin = extractNumber(settings$, "THR: ")
endproc

procedure loadFileInfo:
# Try longsound first
	longsound_info$ = ""
	longsound_info$ = nocheck LongSound info
	if longsound_info$ <> ""
		sound_file$ = extractLine$(longsound_info$, "File name: ")
		sound_object$ = "LongSound " + extractLine$(longsound_info$, "Object name: ")
		sound_duration = extractNumber(longsound_info$, "Duration: ")
	else
		sound_info$ = Sound info
		sound_object$ = "Sound " + extractLine$(sound_info$, "Object name: ")
		sound_duration = extractNumber(sound_info$, "   Total duration: ")
		Select: 0, sound_duration
		Save selected sound as WAV file: "longsound_sound.wav"
		sound_file$ = "longsound_sound.wav"
	endif

	textgrid_info$ = TextGrid info
	textgrid_object$ = "TextGrid " + extractLine$(textgrid_info$, "Object name: ")

	editorinfo$ = Editor info
	selected_tier = extractNumber(editorinfo$, "Selected tier:")
	pitch_on = if extractWord$(editorinfo$, "Pitch show: ") == "yes"
... then 1 else 0 fi
	intensity_on = if extractWord$(editorinfo$, "Intensity show: ") == "yes"
... then 1 else 0 fi
	spectrum_on = if extractWord$(editorinfo$, "Spectrogram show: ") == "yes"
... then 1 else 0 fi
	formant_on = if extractWord$(editorinfo$, "Formant show: ") == "yes"
... then 1 else 0 fi
	pulses_on = if extractWord$(editorinfo$, "Pulses show: ") == "yes"
... then 1 else 0 fi
endproc

procedure indexOfTier: .name$
	.inserted = 0
	if .name$ <> ""
		.number = -1
		.ntiers = Get number of tiers
		for .i to .ntiers
			.tiername$ = Get tier name: .i
			if .tiername$ = .name$
				.number = .i
			endif
		endfor
		if .number = -1
			selected_tier = selected_tier + 1
			Insert interval tier: 1, .name$
			.number = 1
			.inserted = 1
		endif
	endif
endproc

procedure cleanAnnotation: .obj$, .num, .start, .end
	editor: .obj$
		.selected_tier_num = -1
		repeat
			Select next tier
			.editor_info$ = Editor info
			.selected_tier_num = extractNumber(.editor_info$, "Selected tier:")
		until .num = .selected_tier_num
		Select: .start, .end

		Move cursor to: .start
		.interval_end = Get end point of interval

		.to_remove_len = 0
		while .interval_end < .end
			.to_remove_len = .to_remove_len + 1
			Select next interval
			.to_remove[.to_remove_len] = Get starting point of interval
			.interval_end = Get end point of interval
		endwhile
	endeditor

	selectObject: .obj$
	for .i to .to_remove_len
		nocheck Remove boundary at time: .selected_tier_num, .to_remove[.i]
	endfor

	.tiernum = Get interval at time: .selected_tier_num, .start-0.01
	nocheck Set interval text: .selected_tier_num, .tiernum, ""
endproc

procedure toggleGUIValues:
	if pitch_on == 1
		Show pitch
	endif
	if intensity_on == 1
		Show intensity
	endif
	if spectrum_on == 1
		Show spectrogram
	endif
	if formant_on == 1
		Show formants
	endif
	if pulses_on == 1
		Show pulses
	endif
endproc

procedure getBinary: message$, path$, default$, .toask
	.ex$ = ""
	if .toask == 1
		beginPause: "Instructions"
			comment: "Please point me to the " + default$ + " executable."
			comment: "When " + default$ + " is in your " + path$ + " you can cancel this."
			comment: "It can be found " + message$
		.clicked = endPause: "Cancel", "Continue", 2, 1
		if .clicked = 2
			.ex$ = chooseReadFile$("Point me to the " + default$ + " executable")
		endif
		if .ex$ = ""
			.ex$ = default$
		endif
	endif
endproc

procedure insertTableTextGrid: .tablefile$, .obj$, .phon$, .ort$, .wrd$, .can$, .llh$,
... .phonn, .ortn, .wrdn, .cann, .llhn
	nocheck Read Table from comma-separated file: .tablefile$
	if extractWord$(selected$(), "") == "Table"
		.number_rows = Get number of rows
		# Put the results in the textgrid
		for .i to .number_rows
			#Extract the values
			selectObject: "Table praat_temp_out"
			.current_start$ = Get value: .i, "start"
			.current_start = number(.current_start$)
			.current_end$ = Get value: .i, "end"
			.current_end = number(.current_end$)
			.current_value$ = Get value: .i, "label"
			.current_type$ = Get value: .i, "type"
			selectObject: .obj$
		
			if .current_type$ = "p" and .phon$ <> ""
				nocheck Insert boundary: .phonn, .current_start
				nocheck Insert boundary: .phonn, .current_end
				.intnum = Get interval at time: .phonn, .current_start+0.0001
				nocheck Set interval text: .phonn, .intnum, .current_value$
			elif .current_type$ = "w" and .wrd$ <> ""
				nocheck Insert boundary: .wrdn, .current_start
				nocheck Insert boundary: .wrdn, .current_end
				.intnum = Get interval at time: .wrdn, .current_start+0.0001
				nocheck Set interval text: .wrdn, .intnum, .current_value$
			elif .current_type$ = "o" and .wrd$ <> ""
				nocheck Insert boundary: .ortn, .current_start
				nocheck Insert boundary: .ortn, .current_end
				.intnum = Get interval at time: .ortn, .current_start+0.0001
				nocheck Set interval text: .ortn, .intnum, .current_value$
			elif .current_type$ = "c" and .can$ <> ""
				nocheck Insert boundary: .cann, .current_start
				nocheck Insert boundary: .cann, .current_end
				.intnum = Get interval at time: .cann, .current_start+0.0001
				nocheck Set interval text: .cann, .intnum, .current_value$
			elif .current_type$ = "l" and .llh$ <> ""
				nocheck Insert boundary: .llhn, .current_start
				nocheck Insert boundary: .llhn, .current_end
				.intnum = Get interval at time: .llhn, .current_start+0.0001
				nocheck Set interval text: .llhn, .intnum, .current_value$
			endif
		endfor
		
		# Remove temporary table file
		selectObject: "Table praat_temp_out"
		Remove
	endif
endproc
