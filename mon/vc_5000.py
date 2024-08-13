# coding: utf-8
import dbutil
from mapper.domain import Tmp5000
import pandas as pd
import timeit

def test_excel():
    excel_file = "D:\\labs\\vcapi\\海康推送的5000路视频点位信息-new.xlsx"
    pp = pd.read_excel(excel_file)
    #print(pp["sharename"],pp["indexcode"])
    #print(pp.loc[:,["indexcode","sharename"]])
    for index,name in pp.loc[:,["indexcode","sharename"]].values:
        print(index,name)


def test_insert_vc_5000():
    session = dbutil.connect_vc()
    # 查询所有的
    excel_file = "D:\\labs\\vcapi\\海康推送的5000路视频点位信息-new.xlsx"
    df = pd.read_excel(excel_file,header=None,index_col=None,usecols='D:E',)
    print(len(df.values))
    flag = 1
    count = 100
    tmplist = []
    for index,name in df.values:
        if flag == 1:
            flag=0
            continue
        count += 1
        tmp5000 = Tmp5000(id=count,indexcode=str(index),sharename=str(name))
        tmplist.append(tmp5000)
        print(tmp5000)
    session.add_all(tmplist)
    session.commit()
    session.flush()
    #ret= session.add_all()
    #print('结果：',ret)
    session.close()

def test_timeit():
    count = 0
    start = timeit.default_timer()
    for i in range(100):
        count += 1
    print("")
    print(count)
    stop = timeit.default_timer()
    print('time1: ', stop-start)


def test_speedtest():
    from speedtest import Speedtest
    test = Speedtest()
    # Download Speed
    down = test.download()
    print("")
    print("Download Speed: ",down)
    print(f"下载速度：{round(down/(1024*1024),2)}Mbps")
    # Upload Speed
    upload = test.upload()
    print("Upload Speed",upload)
    print(f"上传速度：{round(upload/(1024*1024),2)}Mbps")
    # Ping test
    server_names = []
    test.get_servers(server_names)
    print("Ping test",test.results.ping)