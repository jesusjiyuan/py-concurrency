# coding: utf-8
import json
import os
import time
import uuid
from urllib import parse

import dbutil
from mapper.domain import MonLinkResult, MonVideoResult, MonTask, MonVideoResultExt, MonLink, MonKeyword, MonLinkBatch


def test_select_monlinkbatch():
    session = dbutil.connect()
    # 查询所有的
    lists = session.query(MonLinkBatch).filter(MonLinkBatch.status=="1").all()
    print('查询所有结果：')
    for l in lists:
        print(l )
    print('')
    session.close()
def test_select_monlinkresult():
    session = dbutil.connect()
    # 查询所有的
    lists = session.query(MonLinkResult).filter(MonLinkResult.status=="1").all()
    print('查询所有结果：')
    for l in lists:
        print(l )
    print('')
    session.close()
def test_select_monvideoresult():
    session = dbutil.connect()
    # 查询所有的
    lists = session.query(MonVideoResult).filter(MonVideoResult.status=="1").all()
    print('查询所有结果：')
    for l in lists:
        print(l )
    print('')
    session.close()

def test_select_monvideoresultext():
    session = dbutil.connect()
    # 查询所有的
    lists = session.query(MonVideoResultExt).filter(MonVideoResultExt.id=="10000").all()
    print('查询所有结果：')
    for l in lists:
        print(l.id)
    print('')
    session.close()

def test_select_montask():
    start = time.time()
    session = dbutil.connect()
    # 查询所有的
    #lists = session.query(MonTask).filter(MonTask.status=="1").all()
    lists = session.query(MonTask).all()
    print('查询所有结果：')
    for l in lists:
        print(l )
    print('')
    session.close()
    print("cost time: ",time.time()-start)
def test_update_montask():
    session = dbutil.connect()
    # 查询所有的
    row = session.query(MonTask).filter(MonTask.batchNo=="20231124165654").update({MonTask.status:"2"})
    session.commit()
    print('查询所有结果：')
    print(row)
    session.close()

def test_select_monlink():
    session = dbutil.connect()
    # 查询所有的
    lists = session.query(MonLink).filter(MonLink.typea=="jd").all()
    print('查询所有结果：')
    for l in lists:
        print(l )
    print('')
    session.close()
def test_select_monlink():
    session = dbutil.connect()
    # 查询所有的
    lists = session.query(MonKeyword).filter(MonKeyword.id=="1000").all()
    print('查询所有结果：')
    for l in lists:
        print(l.name)
    print('')
    session.close()
