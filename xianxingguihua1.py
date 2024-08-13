# coding:utf-8
from pulp import LpVariable, LpMaximize, LpProblem, value, LpStatus,LpInteger

# 第一个参数为这个问题取名字，第二个参数表示求目标函数的最大值（LpMaximize）
prob = LpProblem('max_z', sense=LpMaximize)
# name为变量名， lowBound为下边界，None为没边界
x1 = LpVariable(name='x1', lowBound=0, upBound=None,cat=LpInteger)
x2 = LpVariable('x2', 0, None)
x3 = LpVariable('x3', 0, None)

# 设置目标函数
prob += 2*x1+3*x2-5*x3
# 约束条件
prob += x1+x2+x3 == 7
prob += 2*x1-5*x2+x3 >= 10
prob += x1+3*x2+x3 <= 12

status = prob.solve()
print("求解状态:", LpStatus[prob.status])
print(f"目标函数的最大值z={value(prob.objective)}，此时目标函数的决策变量为:", {v.name: v.varValue for v in prob.variables()})

