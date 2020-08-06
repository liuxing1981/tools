#########################################################################
# File Name: test.sh
# Author: xliu074
# mail: xing.1.liu@nokia-sbell.com
# Created Time: 2020-08-06 17:50
#########################################################################
#!/bin/bash
#args: test.ldif
sed -r -i '/^dn/{:a;N;/\n\w+/!ba;s/\n //g}' $1
