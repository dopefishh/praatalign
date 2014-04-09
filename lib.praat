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

##Check if the tier only has silence
#procedure isSilence .tiernumber .start .end .return$
#	.i = .start
#	.ret = 1
#	while .i+0.1<.end and .ret=1
#		.num = Get interval at time... '.tiernumber' '.i'
#		if .num<>0
#			.val$ = Get label of interval... '.tiernumber' '.num'
#			if .val$="" or .val$="#" or .val$="< n i b >" or .val$=">" or .val$="<"
#				.ret = 0
#			endif
#		endif
#		.i = .i+0.1
#	endwhile
#	'.return$' = .ret
#endproc	

##String splitting
#procedure split .sep$ .str$
#	.seplen = length(.sep$) 
#	.length = 0
#	repeat
#		.strlen = length(.str$)
#		.sep = index(.str$, .sep$)
#		if .sep > 0
#			.part$ = left$(.str$, .sep-1)
#			.str$ = mid$(.str$, .sep+.seplen, .strlen)
#		else
#			.part$ = .str$
#		endif
#		.length = .length+1
#		.array$[.length] = .part$
#	until .sep = 0
#endproc
