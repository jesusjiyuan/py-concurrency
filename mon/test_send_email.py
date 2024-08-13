import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def t_11():
    # 发件人邮箱地址
    sendAddress = '15021424696@163.com'
    # 发件人授权码
    password = 'FFHAXLVCJIDMIELZ'
    # 连接服务器
    server = smtplib.SMTP('smtp.163.com', 25)
    # 登录邮箱
    loginResult = server.login(sendAddress, password)
    print(loginResult)

import yagmail
import binascii
from pyDes import des, CBC, PAD_PKCS5
def des_decrypt(secret_key, s):
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de


def send_email(spide_name:str,content:str):
    to_list = ['jesusjiyuan@qq.com', ]
    to_cc =  ['kangzhihao@topwin.net']
    passwd = des_decrypt('X4&dwMDz', b'5ddee105d7e9e24f74cfd827ed8a7547e770b13a6d23f3ad1533e0c8586ff07f').decode('utf-8')
    # 连接服务器
    # 用户名、授权码、服务器地址
    #yag_server = yagmail.SMTP(user='15021424696@163.com', password='FFHAXLVCJIDMIELZ', host='smtp.163.com')
    yag_server = yagmail.SMTP(user='kangzhihao@topwin.net', password=passwd, host='smtp.exmail.qq.com')
    #接着，通过 send() 函数，将邮件发送出去
    # 发送对象列表
    email_to = to_cc
    email_cc = to_list
    email_title = spide_name
    email_content = content
    # 附件列表
    email_attachments = ['D:\\labs\\import用户数据.xlsx', ]
    # 发送邮件
    yag_server.send(email_to, email_title, email_content,email_attachments,cc=email_cc)
    #邮件发送完毕之后，关闭连接即可
    # 关闭连接
    yag_server.close()


send_email("测试","测试测试")