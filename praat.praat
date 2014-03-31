include /home/marlub/Documents/scripts/praat/lib.praat

form Enter new tier
	sentence newtier temp
endform

tg$ = selected$("TextGrid", 1)
snd$ = selected$("LongSound", 1)
select TextGrid 'tg$'
call getTierNumber 'newtier$' tiernumber
if tiernumber=-1
	tiernumber = 1
	Insert interval tier... 1 'newtier$'
endif

plus LongSound 'snd$'
Edit
editor TextGrid 'tg$'
	pause Continue
	start = Get start of selection
	end = Get end of selection
	label$ = Get label of interval
	Add interval on tier 1
endeditor

basetmp$ = "praat_temp_out"
tmp$ = "/tmp/" + basetmp$
system /usr/bin/python /home/marlub/Documents/scripts/pralign/aligner.py "'label$'" 'start' 'end' /home/marlub/Documents/tzeltal/forcealign/2013March27_PaseroKunerolBartolo_L.wav tze /home/marlub/Documents/scripts/pralign/ruleset.tze False > 'tmp$'
Read Table from comma-separated file... 'tmp$'
rows = Get number of rows

for i to rows
	select Table 'basetmp$'
	start$ = Get value... 'i' start
	end$ = Get value... 'i' end
	value$ = Get value... 'i' label
	select TextGrid 'tg$'
	Insert boundary... 'tiernumber' 'end$'
	time = 'start$' + 0.01
	intnum = Get interval at time... 'tiernumber' 'time'
	Set interval text... 'tiernumber' 'intnum' 'value$'
endfor

