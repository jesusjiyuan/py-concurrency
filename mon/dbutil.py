# coding: utf-8
from urllib import parse

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def connect():
    passwd = parse.quote_plus("CC_MZH@topwin123.net")
    #dialect 是SQLAlchemy用来与各种类型的DBAPI和数据库通信的系统。
    #conn_url = 'dm+dmPython://SYSDBA: SYSDBA123@192.168.201.118:5236'
    conn_url = 'dm+dmPython://CC_MZH:{passwd}@101.227.55.53:15236'.format(passwd=passwd)
    #创建Engine对象
    engine = create_engine(conn_url)
    #创建DBSession对象
    DBSession = sessionmaker(bind=engine)
    return DBSession()

def connect_vc():
    passwd = parse.quote_plus("MONITOR@123.net")
    #dialect 是SQLAlchemy用来与各种类型的DBAPI和数据库通信的系统。
    #conn_url = 'dm+dmPython://SYSDBA: SYSDBA123@192.168.201.118:5236'
    conn_url = 'dm+dmPython://MONITOR:{passwd}@101.227.55.53:15236'.format(passwd=passwd)
    #创建Engine对象
    engine = create_engine(conn_url)
    #创建DBSession对象
    DBSession = sessionmaker(bind=engine)
    return DBSession()

def connect_mysql():
    passwd = parse.quote_plus("mysql.")
    #dialect 是SQLAlchemy用来与各种类型的DBAPI和数据库通信的系统。
    #conn_url = 'dm+dmPython://SYSDBA: SYSDBA123@192.168.201.118:5236'
    conn_url = engine = create_engine('mysql+pymysql://root:{passwd}@localhost:robot/test?charset=utf8'.format(passwd=passwd))
    #创建Engine对象
    engine = create_engine(conn_url)
    #创建DBSession对象
    DBSession = sessionmaker(bind=engine)
    return DBSession()
def engine_mysql():
    passwd = parse.quote_plus("mysql.")
    #dialect 是SQLAlchemy用来与各种类型的DBAPI和数据库通信的系统。
    #conn_url = 'dm+dmPython://SYSDBA: SYSDBA123@192.168.201.118:5236'
    conn_url = engine = create_engine('mysql+pymysql://root:{passwd}@localhost:3306/robot?charset=utf8'.format(passwd=passwd))
    #创建Engine对象
    engine = create_engine(conn_url)
    #创建DBSession对象
    #DBSession = sessionmaker(bind=engine)
    return engine

class MYSQL:
    def __init__(self,host="localhost",db=None,port=3306,user=None,pwd=None):
        # MySQL
        self.MYSQL_HOST = host
        self.MYSQL_DB = db
        self.MYSQ_USER = user
        self.MYSQL_PWD = pwd
        self.connect = pymysql.connect(
            host=self.MYSQL_HOST,
            db=self.MYSQL_DB,
            port=port,
            user=self.MYSQ_USER,
            passwd=self.MYSQL_PWD,
            charset='utf8',
            use_unicode=False
        )
        print(self.connect)
        self.cursor = self.connect.cursor()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE car (文章ID int, 链接 VARCHAR(255), 标题 VARCHAR(255),
            发文机关 VARCHAR(255), 发文字号 VARCHAR(255), 来源 VARCHAR(255),
            主题分类 VARCHAR(255), 公文种类 VARCHAR(255), 文件内容 LONGBLOB )""")

    def insert_mysql(self, table,data_json):
        """
        数据插入mysql
        :param data_json:
        :return:
        """
        sql = "insert into {}(id,date,room_id,room_topic,talker_id,talker_name,text,type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)".format(table)
        try:
            self.cursor.execute(sql, (data_json['id'], data_json['date'], data_json['room_id'],data_json['room_topic'],
                                      data_json['talker_id'],data_json['talker_name'],data_json['text'],data_json['type']))
            self.connect.commit()
            print('数据插入成功')
        except Exception as e:
            print('e= ', e)
            print('数据插入错误')