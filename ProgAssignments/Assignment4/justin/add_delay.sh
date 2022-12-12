# apparently, we can't add it from the master node, so we'll send this file to every worker node using scp  
tc qdisc add dev eth0 root netem delay 200ms
