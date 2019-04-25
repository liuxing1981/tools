# -*- coding: utf-8 -*-
import os
import py2chainmap
from stat import S_ISDIR
import paramiko


# 定义一个类，表示一台远端linux主机
class Server(object):
    # 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
    def __init__(self, ip, username, password, port=22, timeout=30):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        # transport和chanel
        self.t = ''
        self.chan = ''
        # 链接失败的重试次数
        self.try_times = 3

    # get单个文件
    def sftp_get_file(self, remotefile, localfile):
        t = paramiko.Transport(sock=(self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if localfile[-1] in ('/', r'\\'):
            localfile += os.path.basename(remotefile)
        sftp.get(remotefile, localfile)
        print('Download file from {} to {}'.format(remotefile, localfile))
        t.close()

    # put单个文件
    def sftp_put_file(self, localfile, remotefile):
        t = paramiko.Transport(sock=(self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if remotefile[-1] in ('/', r'\\'):
            remotefile += os.path.basename(localfile)
        sftp.put(localfile, remotefile)
        print('Upload file from {} to {}'.format(localfile, remotefile))
        t.close()

    # ------获取远端linux主机上指定目录及其子目录下的所有文件------
    def __get_all_files_in_remote_dir(self, sftp, remote_dir):
        # 保存所有文件的列表
        all_files = {}
        # 获取当前指定目录下的所有目录及文件，包含属性值
        files = sftp.listdir_attr(remote_dir)
        for x in files:
            # remote_dir目录中每一个文件或目录的完整路径
            filename = remote_dir + '/' + x.filename
            # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
            if S_ISDIR(x.st_mode):
                all_files[filename] = 'd'
                all_files = py2chainmap.ChainMap(all_files, self.__get_all_files_in_remote_dir(sftp, filename))
            else:
                all_files[filename] = 'f'
        return all_files

    def sftp_get_dir(self, remote_dir, local_dir):
        t = paramiko.Transport(sock=(self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        all_files = self.__get_all_files_in_remote_dir(sftp, remote_dir)
        dirs = [k for k, v in all_files.items() if v == 'd']
        files = [k for k, v in all_files.items() if v == 'f']
        remote_dir = remote_dir if remote_dir.endswith('/') else remote_dir + '/'
        current_dir = remote_dir.split('/')[-2]
        local_dir = local_dir if local_dir.endswith(os.sep) else local_dir + os.sep
        for dir in dirs:
            dir = dir.replace(remote_dir, '')
            dir = os.path.normpath(local_dir + current_dir + os.sep + dir)
            if not os.path.isdir(dir):
                os.makedirs(dir)
        count = 0
        for filename in files:
            local_filename = filename.replace(remote_dir, '')
            local_filename = os.path.normpath(local_dir + current_dir + os.sep + local_filename)
            print('Download file from %s to %s' %(filename, local_filename))
            sftp.get(filename, local_filename)
            count += 1
        print('Total: ' + str(count) + ' files')
    
    # ------获取本地指定目录及其子目录下的所有文件------
    def __get_all_files_in_local_dir(self, local_dir):
        all_files = {}
        # 获取当前指定目录下的所有目录及文件，包含属性值
        files = os.listdir(local_dir)
        for x in files:
            # local_dir目录中每一个文件或目录的完整路径
            filename = os.path.join(local_dir, x)
            # 如果是目录，则递归处理该目录
            if os.path.isdir(filename):
                all_files[filename] = 'd'
                all_files = py2chainmap.ChainMap(all_files, self.__get_all_files_in_local_dir(filename))
            else:
                all_files[filename] = 'f'
        return all_files

    def sftp_put_dir(self, local_dir, remote_dir):
        try:
            t = paramiko.Transport(sock=(self.ip, self.port))
            t.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(t)
            # 去掉路径字符最后的字符'/'，如果有的话
            if remote_dir[-1] == '/':
                remote_dir = remote_dir[0:-1]
            # 获取本地指定目录及其子目录下的所有文件
            all_files = self.__get_all_files_in_local_dir(local_dir)
            dirs = [k for k, v in all_files.items() if v == 'd']
            files = [k for k, v in all_files.items() if v == 'f']
            remote_dir = remote_dir if remote_dir.endswith(os.sep) else remote_dir + '/'
            local_dir = local_dir if local_dir.endswith(os.sep) else local_dir + os.sep
            current_dir = local_dir.split(os.sep)[-2]
            for dir in dirs:
                dir = dir.replace(local_dir, '')
                dir = dir.replace('\\', '/')
                dir = remote_dir + current_dir + '/' + dir
                self.run_command('mkdir -p ' + dir)
            count = 0
            for filename in files:
                remote_filename = filename.replace(local_dir, '')
                remote_filename = remote_filename.replace('\\', '/')
                remote_filename = remote_dir + current_dir + '/' + remote_filename
                print('Upload file from %s to %s' %(filename, remote_filename))
                sftp.put(filename, remote_filename)
                count += 1
            print('Total: ' + str(count) + ' files')
        except Exception as e:
            print(e)
            print('ERROR:  Maybe {} is not a directory. This method only supports directory'.format(local_dir))

    def run_command(self, command, chdir='/tmp'):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip,port=self.port,username=self.username,password=self.password)
        stdin, stdout, stderr = ssh.exec_command("cd %s && %s" %(chdir, command))
        exit_code = stdout.channel.recv_exit_status()
        err = stderr.read()
        if exit_code != 0:
            ssh.close()
            return err, exit_code
        else:
            ssh.close()
            return ('\n').join([x.strip('\n') for x in stdout.readlines()]), exit_code


# if __name__ == '__main__':
#     host = Server('10.67.27.139', 'root', 'root')
#     # print(host.run_command('ls -l', '/root')[0])
#     host.sftp_put_dir(r'/home/xliu074/Pictures', r'/tmp/')
#     host.sftp_get_file(r'/home/xliu074/Pictures/b', r'/tmp/Pictures/b')
#     host.sftp_get_dir(r'/home/xliu074/Pictures', r'/tmp')
