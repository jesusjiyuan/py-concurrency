# coding:utf-8
import time
import math
import sympy
import functools
import numpy as np
import lp_common as lp

class1_1 = 500000
class1_2 = 845000
class1_3 = 532000
class1_4 = 1335000

class2_1 = class1_1 + class1_2 + class1_3
class2_2 = class1_4
class3 = class1_1 + class1_2 + class1_3 + class1_4


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
mode1 = ((   {"name":"class_1_5","class":class1_5 ,"b":0.0218}
             ,{"name":"class_1_6","class":class1_6 ,"b":0.1223}
             ,{"name":"class_1_7","class":class1_7 ,"b":0.0081}
             ,{"name":"class_1_8","class":class1_8 ,"b":0.0388}
             ,{"name":"class_1_9","class":class1_9 ,"b":0.0147}
             ,{"name":"class_1_10","class":class1_10,"b":-0.0546}),(
             {"name":"class_1_11","class":class1_11,"b":-0.0645}
             ,{"name":"class_1_12","class":class1_12,"b":-0.0700}
             ,{"name":"class_1_13","class":class1_13,"b":-0.0570}
             ,{"name":"class_1_14","class":class1_14,"b":0.0209}
         ))

data = [
     [150,0,0,2600,150,0,0,260,150,0,0,2600,2600,150]
    ,[250,450,0,1950,250,450,0,1500,250,450,0,150,1950,250]
    ,[809,2350,150,40,800,250,150,40,800,2350,150,40,40,800]
    ,[2300,150,100,150,1200,150,100,150,2300,150,100,150,150,2300]
    ,[260,100,2150,900,150,100,2150,900,150,100,2150,900,950,150]
    ,[400,1500,40,80,400,1500,40,80,400,1500,40,80,80,400]
    ,[150,2499,150,100,150,2499,150,100,150,2499,150,100,100,150]

]
data_total_maxmin_qty=[
    {"name":'class_1',"max_qty":9000,"min_qty":8700,"rp":329},
    {"name":'class_2',"max_qty":12000,"min_qty":7910,"rp":149},
    {"name":'class_3',"max_qty":9100,"min_qty":8770,"rp":99,"mul":10},
    {"name":'class_4',"max_qty":12000,"min_qty":9460,"rp":99,"mul":10},
    {"name":'class_5',"max_qty":12000,"min_qty":11110,"rp":229},
    {"name":'class_6',"max_qty":12000,"min_qty":6700,"rp":149},
    {"name":'class_7',"max_qty":12000,"min_qty":8950,"rp":99}
]

def run():
    lp.run(mode,data,data_total_maxmin_qty)


start_time = time.time()
print("-----------------------mode0")
run()

print(f"cost time: ",(time.time()-start_time))


