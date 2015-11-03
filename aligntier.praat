include procs.praat
	# Settings loads: phonetier_name$, wordtier_name$, cantier_name$, tmpfile$,
	# pythonex$, boundary_margin
	@loadSettings:

	# Load editor and longsound info: sound_file$, sound_object$,
	# textgrid_object$, selected_tier, sound_duration, pitch_on,
	# intensity_on, spectrum_on, formant_on, pulses_on
	@loadFileInfo:

	# Extract the tier
	Extract entire selected tier
endeditor

# Select the tier and convert it to a table and write it to a file
extracted_tier$ = selected$("TextGrid", 1)
Down to Table: "no", 6, "yes", "no"
Save as tab-separated file: tmpfile$

# Remove all the created temporary objects
Remove
select TextGrid 'extracted_tier$'
Remove

# Write the tier specific settings
writeFileLine("isettings",
..."WAV: ", sound_file$)

# Remove the tiers if they already exist
selectObject: textgrid_object$
number_of_tiers = Get number of tiers
tiernumber = 1
while tiernumber < number_of_tiers
    nametier$ = Get tier name: tiernumber
    if nametier$ = phonetier_name$ or nametier$ = wordtier_name$ or nametier$ = cantier_name$ or nametier$ = llhtier_name$
        Remove tier: tiernumber
    else
        tiernumber = tiernumber + 1
    endif
    number_of_tiers = Get number of tiers
endwhile

# Get the index the tiers
selectObject: textgrid_object$

phonetier_number = -1
llhtier_number = -1
wordtier_number = -1
cantier_number = -1

if phonetier_name$ <> ""
@indexOfTier: phonetier_name$
	phonetier_number = indexOfTier.number
endif

if llhtier_name$ <> ""
@indexOfTier: llhtier_name$
	llhtier_number = indexOfTier.number
	if indexOfTier.inserted == 1
		if phonetier_name$ <> ""
			phonetier_number = phonetier_number + 1
		endif
	endif
endif

if wordtier_name$ <> ""
@indexOfTier: wordtier_name$
	wordtier_number = indexOfTier.number
	if indexOfTier.inserted == 1
		if phonetier_name$ <> ""
			phonetier_number = phonetier_number + 1
		endif
		if llhtier_name$ <> ""
			llhtier_number = llhtier_number + 1
		endif
	endif
endif

if cantier_name$ <> ""
@indexOfTier: cantier_name$
	cantier_number = indexOfTier.number
	if indexOfTier.inserted == 1
		if phonetier_name$ <> ""
			phonetier_number = phonetier_number + 1
		endif
		if llhtier_name$ <> ""
			llhtier_number = llhtier_number + 1
		endif
		if wordtier_name$ <> ""
			wordtier_number = wordtier_number + 1
		endif
	endif
endif

# Do the actual alignment
system 'pythonex$' align.py tier

# Close the editor for more speed
editor: textgrid_object$
    Close
endeditor

# Read the results
@insertTableTextGrid: tmpfile$, textgrid_object$, phonetier_name$,
... wordtier_name$, cantier_name$, llhtier_name$, phonetier_number,
... wordtier_number, cantier_number, llhtier_number

# Reselect the TextGrid and re-open editor
selectObject: textgrid_object$
plusObject: sound_object$
Edit
