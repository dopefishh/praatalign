include procs.praat
	# Settings loads: phonetier_name$, wordtier_name$, cantier_name$, tmpfile$,
	# pythonex$, boundary_margin, llhtier_name$
	@loadSettings: 

	# Load editor and longsound info: longsound_file$, longsound_object$,
	# textgrid_object$, selected_tier, longsound_duration, pitch_on,
	# intensity_on, spectrum_on, formant_on, pulses_on
	@loadFileInfo:

	statusfile$ = "temp.status"

# Get current selection
	selection_start = Get starting point of interval
	selection_end = Get end point of interval
	utterance$ = Get label of interval

# Unshow pitch, intensity and spectrum if they are enabled
	@toggleGUIValues:

# Check if the previous or next interval are empty
    Select previous interval
    interval_label$ = Get label of interval
    if interval_label$ = ""
      margin_before = boundary_margin
    else
      margin_before = 0
    endif
    Select next interval
    Select next interval
    interval_label$ = Get label of interval
    if interval_label$ = ""
      margin_after = boundary_margin
    else
      margin_after = 0
    endif
    Select previous interval
    Zoom to selection
    Zoom out
endeditor

# Calculate the true start and end times with respect to the extended bounds
selection_start = max(selection_start - margin_before, 0)
selection_end = min(selection_end + margin_after, longsound_duration)
selection_duration = selection_end - selection_start

# Get the index the tiers
selectObject: textgrid_object$
@indexOfTier: phonetier_name$
phonetier_number = indexOfTier.number

@indexOfTier: llhtier_name$
llhtier_number = indexOfTier.number
if indexOfTier.inserted = 1
	phonetier_number = phonetier_number + 1
endif

@indexOfTier: wordtier_name$
wordtier_number = indexOfTier.number
if indexOfTier.inserted = 1
	phonetier_number = phonetier_number + 1
	llhtier_number = llhtier_number + 1
endif

@indexOfTier: cantier_name$
cantier_number = indexOfTier.number
if indexOfTier.inserted = 1
	phonetier_number = phonetier_number + 1
	wordtier_number = wordtier_number + 1
	llhtier_number = llhtier_number + 1
endif

# Clean up the phone tier
if phonetier_name$ <> ""
	@cleanAnnotation: textgrid_object$, phonetier_number, selection_start, selection_end
endif
if wordtier_name$ <> ""
	@cleanAnnotation: textgrid_object$, wordtier_number, selection_start, selection_end
endif
if cantier_name$ <> ""
	@cleanAnnotation: textgrid_object$, cantier_number, selection_start, selection_end
endif
if llhtier_name$ <> ""
	@cleanAnnotation: textgrid_object$, llhtier_number, selection_start, selection_end
endif

# Write the interval specific settings to the settings file
writeFileLine("isettings",
..."STA: ", selection_start, newline$,
..."DUR: ", selection_duration, newline$,
..."UTT: ", utterance$, newline$,
..."WAV: ", longsound_file$)

# Do the actual alignment
system 'pythonex$' align.py annotation

returnstatus$ = readFile$: statusfile$
if returnstatus$ == "done"
	@insertTableTextGrid: tmpfile$, textgrid_object$, phonetier_name$,
... wordtier_name$, cantier_name$, llhtier_name$, phonetier_number,
... wordtier_number, cantier_number, llhtier_number
elif returnstatus$ == "missox"
	pause SoX couldn't be found, please set it manually in the settings window
elif returnstatus$ == "mishcopy"
	pause HCopy couldn't be found, please set it manually in the settings window
elif returnstatus$ == "mishvite"
	pause HVite couldn't be found, please set it manually in the settings window
elif returnstatus$ == "unicode"
	pause Error parsing dictionary or ruleset. Is the encoding UTF-8?
elif returnstatus$ == "dictnotfound"
	pause Dictionary file not accessible, does it still exist?
elif returnstatus$ == "rulnotfound"
	pause Ruleset file not accessible, does it still exist?
elif returnstatus$ == "generalio"
	pause Unknown IO error
endif

# Reset pitch, intensity and spectrum if they were unset before
editor
	@toggleGUIValues:
