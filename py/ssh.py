import os
from stat import S_ISDIR
from collections import ChainMap
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
        all_files = {}
        # 获取当前指定目录下的所有目录及文件，包含属性值
        files = sftp.listdir_attr(remote_dir)
        for x in files:
            # remote_dir目录中每一个文件或目录的完整路径
            filename = remote_dir + '/' + x.filename
            # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
            if S_ISDIR(x.st_mode):
                all_files[filename] = 'd'
                all_files = ChainMap(all_files, self.__get_all_files_in_remote_dir(sftp, filename))
            else:
                all_files[filename] = 'f'
        return all_files

    def sftp_get_dir(self, remote_dir, local_dir):
        t = paramiko.Transport(sock=(self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        all_files = self.__get_all_files_in_remote_dir(sftp, remote_dir)
        dirs = [ str(k) for k, v in all_files.items() if v == 'd']
        files = [ k for k, v in all_files.items() if v == 'f']
        remote_dir = remote_dir if remote_dir.endswith(os.sep) else remote_dir + os.sep
        local_dir = local_dir if local_dir.endswith(os.sep) else local_dir + os.sep
        for dir in dirs:
            dir = dir[len(remote_dir):]
            dir = os.path.normcase(local_dir + dir)
            if not os.path.isdir(dir):
                os.makedirs(dir)
        for filename in files:
            local_filename = filename[len(remote_dir):]
            local_filename = os.path.normcase(local_dir + local_filename)
            print('Download file %s to %s' %(filename,local_filename))
            sftp.get(filename, local_filename)
    
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
                all_files = ChainMap(all_files, self.__get_all_files_in_local_dir(filename))
            else:
                all_files[filename] = 'f'
        return all_files

    def sftp_put_dir(self, local_dir, remote_dir):
        t = paramiko.Transport(sock=(self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        # 去掉路径字符最后的字符'/'，如果有的话
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        # 获取本地指定目录及其子目录下的所有文件
        all_files = self.__get_all_files_in_local_dir(local_dir)
        dirs = [ str(k) for k, v in all_files.items() if v == 'd']
        files = [ k for k, v in all_files.items() if v == 'f']
        remote_dir = remote_dir if remote_dir.endswith(os.sep) else remote_dir + '/'
        local_dir = local_dir if local_dir.endswith(os.sep) else local_dir + os.sep
        for dir in dirs:
            dir = dir[len(local_dir):]
            dir = dir.replace('\\', '/')
            dir = remote_dir + dir
            self.run_command('mkdir -p ' + dir)
        for filename in files:
            remote_filename = filename[len(local_dir):]
            remote_filename = remote_filename.replace('\\', '/')
            remote_filename = remote_dir + remote_filename
            print('Upload file from %s to %s' %(filename,remote_filename))
            sftp.put(filename, remote_filename)
     

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
    # host.sftp_get_dir(r'/root/test', r'e:\tmp')
    # # 将本地local_path目录中的所有文件put到远端remote_path目录
    # host.sftp_put_dir(remote_path, local_path)
    host.sftp_get_dir(r'/tmp/Test', r'e:\tmp')
    # # 将本地local_path目录中的所有文件put到远端remote_path目录
    # host.sftp_put_dir(r'e:\tmp', '/tmp')
