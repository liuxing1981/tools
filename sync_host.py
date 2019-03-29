#########################################################################
# File Name: sync_host.py
# Author: root
# mail: lx_figo@qq.com
# Created Time: 2019-01-31 15:37
#########################################################################
#!/usr/bin/python
map = {}
hosts = []
with open('/etc/ansible/hosts', 'rt') as f:
    for line in f.readlines():
        if line is not None:
            spline = line.split()
            host = spline[0]
            ip = spline[1].split('=')[1]
            map[ip] = host

with open('/etc/hosts', 'a+') as f:
    f.seek(0)
    for line in f.readlines():
        if line is not '\n':
            ip = line.split()[0]
            hosts.append(ip)
    ansible_host = list(map.keys())
    ret = list(set(ansible_host) - set(hosts))
    print(ansible_host)
    print(hosts)
    print(ret)
    for ip in ret:
        f.write('{} {}\n'.format(ip, map[ip]))
        print('{} {}'.format(ip, map[ip]))

