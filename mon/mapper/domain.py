# coding: utf-8
from sqlalchemy import Column, Integer, String, Date, Numeric, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()


class MonLinkBatch(Base):
    # 表的名字:
    __tablename__ = 'mon_link_batch'
    # 表的结构:
    id = Column(Integer,primary_key=True)
    batchNo = Column(String(50))
    linkId = Column(String(50))
    linkUrl = Column(String(10))
    status = Column(String(10))
    createTime = Column(DateTime)
    endTime = Column(DateTime)
    delFlag = Column(String(10))
    goodSum = Column(Integer)
class MonLinkResult(Base):
    # 表的名字:
    __tablename__ = 'mon_link_result'
    # 表的结构:
    id = Column(String(50),primary_key=True)
    pUrl = Column(String(50))
    url = Column(String(50))
    picPath = Column(String(50))
    batchNo = Column(String(50))
    ocrStr = Column(Text)
    ocrRaw = Column(Text)
    status = Column(String(10))
    createTime = Column(DateTime)
    updateTime = Column(DateTime)
    matchPicPath = Column(String(50))
    delFlag = Column(String(10))
    kwords = Column(String(50))
    linkId = Column(String(50))

class MonVideoResult(Base):
    # 表的名字:
    __tablename__ = 'mon_video_result'
    # 表的结构:
    id = Column(String(50),primary_key=True)
    vedioUrl = Column(String(50))
    name = Column(String(50))
    status = Column(String(10))
    createTime = Column(DateTime)
    endTime = Column(DateTime)
    raw = Column(Text)
    delFlag = Column(String(10))
    vedioDuration = Column(Integer)

class MonVideoResultExt(Base):
    # 表的名字:
    __tablename__ = 'mon_video_result_ext'
    # 表的结构:
    id = Column(Integer,primary_key=True)
    vId = Column(String(50))
    starts = Column(String(50))
    ends = Column(String(10))
    vSlicePath = Column(String(50))
    kwords = Column(String(50))

class MonKeyword(Base):
    # 表的名字:
    __tablename__ = 'mon_keyword'
    # 表的结构:
    id = Column(Integer,primary_key=True)
    name = Column(String(50))

class MonLink(Base):
    # 表的名字:
    __tablename__ = 'mon_link'
    # 表的结构:
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    url = Column(String(50))
    typea = Column(String(10))
    delFlag = Column(String(10))
    createTime = Column(DateTime)
    updateTime = Column(DateTime)
    business = Column(String(10))

class MonTask(Base):
    # 表的名字:
    __tablename__ = 'mon_task'
    # 表的结构:
    id = Column(String(50),primary_key=True)
    name = Column(String(50))
    batchNo = Column(String(50))
    createTime = Column(DateTime)
    updateTime = Column(DateTime)
    delFlag = Column(String(10))
    targetIds = Column(String(50))
    kwIds = Column(String(50))
    typea = Column(String(10))
    endTime = Column(DateTime)
    status = Column(String(10))


class Tmp5000(Base):
    # 表的名字:
    __tablename__ = 'tmp_5000'
    # 表的结构:
    id = Column(Integer,primary_key=True)
    indexcode = Column(String(200))
    sharename = Column(String(200))