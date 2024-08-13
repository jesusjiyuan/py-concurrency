# coding:utf-8
from sqlalchemy import Column,String,INT,DECIMAL
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()   #创建对象的基类
 
class cluster(Base):    #定义一个类，继承Base
    __tablename__='z_tmp_Cluster'
    ID = Column(INT(),primary_key=True)
    Channel = Column(String(50))
    Account = Column(String(50))
    Cluster = Column(String(50))
    OTB =  Column(DECIMAL())
    def __init__(self,channel,account,cluster,otb):
        self.Channel=channel
        self.Account=account
        self.Cluster=cluster
        self.OTB=otb