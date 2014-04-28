    if not fileReadable("settings")
        exitScript("No settings file found, please run the setup first")
    endif
    settings$ = readFile$("settings")
    out$ = extractLine$(settings$, "OUT: ")
    info$ = Editor info
    curtier = extractNumber(info$, "Selected tier:")
    Extract entire selected tier
endeditor
tg$ = selected$("TextGrid", 1)
Down to Table... "no" 6 "yes" "no"
Save as tab-separated file... 'out$'
Remove
select TextGrid 'tg$'
Remove
tofile$ = chooseWriteFile$("Pick the location to write the dictionary to",
..."missing.txt")
system python generatedict.py 'tofile$'
