# coding: utf-8
from sqlalchemy import Column, Integer, String, Date, Numeric, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

'''
CREATE TABLE "SYSDBA"."PRODUCT"
(
"PRODUCTID" INTEGER IDENTITY(1, 1) NOT NULL,
"NAME" VARCHAR(100) NOT NULL,
"AUTHOR" VARCHAR(25) NOT NULL,
"PUBLISHER" VARCHAR(50) NOT NULL,
"PUBLISHTIME" DATETIME NOT NULL,
"PRODUCTNO" VARCHAR(25) NOT NULL,
"SATETYSTOCKLEVEL" SMALLINT NOT NULL,
"ORIGINALPRICE" DEC(19,4) NOT NULL,
"NOWPRICE" DEC(19,4) NOT NULL,
"DISCOUNT" DECIMAL(2,1) NOT NULL,
"DESCRIPTION" TEXT,
"TYPE" VARCHAR(5),
"PAPERTOTAL" INTEGER,
"WORDTOTAL" INTEGER,
"SELLSTARTTIME" DATETIME NOT NULL,
"SELLENDTIME" DATETIME,
NOT CLUSTER PRIMARY KEY("PRODUCTID"),
UNIQUE("PRODUCTNO")) STORAGE(ON "MAIN", CLUSTERBTR);

'''

# 创建对象的基类:
Base = declarative_base()

class Product(Base):
    # 表的名字:
    __tablename__ = 'product'
    # 表的结构:
    PRODUCTID = Column(Integer,primary_key=True,autoincrement=True)
    NAME = Column(String(100))
    AUTHOR = Column(String(25))
    PUBLISHER = Column(String(50))
    PUBLISHTIME = Column(DateTime)
    PRODUCTNO = Column(String(25))
    SATETYSTOCKLEVEL = Column(Integer)
    ORIGINALPRICE = Column(Numeric(19,4))
    NOWPRICE = Column(Numeric(19,4))
    DISCOUNT = Column(Numeric(2,1))
    DESCRIPTION = Column(Text)
    TYPE = Column(String(5))
    PAPERTOTAL = Column(Integer)
    WORDTOTAL = Column(Integer)
    SELLSTARTTIME = Column(DateTime)
    SELLENDTIME = Column(DateTime)