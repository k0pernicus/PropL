#!/bin/bash
# First parameter is the usegraph used
# Second parameter is the results directory to save results in

bool = false
for d in "tests/*"
do
    if ["$bool" = true]; then
        python3.4 propl.py $d/ 10 --usegraph $1 --rslts_dir $2 --save_tex
    else
        python3.4 propl.py $d/ 10 --usegraph $1 --rslts_dir $2 --clean_tex --save_tex
        bool = true
    fi
done
