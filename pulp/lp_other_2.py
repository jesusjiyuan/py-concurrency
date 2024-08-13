# coding:utf-8
import time
import math
import sympy
import functools
import numpy as np
import mapper

class1_1 = 500000
class1_2 = 845000
class1_3 = 532000
class1_4 = 1335000

#mode = (( {"name":"class_1_1","class":class1_1,"b":0.0046}
#         ,{"name":"class_1_2","class":class1_2,"b":-0.0434}
#         ,{"name":"class_1_3","class":class1_3,"b":0.0111})
#        ,({"name":"class_1_4","class":class1_4,"b":0.0432},))

#data = [
#    [150,0,0,2600,150,0,0,260,150,0,0,2600,2600,150]
#    ,[250,450,0,1950,250,450,0,1500,250,450,0,150,1950,250]
#    ,[809,2350,150,40,800,250,150,40,800,2350,150,40,40,800]
#    ,[2300,150,100,150,1200,150,100,150,2300,150,100,150,150,2300]
#    ,[150,100,2150,900,150,100,2150,900,150,100,2150,900,950,150]
#    ,[400,1500,40,80,400,1500,40,80,400,1500,40,80,80,400]
#    ,[150,2499,150,100,150,2499,150,100,150,2499,150,100,100,150]
#]
data = [[0]]
#data_total_maxmin_qty=[
#    {"name":'class_1',"max_qty":8000,"min_qty":6000,"rp":329},
#    {"name":'class_2',"max_qty":12000,"min_qty":6000,"rp":149},
#    {"name":'class_3',"max_qty":9100,"min_qty":6000,"rp":99,"mul":10},
#    {"name":'class_4',"max_qty":12000,"min_qty":6000,"rp":99,"mul":10},
#    {"name":'class_5',"max_qty":12000,"min_qty":6000,"rp":229},
#    {"name":'class_6',"max_qty":12000,"min_qty":6700,"rp":149},
#    {"name":'class_7',"max_qty":12000,"min_qty":6000,"rp":99}
#]
articleclusterref=[]
data_total_maxmin_qty=[]
np_data = np.array(data)
total_qty=[]
#rp = [329,149,99,99,229,149,99]
rp=[]
sorted_rp=[]
rlist = []
def build_data_total_maxmin_qty():
    data = mapper.query_article_all()
    for i in range(1,len(data)+1):
        _index = i-1
        data_total_maxmin_qty.append({"name":'class_'+str(i),"max_qty":data[_index].MaxQty,"min_qty":data[_index].MinQty,"rp":data[_index].RP},)
        rp.append(data[_index].RP)
    sorted_rp.extend(list(reversed(sorted(rp))))

def func(a, b):
    return a + b

def build_rlist():
    clusters = mapper.query_cluster_all()
    cols = mapper.get_cluster_column_count()
    for c in clusters:
        for i in range(1,len(cols)+1):
            otb = c.OTB - cols[i-1].total
            #{"name":"class_1_1","class":class1_1,"b":0.0046}
            rlist.append({"name":"class_1_"+str(i),"class":otb})

def __build_total_qty():
    total_qty.clear()
    for qty in mapper.get_article_row_count():
        total_qty.append({"name":"class_"+str(qty.ID),"total_qty":qty.total})
    return total_qty
    #sum = np_data.sum(axis=1)
    #for i in range(1,len(np_data[:,0])+1):
    #    total_qty.append({"name":"class_"+str(i),"total_qty":sum[i-1]})
    #return total_qty

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

