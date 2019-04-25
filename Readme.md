# This is my tools
## myssh 
### Description:
> This is a simple tool to replace putty, xshell and so on. 
> The info of servers is located in /etc/ansible/hosts, the same as the ansible inventroy file in ini mode.

### Usage:
#### To depend on sshpass command. If not installed,please install it.
#### Edit your /etc/ansible/hosts file
> If you don't like to modify global file such as /etc/ansible/hosts file, you can create a ansible.hosts file in your local home directory.
#### Create soft link
```
sudo ln -s your_path/myssh.sh /usr/bin/myssh
sudo ln -s your_path/from_remote.sh /usr/bin/fromRemote
sudo ln -s your_path/to_remote.sh /usr/bin/toRemote
```
#### How to use
```
#suppose your /etc/ansible/hosts is as below:
120_server            ansible_ssh_host=135.242.137.120      ansible_ssh_pass=luis       ansible_ssh_user=luis

#ssh to 120_server
myssh 120_server

#run some commands
myssh 120_server "ls -l /tmp"

#copy some files to remote 
toRemote host_alias src_file remote_file

#copy some file from remote
fromRemote host_alias remote_file local_file

#sync /etc/ansble/hosts to /etc/hosts root privilege needed.
sudo python sync.py 
```

## vimrc
### Description:
> This is a vimrc file. To customize your own vimrc file.

### How to use
```
# cp the .vimrc file to your local home, and overwrite the old .vimrc file
cp .vimrc ~/
```

### Main highlight
* F1 Move line to next line. The reserve operation of ctrl + J
* F3 Disable high light search. set no hlsearch
* F4 save and exit all files. :wqa
* F5 Run the script and print out the output. Only .sh .py .pl .exp support.
* F6 change the focus to other window. ctrl + w + left
* F12 delete black line. delete CR M^. 
* crtl + d  Add comment. Support mutil-line.
* ctrl+a select all
* f format code

### How to use F5 when passing some args
```
Type "#args: a b c" in your script could pass the args the script needs.
for ex:

#!/bin/bash
#args: /tmp
ls $1

If the args is /tmp the command is ls /tmp. This is only used for test when press F5 to run.
```

## py/ssh_py2.py and py/ssh_py3.py
### Prerequire
```bash
# for python2
pip2 install paramiko py2chainmap

#  for python3
pip3 install paramiko

``` 
### How to use
#### Create a Server object
```python
host = Server('127.0.0.1', 'root', 'root')
```
#### Remote run some commands
```python
result, status = host.run_command('ls -l', '/root')
```
#### Use sftp to download and upload
```python
    host = Server('127.0.0.1', 'root', 'root')
    # upload the local directory to remote
    host.sftp_put_dir(r'/home/xliu074/Pictures', r'/tmp/')
    # upload the local file to remote
    host.sftp_put_file(r'/home/xliu074/Pictures/b', r'/tmp/Pictures/b')
    
    # download the remote directory to local
    host.sftp_get_dir(r'/home/xliu074/Pictures', r'/tmp')
    # download the remote file to local
    host.sftp_get_file(r'/home/xliu074/Pictures/b', r'/tmp/b')

```