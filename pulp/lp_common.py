# coding:utf-8
import time
import math
import sympy
import functools
import numpy as np

data_total_maxmin_qty=[]
np_data=""
total_qty={}
sorted_rp = []
rlist = []
def func(a, b):
    return a + b
def __build_mode(m):
    b = ''
    if m.get("b") >= 0:
        b = 0-m.get("b")
    else:
        b = -(0+m.get("b"))
    rlist.append({"name":m.get("name"),"class":m.get("class")*(b)})

def build_rlist1(_mode):
    for m in _mode:
        for _m in m:
            __build_mode(_m)

def build_xy_rp():
    _rlist = []
    for i in range(len(np_data[:1,:][0])):
        _count = 0
        for j in range(1,len(np_data[:,:i])+1):
            for _rp in data_total_maxmin_qty:
                if j == int(_rp.get("name").split("_")[1]):
                    _count += np_data[j-1,i] * _rp.get("rp")
                    #print(_count,np_data[j-1,i] * _rp.get("rp"))
        _rlist.append(_count)
    return _rlist

def build_rlist(_mode):
    #TODO 有顺序要求
    _xy_rp =  build_xy_rp()
    for m in _mode:
        for _m in m:
            _index = int(_m.get("name").split("_")[2])
            _r = int(_m.get("class")) - _xy_rp[int(_index-1)]
            rlist.append({"name":_m.get("name"),"class":_r})
    return rlist;

def build_sorted_rp(data_total_maxmin_qty):
    sorted_rp.clear()
    _data_total_maxmin_qty = data_total_maxmin_qty.copy()
    _tmp = []
    for m in _data_total_maxmin_qty:
        _total_qty =  total_qty.get(m.get("name"))
        if m.get("max_qty") >= _total_qty and  m.get("min_qty") <=_total_qty:
            _tmp.append({"total_qty":_total_qty,"sort":1000000000,"rp":m.get("rp")})
        if m.get("min_qty") > _total_qty:
            _tmp.append({"total_qty":_total_qty,"sort":(m.get("min_qty") - _total_qty),"rp":m.get("rp")})
            #sorted_rp.append(m.get("rp"))
        if m.get("max_qty") < _total_qty:
            _tmp.append({"total_qty":_total_qty,"sort":(m.get("max_qty") - _total_qty),"rp":m.get("rp")})
            #sorted_rp.append(m.get("rp"))
    _tmp.sort(key=lambda x: x["sort"], reverse=False)
    [sorted_rp.append(i.get("rp")) for i in _tmp]
    return sorted_rp

def __build_total_qty(_data):
    #for i in range(1,len(_data)+1):
    #    count = functools.reduce(func,data[i-1])
    #    total_qty.append({"name":"class_"+str(i),"total_qty":count})
    #return total_qty
    sum = np_data.sum(axis=1)
    for i in range(1,len(np_data[:,0])+1):
        total_qty.update({"class_"+str(i):sum[i-1]})
    return total_qty

#def merge_mm_total_qty(_data,_data_maxmin_qty):
#   result = {}
#   for mm in _data_maxmin_qty:
#        tmp = build_total_qty(_data)
#        if mm.get("name") == tmp.get("name"):
#            mm.update(tmp.)
#   return _data_maxmin_qty
def cond_mutil_10(_data):
    h = []
    for t in data_total_maxmin_qty:
        if t.get("mul") != None:
            h.append(int(t.get("name").split("_")[1]))
    for i in h:
        ll = np_data[i-1:i,:]
        for j in range(len(ll[0])):
            _pty = np_data[i-1,j]
            _rem = _pty % 10
            if _rem >0:
                np_data[i-1,j] = _pty - _rem
    __build_total_qty(_data)

def cond_mutil_2():
    pass
def cond_ge_some_qty():
    pass

def remove_data_total_maxmin_qty(maxmin_qty,m):
    _tmp_data_total_maxmin_qty = maxmin_qty.copy()
    _tmp_data_total_maxmin_qty.remove(m)
    return _tmp_data_total_maxmin_qty

def qty_allot(h,v,_int):
    _xy = np_data[h-1,v-1]
    _xy = (_xy + _int) if _int < 0 else ( _xy - _int)
    np_data[h-1,v-1] = _xy


def get_name_by_rp(rp):
    for d in data_total_maxmin_qty:
        if d.get("rp") == rp:
            return d.get("name")

