# coding:utf-8
import paramiko
import datetime
import os

hostname='47.103.118.47'
username='webs'
password='u7power@webs'
port=22

class SSHConnection():
	def __init__(self, host_dict):
		print(host_dict['host'])
		self.host = host_dict['host']
		self.port = host_dict['port']
		self.username = host_dict['username']
		self.pwd = host_dict['pwd']
		self.__transport = None
        self._sftp = None
        self._ssh = None
        self._connect()  # 建立连接
		self.__k = None

	def _connect(self):
		transport = paramiko.Transport((self.host,self.port))
		transport.connect(username=self.username,password=self.pwd)
		self.__transport = transport

	def close(self):
		self.__transport.close()

	def run_cmd(self, command):
		"""
		 执行shell命令,返回字典
		 return {'color': 'red','res':error}或
		 return {'color': 'green', 'res':res}
		:param command:
		:return:
		"""
		if self._ssh is None:
			self._ssh = paramiko.SSHClient()
			self._ssh._transport = self.__transport
		# 执行命令
		stdin, stdout, stderr = self._ssh.exec_command(command)
		if isinstance(stdout, bytes):
			value = bytes_or_str.decode('utf-8')
		else:
			print('step 1')
			value = stdout
			print(value)
			print(stdin)
			print(stderr)
		#print(stdout.decode('utf-8'))
		# 获取命令结果
		#res = self.to_str(stdout.read())
		# 获取错误信息
		error = "123"   #self.to_str(stderr.read())
		# 如果有错误信息，返回error
		# 否则返回res
		if error.strip():
			return {'color':'red','res':error}
		else:
			return {'color': 'green', 'res':res}
	def upload(self,local_path, target_path):
		if self._sftp is None:
			# 连接，上传
			self._sftp = paramiko.SFTPClient.from_transport(self.__transport)
		# 将location.py 上传至服务器 /tmp/test.py
		self._sftp.put(local_path, target_path, confirm=True)
		print(os.stat(local_path).st_mode)
		# 增加权限
		# sftp.chmod(target_path, os.stat(local_path).st_mode)
		#sftp.chmod(target_path, 0o755)  # 注意这里的权限是八进制的，八进制需要使用0o作为前缀	
	def download(self,target_path, local_path):
		if self._sftp is None:
			# 连接，下载
			self._sftp = paramiko.SFTPClient.from_transport(self.__transport)
		# 将location.py 下载至服务器 /tmp/test.py
		self._sftp.get(target_path, local_path)
	# 销毁
	def __del__(self):
		self.close()

#unicode_utils.py
def to_str(bytes_or_str):
	"""
	把byte类型转换为str
	:param bytes_or_str:
	:return:
	"""
	if isinstance(bytes_or_str, bytes):
		value = bytes_or_str.decode('utf-8')
	else:
		value = bytes_or_str
	return value


def login():
	transport = paramiko.Transport((hostname, port))
	transport.connect(username=username, password=password)
	sftp=paramiko.SFTPClient.from_transport(transport)
	return sftp,transport


def upload(local_dir,remote_dir):
	try:
		sftp,transport=login()	
		print('upload file start %s ' %datetime.datetime.now())
		for root,dirs,files in os.walk(local_dir):
			print('[%s][%s][%s]' % (root,dirs,files))
			for filespath in files:
				local_file=os.path.join(root,filespath)
				print(11,'[%s][%s][%s][%s]' % (root,filespath,local_file,local_dir))
				a = local_file.replace(local_dir,'').replace('\\','/').lstrip('/')
				print('01',a,'[%s]' % remote_dir)
				remote_file = os.path.join(remote_dir,a)
				print(22,remote_file)
				try:
					sftp.put(local_file,remote_file)
				except Exception as e:
					sftp.mkdir(os.path.split(remote_file)[0])
					sftp.put(local_file,remote_file)
					print("66 upload %s to remote %s " % (local_file,remote_file))
			for name in dirs:
				local_path = os.path.join(root,name)
				print(0,local_path,local_dir)
				a = local_path.replace(local_dir,'').replace('\\','')
				print(1,remote_dir,a)
				remote_path = os.path.join(remote_dir,a)
				try:
					sftp.mkdir(remote_path)
					print(44,"mkdir path %s " % remote_path)
				except Exception as e:
					print(55,e)
		print('77,upload file success %s ' % datetime.datetime.now())
		transport.close()				
	except Exception as e:
		print(88,e)

def download(remote_path,local_path):
	sftp,transport=login()
	sftp.get(remote_path,local_path)
	transport.close()


    
def ssh_upload(host_dict,uploadfile,remote_dir):
	print(host_dict['host'])
	ssh = SSHConnection(host_dict)
	ssh.connect()
	ssh.upload(uploadfile,remote_dir)
	ssh.close()
def tmp():
	host_conf={
		"host":'47.103.118.47',
		"username":'webs',
		"pwd":'u7power@webs',
		"port":22
	}
	ssh_upload(host_conf,r"C:\Users\Thinkpad\Downloads\dist\dist.zip",remote_dir)



if	__name__ == '__main__':
	local_dir=r"D:\\tmp\\download"
	remote_dir='/home/webs/'
	#upload(local_dir,remote_dir)
	#download(remote_dir+'123.txt',r"D:\tmp\download\a\123.txt")
	tmp()

#f __name__ == "__main__":
#    conn = SSHConnection('ip', port, 'username', 'password')
 
#    conn.exec_command('ls -ll')
#    conn.exec_command('cd /home/test;pwd')  #cd需要特别处理
#    conn.exec_command('pwd')
#    conn.exec_command('tree /home/test')



