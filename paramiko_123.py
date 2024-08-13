# coding:utf-8
import paramiko

hostname='47.103.118.47'
port=22
username='webs'
password='u7power@webs'

#基于用户名和密码的 sshclient 方式登录
def test00():
    client = paramiko.SSHClient()
    # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = client.exec_command('df -h ')  # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值

    print(stdout.read().decode('utf-8'))
    client.close()

#基于用户名和密码的 transport 方式登录 SSHClient 封装 Transport
def test01():
    # 创建一个通道
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    ssh = paramiko.SSHClient()
    ssh._transport = transport

    stdin, stdout, stderr = ssh.exec_command('df -h')
    print(stdout.read().decode('utf-8'))
    transport.close()

#基于公钥密钥的 SSHClient 方式登录
def test02():
    # 指定本地的RSA私钥文件,如果建立密钥对时设置的有密码，password为设定的密码，如无不用指定password参数
    pkey = paramiko.RSAKey.from_private_key_file('/home/super/.ssh/id_rsa', password='12345')
    # 建立连接
    ssh = paramiko.SSHClient()
    ssh.connect(hostname='192.168.2.129',
                port=22,
                username='super',
                pkey=pkey)
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command('df -hl')
    # 结果放到stdout中，如果有错误将放到stderr中
    print(stdout.read().decode())
    # 关闭连接
    ssh.close()

#基于密钥的 Transport 方式登录
def test03():
    # 指定本地的RSA私钥文件,如果建立密钥对时设置的有密码，password为设定的密码，如无不用指定password参数
    pkey = paramiko.RSAKey.from_private_key_file('/home/super/.ssh/id_rsa', password='12345')
    # 建立连接
    trans = paramiko.Transport(('192.168.2.129', 22))
    trans.connect(username='super', pkey=pkey)

    # 将sshclient的对象的transport指定为以上的trans
    ssh = paramiko.SSHClient()
    ssh._transport = trans

    # 执行命令，和传统方法一样
    stdin, stdout, stderr = ssh.exec_command('df -hl')
    print(stdout.read().decode())

    # 关闭连接
    trans.close()

def single_file():
    # 创建一个通道
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    # 设置上传的本地/远程文件路径
    localpath = r"D:\tmp\download\123.zip"
    remotepath = "/home/webs/123.zip"
    
    # 执行上传动作
    sftp.put(localpath, remotepath)
    # 执行下载动作
    #ssh.get(remotepath, localpath)
    sftp.close()

    #D:\Pycharm\hadoop_spark\ssh_files\id_rsa      本地路径,（windows)
    #/usr/local/id_rsa                             远端服务器路径，（Linux）
    #两边路径必须都写上文件名

def nulti_file():
    transport = paramiko.Transport(('host',port))
    transport.connect(username='root',password='123')
    sftp = paramiko.SFTPClient.from_transport(transport)
    for path in dir_list:
        for root, dirs, files in os.walk('D:/Pycharm/hadoop_spark/hadoop_config/'):
    　　　for i in files:
                sftp.put('D:/Pycharm/hadoop_spark/hadoop_config/' + i,'/usr/local/' + i)
    transport.close()

#实现输入命令立马返回结果的功能 
def test04():

    import paramiko
    import os
    import select
    import sys

    # 建立一个socket
    trans = paramiko.Transport(('192.168.2.129', 22))
    # 启动一个客户端
    trans.start_client()

    # 如果使用rsa密钥登录的话
    '''
    default_key_file = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
    prikey = paramiko.RSAKey.from_private_key_file(default_key_file)
    trans.auth_publickey(username='super', key=prikey)
    '''
    # 如果使用用户名和密码登录
    trans.auth_password(username='super', password='super')
    # 打开一个通道
    channel = trans.open_session()
    # 获取终端
    channel.get_pty()
    # 激活终端，这样就可以登录到终端了，就和我们用类似于xshell登录系统一样
    channel.invoke_shell()
    # 下面就可以执行你所有的操作，用select实现
    # 对输入终端sys.stdin和 通道进行监控,
    # 当用户在终端输入命令后，将命令交给channel通道，这个时候sys.stdin就发生变化，select就可以感知
    # channel的发送命令、获取结果过程其实就是一个socket的发送和接受信息的过程
    while True:
        readlist, writelist, errlist = select.select([channel, sys.stdin,], [], [])
        # 如果是用户输入命令了,sys.stdin发生变化
        if sys.stdin in readlist:
            # 获取输入的内容
            input_cmd = sys.stdin.read(1)
            # 将命令发送给服务器
            channel.sendall(input_cmd)

        # 服务器返回了结果,channel通道接受到结果,发生变化 select感知到
        if channel in readlist:
            # 获取结果
            result = channel.recv(1024)
            # 断开连接后退出
            if len(result) == 0:
                print("\r\n**** EOF **** \r\n")
                break
            # 输出到屏幕
            sys.stdout.write(result.decode())
            sys.stdout.flush()

    # 关闭通道
    channel.close()
    # 关闭链接
    trans.close()

#支持tab自动补全
def test05():
    import paramiko
    import os
    import select
    import sys
    import tty
    import termios

    '''
    实现一个xshell登录系统的效果，登录到系统就不断输入命令同时返回结果
    支持自动补全，直接调用服务器终端

    '''
    # 建立一个socket
    trans = paramiko.Transport(('192.168.2.129', 22))
    # 启动一个客户端
    trans.start_client()

    # 如果使用rsa密钥登录的话
    '''
    default_key_file = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
    prikey = paramiko.RSAKey.from_private_key_file(default_key_file)
    trans.auth_publickey(username='super', key=prikey)
    '''
    # 如果使用用户名和密码登录
    trans.auth_password(username='super', password='super')
    # 打开一个通道
    channel = trans.open_session()
    # 获取终端
    channel.get_pty()
    # 激活终端，这样就可以登录到终端了，就和我们用类似于xshell登录系统一样
    channel.invoke_shell()

    # 获取原操作终端属性
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        # 将现在的操作终端属性设置为服务器上的原生终端属性,可以支持tab了
        tty.setraw(sys.stdin)
        channel.settimeout(0)

        while True:
            readlist, writelist, errlist = select.select([channel, sys.stdin,], [], [])
            # 如果是用户输入命令了,sys.stdin发生变化
            if sys.stdin in readlist:
                # 获取输入的内容，输入一个字符发送1个字符
                input_cmd = sys.stdin.read(1)
                # 将命令发送给服务器
                channel.sendall(input_cmd)

            # 服务器返回了结果,channel通道接受到结果,发生变化 select感知到
            if channel in readlist:
                # 获取结果
                result = channel.recv(1024)
                # 断开连接后退出
                if len(result) == 0:
                    print("\r\n**** EOF **** \r\n")
                    break
                # 输出到屏幕
                sys.stdout.write(result.decode())
                sys.stdout.flush()
    finally:
        # 执行完后将现在的终端属性恢复为原操作终端属性
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

    # 关闭通道
    channel.close()
    # 关闭链接
    trans.close()

if __name__=='__main__':
    #test01()
    single_file()