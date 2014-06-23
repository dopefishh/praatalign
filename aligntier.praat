	pause Are you sure, this takes a long time...
    if not fileReadable("settings")
        exitScript("No settings file found, please run the setup first")
    endif
    settings$ = readFile$("settings")
    out$ = extractLine$(settings$, "OUT: ")
    new$ = extractLine$(settings$, "NEW: ")
    wrd$ = extractLine$(settings$, "WRD: ")

    info$ = Editor info
    curtier = extractNumber(info$, "Selected tier:")

    info$ = LongSound info
    wav$ = extractLine$(info$, "File name: ")
    snd$ = extractLine$(info$, "Object name: ")

    info$ = TextGrid info
    curtg$ = extractLine$(info$, "Object name: ")
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
    if nametier$ = new$ or nametier$ = wrd$
        Remove tier... 'i'
    else
        i = i + 1
    endif
    numtiers = Get number of tiers
endwhile
Insert interval tier... 1 'wrd$'
tiernum_w = 1
Insert interval tier... 2 'new$'
tiernum_p = 2

editor TextGrid 'curtg$'
    Close
endeditor

for i to rows
    select Table praat_temp_out
    sstart$ = Get value... 'i' start
    send$ = Get value... 'i' end
    svalue$ = Get value... 'i' label
    stype$ = Get value... 'i' type
    select TextGrid 'curtg$'
    if stype$ = "p"
        nocheck Insert boundary... 'tiernum_p' 'sstart$'
        nocheck Insert boundary... 'tiernum_p' 'send$'
        intnum = Get interval at time... 'tiernum_p' 'sstart$' + 0.0001
        Set interval text... 'tiernum_p' 'intnum' 'svalue$'
    elif stype$ = "w"
        nocheck Insert boundary... 'tiernum_w' 'sstart$'
        nocheck Insert boundary... 'tiernum_w' 'send$'
        intnum = Get interval at time... 'tiernum_w' 'sstart$' + 0.0001
        Set interval text... 'tiernum_w' 'intnum' 'svalue$'
    endif
endfor

select Table praat_temp_out
Remove
select TextGrid 'curtg$'
plus LongSound 'snd$'
Edit
