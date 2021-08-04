# coding=utf-8
import os,sys,configparser
from ftplib import FTP  # 引入ftp模块


class MyFtp:

    ftp = FTP()

    def __init__(self,host,port=21):
        self.ftp.connect(host,port)

    def login(self,username,pwd):
        self.ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
        self.ftp.login(username,pwd)
        print(self.ftp.welcome)

    def downloadFile(self,localpath,remotepath):
        os.chdir(localpath)   # 切换工作路径到下载目录
        self.ftp.cwd(remotepath)   # 要登录的ftp目录
        #self.ftp.nlst()  # 获取目录下的文件

        names = self.ftp.nlst()
        final_names = [line for line in names]
        latest_time = None
        latest_name = None
        for name in final_names:
            time = self.ftp.sendcmd("MDTM " + name)
            if (latest_time is None) or (time > latest_time):
                latest_name = name
                latest_time = time
        print(latest_name)
        file_handle = open(latest_name,"wb").write   # 以写模式在本地打开文件
        self.ftp.retrbinary('RETR %s' % os.path.basename(latest_name),file_handle,blocksize=1024)  # 下载ftp文件
        # ftp.delete（filename）  # 删除ftp服务器上的文件

    def close(self):
        self.ftp.set_debuglevel(0)  # 关闭调试
        self.ftp.quit()

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    elif __file__:
        path = os.path.dirname(__file__)

    '''
    parent_path = os.path.dirname(path)
    print("parentpath:")
    print(parent_path)
    '''
    print(path)
    configPath = os.path.join(path, "ftp.ini")
    config = configparser.ConfigParser()
    config.read_file(open(configPath))
    host = config.get("Config", "ftphost")
    user = config.get("Config", "username")
    psw = config.get("Config", "password")
    ftppath = config.get("Config", "ftppath")
    localpath = config.get("Config", "localpath")
    ftp = MyFtp(host)
    ftp.login(user,psw)
    ftp.downloadFile(localpath,ftppath)
    ftp.close()