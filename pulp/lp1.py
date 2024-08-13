# coding:utf-8
import time

from pulp import LpVariable, LpMaximize, LpMinimize, LpProblem, value, LpStatus, LpInteger, pulp, GLPK, MIPCL_CMD, \
    CPLEX_PY, PULP_CBC_CMD, CPLEX_CMD, GUROBI_CMD, GUROBI
from pulp.constants import LpStatusNotSolved,LpStatusOptimal,LpStatusInfeasible
from sqlalchemy import and_,text
from cluster import cluster
import util
from mapper import get_class3,get_class2,db,get_article_all,get_cluster_all
import datetime

from tmp_result import result


def build_prob():
    # 第一个参数为这个问题取名字，第二个参数表示求目标函数的最大值（LpMaximize）
    return LpProblem('min', sense=LpMaximize)
    # name为变量名， lowBound为下边界，None为没边界, cat约束变量的类型LpInteger为整型]

#------2
x = [[0]]
def build_lpvar(_articles,_clusters):
    for i in range(1, len(_articles)+1, 1):
        tmp = [0]
        for j in range(1,len(_clusters)+1,1):
            #LpVariable.dicts()
            tmp.append(LpVariable(name='x_'+str(i)+'_'+str(j), lowBound=0, upBound=None,cat=LpInteger))
        x.append(tmp)
def make_rpmap(_articles):
    tmp = {}
    [tmp.update({r.ID:r.RP}) for r in _articles]
    return tmp

def make_otbmap(_clusters):
    tmp = {}
    [tmp.update({i.ID:i.OTB}) for i in _clusters]
    return tmp

rp = {}
var_names = []
tmp_names = []
def resoleLp(_class3,_articles,_clusters,_rp):
    var_names.clear()
    tmp = ""
    for i in range(1, len(_articles)+1, 1):
        for j in range(1,len(_clusters)+1,1):
            tmp += x[i][j]*round(_rp.get(i))
            var_names.append('x_'+str(i)+'_'+str(j))
    tmp += tmp - round(_class3[0])
    return tmp


# # 约束条件
# 一级约束
def c1_cond(_prob,_rp):
    for c in db.query_list(cluster,cluster.Channel=='BLR'):
        otb = round(c.OTB)
        tmp = ""
        for i in range(1,len(_rp)+1):
            tmp += int(_rp.get(i))*x[i][c.ID]
        _prob += (tmp - otb) <= 0.02 * otb
        _prob += -(tmp - otb) >= -(0.02 * otb)
# 二级约束
def c2_cond(_prob,_class2,_rp):
    for c in _class2:
        account = c[0]
        otb = round(c[1])
        tmp = ""
        for z in db.query_list(cluster,and_(cluster.Channel=='BLR',cluster.Account==account)):
            for i in range(1,len(_rp)+1):
                tmp += int(_rp.get(i))*x[i][z.ID]
        _prob += (tmp - otb) <= 0.005 * otb
        _prob += -(tmp - otb) >= -(0.05 * otb)
# 三级约束
def c3_cond(_prob,_resoleLp,_class3):
    otb1 = round(_class3[0])
    _prob += (_resoleLp-otb1) <= 0.005/1000 * otb1
    _prob += -(_resoleLp-otb1) >= -(0.005/1000 * otb1)


#prob += (x[1][3]*1) % (10) == 0
#prob += x[1][1] >= 100

# total 最小最大
sql_pty = '''
    select isnull(sum(MaxQty),0), isnull(SUM(MinQty),0), ID  from z_tmp_article
    group by ID 
    '''
ptyss = db.session.execute(text(sql_pty)).fetchall()
def cond_total_pty(_prob):
    sql_pty1 = 'select rf.ClusterID, rf.ROS, rf.MinQty,a.ID  from z_tmp_assortment rf ' \
               'inner join z_tmp_article a on a.ArticleNo = rf.Article ' \
               'where a.ID = {0}'
    for c in ptyss:
        max_pty = c[0]
        mix_pty = c[1]
        id = c[2]
        tmp = ""
        for z in db.session.execute(text(sql_pty1.format(id))).fetchall():
            clusterID = z[0]
            tmp += x[id][clusterID]
        if max_pty != 0:
            _prob +=  tmp <= max_pty
        if mix_pty != 0:
            _prob +=  tmp >= mix_pty

# 单个pty最小最大
sql_pty2 = 'select rf.ClusterID, rf.ROS, rf.MinQty, a.ID, rf.SourceQty,rf.MaxQty  from z_tmp_assortment rf ' \
           'inner join z_tmp_article a on a.ArticleNo = rf.Article ' \
           'where a.ID in {0}'
