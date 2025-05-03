
pre_in="../dataset/mitosis-5d"
pre_out="/tmp/saida_"
suf=".tif "
w=24
cmd2="convert "
h=13
for i in $(seq 0 $h)
do
    cmd="convert " 
    min=$(($i*$w))
    max=$(( $(($i+1))*$w-1 ))
    for j in $(seq -f "%04g" $min $max)
    do
      #echo $min $max
      cmd=$cmd$pre_in$j$suf
    done
    cmd=$cmd" +append /tmp/saida_"$i".tif"
    echo $cmd
    $cmd
    cmd2=$cmd2$pre_out$i$suf
done
cmd2=$cmd2" -append /tmp/saida.tif"
echo $cmd2
$cmd2

