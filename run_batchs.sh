#!/bin/bash

i=0

while [ $i -le 30 ];
do

	if [ $i -eq 0 ] ;
		then
			python3.4 propl.py $1 10 --usegraph usegraph_C.graphml --algorithm update_all_edges_online_opt --save_tex --rslts_dir Rslts_paper/PRF/;
		else
			python3.4 propl.py $1 10 --usegraph usegraph_C.graphml --algorithm update_all_edges_online_opt --save_tex --rslts_dir Rslts_paper/PRF/ --nb_batch $i;
	fi;

	i=$(($i+3));

done
