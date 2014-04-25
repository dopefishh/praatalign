	settings$ = readFile$("settings")
	new$ = extractLine$(settings$, "NEW: ")
	tmp$ = extractLine$(settings$, "TMP: ")

    start = Get starting point of interval
    end = Get end point of interval
    utt$ = Get label of interval
	info$ = TextGrid info
	tg$ = extractLine$(info$, "Object name: ")
    info$ = LongSound info
    wav$ = extractLine$(info$, "File name: ")
	snd$ = extractLine$(info$, "Object name: ")
endeditor
select TextGrid 'tg$'
tiernumber = -1
numtier = Get number of tiers
for i to numtier
	name$ = Get tier name... i
	if name$ == new$
		tiernumber = i
	endif
endfor
if tiernumber = -1
	Insert interval tier... 1 'new$'
	tiernumber = 1
endif
editor TextGrid 'tg$'
	curtier = -1
	repeat
		Select next tier
		info$ = Editor info
   		curtier = extractNumber(info$, "Selected tier:")
	until tiernumber = curtier
	Select... 'start' 'end'
include cleaninterval.praat
select TextGrid 'tg$'

dur = end - start
writeFileLine("isettings",
..."STA: ", start, newline$,
..."DUR: ", dur, newline$,
..."UTT: ", utt$, newline$,
..."WAV: ", wav$, newline$,
..."OUT: ", tmp$, "praat_temp_out")
printline python alignannotation.py
system python alignannotation.py

# Read the results
Read Table from comma-separated file... 'tmp$'praat_temp_out

# Put the results in the textgrid
rows = Get number of rows
select TextGrid 'tg$'
nocheck Insert boundary... 'tiernumber' 'start'
for i to rows
	select Table praat_temp_out
	sstart$ = Get value... 'i' start
	send$ = Get value... 'i' end
	svalue$ = Get value... 'i' label
	select TextGrid 'tg$'
	Insert boundary... 'tiernumber' 'send$'
	intnum = Get interval at time... 'tiernumber' 'sstart$'+0.0001
	Set interval text... 'tiernumber' 'intnum' 'svalue$'
endfor

# Remove temp files and reselect the TextGrid and LongSound
select Table praat_temp_out
Remove
