#!/bin/bash
# First parameter is the tests directory
# Second parameter is the usegraph used
# Third parameter is the results directory to save results in
# After, the algorithm used

bool=false
for d in $1/*
do
  if [ "$4" != "tag_on_usefull_edges" ]; then
    echo "update_edges"
    if $bool; then
        python3.4 propl.py $d/ 10 --usegraph $2 --nb_batch 20 --rslts_dir $3 --save_tex --algorithm $4
    else
        python3.4 propl.py $d/ 10 --usegraph $2 --nb_batch 20 --rslts_dir $3 --clean_tex --save_tex --algorithm $4
        bool=true
    fi
  else
    echo "tag_edges"
    if $bool; then
        python3.4 propl.py $d/ 10 --usegraph $2 --rslts_dir $3 --save_tex --algorithm $4
    else
        python3.4 propl.py $d/ 10 --usegraph $2 --rslts_dir $3 --clean_tex --save_tex --algorithm $4
        bool=true
    fi
  fi
done