def hander_total_minqty(_r,name,_int,_sorted_rp,_rp,_rem,_data_total_maxmin_qty,m,q,total):
    result = 0
    _sorted_rp1 = _sorted_rp.copy()
    _sorted_rp1.remove(_rp)
    _data_total_maxmin_qty1 = _data_total_maxmin_qty.copy()
    _data_total_maxmin_qty1.remove(m)
    # 不能再减
    if _int < 0:
        solve(_r,name,_sorted_rp1,_data_total_maxmin_qty1)
        return (result+1)
    if int(m.get("min_qty")) <= total :
        # 修改max_qty
        q.update({"name":q.get("name"),"total_qty": total})

        results.append((name,_int,_rp,_rem))
        print(name,_int,_rp,_rem)
    else:
        print("minqty不满足",name,_int,_rp,_rem)

        #min_qty取溢出数
        _total = int(m.get("min_qty")) - total

        _in_r =  _r - (_total * _rp)  if _r > 0 else _r + (_total * _rp)
        _int1 = (_int - _total) if _int > 0 else  (_int + _total)
        _rem1 = (_int1*_rp + _rem) if _int1 > 0 else (_int1*_rp - _rem)
        # 修改total_qty
        _total_qty = (q.get("total_qty") + _int) if _int > 0 else (q.get("total_qty") - _int)
        q.update({"name":q.get("name"),"total_qty": _total_qty})

        results.append((name,_int,_rp,_rem))
        print(name,_int,_rp,_rem)
    hander_rem(name,_rem,_sorted_rp1,_data_total_maxmin_qty1)
    return result

def hander_total_maxqty(_r,name,_int,_sorted_rp,_rp,_rem,_data_total_maxmin_qty,m,q,total):
    result = 0
    _sorted_rp1 = _sorted_rp.copy()
    _sorted_rp1.remove(_rp)
    _data_total_maxmin_qty1 = _data_total_maxmin_qty.copy()
    _data_total_maxmin_qty1.remove(m)

    # 不能再加
    if _int > 0:
        solve(_r,name,_sorted_rp1,_data_total_maxmin_qty1)
        return (result+1)
    if int(m.get("max_qty")) >= total :
        # 修改total_qty
        q.update({"name":q.get("name"),"total_qty": total})

        results.append((name,_int,_rp,_rem))
        print(name,_int,_rp,_rem)

    else:
        #_total_qty.remove(q)
        print("maxqty不满足",name,_int,_rp,_rem)

        #修改total_qty
        _total = total - int(m.get("max_qty"))

        _tmp_int = _int if _int > 0 else -_int
        #if _total - _tmp_int >0:

        _in_r =  _r + (_total * _rp)  if _r > 0 else _r - (_total * _rp)
        _int1 = (_int - _total) if _int > 0 else  (_int + _total)
        _rem1 = (_int1*_rp + _rem) if _int1 > 0 else (_int1*_rp - _rem)

        ## 修改total_qty
        _total_qty = (q.get("total_qty") - _int) if _int > 0 else (q.get("total_qty") + _int)
        q.update({"name":q.get("name"),"total_qty": _total_qty})

        results.append((name,_int,_rp,_rem))
        print(name,_int,_rp,_rem)
    hander_rem(name,_rem,_sorted_rp1,_data_total_maxmin_qty1)
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
        solve(_rem,name,_sorted_rp,_data_total_maxmin_qty)

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
    _rp = rp
    _sorted_rp0 = sorted_rp.copy()
    _sorted_rp0.remove(_rp)
    _data_total_maxmin_qty0 = data_total_maxmin_qty.copy()
    _data_total_maxmin_qty0.remove(m)
    solve(_r,name,_sorted_rp0,_data_total_maxmin_qty0)


