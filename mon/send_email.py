# --coding--:utf-8
import pandas as pd
import pymysql
import yagmail
import binascii
from pyDes import des, CBC, PAD_PKCS5

data_flag = False
file_name = '物业系统群本周问题.xlsx'
def des_decrypt(secret_key, s):
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de

def select_message():
    # 返回一个 Connection 对象
    #dev
    #passwd = des_decrypt('X4&dwMDz', b'6ce1ab20f162f4ca').decode('utf-8')
    passwd = des_decrypt('X4&dwMDz', b'0a6b882c736f834f3ac73e0757f23dce').decode('utf-8')
    db_conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password=passwd,
        database='robot',
        charset='utf8'
    )
    # 执行sql操作
    sql="select * from messages " \
        "WHERE room_id = '35048193823@chatroom' and text like '%@topwin%'" \
        "and date BETWEEN DATE_SUB(DATE_FORMAT(sysdate(),'%Y-%m-%d'),INTERVAL 3 DAY) and DATE_FORMAT(sysdate(),'%Y-%m-%d') " \
        "order by date desc"
    df = pd.read_sql(sql,con=db_conn)
    if len(df.values) >0:
        global data_flag
        data_flag = True

        df.rename(columns={"id": "ID","date":"日期","text":"内容","type":"类型","room_id":"群ID","room_topic":"群名","talker_id":"发言人ID","talker_name":"发言人名"}, inplace=True)
        print(df.iloc[:,1:])
        df = df.iloc[:,1:]
        df.to_excel(file_name,index=False)

def send_email(spide_name:str,content:str):
    to_list = ['kangzhihao@topwin.net']
    to_cc =  []
    passwd = des_decrypt('X4&dwMDz', b'5ddee105d7e9e24f74cfd827ed8a7547e770b13a6d23f3ad1533e0c8586ff07f').decode('utf-8')
    # 连接服务器
    # 用户名、授权码、服务器地址
    yag = yagmail.SMTP(user=to_list[0], password=passwd, host='smtp.exmail.qq.com')
    #接着，通过 send() 函数，将邮件发送出去
    # 发送对象列表
    email_to = to_cc
    email_cc = to_list
    email_title = spide_name
    email_content = content
    # 附件列表
    email_attachments = [file_name ]
    # 发送邮件
    yag.send(email_to, email_title, email_content,email_attachments,cc=email_cc)
    #邮件发送完毕之后，关闭连接即可
    # 关闭连接
    yag.close()

select_message()
if data_flag:
    contont = '''
    您好，
    
    本周物业系统群提出的问题已经整理成文件，详情请查看附件
    
    谢谢！
    -----------------------------------------------------------------------
    zhihao Kang
    上海同威数码科技有限公司 Shanghai Top-Win Digital Technology Co., Ltd
    上海市虹口区溧阳路735号（半岛湾创意产业园）3幢3201室
    电子邮件：kangzhiao@topwin.net
    电话: 021-63362266*808
    专业服务，全面提升企业IT效能
    Professional service boosts enterprise IT performance
    -----------------------------------------------------------------------
    
    '''
    send_email("物业系统群本周问题",contont)