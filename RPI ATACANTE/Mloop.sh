IN="/run/user/1000/outF0"
OUT=$1
datafile=$2
nmuestras=$3
x=`seq 1 $nmuestras`
#http://swigerco.com/cswiger/plotting.html
#Por sis quieres ver como funciona el raw2num
mkdir $1
for i in $x; do
    var=`./lectura /home/adam/$datafile $i`
    sudo ./launcher $var /home/adam/$OUT/file1.txt $i &
    sudo python ./top_block.py
    if [ -f /run/user/1000/NO.txt ];
    then
    break

    else
    mv $IN $OUT"/out_"$i
    fi
done

