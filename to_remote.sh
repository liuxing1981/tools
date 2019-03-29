#########################################################################
# File Name: myscp.sh
# Author: root
# mail: lx_figo@qq.com
# Created Time: 2018-12-15 09:57
#########################################################################
#!/bin/bash
#args: 120 *.sh
CONFIG=/etc/ansible/hosts
myhost=$1
src=$2
dest=$3
dest=${dest:="/tmp"}

line=`awk -v myhost=$myhost '{if($1 == myhost) print $0}' $CONFIG`
USER=`echo $line | egrep -o "ansible_ssh_user=\w+" | awk -F= '{print $2}'`
SERVER=`echo $line | egrep -o "ansible_ssh_host=\w+\.\w+\.\w+\.\w+" | awk -F= '{print $2}'`
PASSWORD=`echo $line | egrep -o "ansible_ssh_pass=\w+" | awk -F= '{print $2}'`
PORT=`echo $line | egrep -o "ansible_ssh_ports\w+" | awk -F= '{print $2}'`

scp_to_remote(){
	if [ -f "$SERVER.pem" ];then
		cmd="scp -r -o stricthostkeychecking=no -i $src $SERVER.pem $USER@$SERVER:$dest"
	else
	    cmd="sshpass -p $PASSWORD scp -r -o stricthostkeychecking=no $src $USER@$SERVER:$dest"
	fi
	echo $cmd
	eval $cmd
}

scp_to_remote
