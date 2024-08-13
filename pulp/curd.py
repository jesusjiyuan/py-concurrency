# coding:utf-8
from sqlalchemy import create_engine
from db_mg import DatabaseManagement
from sqlalchemy import and_,text
from article import article
engine = create_engine('sqlite:///testdb.db')

def test_select_statement():
    with engine.connect() as conn:
        result_proxy = conn.execute("select * from employees")  # 返回值为ResultProxy类型
        result = result_proxy.fetchall()

        for item in result:
            print(item)
#带有参数的 SQL 语句
#SQLAlchemy 支持两种格式的 sql 语句：？和 :number。
def test_parameter_method1():
    with engine.connect() as conn:
        conn.execute(
            """INSERT INTO employees
                   (EMP_ID, FIRST_NAME, LAST_NAME, GENDER, 
                    AGE, EMAIL, PHONE_NR,EDUCATION, 
                    MARITAL_STAT, NR_OF_CHILDREN)
               VALUES (?,?,?,?,?,?,?,?,?,?);
            """,
            ('9002', 'Stone2', 'Wang', 'M', 20,
             'stone@gmail.com', '138xxx', 'Bachelor', 'Single', 0)
        )
def test_parameter_method2():
    with engine.connect() as conn:
        conn.execute(
            """INSERT INTO employees
                   (EMP_ID, FIRST_NAME, LAST_NAME, GENDER, 
                    AGE, EMAIL, PHONE_NR, EDUCATION, 
                    MARITAL_STAT, NR_OF_CHILDREN)
               VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10);
            """,
            ('9003', 'Stone3', 'Wang', 'M', 20, 'stone@gmail.com',
             '138xxx', 'Bachelor', 'Single', 0)
        )
#插入多行
#SQLAlchemy 支持一次插入多行，需要插入的数据放在 list 中：
def test_insert_multiple_rows(self):
    with engine.connect() as conn:
        values = [
            ('9004', 'Stone4', 'Wang', 'M', 20, 'stone@gmail.com', '138xxx', 'Bachelor', 'Single', 0),
            ('9005', 'Stone5', 'Wang', 'M', 20, 'stone@gmail.com', '138xxx', 'Bachelor', 'Single', 0),
            ('9006', 'Stone6', 'Wang', 'M', 20, 'stone@gmail.com', '138xxx', 'Bachelor', 'Single', 0)
        ]
        conn.execute(
            """INSERT INTO employees
                   (EMP_ID, FIRST_NAME, LAST_NAME, GENDER, 
                    AGE, EMAIL, PHONE_NR, EDUCATION, 
                    MARITAL_STAT, NR_OF_CHILDREN)
               VALUES (?,?,?,?,?,?,?,?,?,?);
            """, values)
#事务操作
#由于执行 sql 插入操作自动提交 (commit)，sqlalchemy 提供了 Transactions 来管理 commit 和 rollback，需要提交的时候用 commit() 方法，需要回滚的时候用 rollback() 方法。
def test_txn(self):
    conn = engine.connect()
    with conn.begin() as txn:
        conn.execute(
            """INSERT INTO employees
                   (EMP_ID, FIRST_NAME, LAST_NAME, GENDER, AGE, EMAIL, PHONE_NR,
                    EDUCATION, MARITAL_STAT, NR_OF_CHILDREN)
               VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10);
            """,
            ('9007', 'Stone7', 'Wang', 'M', 20, 'stone@gmail.com', '138xxx', 'Bachelor', 'Single', 0)
        )

        txn.commit()
    conn.close()


class MyTest():
    def __init__(self):
        self.db_obj = DatabaseManagement()

    def process(self):
        person_obj = Person("james",18)
        person_obj = self.db_obj.add_obj(person_obj)
        query_filter=and_(Person.Name=="james",Person.Age==18)
        person_list = self.db_obj.query_list(Person, query_filter)
        for i in person_list:
            print(i.Name)
