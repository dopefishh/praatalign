# Read all the settings
    if not fileReadable("settings")
        exitScript("No settings file found, please run the setup first")
    endif
    settings$ = readFile$("settings")
    tmpfile$ = extractLine$(settings$, "OUT: ")
    phonetier_name$ = extractLine$(settings$, "NEW: ")
    wordtier_name$ = extractLine$(settings$, "WRD: ")
    pythonex$ = extractLine$(settings$, "PY2: ")

# Get the current selected tier
    editor_info$ = Editor info
    curtier = extractNumber(editor_info$, "Selected tier:")

# Extract the file name of the wave file
    longsound_info$ = LongSound info
    longsound_file$ = extractLine$(longsound_info$, "File name: ")
    longsound_object$ = extractLine$(longsound_info$, "Object name: ")

# Extract the object name
    textgrid_info$ = TextGrid info
    textgrid_object$ = extractLine$(textgrid_info$, "Object name: ")

# Extract the tier
    Extract entire selected tier
endeditor

# Select the tier and convert it to a table and write it to a file
extracted_tier$ = selected$("TextGrid", 1)
Down to Table... "no" 6 "yes" "no"
Save as tab-separated file... 'tmpfile$'

# Remove all the created temporary objects
Remove
select TextGrid 'extracted_tier$'
Remove

# Write the tier specific settings
writeFileLine("isettings",
..."WAV: ", longsound_file$)

# Do the actual alignment
system 'pythonex$' align.py tier

# Read the results
Read Table from comma-separated file... 'tmpfile$'

# Remove the tiers if they already exist
number_of_rows = Get number of rows
select TextGrid 'textgrid_object$'
number_of_tiers = Get number of tiers
tiernumber = 1
while tiernumber < number_of_tiers
    nametier$ = Get tier name... 'tiernumber'
    if nametier$ = phonetier_name$ or nametier$ = wordtier_name$
        Remove tier... 'tiernumber'
    else
        tiernumber = tiernumber + 1
    endif
    number_of_tiers = Get number of tiers
endwhile

# Create the tiers again(easier cleaning)
Insert interval tier... 1 'wordtier_name$'
wordtier_index = 1
Insert interval tier... 2 'phonetier_name$'
phontier_index = 2

# Close the editor for more speed
editor TextGrid 'textgrid_object$'
    Close
endeditor

# Put the results in the textgrid
for current_row to number_of_rows
# Extract the values
    select Table praat_temp_out
    fto_start$ = Get value... 'current_row' start
    fto_end$ = Get value... 'current_row' end
    fto_value$ = Get value... 'current_row' label
    fto_type$ = Get value... 'current_row' type
    select TextGrid 'textgrid_object$'
# Create either a phone or a word interval
    if fto_type$ = "p"
        nocheck Insert boundary... 'phontier_index' 'fto_start$'
        nocheck Insert boundary... 'phontier_index' 'fto_end$'
        intnum = Get interval at time... 'phontier_index' 'fto_start$' + 0.0001
        Set interval text... 'phontier_index' 'intnum' 'fto_value$'
    elif fto_type$ = "w"
        nocheck Insert boundary... 'wordtier_index' 'fto_start$'
        nocheck Insert boundary... 'wordtier_index' 'fto_end$'
        intnum = Get interval at time... 'wordtier_index' 'fto_start$' + 0.0001
        Set interval text... 'wordtier_index' 'intnum' 'fto_value$'
    endif
endfor

# Remove temporary table file
select Table praat_temp_out
Remove

# Reselect the TextGrid and re-open editor
select TextGrid 'textgrid_object$'
plus LongSound 'longsound_object$'
Edit
