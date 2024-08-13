
# 导入pandas 和 pymysql 包
import pandas as pd
import pymysql

import dbutil

# 返回一个 Connection 对象
db_conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='mysql.',
    database='robot',
    charset='utf8'
)

def test_import_sql():
    mysql = dbutil.MYSQL(db='robot',user='root',pwd='mysql.')
    df = pd.read_excel('D:\\tmp\\消息内容.xlsx')
    df.rename(columns={"ID":"id","日期":"date","内容":"text","类型":"type","群ID":"room_id","群名":"room_topic","发言人ID":"talker_id","发言人名":"talker_name"}, inplace=True)
    df["id"]=df["id"].astype(str)
    df["room_id"].astype(str)
    #将data写入数据库，如果表存在就替换，将data的index也写入数据表，写入字段名称为id_name
    #df.to_sql('messages',con=dbutil.engine_mysql(),schema='robot',chunksize=10000,index=False,if_exists='replace')
    # orient='records', 表示将DataFrame的数据转换成我想要的json格式
    data_json = df.to_dict(orient='records')

    for dt in data_json:
        print(dt)
        mysql.insert_mysql('messages',dt)


def test_1():
    # 执行sql操作
    sql="select * from messages " \
        "WHERE room_id = '35048193823@chatroom' " \
        "and date BETWEEN DATE_SUB(DATE_FORMAT(sysdate(),'%Y-%m-%d'),INTERVAL 7 DAY) and DATE_FORMAT(sysdate(),'%Y-%m-%d') " \
        "order by date desc"
    df = pd.read_sql(sql,con=db_conn)
    df.rename(columns={"id": "ID","date":"日期","text":"内容","type":"类型","room_id":"群ID","room_topic":"群名","talker_id":"发言人ID","talker_name":"发言人名"}, inplace=True)
    print(df.iloc[:,1:])
    df = df.iloc[:,1:]
    df.to_excel('物业系统群本周问题.xlsx',index=False)

def test_2():
    # 执行sql操作
    sql = "select * from messages where id = %s"
    df = pd.read_sql(sql,con=db_conn,params=[2])
    print(df.values)

def test_3():
    # 执行sql操作
    sql = "select * from messages"
    df = pd.read_sql(sql,con=db_conn,index_col="type")
    print(df.values)