def verity_bottom(name,data_total_maxmin_qty):
    _data_total_maxmin_qty = data_total_maxmin_qty.copy()
    _total1 = 0
    _total2 = 0
    for m in _data_total_maxmin_qty:
        _total_qty =  total_qty.get(m.get("name"))
        if m.get("max_qty") < _total_qty:
            _xy = get_xy_data(name,m)
            if _total_qty - m.get("max_qty") > _xy:
                _total1  += (_xy)* m.get("rp")
            else:
                _total1  += (_total_qty - m.get("max_qty"))* m.get("rp")
        if m.get("min_qty") > _total_qty:
            _total2  += (m.get("min_qty") - _total_qty)* m.get("rp")
    return  ((-_total1) + (_total2))


def hander_total_minqty(_r,name,_int,_sorted_rp,_rp,_rem,_data_total_maxmin_qty,m,q,total):
    result = 0
    _sorted_rp1 = _sorted_rp.copy()
    _sorted_rp1.remove(_rp)
    _data_total_maxmin_qty1 = _data_total_maxmin_qty.copy()
    _data_total_maxmin_qty1.remove(m)
    _xy_name = get_xy_name(name,m)
    #if _int < 0:
    #    solve(_r,name,_data_total_maxmin_qty1)
    #    return (result+1)
    if int(m.get("min_qty")) <= total :
        # 修改max_qty
        q.update({m.get("name"): total})

        results.append((name,_int,_rp,_rem))
        print(name,_int,_rp,_rem)
    else:
        print("minqty不满足",_xy_name,_int,_rp,_rem)

        #min_qty取溢出数
        _total = int(m.get("min_qty")) - total

        #可以加多少
        _name1 = name.split("_")[2]
        _name0 = m.get("name").split("_")[1]
        _xy = np_data[int(_name0)-1,int(_name1)-1]

        ##判断底线 数量
        #_upper = verity_bottom(name,_data_total_maxmin_qty1)

        if _int > _total:
            _int1 = _total
            _rem1 = (_r - _int1 * _rp )
        if _int <= _total:
            _int1 = _int
            _rem1 = _rem

        # 处理倍数
        if (m.get("mul")==10):
            _int1 = int(_int/10 )*10
            _rem1 = (_r - _int1 * _rp )

        #_in_r =  _r - (_total * _rp)  if _r > 0 else _r + (_total * _rp)
        #_int1 = (_int - _total) if _int > 0 else  (_int + _total)
        #_rem1 = (_int1*_rp + _rem) if _int1 > 0 else (_int1*_rp - _rem)
        # 修改total_qty
        _total_qty = (q.get(m.get("name")) + _int1)
        q.update({m.get("name"): _total_qty})

        _xy_name = get_xy_name(name,m)
        results.append((_xy_name,_int1,_rp,_rem1))
        print(_xy_name,_int1,_rp,_rem1)

        solve(_rem1,name,_data_total_maxmin_qty1)
    return result

def hander_total_maxqty(_r,name,_int,_sorted_rp,_rp,_rem,_data_total_maxmin_qty,m,q,total):
    result = 0
    _sorted_rp1 = _sorted_rp.copy()
    _sorted_rp1.remove(_rp)
    _data_total_maxmin_qty1 = _data_total_maxmin_qty.copy()
    _data_total_maxmin_qty1.remove(m)
    _xy_name = get_xy_name(name,m)
    # 不能再加
    #if _int > 0:
    #    solve(_r,name,_data_total_maxmin_qty1)
    #    return (result+1)
    if int(m.get("max_qty")) >= total :
        # 修改total_qty
        q.update({m.get("name"): total})

        results.append((name,_int,_rp,_rem))
        print(name,_int,_rp,_rem)

    else:
        #_total_qty.remove(q)
        print("maxqty不满足",_xy_name,_int,_rp,_rem)

        #修改total_qty
        _total = total - int(m.get("max_qty"))

        #可以减多少
        _name1 = name.split("_")[2]
        _name0 = m.get("name").split("_")[1]
        _xy = np_data[int(_name0)-1,int(_name1)-1]

        _int1 = _xy if _total > _xy else _total
        _rem = (_r + _int1 * _rp )


        # 处理倍数
        if (m.get("mul")==10):
            _int1 = int(_int/10 )*10
            _rem = (_r + _int1 * _rp )

        ## 修改total_qty
        _total_qty = (q.get(m.get("name")) - _int1)
        q.update({m.get("name"): _total_qty})

        results.append((_xy_name,-_int1,_rp,_rem))
        print(_xy_name,-_int1,_rp,_rem)

        solve(_rem,name,_data_total_maxmin_qty1)

    #hander_rem(name,_rem,_sorted_rp1,_data_total_maxmin_qty1)
    return result

