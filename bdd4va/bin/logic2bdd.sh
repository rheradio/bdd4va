export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$1
out=$($1/logic2bdd -line-length 50 -min-nodes 100000 -constraint-reorder minspan -base $2.dddmp $2.var $2.exp)
echo "$out"
