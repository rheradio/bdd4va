export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$1
out=$($1/BDDSampler -names $2 $3)
echo "$out"
