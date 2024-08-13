# coding:utf-8
from datetime import datetime

from sqlalchemy import Column, String, INT, DECIMAL, Time, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()   #创建对象的基类

class result(Base):    #定义一个类，继承Base
    __tablename__='z_tmp_result'
    id = Column(INT(),primary_key=True)
    articleId = Column(String(50))
    clusterId = Column(INT())
    pty = Column(String(50))
    updateTime = Column(DateTime,onupdate=datetime.now, default=datetime.now)
    def __init__(self,articleId,clusterId,pty,updateTime):
        self.articleId=articleId
        self.clusterId=clusterId
        self.pty=pty
        self.updateTime=updateTime
