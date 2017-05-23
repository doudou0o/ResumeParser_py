#!/bin/sh

echo "working path: "$(cd `dirname $0`; pwd)

servername="ecv_parser_gm_server.py"

pids=`ps aux | grep "$servername" | grep -v "grep" | awk '{print $2}' `

echo "PIDS:"${pids}

pids_l=($pids)
len=${#pids_l[*]}

echo "num of processes: "${#pids_l[*]}
echo "main process:"${pids_l[0]}
# kill sub process
for ((i=1;i<${len};i++))
do
    echo "kill sub process "$i": "${pids_l[i]}
    kill -9 ${pids_l[i]}
done

# kill main process
echo "waiting main process terminated..."
sleep 1

kill -9 ${pids_l[0]}

echo "start server..."
nohup python ecv_parser_gm_server.py >> ../log/nohuo.out &
echo "enjoy it"
