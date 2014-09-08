# Read all the settings
    if not fileReadable("settings")
        exitScript("No settings file found, please run the setup first")
    endif
    settings$ = readFile$("settings")
    new$ = extractLine$(settings$, "NEW: ")
    wrd$ = extractLine$(settings$, "WRD: ")
    out$ = extractLine$(settings$, "OUT: ")
		thr = extractNumber(settings$, "THR: ")

# Get current selection
    start = Get starting point of interval
    end = Get end point of interval

# Extract file name and duration of the entire wave file
    info$ = LongSound info
    wav$ = extractLine$(info$, "File name: ")
    utt$ = Get label of interval
		fullduration = extractNumber(info$, "Duration: ")

# Extract the object name
    info$ = TextGrid info
    tg$ = extractLine$(info$, "Object name: ")

# Check if the previous or next interval are empty
		Select previous interval
		int$ = Get label of interval
		if int$ = ""
			before = thr
		else
			before = 0
		endif
		Select next interval
		Select next interval
		int$ = Get label of interval
		if int$ = ""
			after = thr
		else
			after = 0
		endif
endeditor

# Get the index of the phone tier
select TextGrid 'tg$'
tiernum_p = -1
numtier = Get number of tiers
for i to numtier
    name$ = Get tier name... i
    if name$ = new$
        tiernum_p = i
    endif
endfor
# If it doesn't exist, create it
if tiernum_p = -1
    Insert interval tier... 1 'new$'
    tiernum_p = 1
endif

# Get the index of the word tier
tiernum_w = -1
numtier = Get number of tiers
for i to numtier
    name$ = Get tier name... i
    if name$ == wrd$
        tiernum_w = i
    endif
endfor
# If it doesn't exist, create it
if tiernum_w = -1
    Insert interval tier... 1 'wrd$'
    tiernum_w = 1
endif

# Calculate the true start and end times with respect to the extended bounds
start = max(start - before, 0)
end = min(end + after, fullduration)
dur = end - start

# Clean up the phone tier
editor TextGrid 'tg$'
# Select the interval
    curtier = -1
    repeat
        Select next tier
        info$ = Editor info
        curtier = extractNumber(info$, "Selected tier:")
    until tiernum_p = curtier
    Select... 'start' 'end'
# Clean up
include cleaninterval.praat

# Clean up the word tier
editor TextGrid 'tg$'
# Select the tier
    curtier = -1
    repeat
        Select next tier
        info$ = Editor info
        curtier = extractNumber(info$, "Selected tier:")
    until tiernum_w = curtier
    Select... 'start' 'end'
# Clean up
include cleaninterval.praat

# Write the interval specific settings to the settings file
writeFileLine("isettings",
..."STA: ", start, newline$,
..."DUR: ", dur, newline$,
..."UTT: ", utt$, newline$,
..."WAV: ", wav$)

# Do the actual alignment
system python alignannotation.py

# Read the results
Read Table from comma-separated file... 'out$'

# Put the results in the textgrid
rows = Get number of rows
for i to rows
#Extract the values
    select Table praat_temp_out
    sstart$ = Get value... 'i' start
    send$ = Get value... 'i' end
    svalue$ = Get value... 'i' label
    stype$ = Get value... 'i' type
    select TextGrid 'tg$'
# Create either a phone or a word interval
    if stype$ = "p"
        nocheck Insert boundary... 'tiernum_p' 'sstart$'
        nocheck Insert boundary... 'tiernum_p' 'send$'
        intnum = Get interval at time... 'tiernum_p' 'sstart$'+0.0001
        Set interval text... 'tiernum_p' 'intnum' 'svalue$'
    elif stype$ = "w"
        nocheck Insert boundary... 'tiernum_w' 'sstart$'
        nocheck Insert boundary... 'tiernum_w' 'send$'
        intnum = Get interval at time... 'tiernum_w' 'sstart$'+0.0001
        Set interval text... 'tiernum_w' 'intnum' 'svalue$'
    endif
endfor

# Remove temporary table file
select Table praat_temp_out
Remove
