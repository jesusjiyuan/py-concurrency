#!/usr/bin/python
#coding:utf-8
import dmPython
try:
    conn = dmPython.connect(user='MONITOR', password='MONITOR@123.net', server='101.227.55.53:15236',  port=51236)
    cursor  = conn.cursor()
    try:
        #清空表，初始化测试环境
        cursor.execute('delete from MONITOR.TEST')
    except (dmPython.Error, Exception) as err:
        print(err)

    try:
        #插入数据
        cursor.execute("insert into MONITOR.TEST(NAME) values('语文'), ('数学'), ('英语'), ('体育')")
        print('python: insert success!')
        #删除数据
        cursor.execute("delete from MONITOR.TEST where name='数学'")
        print('python: delete success!')

        #更新数据
        cursor.execute('update MONITOR.TEST set name = \'英语-新课标\' where name=\'英语\'')
        print('python: update success!')

        #查询数据
        cursor.execute("select name from MONITOR.TEST")
        res = cursor.fetchall()
        for tmp in res:
            for c1 in tmp:
                print(c1)

        print('python: select success!')
    except (dmPython.Error, Exception) as err:
        print(err)

    conn.close()
except (dmPython.Error, Exception) as err:
    print(err)
