#########################################################################
# File Name: myssh.sh
# Author: luis.liu
# mail: lx_figo@qq.com
# Created Time: 2018-12-15 09:57
#########################################################################
#!/bin/bash
#args: pgw1
if [ -f ~/ansible.host ];then
	CONFIG=~/ansible.host
else 
	CONFIG=/etc/ansible/hosts
fi
echo $CONFIG
if [ ! "$1" ];then
	echo "no hosts!"
	awk '{printf "%-10s  %s\n",$1,$2}' $CONFIG | sed 's/ansible_ssh_host=//' | sort
	exit 1
fi
host=$1
cmd=$2
line=`awk -v myhost=$myhost '{if($1 == myhost) print $0}' $CONFIG`
USER=`echo $line | egrep -o "ansible_ssh_user=\w+" | awk -F= '{print $2}'`
SERVER=`echo $line | egrep -o "ansible_ssh_host=\w+\.\w+\.\w+\.\w+" | awk -F= '{print $2}'`
PASSWORD=`echo $line | egrep -o "ansible_ssh_pass=\w+" | awk -F= '{print $2}'`
PORT=`echo $line | egrep -o "ansible_ssh_ports\w+" | awk -F= '{print $2}'`
${PORT:=22}

login_remote(){
	if [ -f "$SERVER.pem" ];then
		cmd="ssh -p $PORT -o stricthostkeychecking=no -i $SERVER.pem $USER@$SERVERi $command"
	else
		cmd="sshpass -p $PASSWORD ssh -p $PORT -o stricthostkeychecking=no -tt $USER@$SERVER $command"
	fi
	echo $cmd
	eval $cmd
}

login_remote 
