# Read all the settings
    if not fileReadable("settings")
        exitScript("No settings file found, please run the setup first")
    endif
    settings$ = readFile$("settings")
    phonetier_name$ = extractLine$(settings$, "NEW: ")
    wordtier_name$ = extractLine$(settings$, "WRD: ")
    tmpfile$ = extractLine$(settings$, "OUT: ")
		boundary_margin = extractNumber(settings$, "THR: ")

# Get current selection
    selection_start = Get starting point of interval
    selection_end = Get end point of interval

# Extract file name and duration of the entire wave file
    longsound_info$ = LongSound info
    wav_filepath$ = extractLine$(longsound_info$, "File name: ")
    wav_object$ = extractLine$(longsound_info$, "Object name: ")
    utterance$ = Get label of interval
		fullduration = extractNumber(longsound_info$, "Duration: ")

# Extract current tier to later match with word and phon tier
    editor_info$ = Editor info
    current_tier = extractNumber(editor_info$, "Selected tier: ")

# Unshow pitch, intensity and spectrum if they are enabled
		pitch_on = 0
		intensity_on = 0
		formant_on = 0
		spectrum_on = 0
		pulses_on = 0
		if extractWord$(editor_info$, "Pitch show: ") == "yes"
			pitch_on = 1
			Show pitch
		endif
		if extractWord$(editor_info$, "Intensity show: ") == "yes"
			intensity_on = 1
			Show intensity
		endif
		if extractWord$(editor_info$, "Spectrogram show: ") == "yes"
			spectrum_on = 1
			Show spectrogram
		endif
		if extractWord$(editor_info$, "Formant show: ") == "yes"
			formant_on = 1
			Show formants
		endif
		if extractWord$(editor_info$, "Pulses show: ") == "yes"
			pulses_on = 1
			Show pulses
		endif

# Extract the object name
    textgrid_info$ = TextGrid info
    textgrid_object$ = extractLine$(textgrid_info$, "Object name: ")

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
selection_end = min(selection_end + margin_after, fullduration)
selection_duration = selection_end - selection_start

# Get the index of the phone tier
select TextGrid 'textgrid_object$'
phonetier_number = -1
number_tiers = Get number of tiers
for i to number_tiers
    tiername$ = Get tier name... i
    if tiername$ = phonetier_name$
        phonetier_number = i
    endif
endfor
# If it doesn't exist, create it
if phonetier_number = -1
    current_tier = current_tier + 1
    Insert interval tier... 1 'phonetier_name$'
    phonetier_number = 1
endif

# Get the index of the word tier
wordtier_number = -1
number_tiers = Get number of tiers
for i to number_tiers
    tiername$ = Get tier name... i
    if tiername$ == wordtier_name$
        wordtier_number = i
    endif
endfor
# If it doesn't exist, create it
if wordtier_number = -1
    current_tier = current_tier + 1
    Insert interval tier... 1 'wordtier_name$'
    wordtier_number = 1
		phonetier_number = phonetier_number + 1
endif

# If the phone tier is the same as the word tier, let know
if current_tier == phonetier_number or current_tier == wordtier_number
	pause You have selected your word or phonetier as source tier... Are you sure
... you want to continue
elif phonetier_number == wordtier_number
pause The phone tier is the same as the word tier... Are you sure you want 
...to continue?
endif

# Clean up the phone tier
editor TextGrid 'textgrid_object$'
# Select the interval
    current_tier_num = -1
    repeat
        Select next tier
        editor_info$ = Editor info
        current_tier_num = extractNumber(editor_info$, "Selected tier:")
    until phonetier_number = current_tier_num
    Select... 'selection_start' 'selection_end'
# Clean up
include cleaninterval.praat

# Clean up the word tier
editor TextGrid 'textgrid_object$'
# Select the tier
    current_tier_num = -1
    repeat
        Select next tier
        editor_info$ = Editor info
        current_tier_num = extractNumber(editor_info$, "Selected tier:")
    until wordtier_number = current_tier_num
    Select... 'selection_start' 'selection_end'
# Clean up
include cleaninterval.praat

# Write the interval specific settings to the settings file
writeFileLine("isettings",
..."STA: ", selection_start, newline$,
..."DUR: ", selection_duration, newline$,
..."UTT: ", utterance$, newline$,
..."WAV: ", wav_filepath$)

# Do the actual alignment
system python alignannotation.py

# Read the results
Read Table from comma-separated file... 'tmpfile$'

# Put the results in the textgrid
number_rows = Get number of rows
for i to number_rows
#Extract the values
    select Table praat_temp_out
    current_start$ = Get value... 'i' start
    current_end$ = Get value... 'i' end
    current_value$ = Get value... 'i' label
    current_type$ = Get value... 'i' type
    select TextGrid 'textgrid_object$'
# Create either a phone or a word interval
    if current_type$ = "p"
        nocheck Insert boundary... 'phonetier_number' 'current_start$'
        nocheck Insert boundary... 'phonetier_number' 'current_end$'
        intnum = Get interval at time... 'phonetier_number'
... 'current_start$'+0.0001
        Set interval text... 'phonetier_number' 'intnum' 'current_value$'
    elif current_type$ = "w"
        nocheck Insert boundary... 'wordtier_number' 'current_start$'
        nocheck Insert boundary... 'wordtier_number' 'current_end$'
        intnum = Get interval at time... 'wordtier_number'
... 'current_start$'+0.0001
        Set interval text... 'wordtier_number' 'intnum' 'current_value$'
    endif
endfor

# Remove temporary table file
select Table praat_temp_out
Remove

# Reset pitch, intensity and spectrum if they were unset before
editor
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
