# -- coding:utf8 --
import numpy as np

import numpy as np

arr = np.random.rand(3, 4)
print(arr)

a = np.array([1, 2, 3, 4])
print(a.shape)

b = a[np.newaxis, :]
print(b.shape)

###

import numpy as np
import pandas as pd

array_1 = np.array([[1, 2], [3, 4]])
data = pd.DataFrame(array_1 )

print(data)
with pd.ExcelWriter('test.xlsx') as writer:
    data.to_excel(writer, 'sheet_1', float_format='%.2f',header=False,index=False)
    writer._save()


###

import pandas as pd

# 读取Excel文件
file_path = 'D:\DOC\docker-k8s\conf\算法\OTB 碰平算法-验证-ok2.xlsx'
#我们指定了要读取的列为A到E，忽略前2行，往下读10行
df = pd.read_excel(file_path, sheet_name='Order-Cluster buy',header=None,index_col=None, usecols='H:Y', skiprows=11 ,nrows=7)
#- usecols: 要读取的列，可以指定列的名称或列的索引。
#- nrows：要读取的行数。
#- skiprows：要跳过的行数。
# 打印指定区域的数据
print(df.head(n=7))
print(df.values[0,0])
with pd.ExcelWriter('test1.xlsx') as writer:
    df.to_excel(writer, 'sheet_1', float_format='%.2f',header=False,index=False)
    writer._save()

print(df.values[4,4])
# rp * qty 再相加
print((df.values[:,4:5] * df.values[:,:1]).sum())


###

df = pd.DataFrame({
    "sex":["male","male","female","female","male"],
    "age":[22,24,25,26,24],
    "chinese":[100,120,110,100,90],
    "math":[90,np.nan,100,80,120],  # 存在空值
    "english":[90,130,90,80,100]})

print(df)
print(df.describe())
print(df.describe(include="all"))
print(df.count())
print(df.min())
print(df.max())
print(df.sum())