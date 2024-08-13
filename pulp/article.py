# coding:utf-8
from sqlalchemy import Column,String,INT,DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()   #创建对象的基类
 
class article(Base):    #定义一个类，继承Base
    __tablename__='z_tmp_article'
    ID = Column(INT(),primary_key=True)
    ArticleNo = Column(String(50))
    ProductType = Column(String(50))
    RP = Column(DECIMAL(6))
    MaxQty =  Column(INT(), default=0)
    MinQty =  Column(INT(), default=0)
    def __init__(self,articleNo,productType,rp,maxQty,minQty):
        self.ArticleNo=articleNo
        self.ProductType=productType
        self.RP=rp
        self.MaxQty=maxQty
        self.MinQty=minQty