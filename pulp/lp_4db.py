# coding:utf-8
import time
import math
import sympy
import functools
import numpy as np
import lp_common_db as lp
import mapper
import sys
sys.setrecursionlimit(10000)

class1_1 = 500000
class1_2 = 845000
class1_3 = 532000
class1_4 = 1335000

class1_5  = 385000
class1_6  = 535000
class1_7  = 533600
class1_8  = 535000
class1_9  = 495000
class1_10 = 855000
class1_11 = 575000
class1_12 = 1209080
class1_13 = 1489000
class1_14 = 492000
mode = (( {"name":"class_1_1","class":class1_1,"b":0.0046}
          ,{"name":"class_1_2","class":class1_2,"b":-0.0434}
          ,{"name":"class_1_3","class":class1_3,"b":0.0111})
        ,({"name":"class_1_4","class":class1_4,"b":0.0432},)
        , (  {"name":"class_1_5","class":class1_5 ,"b":0.0218}
             ,{"name":"class_1_6","class":class1_6 ,"b":0.1223}
             ,{"name":"class_1_7","class":class1_7 ,"b":0.0081}
             ,{"name":"class_1_8","class":class1_8 ,"b":0.0388}
             ,{"name":"class_1_9","class":class1_9 ,"b":0.0147}
             ,{"name":"class_1_10","class":class1_10,"b":-0.0546}),(
            {"name":"class_1_11","class":class1_11,"b":-0.0645}
            ,{"name":"class_1_12","class":class1_12,"b":-0.0700}
            ,{"name":"class_1_13","class":class1_13,"b":-0.0570}
            ,{"name":"class_1_14","class":class1_14,"b":0.0209}
        )
        )

data = [[0]]
data_total_maxmin_qty=[]


def build_data_total_maxmin_qty():
    data = mapper.query_article_all()
    for i in range(1,len(data)+1):
        _index = i-1
        data_total_maxmin_qty.append({"name":'class_'+str(i),"max_qty":data[_index].MaxQty,"min_qty":data[_index].MinQty,"rp":data[_index].RP},)

def build_data():
    _tmp = []
    for c in mapper.query_cluster_all():
        _tmp1 = []
        _tmp1.append(c.ID)
        _tmp.append(_tmp1)
    _data = mapper.get_xy_data(tuple(_tmp))
    for i in range(len(_data)):
        d = _data[i]
        #print(d[0],d[1],d[2:])
        data.append(list(d[2:]))
    data.pop(0)
    return data

def run():
    build_data_total_maxmin_qty()
    build_data()
    lp.run(data,data_total_maxmin_qty)


start_time = time.time()
print("-----------------------mode0")
run()

print(f"cost time: ",(time.time()-start_time))