def cond_maxmin_pty(_prob,_clusters):
    tmp_list = []
    for i in range(1,len(ptyss)+1):
        tmp_list.append(i)
    pty_results = db.session.execute(text(sql_pty2.format(tuple(tmp_list)))).fetchall()
    for z in pty_results:
        clusterID = z[0]
        ros = z[1]
        mpty = z[2]
        id = z[3]
        _prob += x[id][clusterID] >= 220
        _prob += x[id][clusterID] <= 2000
        #横向比例
        tmp = ""
        for i in range(1,len(_clusters)+1):
            tmp += x[id][i]
        #_prob += x[id][clusterID] >= (round(ros*10)/ 100) *( tmp)
        #纵向比例
        #tmp1 = ""
        #for i in range(1,len(ptyss)+1):
        #    tmp1 += x[i][clusterID]
        #_prob += x[id][clusterID] >= (round(ros*10)/ 100) *( tmp1)

        tmp_names.append('x_'+str(id)+'_'+str(clusterID))

    for i in var_names:
        if i not in tmp_names:
            sp = i.split("_")
            id = int(sp[1])
            clusterID = int(sp[2])
            _prob += x[id][clusterID] == 0


def cond_base_pty_maxmin(_prob):
    tmp_list = []
    for i in range(1,len(ptyss)+1):
        tmp_list.append(i)
    pty_results = db.session.execute(text(sql_pty2.format(tuple(tmp_list)))).fetchall()
    for z in pty_results:
        clusterID = z[0]
        ros = z[1]
        minPty = z[2]
        id = z[3]
        sourceQty = z[4]
        maxPty = z[5]
        _prob += (x[id][clusterID]) >= minPty
        _prob += (x[id][clusterID]) <= maxPty
        tmp_names.append('x_'+str(id)+'_'+str(clusterID))
    for i in var_names:
        if i not in tmp_names:
            sp = i.split("_")
            id = int(sp[1])
            clusterID = int(sp[2])
            _prob += x[id][clusterID] == 0

# write excel
def write_excel(_prob):
    tp = [[]]
    tm = []
    for v in _prob.variables():
        tm.append(int(v.varValue))
    for i in range(0,len(tm)+1,4):
        tp.append(tm[i:i+4])
    tp.pop(0)
    util.write_excel_file("D:\DOC\docker-k8s\conf\算法",tp)

### update db pty
def update_pty(_prob):
    update_pty = 'update z_tmp_assortment set qty = {} '\
                 'where id  = ( ' \
                 '    select rf.ID  from z_tmp_assortment rf ' \
                 'inner join z_tmp_article a on a.ArticleNo = rf.Article ' \
                 'where a.ID = {} ' \
                 'and rf.ClusterID = {} ' \
                 ')'
    for v in _prob.variables():
        sp = str(v.name).split("_")
        id = int(sp[1])
        clusterID = int(sp[2])
        val = int(v.varValue)
        #print(update_pty.format(val,id,clusterID))
        db.session.execute(text(update_pty.format(val,id,clusterID)))
        db.commit()
def batch_insert(_prob):
    sql_delete="delete from z_tmp_result"
    mappers = []
    for v in _prob.variables():
        sp = str(v.name).split("_")
        id = int(sp[1])
        clusterID = int(sp[2])
        val = int(v.varValue)
        mappers.append({"articleId":id,"clusterId":clusterID,"pty":val})
    db.session.execute(sql_delete)
    db.session.bulk_insert_mappings(result,mappers)
    db.session.commit()

def make_solve():

    start_time = time.time()
    _prob = build_prob()
    # 变量
    _class3 = get_class3()
    _articles = get_article_all()
    _clusters = get_cluster_all()

    rp = make_rpmap(_articles)
    otbmap = make_otbmap(_clusters)
    #
    build_lpvar(_articles,_clusters)
    #
    _resoleLp = resoleLp(_class3,_articles,_clusters,rp)
    _prob += _resoleLp

    c1_cond(_prob,rp)
    _class2 = get_class2()
    c2_cond(_prob,_class2,rp)
    c3_cond(_prob,_resoleLp,_class3)

    cond_total_pty(_prob)
    #cond_maxmin_pty(_prob,_clusters)
    cond_base_pty_maxmin(_prob)

    print("开始求解")
    #status = _prob.solve(pulp.PULP_CBC_CMD(msg=1, options=['DivingVectorlength on','DivingSome on']))
    solver = pulp.PULP_CBC_CMD(msg=True, warmStart=True,threads=8,timeLimit=120)
    #solver = CPLEX_CMD(msg=True, warmStart=True)
    #solver = GUROBI_CMD(msg=True, warmStart=True)
    #solver = CPLEX_PY(msg=True, warmStart=True)
    #solver = GUROBI(msg=True, warmStart=True)
    status = _prob.solve(solver)
    print("求解状态:", LpStatus[_prob.status])
    if LpStatusOptimal == _prob.status:
        print(f"目标函数的最大值z={value(_prob.objective)}，此时目标函数的决策变量为:",
              {v.name: v.varValue for v in _prob.variables()})
        print(f"lp cost time: ",(time.time()-start_time))
        batch_insert(_prob)
        #write_excel(_prob)
        #update_pty(_prob)
        return 0
    else:
        print("问题没有可行解")
        return 1
