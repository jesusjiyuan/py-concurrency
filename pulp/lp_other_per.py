# coding:utf-8
import time
import math
import sympy
import functools

class1_1 = 500000
class1_2 = 845000
class1_3 = 532000
class1_4 = 1335000

class2_1 = class1_1 + class1_2 + class1_3
class2_2 = class1_4
class3 = class1_1 + class1_2 + class1_3 + class1_4

mode = (( {"name":"class1_1","class1":class1_1,"b":-0.0726}
         ,{"name":"class1_2","class1":class1_2,"b":0.0198}
         ,{"name":"class1_3","class1":class1_3,"b":0.0195})
        ,{"name":"class1_4","class1":class1_4,"b":0.0093})
rp = [329,149,99,99,229,149,99]
sorted_rp = sorted(set(rp))
rlist = []
def make_mode(m):
    b = ''
    if m.get("b") >= 0:
        b = 0-m.get("b")
    else:
        b = -(0+m.get("b"))
    rlist.append({"name":m.get("name"),"class1":m.get("class1")*(b)})

def build_rlist():
    for m in mode[0]:
        make_mode(m)
    make_mode(mode[1])

def func(a, b):
    return a + b

results=[]
def solve(g,r,name:str):
    _r = math.ceil(r)
    for i in sorted_rp:
        tmp = _r//i
        _r = _r - i*tmp
        tmp += g
        results.append((name,tmp,i,_r))
        #print(name,tmp,i,_r)

def make_result():
    count = functools.reduce(func,rp)
    for r in rlist:
        tmp:int
        if r.get("class1")>=0:
            g = int(r.get("class1")/count)
            tmp = r.get("class1")-count*g
        else:
            g = int(r.get("class1")/count)
            tmp = r.get("class1")+count*g
        #g=0
        #tmp = r.get("class1")
        #solve(g,tmp,r.get("name"))

def run():
    build_rlist()
    make_result()
    [print(r) for r in results]

run()