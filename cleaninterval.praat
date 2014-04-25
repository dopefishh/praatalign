    start = Get start of selection
    end = Get end of selection
    info$ = Editor info
    tiernumber = extractNumber(info$, "Selected tier:")
	info$ = TextGrid info
	tg$ = extractLine$(info$, "Object name: ")
    i = 0
    Move cursor to... 'start'
	endpnt = Get end point of interval
	while endpnt < end
		i = i + 1
        Select next interval
        toremove[i] = Get starting point of interval
        endpnt = Get end point of interval
	endwhile
endeditor
select TextGrid 'tg$'
for j to i
    nocheck Remove boundary at time... 'tiernumber' toremove[j]
endfor
tiernum = Get interval at time... 'tiernumber' start-0.01
nocheck Set interval text... 'tiernumber' 'tiernum'   
