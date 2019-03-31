#echo -e "\033[30m 黑色字 \033[0m"
#echo -e "\033[31m ERROR \033[0m"
#echo "\033[32m GREEN \033[0m"
#echo -e "\033[33m 黄色字 \033[0m"
#echo -e "\033[34m 蓝色字 \033[0m"
#echo -e "\033[35m 紫色字 \033[0m"
#echo -e "\033[36m 天蓝字 \033[0m"
#echo -e "\033[37m 白色字 \033[0m"


color(){
	text=$1
	color=$2
	if [ "$color" = "red" ];then
		nu=31
	elif [ "$color" = "green" ];then
		nu=32
	elif [ "$color" = "yellow" ];then
		nu=33
	elif [ "$color" = "blue" ];then
		nu=34
	elif [ "$color" = "purper" ];then
		nu=35
	elif [ "$color" = "skyblue" ];then
		nu=36
	elif [ "$color" = "white" ];then
		nu=37
	fi
	echo "\033[0;40;${nu}m$text\033[0m"
}


color hiasdfasdfaa blue
