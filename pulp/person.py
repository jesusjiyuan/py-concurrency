# coding:utf-8
from sqlalchemy import Column,String,INT
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()   #创建对象的基类
 
class Person(Base):    #定义一个类，继承Base
    __tablename__='Person'
    ID = Column(INT(),primary_key=True)
    Name = Column(String(50))
    Age = Column(INT())
 
    def __init__(self,name,age):
        self.Name=name
        self.Age=age