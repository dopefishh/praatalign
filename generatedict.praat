clearinfo

include lib.praat

form Set the variables
	comment Name of the tier
	sentence tiername 
	
	comment Select language for the phonetizer
include languageselection.praat

	comment Create example entry?
	boolean example 0

	comment Directory for storing temporary files
	sentence tmp /tmp/
endform
# Remember the TextGrid selected and set the variables
tg$ = selected$("TextGrid", 1)
dictpath$ = chooseWriteFile$("Select the location to put the dictionary", "missing.txt")
example$ = if example then "True" else "False" fi
call getTierNumber 'tiername$' tiernumber

tmp$="'tmp$'praat_temp_out"

#Extract the tier, convert to csv and 
Extract one tier... 'tiernumber'
Down to Table... "no" 6 "yes" "no"
Save as tab-separated file... 'tmp$'
select TextGrid 'tiername$'
plus Table 'tiername$'
Remove
select TextGrid 'tg$'

printline python generatedict.py 'lang$' 'example$' 'tmp$' 'dictpath$'
system python generatedict.py 'lang$' 'example$' 'tmp$' 'dictpath$'
pause Done generating, you can find your file at 'dictpath$'
