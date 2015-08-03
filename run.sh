#!/bin/bash
# First parameter is the tests directory
# Second parameter is the usegraph used
# Third parameter is the results directory to save results in

bool=false
for d in $1/*
do
    if ! $bool; then
        python3.4 propl.py $d/ 10 --usegraph $2 --rslts_dir $3 --save_tex
    else
        python3.4 propl.py $d/ 10 --usegraph $2 --rslts_dir $3 --clean_tex --save_tex
        bool=true
    fi
done
