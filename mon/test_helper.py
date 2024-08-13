# coding: utf-8
import os
import time
import uuid
from urllib import parse

import pytest

import dmPython
import dbhepler

from datetime import datetime

import dbmapper
from entity import LinkMonResult, MonTask, MonKeyword, MonVideoResultExt

def test_create_conn_str():
    passwd = parse.quote_plus("CC_MZH@topwin123.net")
    #dialect 是SQLAlchemy用来与各种类型的DBAPI和数据库通信的系统。
    #conn_url = 'dm+dmPython://SYSDBA: SYSDBA123@192.168.201.118:5236'
    conn_url = 'dm+dmPython://CC_MZH:{passwd}@101.227.55.53:15236'.format(passwd=passwd)
    print(conn_url)

def test_mk_domain():

    passwd = parse.quote_plus("CC_MZH@topwin123.net")
    conn_url = 'dm+dmPython://CC_MZH:{passwd}@101.227.55.53:15236'.format(passwd=passwd)
    os.system("sqlacodegen --outfile models.py {}".format(conn_url))
    #os.system("flask-sqlacodegen --flask --outfile models.py {}".format(conn_url))
    print(conn_url)
def test_conn():
    conn = dbhepler.connect()
    cursor  = conn.cursor()
    try:
        cursor.execute("select * from CC_MZH.TEST")
        res = cursor.fetchall()
        for tmp in res:
            for c1 in tmp:
                print(c1)
    except (dmPython.Error, Exception) as err:
        print(err)
    dbhepler.close(conn)

def test_time():
    print(str(datetime.now()))
    print(str(time.time()))
    print(str(time.time_ns()))
    print(time.strftime('%Y%m%d%H%M%S',time.localtime()))
    #print(time.strftime('%Y%m%d%H%M%S%f',time.localtime()))
    print(datetime.now().strftime("%Y%m%d%H%M%S%f"))



def test_uuid():
    print(str(uuid.uuid4().int))

def test_format():
    print("values ('{}','{}','{}')".format(1,2,3))

def test_monlinkresult_select():
    res = dbmapper.LinkMonResultMapper.list(LinkMonResult(id='101247059043041103773388847304454036250',status=1))
    for r in res:
        print(r.id,r.pUrl,r.url,r.picPath)
def test_montask_list():
    start = time.time()
    lists = dbmapper.MonTaskMapper.list(MonTask())
    #l = r.kwIds.split(",")
    for r in lists:
        print(r.id,r.name,r.batchNo,r.targetIds,r.kwIds,r.typea)
        print(type(r),r)
    print("cost time: ",time.time()-start)
def test_montask_by_batchno():
    r = dbmapper.MonTaskMapper.get_by_batchno("20231121135814")
    print(r.id,r.name,r.batchNo,r.targetIds,r.kwIds,r.typea)
    l = r.kwIds.split(",")
    print(type(l),l)

def test_monlink_list_by_ids():
    l = "1000,1001,1002,1003".split(",")
    res = dbmapper.MonLinkMapper.list_by_ids(l,'jd')
    for r in res:
        print(r.id,r.name,r.url,r.typea)

def test_monlinkresult_list():
    #res = dbmapper.LinkMonResultMapper.list(LinkMonResult(batchNo="20231122103113"))
    res = dbmapper.LinkMonResultMapper.list(LinkMonResult())
    for r in res:
        print(r.id,r.pUrl,r.url,r.picPath)
def test_monlinkresult_count():
    count = dbmapper.LinkMonResultMapper.count(LinkMonResult(pUrl="https://mall.jd.com/index-11388268.html?from=pc",batchNo="20231123093839"))
    print(count)
def test_monlinkresult_update():
    dbmapper.LinkMonResultMapper.update(LinkMonResult(status="0",updateTime=time.localtime(),pUrl="https://mall.jd.com/index-11388268.html?from=pc",batchNo="20231123093839"))
def test_monkeyword_list():
    res = dbmapper.MonKeywordMapper.list(MonKeyword(id="1001"))
    #res = dbmapper.MonKeywordMapper.list()
    for r in res:
        print(r.id,r.name)
def test_monvedioresult_list():
    res = dbmapper.MonVideoResultMapper.list()
    for r in res:
        print(r.id)
def test_monvedioresult_list_by_ids():
    ids = "b3a1f654a4c4885a69beea47f07a98f2".split(",")
    #ids = ["'"+str(id)+"'" for id in ids]
    res = dbmapper.MonVideoResultMapper.list_by_ids(ids)
    for r in res:
        print(r.id,r.name)

def test_monvedioresultext_list():
    res = dbmapper.MonVideoResultExtMapper.count(MonVideoResultExt(vId='b3a1f654a4c4885a69beea47f07a98f2',start='46.42',end="48.76"))
    print(res)

def test_montask_updatestatus():
    dbmapper.MonTaskMapper.updateStatus(MonTask(batchNo="20231124173656",status="1",endTime=time.localtime()))