def cond_maxmin_total_qty(name,_r,_int,_rem,sorted_rp,data_total_maxmin_qty):
    _rp = sorted_rp[0]
    _name = name.split("_")[0]
    _name1 = name.split("_")[2]
    _sorted_rp = sorted_rp.copy()
    _data_total_maxmin_qty = data_total_maxmin_qty.copy()
    #_total_qty = build_total_qty(data)
    _rp_flag = 0
    for m in _data_total_maxmin_qty:
        if m.get("rp") == _rp:
            _rp_flag += 1
            # 精简
            #_tmp_data_total_maxmin_qty = remove_data_total_maxmin_qty(_data_total_maxmin_qty,m)
            _name0 = m.get("name").split("_")[1]
            #获取坐标值
            #_xy = np_data[int(_name0)-1,int(_name1)-1]
            _xy = iterater_articleclusterref(_name0,_name1)
            #跳过
            if (_xy == 0 and _int < 0) or (m.get("mul")==10):
                _sorted_rp0 =  sorted_rp.copy()
                _sorted_rp0.remove(_rp)
                _data_total_maxmin_qty0 = _data_total_maxmin_qty.copy()
                _data_total_maxmin_qty0.remove(m)
                solve(_r,name,_sorted_rp0,_data_total_maxmin_qty0)
                break
            if _rp_flag > 1 :
                break
            for q in total_qty:
                if m.get("name") == q.get("name") :
                    total = (q.get("total_qty") + _int) if _int > 0 else (q.get("total_qty") + _int)
                    if  (_xy + _int < 0 and _int < 0):
                        _int1 = - _xy
                        q.update({"name":q.get("name"),"total_qty": (q.get("total_qty")+_int1)})

                        _in_r = (_xy + _int)*_rp - _rem
                        results.append((name,_int1,_rp,-_in_r))
                        print(name,_int1,_rp,_in_r)

                        again_sovle(_in_r,name,_rp,sorted_rp,_data_total_maxmin_qty,m)
                        break

                    if int(m.get("max_qty")) >= q.get("total_qty") and int(m.get("min_qty")) <= q.get("total_qty"):
                        if int(m.get("max_qty")) >= total and int(m.get("min_qty")) <= total:
                            if verify_rem(_rem,_sorted_rp) > 0:
                                _sorted_rp0 =  sorted_rp.copy()
                                _sorted_rp0.remove(_rp)
                                _data_total_maxmin_qty0 = _data_total_maxmin_qty.copy()
                                _data_total_maxmin_qty0.remove(m)
                                hander_rem(name,_rem,_sorted_rp0,_data_total_maxmin_qty0)
                            if _rp_flag > 1 :
                                break
                            # 修改total_qty
                            q.update({"name":q.get("name"),"total_qty": total})

                            results.append((name,_int,_rp,_rem))
                            print(name,_int,_rp,_rem)

                        if int(m.get("max_qty")) < total:
                            result = hander_total_maxqty(_r,name,_int,_sorted_rp,_rp,_rem,_data_total_maxmin_qty,m,q,total)
                            #if result != 0:
                            break
                        if int(m.get("min_qty")) > total:
                            result = hander_total_minqty(_r,name,_int,_sorted_rp,_rp,_rem,_data_total_maxmin_qty,m,q,total)
                            #if result != 0:
                            break
                    if int(m.get("max_qty")) < q.get("total_qty"):
                        result = hander_total_maxqty(_r,name,_int,_sorted_rp,_rp,_rem,_data_total_maxmin_qty,m,q,q.get("total_qty"))
                        #if result != 0:
                        break
                    if int(m.get("min_qty")) > q.get("total_qty"):
                        result = hander_total_minqty(_r,name,_int,_sorted_rp,_rp,_rem,_data_total_maxmin_qty,m,q,q.get("total_qty"))
                        #if result != 0:
                        break
                           #_in_rp = _sorted_rp[0]
                           #_in_int = _in_r//_in_rp
                           #_in_rem = _in_r - _in_rp * _in_int
                           #_in_int = _in_int if _int > 0 else -_in_int
                           #cond_maxmin_total_qty(name,_r,_sorted_rp[0],_in_int,_in_rem,_sorted_rp,_data_total_maxmin_qty)

def iterater_articleclusterref(articleId,clusterId):
    result = 0
    for rf in articleclusterref:
        if rf.ArticleID == articleId and rf.ClusterID == clusterId:
            result = rf.Qty
    return result

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

def solve(r,name:str,sorted_rp,data_total_maxmin_qty):
    _r = math.ceil(r)
    #for i in sorted_rp[0]:
    if len(sorted_rp) > 0:
        _rp = sorted_rp[0]
        _int = _r//_rp
        _rem = _r - _rp*_int

        #results.append((name,_int,i,_r))
        #print((name,_int,i,_r))
        cond_maxmin_total_qty(name,_r,_int,_rem,sorted_rp,data_total_maxmin_qty)

def make_result():
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
        solve(tmp,r.get("name"),sorted_rp,data_total_maxmin_qty)


def run_modex():
    build_data_total_maxmin_qty()
    articleclusterref.extend(mapper.get_articleclusterref_all())
    #cond_mutil_10(data)
    __build_total_qty()
    build_rlist()
    make_result()
    [print(r) for r in results]
    return results

def run():
    rlist.clear()
    run_modex()

start_time = time.time()
print("-----------------------mode0")
run()
print("-----------------------mode1")
print(f"cost time: ",(time.time()-start_time))


