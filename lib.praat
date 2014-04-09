#Get the tier number
procedure getTierNumber .tiername$ .tiernumber$
	.n = Get number of tiers
	'.tiernumber$' = -1
	for .i to .n
		.name$ = Get tier name... .i
		if .name$ = .tiername$
			'.tiernumber$' = .i
		endif
	endfor
endproc

#Remove all intervals between times
procedure removeBetween .tiernumber .start .end
	.i = .start
	repeat
		.numint = Get interval at time... '.tiernumber' '.i'
		.startpnt = Get start point... '.tiernumber' '.numint'
		if .startpnt >= .start
			Remove left boundary... '.tiernumber' '.numint'
		endif
		.i += 0.001
	until .i>=.end
	.numint = Get interval at time... '.tiernumber' '.start'+0.001
	.endpnt = Get end point... '.tiernumber' '.numint'
	if .endpnt <= .end
		Remove right boundary... '.tiernumber' '.numint'
	endif
	Set interval text... '.tiernumber' '.numint' 
endproc
