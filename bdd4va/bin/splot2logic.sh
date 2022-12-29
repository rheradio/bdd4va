export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$1
out=$($1/splot2logic -use-XOR $2)
echo "$out"
