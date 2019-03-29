#########################################################################
# File Name: docker.sh
# Author: root
# mail: lx_figo@qq.com
# Created Time: 2019-01-16 16:15
#########################################################################
#!/bin/bash
#args: mysql
mysql() {
docker run --name mysql \
	-p 3306:3306 \
	-e MYSQL_ROOT_PASSWORD=root \
	-d mysql:5.7 \
	--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
}
docker rm -f $1 2>/dev/null
eval $1
