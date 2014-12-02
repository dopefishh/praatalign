# Extract settings
    if not fileReadable("settings")
        exitScript("No settings file found, please run the setup first")
    endif
    settings$ = readFile$("settings")
    tmpfile$ = extractLine$(settings$, "OUT: ")
    editor_info$ = Editor info
    curtier = extractNumber(editor_info$, "Selected tier:")

# Extract tier
    Extract entire selected tier
endeditor
textgrid_object$ = selected$("TextGrid", 1)

# Create table and save
Down to Table... "no" 6 "yes" "no"
Save as tab-separated file... 'tmpfile$'

# Clean up
Remove
select TextGrid 'textgrid_object$'
Remove

# Ask for location and write the dictionary
dict_filepath$ = chooseWriteFile$("Pick the location for the dictionary",
..."missing.txt")
system python generatedict.py 'dict_filepath$'
pause "Dictionary successfully generated"
