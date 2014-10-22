# Get the selection and tiernumber
    selection_start = Get start of selection
    selection_end = Get end of selection
    editor_info$ = Editor info
    selected_tier_number = extractNumber(editor_info$, "Selected tier:")

# Extract the object name for later reselection
	editor_info$ = TextGrid info
	textgrid_object$ = extractLine$(editor_info$, "Object name: ")

# Move the cursor to the start of the selection
	Move cursor to... 'selection_start'
	interval_end = Get end point of interval
# Find all boundaries until the end is reached and save them for later
	to_remove_len = 0
	while interval_end < selection_end
		to_remove_len = to_remove_len + 1
		Select next interval
		to_remove[to_remove_len] = Get starting point of interval
		interval_end = Get end point of interval
	endwhile

# Close the editor for faster removal and select the TextGrid
endeditor
select TextGrid 'textgrid_object$'

# Remove all the boundaries found earlier
for i to to_remove_len
	nocheck Remove boundary at time... 'selected_tier_number' to_remove[i]
endfor

# Clean the concatenated text
tiernum = Get interval at time... 'selected_tier_number' selection_start-0.01
nocheck Set interval text... 'selected_tier_number' 'tiernum'   
