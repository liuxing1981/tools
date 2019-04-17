import os
from stat import *

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

    # 调用该方法连接远程主机
    def connect(self):
         pass

    # 断开连接
    def close(self):
        pass

    # 发送要执行的命令
    def send(self, cmd):
        pass

    # get单个文件
    def sftp_get_file(self, remotefile, localfile):
        t = paramiko.Transport(sock=(self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(remotefile, localfile)
        t.close()

    # put单个文件
    def sftp_put_file(self, localfile, remotefile):
        t = paramiko.Transport(sock=(self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(localfile, remotefile)
        t.close()

    # ------获取远端linux主机上指定目录及其子目录下的所有文件------
    def __get_all_files_in_remote_dir(self, sftp, remote_dir):
        # 保存所有文件的列表
        all_files = list()

        # 去掉路径字符串最后的字符'/'，如果有的话
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        # 获取当前指定目录下的所有目录及文件，包含属性值
        files = sftp.listdir_attr(remote_dir)
        for x in files:
            # remote_dir目录中每一个文件或目录的完整路径
            filename = remote_dir + '/' + x.filename
            # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
            if S_ISDIR(x.st_mode):
                all_files.extend(self.__get_all_files_in_remote_dir(sftp, filename))
            else:
                all_files.append(filename)
        return all_files

    def sftp_get_dir(self, remote_dir, local_dir):
        t = paramiko.Transport(sock=(self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        relative_path = remote_dir.split('/')[-1]
        if relative_path == '':
            relative_path = remote_dir.split('/')[-2]
        # 获取远端linux主机上指定目录及其子目录下的所有文件
        all_files = self.__get_all_files_in_remote_dir(sftp, remote_dir)
        # 依次get每一个文件
        for x in all_files:
            dirname = x.split('/')[-1]
            # dirname = os.path.join(local_dir, os.path.dirname(x))
            filename = os.path.join(dirname, os.path.basename(x))
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            print('Download file %s ...' % filename)
            sftp.get(x, filename)
    
    # ------获取本地指定目录及其子目录下的所有文件------
    def __get_all_files_in_local_dir(self, local_dir):
        # 保存所有文件的列表
        all_files = list()

        # 获取当前指定目录下的所有目录及文件，包含属性值
        files = os.listdir(local_dir)
        for x in files:
            # local_dir目录中每一个文件或目录的完整路径
            filename = os.path.join(local_dir, x)
            # 如果是目录，则递归处理该目录
            if os.path.isdir(x):
                all_files.extend(self.__get_all_files_in_local_dir(filename))
            else:
                all_files.append(filename)
        return all_files

    def sftp_put_dir(self, local_dir, remote_dir):
        t = paramiko.Transport(sock=(self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)

        # 去掉路径字符穿最后的字符'/'，如果有的话
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        # 获取本地指定目录及其子目录下的所有文件
        all_files = self.__get_all_files_in_local_dir(local_dir)
        # 依次put每一个文件
        for x in all_files:
            filename = os.path.split(x)[-1]
            remote_filename = remote_dir + '/' + filename
            print('Upload file %s ...' % filename)
            sftp.put(x, remote_filename)

    def run_command(self, command, chdir='/tmp'):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip,port=self.port,username=self.username,password=self.password)
        stdin, stdout, stderr = ssh.exec_command("cd %s && %s" %(chdir, command))
        if stdout is not None:
            return [ x.strip('\n') for x in stdout.readlines() ]
        if stderr is not None:
            print(stderr.readlines())
        ssh.close()


if __name__ == '__main__':
    host = Server('114.215.64.121', 'root', 'SvL9n9123!')
    # print(host.run_command('ls -l', '/root/test'))
    # 将远端remote_path目录中的所有文件get到本地local_path目录
    host.sftp_get_dir(r'/root/test', r'e:\tmp')
    # # 将本地local_path目录中的所有文件put到远端remote_path目录
    # host.sftp_put_dir(remote_path, local_path)
