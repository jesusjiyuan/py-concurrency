# coding:utf-8
from sqlalchemy import Column,String,INT,DECIMAL
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()   #创建对象的基类
 
class articleclusterref(Base):    #定义一个类，继承Base
    __tablename__='z_tmp_assortment'
    ID = Column(INT(),primary_key=True)
    Article = Column(String(50))
    ArticleID = Column(String(50))
    ClusterID = Column(INT())
    ROS = Column(DECIMAL())
    MinQty =  Column(INT())
    Qty =  Column(INT())
    SourceQty =  Column(INT())
    MaxQty =  Column(INT())
