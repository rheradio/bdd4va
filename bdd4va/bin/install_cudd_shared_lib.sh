#parameter_values=$@
current_dir=$(pwd)

#echo $path
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$path
echo $LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$path
#echo $LD_LIBRARY_PATH
#echo $1
#$($path/logic2bdd -base $1.dddmp $1.var $1.exp)
#echo me cago en la mar
#echo ${path}//logic2bdd
$($path logic2bdd)
