import sys
import threading
import pymysql
import DBUtils.PooledDB

connargs = { "host":"localhost", "user":"user1", "passwd":"123456", "db":"test" }
def test(conn):
    try:
        cursor = conn.cursor()
        count = cursor.execute("select * from users")
        rows = cursor.fetchall()
        for r in rows: pass
    finally:
        conn.close()

def testloop():
    print ("testloop")
    for i in range(1000):
        conn = pymysql.connect(**connargs)
        test(conn)

def testpool():
    print ("testpool")
    pooled = DBUtils.PooledDB.PooledDB(pymysql, **connargs)
    for i in range(1000):
        conn = pooled.connection()
        test(conn)

def main():
    t = testloop if len(sys.argv) == 1 else testpool
    for i in range(10):
        threading.Thread(target = t).start()

if __name__ == "__main__":
    main()
