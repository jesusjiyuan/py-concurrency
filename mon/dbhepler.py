# coding: utf-8
import dmPython
def connect() -> object:
    conn = dmPython.connect(user='CC_MZH', password='CC_MZH@topwin123.net', server='101.227.55.53:15236',  port=51236)
    return conn
def close(conn):
    conn.close()


import dmPython


class MyDM:

    SHOW_SQL = True

    def __init__(self, host='101.227.55.53', port=15236, user='CC_MZH', password='CC_MZH@topwin123.net'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def get_con(self):
        try:
            conn = dmPython.connect(user=self.user, password=self.password, server=self.host, port=self.port, autoCommit=True)
            return conn
        except dmPython.Error as e:
            print("dmPython Error:%s" % e)


    def select_all(self, sql):
        try:
            con = self.get_con()
            # print(con)
            cur = con.cursor()
            cur.execute(sql)
            fc = cur.fetchall()
            return fc
        except dmPython.Error as e:
            print("dmPython Error:%s" % e)
        finally:
            cur.close()
            con.close()

    def select_by_where(self, sql, data):
        try:
            con = self.get_con()
            # # print(con)
            d = (data,)
            cur = con.cursor()
            cur.execute(sql, d)
            fc = cur.fetchall()
            # if len(fc) > 0:
            #     for e in range(len(fc)):
            #         print(fc[e])
            return fc
        except dmPython.Error as e:
            print("dmPython Error:%s" % e)
        finally:
            cur.close()
            con.close()

    def dml_by_where(self, sql, params):
        try:
            con = self.get_con()
            cur = con.cursor()

            for d in params:
                if self.SHOW_SQL:
                    print('执行sql:[{}],参数:[{}]'.format(sql, d))
                cur.execute(sql, d)
            con.commit()

        except dmPython.Error as e:
            con.rollback()
            print("dmPython Error:%s" % e)
        finally:
            cur.close()
            con.close()

    # 不带参数的更新方法
    def dml_nowhere(self, sql):
        try:
            con = self.get_con()
            cur = con.cursor()
            count = cur.execute(sql)
            con.commit()
            return count
        except dmPython.Error as e:
            con.rollback()
            print("dmPython Error:%s" % e)
        finally:
            cur.close()
            con.close()

# 开始测试函数

def select_all():
    sql = "select * from  TEST"
    fc = db.select_all(sql)
    for row in fc:
        print(row)


def select_by_where():
    sql = "select * from  TEST where USER_ID= :1"
    data = '0551'
    fc = db.select_by_where(sql, data)

    for row in fc:
        print(row)


def ins_by_param():
    sql = "insert into  TEST(USERNAME,USER_ID) values(:1,:2)"
    data = [('https://www.cndba.cn', '0551'), ('https://www.cndba.cn/ TEST', '0556')]
    db.dml_by_where(sql, data)


def del_by_where():
    sql = "delete from  TEST where USERNAME = :1 or USER_ID=:2"
    data = [('huaining', '0556')]
    db.dml_by_where(sql, data)


def update_by_where():
    sql = "update  TEST set USER_ID=:1 where USER_ID=:2"
    data = [('0556', '0551')]
    db.dml_by_where(sql, data)


def del_nowhere():
    sql = "delete from  TEST"
    print(db.dml_nowhere(sql))


if __name__ == "__main__":
    #db = MyDM( '192.168.20.171', port=5236, user='SYSDBA', password='SYSDBA'))
    db = MyDM()

    #ins_by_param()
    select_by_where()
    #del_by_where()
    #select_all()
    #update_by_where()
    #del_nowhere()
    #select_all()