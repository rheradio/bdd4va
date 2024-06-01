export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$1
out=$($1/feature_probabilities ${@:2})
echo "$out"