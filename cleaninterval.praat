include procs.praat
	selection_start = Get start of selection
	selection_end = Get end of selection
	editor_info$ = TextGrid info
	textgrid_object$ = "TextGrid " + extractLine$(editor_info$, "Object name: ")
	editor_info$ = Editor info
	selected_tier_number = extractNumber(editor_info$, "Selected tier:")
endeditor
	@cleanAnnotation: textgrid_object$, selected_tier_number, selection_start, selection_end
