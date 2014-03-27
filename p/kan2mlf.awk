#
# transforms the KAN tier of a Partitur file into a list of Phonemes
# defined in the file INVENTAR (usually KANINVENTAR)
# INVENTAR must contain the valid phones in reverse length 
# order ('aI' before 'a'. It may contain the silence symbols
# '#', '<', '>' and '&'.
# Special characters '#', ''', '"' and '+' are deleted from the 
# KAN tier befor processing. 
# Numeric phoneme labels are translated into 'P' + label to match 
# HTK requirements (e.g. '6' -> 'P6').
# At the beginning the script print a '<' and at the end a '>' for
# beginning and ending silence resp.

# If the internal phoneme set of MAUS (usually GRAPHINVENTAR) differs 
# for some reasons (e.g. HMM sharing) from INVENTAR, these mappings have to 
# be handled here and the reverse mapping is handled in the script
# PARAM/rec2mau.awk respectively. (see comment 'MAPPING')
#
# This script can be used to create a phonemic MLF without timing information,
# but magic number and file name are not written here.

# If the option STARTWORD is greater than 0, the script starts with the 
# the word number in STARTWORD and ends with the word given in the option
# ENDWORD. ENDWORD must be greater than STARTWORD; if ENDWORD is 0, it is
# set to 999999.

BEGIN {
        invcount = 0
        while ( getline < INVENTAR > 0 )
        { 
          inv[$0] = invcount
#          print $0
          invcount ++
        }
        print "<"
        firstpause = 0
	if ( ENDWORD == "" || ENDWORD == 0 ) ENDWORD = 999999
	if ( STARTWORD == "" ) STARTWORD = 0
	if ( STARTWORD > ENDWORD ) 
	{
	  printf("ERROR in kan2mlf: STARTWORD (%d) is greater than ENDWORD (%d)\n",STARTWORD,ENDWORD) > "/dev/stderr"
	  exit 2
	}  
	wordnr = 0
      }

/^KAN:/ {
          if ( wordnr < STARTWORD ) 
	  {  
	    wordnr ++
	    next
	  }
	  if ( wordnr > ENDWORD ) next

          if ( firstpause == 0 )
            firstpause = 1
          else
            print "#"

          # the SAMPA transcript is blank separated, therefore we take the 
	  # line starting with $3 as phones
	  n = 3
	  while(n<=NF) { 
	    phon = $n; 
	    # delete accent markers, function word markers and compound markers.
	    #gsub(/#/,"",phon)
            gsub(/'/,"",phon)
            gsub(/"/,"",phon)
            gsub(/\+/,"",phon)
            if ( inv[phon] == "" )
            {
              printf("ERROR: unknown phoneme (%s) in %s\n",phon,$0) > "/dev/stderr"
              exit 1 
            }
            gsub(/1/,"P1",phon)
            gsub(/2/,"P2",phon)
            gsub(/3/,"P3",phon)
            gsub(/4/,"P4",phon)
            gsub(/5/,"P5",phon)
            gsub(/6/,"P6",phon)
            gsub(/7/,"P7",phon)
            gsub(/8/,"P8",phon)
            gsub(/9/,"P9",phon)
	    print phon

	    n++; 
	  }
	  wordnr ++
        }
END     {
          print ">"

          print "."
        }
