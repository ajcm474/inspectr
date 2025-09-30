#!/usr/bin/env bash

# Minimum block size
BLOCK=1

# Minimum occurrences
MIN_OCCUR=2

# Combine all files, prefix each line with filename:linenumber
awk -v blk="$BLOCK" '
FNR==1{file=FILENAME}
{
  lines[NR] = $0
  files[NR] = file
  lnum[NR] = FNR
}
END {
  for (i=1; i<=NR-blk+1; i++) {
    s=""
    for (j=0;j<blk;j++) {
      s = s lines[i+j] "\034"   # \034 is a record separator to avoid ambiguity
    }
    print s "\t" files[i] "\t" lnum[i]
  }
}
' ./*.py | sort | uniq -c | awk -v min="$MIN_OCCUR" '$1>=min {print $3 ":" $4}'