def hander_rem(name,rem,sorted_rp,data_total_maxmin_qty):
    _rem = rem
    _sorted_rp = sorted_rp.copy()
    _data_total_maxmin_qty = data_total_maxmin_qty.copy()
    for r in sorted_rp:
        if _rem // r > 0:
            break
        else:
            _sorted_rp.remove(r)
    if (len(_sorted_rp) >= 1 ):
        solve(_rem,name,_data_total_maxmin_qty)

def verify_rem(rem,sorted_rp):
    _rem = rem
    _sorted_rp = sorted_rp.copy()
    for r in sorted_rp:
        if _rem // r > 0:
            break
        else:
            _sorted_rp.remove(r)
    result = 1 if len(_sorted_rp) > 0 else 0
    return result

def again_sovle(_r,name,rp,sorted_rp,data_total_maxmin_qty,m):
    if len(sorted_rp) > 0:
        _rp = rp
        _sorted_rp0 = sorted_rp.copy()
        _sorted_rp0.remove(_rp)
        _data_total_maxmin_qty0 = data_total_maxmin_qty.copy()
        _data_total_maxmin_qty0.remove(m)
    if len(_sorted_rp0) > 0:
        solve(_r,name,_data_total_maxmin_qty0)

def get_xy_name(name,m):
    _name0 = m.get("name").split("_")[1]
    _name1 = name.split("_")[2]
    return "class_"+_name0+"_"+_name1

def get_xy_data(name,m):
    _name0 = m.get("name").split("_")[1]
    _name1 = name.split("_")[2]
    _xy = np_data[int(_name0)-1,int(_name1)-1]
    return _xy
def get_single_total_maxmin_qty(data_total_maxmin_qty,rp,total_qty):
    _data_total_maxmin_qty = data_total_maxmin_qty.copy()
    _tmp1=[]
    _tmp2=[]

    for m in _data_total_maxmin_qty:
        _total_qty = total_qty.get(m.get("name"))
        if m.get("rp") == rp:
            if m.get("max_qty") >= _total_qty  and m.get("min_qty") <= _total_qty:
                _tmp1.append(m)
            else:
                _tmp2.append(m)
    _tmp2.extend(_tmp1)
    return _tmp2[0]

