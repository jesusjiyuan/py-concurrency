# coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
# Data Source=topwindevdb.database.chinacloudapi.cn;initial catalog=adOMBDev;user id=topwin;password=63362266.net;
class DatabaseManagement():
    def __init__(self):
        #self.engine = create_engine('mssql+pymssql://topwin:63362266.net@topwindevdb.database.chinacloudapi.cn/adOMBDev',echo=True)    #初始化数据库连接
        self.engine = create_engine('mssql+pymssql://topwin:TP#345.top.net@topwindevdb.database.chinacloudapi.cn/adOMBDev',pool_recycle=7200,echo=True)    #初始化数据库连接
        DBsession = sessionmaker(bind=self.engine)    #创建DBsession类
        self.session = DBsession()    #创建对象
 
    def add_obj(self,obj):    #添加内容
        self.session.add(obj)
        self.session.commit()    #提交
        return obj
 
    def query_list(self,target_class,query_filter):    #查询内容
        result_list = self.session.query(target_class).filter(query_filter).all()
        return result_list

    def query_all(self,target_class):    #查询内容
        result_list = self.session.query(target_class).all()
        return result_list
 
    def update_by_filter(self, obj, update_hash,query_filter):     #更新内容
        self.session.query(obj.__class__).filter(query_filter).update(update_hash)
        self.session.commit()
 
    def delete_by_filter(self, obj, query_filter):     #删除内容
        self.session.query(obj).filter(query_filter).delete()
 
    def close(self):    #关闭session
        self.session.close()

    def commit(self):    #关闭commit
        self.session.commit()
 
    def execute_sql(self, sql_str):    #执行sql语句
        return self.session.execute(sql_str)