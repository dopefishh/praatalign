	if not fileReadable("settings")
		exitScript("No settings file found, please run the setup first")
	endif
	settings$ = readFile$("settings")
	out$ = extractLine$(settings$, "OUT: ")
	new$ = extractLine$(settings$, "NEW: ")
	info$ = LongSound info
	wav$ = extractLine$(info$, "File name: ")
	snd$ = extractLine$(info$, "Object name: ")
	info$ = Editor info
	curtier = extractNumber(info$, "Selected tier:")
	curtg$ = extractLine$(info$, "Data name: ")
	Extract entire selected tier
endeditor
tg$ = selected$("TextGrid", 1)
Down to Table... "no" 6 "yes" "no"
Save as tab-separated file... 'out$'
Remove
select TextGrid 'tg$'
Remove

writeFileLine("isettings",
..."WAV: ", wav$)

system python aligntier.py

Read Table from comma-separated file... 'out$'

rows = Get number of rows
select TextGrid 'curtg$'
numtiers = Get number of tiers
i = 1
while i < numtiers
	nametier$ = Get tier name... 'i'
	if nametier$ = new$
		Remove tier... 'i'
	endif
	numtiers = Get number of tiers
	i = i + 1
endwhile
Insert interval tier... 1 'new$'
tiernumber = 1

editor TextGrid 'curtg$'
	Close
endeditor

nocheck Insert boundary... 'tiernumber' 'start'
for i to rows
	select Table praat_temp_out
	sstart$ = Get value... 'i' start
	send$ = Get value... 'i' end
	svalue$ = Get value... 'i' label
	select TextGrid 'curtg$'
	nocheck Insert boundary... 'tiernumber' 'sstart$'
	Insert boundary... 'tiernumber' 'send$'
	intnum = Get interval at time... 'tiernumber' 'sstart$'+0.0001
	Set interval text... 'tiernumber' 'intnum' 'svalue$'
endfor

select Table praat_temp_out
Remove

select TextGrid 'curtg$'
plus LongSound 'snd$'

Edit
