# coding:utf-8
from pulp import LpVariable, LpMaximize, LpProblem, value, LpStatus, LpInteger, LpMinimize

# 第一个参数为这个问题取名字，第二个参数表示求目标函数的最小值（LpMinimize）
prob = LpProblem('min', sense=LpMinimize)
# name为变量名， lowBound为下边界，None为没边界
x = [[0]]
for i in range(1,5,1):
  tmp = [0]
  for j in range(1,5-i+1,1):
    tmp.append(LpVariable(name='x'+str(i)+str(j),lowBound=0,upBound=None,cat=LpInteger))
  x.append(tmp)

# 约束条件
prob += 2800*(x[1][1] + x[2][1] + x[3][1] + x[4][1]) + 4500*(x[1][2] + x[2][2] + x[3][2]) + 6000*(x[1][3] + x[2][3]) + 7300 * x[1][4]
prob += x[1][1] + x[1][2] + x[1][3] + x[1][4] >= 15
prob += x[1][2] + x[1][3] + x[1][4] + x[2][1] + x[2][2] + x[2][3] >= 10
prob += x[1][3] + x[1][4] + x[2][2] + x[2][3] + x[3][1] + x[3][2] >= 20
prob += x[1][4] + x[2][3] + x[3][2] + x[4][1] >= 12

status = prob.solve()
print("求解状态:", LpStatus[prob.status])
print(f"目标函数的最小值z={value(prob.objective)}，此时目标函数的决策变量为:", {v.name: v.varValue for v in prob.variables()})

