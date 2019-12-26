#########################################################################
# File Name: validate_json.py
# Author: xliu074
# mail: xing.1.liu@nokia-sbell.com
# Created Time: 2019-12-03 15:26
#########################################################################
#!/usr/bin/python
import json
import sys
from collections import OrderedDict

file = sys.argv[1]
with open(file) as f:
    try:
        data = json.load(f,object_pairs_hook=OrderedDict)
    except Exception as e:
        print(e)
        sys.exit(1)

if data is not None:
    with open(file,"w") as f:
        json.dump(data,f,indent=4)
