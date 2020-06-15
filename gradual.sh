#!/bin/bash

limit=$1
increment=$2
IN=`seq 1 $limit`

carpeta=$3
dirmuestras=$4
algo=$5
mkdir $carpeta

for i in $IN; do
    par=$((i*increment))
    
    cd $carpeta
    mkdir $par
    cd /home/jaimeb/Documentos/tesis_malagon/src/tools/aes
    
    ./aes.bin random_data.input $par
    mv spec.txt "spec"$i".txt"
    mv "spec"$i".txt" $dirmuestras
    cd $dirmuestras
    /home/jaimeb/Documentos/tesis_malagon/src/tools/paa/src/apps/aes-paa -t $dirmuestras"/spec"$i".txt" -s $dirmuestras -l 9 -k 256 -b 8 algorithm=$algo device=aes-hw-plain-text -p -D 2> paa.dat.debug > "paa.dat.progress"$i
    mv "paa.dat.progress"$i $carpeta"/"$par
    cd /tmp
    mv debug.* $carpeta"/"$par
    
   
done
