# Get the selection and tiernumber
    start = Get start of selection
    end = Get end of selection
    info$ = Editor info
    tiernumber = extractNumber(info$, "Selected tier:")

# Extract the object name for later reselection
	info$ = TextGrid info
	tg$ = extractLine$(info$, "Object name: ")
	i = 0

# Move the cursor to the start of the selection
	Move cursor to... 'start'
	endpnt = Get end point of interval
# Find all boundaries until the end is reached and save them for later
	while endpnt < end
		i = i + 1
		Select next interval
		toremove[i] = Get starting point of interval
		endpnt = Get end point of interval
	endwhile

# Close the editor for faster removal and select the TextGrid
endeditor
select TextGrid 'tg$'

# Remove all the boundaries found earlier
for j to i
	nocheck Remove boundary at time... 'tiernumber' toremove[j]
endfor

# Clean the concatenated text
tiernum = Get interval at time... 'tiernumber' start-0.01
nocheck Set interval text... 'tiernumber' 'tiernum'   
