from pulp import LpVariable, LpMaximize, LpProblem, value, LpStatus, LpInteger, LpMinimize

# 第一个参数为这个问题取名字，第二个参数表示求目标函数的最大值（LpMaximize）
prob = LpProblem('min', sense=LpMaximize)
# name为变量名， lowBound为下边界，None为没边界, cat约束变量的类型LpInteger为整型]
x = [[0]] 
for i in range(1, 4, 1):
    tmp = [0]
    for j in range(1, 4, 1):
        tmp.append(LpVariable(name='x'+str(i)+str(j), lowBound=0, upBound=None))
    x.append(tmp)

print(x)
# # 约束条件
prob += 9*(x[1][1] + x[1][2] + x[1][3]) + 7*(x[2][1] + x[2][2] + x[2][3]) + 8*(x[3][1] + x[3][2] + x[3][3]) - 5.5*(x[1][1] + x[2][1] + x[3][1]) - 4*(x[1][2] + x[2][2] + x[3][2]) - 5*(x[1][3] + x[2][3] + x[3][3])

prob += x[1][1] >= 0.5*(x[1][1] + x[1][2] + x[1][3])
prob += x[1][2] <= 0.2*(x[1][1] + x[1][2] + x[1][3])
prob += x[2][1] >= 0.3*(x[2][1] + x[2][2] + x[2][3])
prob += x[2][3] <= 0.3*(x[2][1] + x[2][2] + x[2][3])
prob += x[3][3] >= 0.5*(x[3][1] + x[3][2] + x[3][3])
prob += x[1][1] + x[1][2] + x[1][3] <= 5
prob += x[2][1] + x[2][2] + x[2][3] <= 18
prob += x[3][1] + x[3][2] + x[3][3] <= 10
prob += x[1][1] + x[1][2] + x[1][3] + x[2][1] + x[2][2] + x[2][3] + x[3][1] + x[3][2] + x[3][3] <= 30

status = prob.solve()
print("求解状态:", LpStatus[prob.status])
print(f"目标函数的最大值z={value(prob.objective)}，此时目标函数的决策变量为:",
      {v.name: v.varValue for v in prob.variables()})

