# transforms the HVite output *.rec which lists the found segments
# in terms of:
# beg end label
# where beg, end are times measured in 10nsec units
# into a mau tier based on SIGNALRATE
# inter-word silence is treated in a complicated way (see maus)

# Insert any reverse mapping from GRAPHINVENTAR to KANINVENTAR here 
# (see comment 'MAPPING')

# File given in PLOSIVES residing in the local dir contains all SAMPA symbols
# (one per line) that should be treated as plosives at word boundaries;
# this file can contain a super-set of necessary symbols (e.g. all 
# known SAMPA plosives)

BEGIN   {
          idx = 0
	  begoffset = 0
	  wrdidx = STARTWORD
	  spread = 0
          shiftsam = MAUSSHIFT * SIGNALRATE / 1000 
	  shiftframe = MAUSSHIFT * FRAMERATE / 1000
	  framelengthsam = SIGNALRATE / FRAMERATE
          if ( PLOSIVES != "" ) {
            while ( getline < PLOSIVES > 0 ) { 
              plosives[$0] = 1
            }
          }
	}  
	
	{ begsam =  $1 * SIGNALRATE / 10000000  
	  durframe = ($2 - $1) * FRAMERATE / 10000000
	  dursam = ( ($2 - $1) * SIGNALRATE / 10000000 ) - 1
	  # first label at 0? -> duration is increased by shift
	  if ( begsam == 0 )
	  {
	    dursam += shiftsam
	    durframe += shiftframe
	  }  
	  else
	  # other segments shifted but have the same length
	  {
	    begsam += shiftsam
	  }  
	  # correct for the case that begsam gets negative (first label and 
	  # MAUSSHIFT is negativ) -> duration is decreased
	  if ( begsam < 0 ) 
	  {
	    dursam -= begsam 
	    durframe -= begsam / framelengthsam
	    begsam = 0
	  }  
	  label = $3
	  # reverse MAPPING : the mapping of input phoneme set to 
	  # internal phoneme set that took place in kan2mlf.awk
	  # has to be reversed here to produce consistent output
	  gsub(/P1/,"1",label)
	  gsub(/P2/,"2",label)
	  gsub(/P3/,"3",label)
	  gsub(/P4/,"4",label)
	  gsub(/P5/,"5",label)
	  gsub(/P6/,"6",label)
	  gsub(/P7/,"7",label)
	  gsub(/P8/,"8",label)
	  gsub(/P9/,"9",label)

	  if ( label == "#" || label == "&" || label == "<p:>" )
	  {
	    # special treatment for word delimiter and word-internal pauses
	    wrdidx ++
	    if ( idx == 0 ) 
	    {
	      printf("ERROR: The first segment cannot be a word delimiter - exiting\n") > "/dev/stderr"
	      exit -1
	    } 
	    if ( durframe < MINPAUSLEN )
	    {
	      # pause is smaller than limit:
	      # segment is not output and spread to its adjacent segments 
	      # when the next regular segment is read
	      begoffset = (dursam+1)/2
	    }
	    else
	    {
	      # pause is of minimum length or larger - pause is output as a regular segment
	      begins[idx] = begsam
	      durations[idx] = dursam
	      labels[idx] = "<p:>"
	      wrdindices[idx] = -1
	      idx ++
	    }
	  }
	  else
	  {
	    # regular segment
	    gsub(/^<$/,"<p:>",label)
	    gsub(/^>$/,"<p:>",label)
	    if ( begoffset != 0 ) 
	    # the previous segment was a deleted silence interval
	    # now there are 4 cases: 
	    # plosive sil plosive : spread deleted sil to both plosives
	    # non-plosive sil non-plosive : spread deleted sil to both non-plosives
	    # plosive sil non-plosive : spread deleted sil to previous plosive
	    # non-plosive sil plosive : spread deleted sil to following plosive
	    {
	      if ( ( plosives[substr(label,1,1)] == 1 && plosives[substr(labels[idx-1],1,1)] == 1 ) || ( plosives[substr(label,1,1)] != 1 && plosives[substr(labels[idx-1],1,1)] != 1 ) )
	      {
	      # correct current and previous segment by half of 
	      # the deleted silence
	        begsam -= begoffset
	        dursam += begoffset
		durations[idx-1] += begoffset
	      } 
	      else
	      # correct plosive by fully adding the previously deleted silence
	      {
	        # current segment is a plosive
	        if ( plosives[substr(label,1,1)] == 1 )
		{
	          begsam -= begoffset * 2
	          dursam += begoffset * 2
		}  
		else
		# previous segment was a plosive
		{
		  durations[idx-1] += begoffset * 2
		}  
	      }
	      begoffset = 0
	    }
	    # now store the current segment
	    begins[idx] = begsam
	    durations[idx] = dursam
	    labels[idx] = label
	    if ( label != "<p:>" ) wrdindices[idx] = wrdidx
	    else wrdindices[idx] = -1
	    idx ++
	  }
	}
END     {
          for ( id=0; id<idx; id++ )
          {
            #print "begin : " begins[id] " dur : " durations[id]
            if ( id == ( idx-2) )
            {
            #print "begin-2 : " begins[id] " du-2 : " durations[id] "begin-1 : " begins[id+1] " du-1 : " durations[id+1]
              # correct the duration of the last segment so that the total
              # length of the utterance stays constant
              durations[id+1] -= shiftsam
              # Version 2.33
              # Because of a bug in HTK the last silence interval segment '>'
              # can be of length 0 (although it should have at least 1 frame).
              # This combined with the above correction can cause a last
              # segment with negative length. To prevent this we set the
              # length of the last segment to zero and correct the length
              # of the previous segment accordingly, so that the total
              # utterance length stays constant
              if ( durations[id+1] < 0 )
              {
                durations[id] += durations[id+1] + 1
                begins[id+1] += durations[id+1] + 1
                durations[id+1] = 0
              }
            #print "begin-2 : " begins[id] " du-2 : " durations[id] "begin-1 : " begins[id+1] " du-1 : " durations[id+1]
            }
            # Version 2.18
            # check for consecutive segments (important for Emu import!)
            # the start of a segment must be exactly the end of the previous
            # segment (start + dur) plus 1
            #
            # Although this is not required from the BPF format, import
            # routines of other programs seem to have
            # a problem with non-consecutive
            # segmentations; therefore we do it here, since it does not
            # hurt anyway.
            #print "begin : " begins[id] " dur : " durations[id]
            if ( id > 0 )
            {
              begin_l = begins[id-1]+durations[id-1]+1
              if ( begins[id] != begin_l )
              {
                durations[id] = durations[id]+(begins[id]-begin_l)
                begins[id] = begin_l
              }
            }
            #print "begin : " begins[id] " dur : " durations[id]
            printf("MAU:\t%d\t%d\t%d\t%s\n",begins[id],durations[id],wrdindices[id],labels[id])
          }

	}  
       	
