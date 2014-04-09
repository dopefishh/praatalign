clearinfo

include lib.praat

form Set the variables
	comment Name the tier to align
	sentence tiername 
	comment Name for the output tier
	sentence newtier align
	
	comment Select language
	optionmenu lang: 1
		option tze
		option spa
	
	comment Custom dictionary path
	boolean dictpath 0

	comment Use ruleset(name ruleset.lang)
	boolean ruleset 0
	
	comment Temporary file directory
	sentence tmpdir /tmp/
endform

# Parse options
dictpath$ = if dictpath then chooseReadFile$("Open the dictionary") else "" fi
ruleset$ = if ruleset then "None" else "ruleset.'lang$'" fi
basetmp$ = "praat_temp_out"
tmp$ = tmpdir$ + basetmp$

# Get selections and set variables
tg$ = selected$("TextGrid", 1)
snd$ = selected$("LongSound", 1)

# Remove tier if already present
select TextGrid 'tg$'
call getTierNumber 'newtier$' tiernumber
if tiernumber <> -1
	Remove tier... 'tiernumber'
endif

# Create table from the tier
call getTierNumber 'tiername$' tiernumber
Extract one tier... 'tiernumber'
select TextGrid 'tiername$'
Down to Table... no 6 no no
Save as tab-separated file... temp.txt
Remove
select TextGrid 'tiername$'
Remove

# Extract filename from longsound
select LongSound 'snd$'
View
editor LongSound 'snd$'
	t$ = LongSound info
	sndpath$ = extractWord$(t$, "File name: ")
	Close
endeditor

# Align the tier
printline python aligner.py tier temp.txt 'sndpath$' 'lang$' 'ruleset$' ./ 'dictpath$' > 'tmp$'
system python aligner.py tier temp.txt 'sndpath$' 'lang$' 'ruleset$' ./ 'dictpath$' > 'tmp$'

# Create the new tier
select TextGrid 'tg$'
Insert interval tier... 1 'newtier$'
tiernumber = 1

# Read the table
Read Table from comma-separated file... 'tmp$'
rows = Get number of rows
for i to rows
	# Insert the intervals
    select Table 'basetmp$'
    sstart$ = Get value... 'i' start
    send$ = Get value... 'i' end
    svalue$ = Get value... 'i' label
    select TextGrid 'tg$'
    if svalue$ = "<"
        Insert boundary... 'tiernumber' 'sstart$'
    endif
    Insert boundary... 'tiernumber' 'send$'
    intnum = Get interval at time... 'tiernumber' 'sstart$'+0.0001
    Set interval text... 'tiernumber' 'intnum' 'svalue$'
endfor

# Remove temp files and reselect the TextGrid and LongSound
select Table 'basetmp$'
Remove
select TextGrid 'tg$'
plus LongSound 'snd$'
pause Done aligning the tier
