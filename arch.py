#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, getopt
import zipfile
import os
import paramiko
import datetime

remote_dir=""

class SSHConnection():
	def __init__(self, host_dict):
		print(host_dict['host'])
		self.host = host_dict['host']
		self.port = host_dict['port']
		self.username = host_dict['username']
		self.pwd = host_dict['pwd']
		self.__k = None

	def connect(self):
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
		ssh = paramiko.SSHClient()
		ssh._transport = self.__transport
		# 执行命令
		stdin, stdout, stderr = ssh.exec_command(command)
		# 获取命令结果
		res = to_str(stdout.read())
		# 获取错误信息
		error = to_str(stderr.read())
		# 如果有错误信息，返回error
		# 否则返回res
		if error.strip():
			return {'color':'red','res':error}
		else:
			return {'color': 'green', 'res':res}
	def upload(self,local_path, target_path):
		# 连接，上传
		sftp = paramiko.SFTPClient.from_transport(self.__transport)
		# 将location.py 上传至服务器 /tmp/test.py
		sftp.put(local_path, target_path, confirm=True)
		# print(os.stat(local_path).st_mode)
		# 增加权限
		# sftp.chmod(target_path, os.stat(local_path).st_mode)
		#sftp.chmod(target_path, 0o755)  # 注意这里的权限是八进制的，八进制需要使用0o作为前缀	
	def download(self,target_path, local_path):
		# 连接，下载
		sftp = paramiko.SFTPClient.from_transport(self.__transport)
		# 将location.py 下载至服务器 /tmp/test.py
		sftp.get(target_path, local_path)
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


def main(argv):

   inputfile = ''
   outputfile = ''
   host=''
   username=''
   pwd=''
   remote_dir=''
   try:
      opts, args = getopt.getopt(argv,"i:o:h:u:p:r:",["help","ifile=","ofile=","host=","username=","pwd=","remote_dir="])
      #print(opts)  
   except getopt.GetoptError:
      print("arch.py -i <inputfile> -o <outputfile>")
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         host = arg 
         #print("test.py -i <inputfile> -o <outputfile> -h <> -u <> -p <> -r" )
         #sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      #elif opt in ("-h", "--host"):
      #   host = arg   
      elif opt in ("-u", "--username"):
         username = arg   
      elif opt in ("-p", "--pwd"):
         pwd = arg   
      elif opt in ("-r", "--remote_dir"):
         remote_dir = arg   
   print('输入的文件为：', inputfile)
   print('输出的文件为：', outputfile)
   print('输出的文件为：', host)
   print('输出的文件为：', username)
   print('输出的文件为：', pwd)
   print('输出的文件为：', remote_dir)
   host_dict = {
      "host":host,
      "port":22,
      "username":username,
      "pwd":pwd
   }
   print(host_dict)
   return outputfile,host_dict,remote_dir
   

#i E:\project\jiyuan\framework\svn\branches\test\hzwelfare\hz-web\dist
#o E:\project\jiyuan\framework\svn\branches\test\hzwelfare\hz-web
#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
  zipf = zipfile.ZipFile(output_filename, 'w')
  pre_len = len(os.path.dirname(source_dir))
  for parent, dirnames, filenames in os.walk(source_dir):
    for filename in filenames:
      pathfile = os.path.join(parent, filename)
      arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
      zipf.write(pathfile, arcname)
  zipf.close()

    
def upload(host_dict,uploadfile,remote_dir):
   ssh = SSHConnection(host_dict)
   ssh.connect()
   ssh.upload(uploadfile,remote_dir)
   ssh.close()

if __name__ == "__main__":
   uploadfile ,hdict,remote_dir= main(sys.argv[1:])
   #inputfile="E:\\home\\ruoyi"
   #outputfile="E:\\home\\ruoui.zip"
   make_zip(inputfile,outputfile)
   upload(hdict,uploadfile,remote_dir)