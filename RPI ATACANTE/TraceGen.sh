#!/bin/bash

IN="/run/user/1000/outF0"
OUT="/media/X1/lasttry/out_"
#http://swigerco.com/cswiger/plotting.html
#Por sis quieres ver como funciona el raw2num
for i in `seq 1 64000`; do
    var=`./lectura /home/adam/random_data.input $i`
    sudo ./launcher $var /media/X1/lasttry/file1.txt $i &
    sudo python ./top_block.py
    if [ -f /run/user/1000/NO.txt ];
    then
    break

    else
    mv $IN $OUT$i
    fi
done