def cond_maxmin_total_qty(name,_r,_int,_rem,sorted_rp,data_total_maxmin_qty):
    _rp = sorted_rp[0]
    _name = name.split("_")[0]
    _name1 = name.split("_")[2]
    _sorted_rp = sorted_rp.copy()
    _data_total_maxmin_qty = data_total_maxmin_qty.copy()
    #_total_qty = build_total_qty(data)
    _rp_flag = 0
    #for m in _data_total_maxmin_qty:
    #    if m.get("rp") == _rp:
    m = get_single_total_maxmin_qty(_data_total_maxmin_qty,_rp,total_qty)
    #_rp_flag += 1
    # 精简
    #_tmp_data_total_maxmin_qty = remove_data_total_maxmin_qty(_data_total_maxmin_qty,m)
    _name0 = m.get("name").split("_")[1]
    #获取坐标值
    _xy = np_data[int(_name0)-1,int(_name1)-1]
    #跳过
    if (_xy == 0 and _int < 0):
        _sorted_rp0 =  sorted_rp.copy()
        _sorted_rp0.remove(_rp)
        _data_total_maxmin_qty0 = _data_total_maxmin_qty.copy()
        _data_total_maxmin_qty0.remove(m)
        solve(_r,name,_data_total_maxmin_qty0)
        #break
        return

    _total_qty = total_qty.get(m.get("name"))
    if  (_xy + _int < 0 and _int < 0):
        _int1 = - _xy
        total_qty.update({m.get("name"): (_total_qty+_int1)})

        _in_r = (_xy + _int)*_rp - _rem

        _xy_name = get_xy_name(name,m)
        results.append((_xy_name,_int1,_rp,-_in_r))
        print(_xy_name,_int1,_rp,_in_r)

        again_sovle(_in_r,name,_rp,_sorted_rp,_data_total_maxmin_qty,m)
        return
        #break

    if int(m.get("max_qty")) >= _total_qty and int(m.get("min_qty")) <= _total_qty:
        total = (_total_qty + _int) if _int > 0 else (_total_qty + _int)
        if int(m.get("max_qty")) >= total and int(m.get("min_qty")) <= total:
            #if verify_rem(_rem,_sorted_rp) > 0:
            #    _sorted_rp0 =  sorted_rp.copy()
            #    _sorted_rp0.remove(_rp)
            #    _data_total_maxmin_qty0 = _data_total_maxmin_qty.copy()
            #    _data_total_maxmin_qty0.remove(m)
            #    hander_rem(name,_rem,_sorted_rp0,_data_total_maxmin_qty0)

            #if _rp_flag > 1 :
            #    break

            _int1=_int
            _rem1=_rem

            # 处理倍数
            if (m.get("mul")==10):
                _int1 = int(_int/10 )*10
                _rem1 = (_r - _int1 * _rp ) if _int1 < 0 else (_r + _int1 * _rp )

            if _int1 < 0 and (-_int1 > _xy):
                _int1 = -_xy
                _rem1 = (_r - _int1 * _rp ) if _int1 < 0 else (_r + _int1 * _rp )


            # 修改total_qty
            total_qty.update({m.get("name"): total_qty.get(m.get("name")) + _int1})

            _xy_name = get_xy_name(name,m)
            results.append((_xy_name,_int1,_rp,_rem1))
            print(_xy_name,_int1,_rp,_rem1)

            again_sovle(_rem1,name,_rp,_sorted_rp,_data_total_maxmin_qty,m)

        if int(m.get("max_qty")) < total:
            result = hander_total_maxqty(_r,name,_int,_sorted_rp,_rp,_rem,_data_total_maxmin_qty,m,total_qty,total)
            #if result != 0:
            #break
            return
        if int(m.get("min_qty")) > total:
            result = hander_total_minqty(_r,name,_int,_sorted_rp,_rp,_rem,_data_total_maxmin_qty,m,total_qty,total)
            #if result != 0:
            #break
            return
    if int(m.get("max_qty")) < _total_qty:
        result = hander_total_maxqty(_r,name,_int,_sorted_rp,_rp,_rem,_data_total_maxmin_qty,m,total_qty,_total_qty)
        #if result != 0:
        #break
        return
    if int(m.get("min_qty")) > _total_qty:
        result = hander_total_minqty(_r,name,_int,_sorted_rp,_rp,_rem,_data_total_maxmin_qty,m,total_qty,_total_qty)
        #if result != 0:
        #break
        return
    #break
    #_in_rp = _sorted_rp[0]
    #_in_int = _in_r//_in_rp
    #_in_rem = _in_r - _in_rp * _in_int
    #_in_int = _in_int if _int > 0 else -_in_int
    #cond_maxmin_total_qty(name,_r,_sorted_rp[0],_in_int,_in_rem,_sorted_rp,_data_total_maxmin_qty)
results=[]
def solve_old(g,r,name:str):
    _r = math.ceil(r)
    for i in sorted_rp:
        _int = _r//i
        _r = _rem = _r - i*_int
        _int += g

        results.append((name,_int,i,_r))
        print((name,_int,i,_r))
        #cond_maxmin_total_qty(name,i,_int,_rem)

def solve(r,name:str,data_total_maxmin_qty):
    _r = math.ceil(r)
    _sorted_rp = build_sorted_rp(data_total_maxmin_qty)
    #for i in sorted_rp[0]:
    if len(_sorted_rp) > 0:
        _rp = _sorted_rp[0]
        _int = _r//_rp
        _rem = _r - _rp*_int

        #results.append((name,_int,i,_r))
        #print((name,_int,i,_r))
        cond_maxmin_total_qty(name,_r,_int,_rem,_sorted_rp,data_total_maxmin_qty)

def make_result():
    #count = functools.reduce(func,rp)
    for r in rlist:
        tmp:int
        #if r.get("class1")>=0:
        #    g = int(r.get("class1")/count)
        #    tmp = r.get("class1")-count*g
        #else:
        #    g = int(r.get("class1")/count)
        #    tmp = r.get("class1")+count*g
        g=0
        tmp = r.get("class")
        #solve_old(g,tmp,r.get("name"))
        solve(tmp,r.get("name"),data_total_maxmin_qty)

def run_modex(_mode,data):
    cond_mutil_10(data)
    build_rlist(_mode)
    make_result()
    [print(r) for r in results]
    return results

def run(_mode,data,_data_total_maxmin_qty):
    data_total_maxmin_qty.extend(_data_total_maxmin_qty)
    global np_data
    np_data = np.array(data)
    np_data[np_data == None] = 0
    rlist.clear()
    total_qty.clear()
    run_modex(_mode,data)

#start_time = time.time()
#print("-----------------------mode0")
#run(mode)
#
#print(f"cost time: ",(time.time()-start_time))

