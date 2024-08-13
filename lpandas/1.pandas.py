import numpy as np
import pandas as pd
from PIL._imaging import display
import matplotlib.pyplot as plt


# 行列数据
def test1():
    df = pd.DataFrame(data = np.random.randint(0, 100, size = (10, 3)),
                      index = list('ABCDEFHIJK'),
                      columns = ['Python', 'Tensorflow', 'Keras'])
    print(df)
    # 转置
    print(df.T)

# 1.2 多层索引 列
def test2():
    df2 = pd.DataFrame(data = np.random.randint(0, 100, size = (20, 3)),
                       index = pd.MultiIndex.from_product([list('ABCDEFHIJK'),
                                                           ['期中', '期末']]),#多层索引
                       columns = ['Python', 'Tensorflow', 'Keras'])
    print(df2)
    # 行索引变列索引,结构改变
    # 默认情况下,最里层调整
    print(df2.unstack())
    #可以看出来，只是把行索引最里层的期中期末 移到了列索引的位置，我们也可以把行索引外层的 ABCDEFHIJK 移动至列索引的位置：
    print(df2.unstack(level = 0))

    #sum() 求和运算：
    print(df2.sum())
    print(df2.sum(axis = 1))

    # 期中，期末消失
    # 计算的是每个人，期中期末的总分数
    #print(df2.sum(level = 0))

    # 同学消失
    # 计算的是所有同学期中期末平均分
    #print(df2.mean(level = 1))

# 多层索引 行
def test3():
    df3 = pd.DataFrame(data = np.random.randint(0, 100, size = (10, 6)),
                       index = list('ABCDEFHIJK'),
                       columns = pd.MultiIndex.from_product([['Python', 'Math', 'English'],
                                                             ['期中', '期末']]))
    print(df3)
    # 列索引变行索引,结构改变
    # 默认情况下,最里层调整
    #print(df3.stack())
    #同样，我们通过调整参数可以实现使得列索引的最外层变成行索引：
    #print(df3.stack(level = 0))

    # df3是多层列索引,可以直接使用[],根据层级关系取数据
    # 取出 A 同学的 Python 科目的期中成绩
    print(df3['Python', '期中']['A'])

def convert(x):
    if x > 80:
        return np.NaN
    else:
        return x
def test4():
    import numpy as np
    import pandas as pd

    df = pd.DataFrame(data = np.random.randint(0, 100,size = (20, 3)),
                      index = list('ABCDEFHIJKLMNOPQRSTU'),
                      columns = ['Python', 'Tensorflow', 'Keras'])
    print(df)
    print("#把一部分数据设置为空：")
    df['Python'] = df['Python'].map(convert)
    df['Tensorflow'] = df['Tensorflow'].apply(convert)
    df['Keras'] = df['Keras'].transform(convert)
    print(df)

    print("# 统计非空数据的个数")
    print(df.count())

    print("# 中位数")
    print(df.median())

    print("# 返回位于数据 50% 位置的数")
    print(df.quantile(q = 0.5))
    print("# 返回位于数据 80% 位置的数")
    print(df.quantile(q = 0.8))
    print(df.quantile(q = [0.5, 0.8]))

    print("# 计算最小值位置")
    print(df['Python'].argmin()) # 计算最小值位置
    print("# 最大值位置")
    print(df['Keras'].argmax())

    print(" # 最大值索引标签")
    print(df.idxmax())
    print("# 最小值索引标签")
    print(df.idxmin())

    print("# 统计元素出现次数")
    print(df['Python'].value_counts())

    print("# 去重")
    print(df['Python'].unique())

    df = pd.DataFrame(data = np.random.randint(0, 5,size = (20, 3)),
                      index = list('ABCDEFHIJKLMNOPQRSTU'),
                      columns = ['Python', 'Tensorflow', 'Keras'])
    print(df)
    print("# 累加")
    # 累加
    print(df.cumsum())
    print("# 累乘")
    # 累乘
    print(df.cumprod())


    print("# 计算标准差")
    print(df.std())
    print("# 计算方差")
    print(df.var())

    # 计算差分
    print("# 差分:和上一行相减")
    print(df.diff())
    print("# 计算百分比变化")
    print(df.pct_change())



def test_sort1():
    import numpy as np
    import pandas as pd
    df = pd.DataFrame(data = np.random.randint(0, 30, size = (30, 3)),
                      index = list('qwertyuioijhgfcasdcvbnerfghjcf'),
                      columns = ['Python', 'Keras', 'Pytorch'])
    print(df)

    print("# 按列名排序，升序")
    print(df.sort_index(axis = 0, ascending = True))
    print("# 按行名排序，降序")
    print(df.sort_index(axis = 1, ascending = False))

    # 按Python属性值排序
    print("# 按Python属性值排序")
    print(df.sort_values(by = ['Python']))
    # 先按Python，再按Keras排序
    print("# 先按Python，再按Keras排序")
    print(df.sort_values(by = ['Python', 'Keras']))

    # 根据属性Keras排序,返回最大3个数据
    print("# 根据属性Keras排序,返回最大3个数据")
    print(df.nlargest(3, columns = 'Keras'))
    # 根据属性Python排序，返回最小5个数据
    print("# 根据属性Python排序，返回最小5个数据")
    print(df.nsmallest(5, columns = 'Python'))

# 分箱
#分箱操作就是将连续数据转换为分类对应物的过程。比如将连续的身高数据划分为：矮中高。
#分箱操作分为等距分箱和等频分箱。
#分箱操作也叫面元划分或者离散化。
def test_group():
    import numpy as np
    import pandas as pd

    df = pd.DataFrame(data = np.random.randint(0, 150, size = (100, 3)),
                      columns = ['Python', 'Tensorflow', 'Keras'])
    print(df)

    print("等宽分箱")
    #等宽分箱在实际操作中意义不大，因为我们一般都会给一个特定的分类标准，比如高于 60 是及格，等分在生活中应用并不多
    # bins = 3 表示把 Python 成绩划分成三份
    print(pd.cut(df.Python, bins = 3))

    print("自定义等宽分箱")
    #自行定义宽度进行分箱操作，在下述带啊中，不及格是 [ 0 , 60 ) [0,60) [0,60)，中等是 [ 60 , 90 ) [60, 90) [60,90)，良好是 [ 90 , 120 ) [90, 120) [90,120)，优秀是 [ 120 , 150 ) [120, 150) [120,150) 均为左闭右开，这个是由 right = False 设定的
    print(pd.cut(df.Keras,   #分箱数据
           bins = [0, 60, 90, 120, 150],  # 分箱断点
           right = False,      # 左闭右开
           labels=['不及格', '中等', '良好', '优秀']))# 分箱后分类

    print("等频分箱是按照大家的普遍情况进行等分的操作")
    print(pd.qcut(df.Python,q = 4,                 # 4等分
            labels=['差', '中', '良', '优'])) # 分箱后分类


def count(x):
    return len(x)

def test_group1():
    import numpy as np
    import pandas as pd
    # 准备数据
    df = pd.DataFrame(data = {'sex':np.random.randint(0, 2, size = 300), # 0男，1女
                              'class':np.random.randint(1, 9, size = 300),# 1~8八个班
                              'Python':np.random.randint(0, 151, size = 300),# Python成绩
                              'Keras':np.random.randint(0, 151, size =300),# Keras成绩
                              'Tensorflow':np.random.randint(0, 151, size = 300),
                              'Java':np.random.randint(0, 151,size = 300),
                              'C++':np.random.randint(0, 151, size = 300)})
    df['sex'] = df['sex'].map({0:'男', 1:'女'})             # 将0，1映射成男女
    print(df)

    print("根据性别分组并求出平均值，并把平均值保留一位小数：")
    print(df.groupby(by = 'sex').mean().round(1))

    print("分组统计男女的数量：")
    print(df.groupby(by = 'sex').size())

    print("根据性别和班级两个属性进行分组：")
    print(df.groupby(by = ['sex', 'class']).size())

    print("获取每个班，男生女生Python，Java 最高分")
    print(df.groupby(by = ['sex', 'class'])[['Python', 'Java']].max())
    print(df.groupby(by = ['class', 'sex'])[['Python', 'Java']].max())
    print(df.groupby(by = ['class', 'sex'])[['Python', 'Java']].max().unstack())

    print("apply 返回的是汇总后的情况，对于每一个分组大类都只返回一个结果")
    print(df.groupby(by = ['class','sex'])[['Python','Keras']].apply(np.mean).round(1))

    print("transform 是把所有的元素全部返回：")
    print(df.groupby(by = ['class','sex'])[['Python','Keras']].transform(np.mean).round(1))

    print("# 按照班级和性别进行划分,统计 Tensorflow 和 Keras 这两门学科的最大值,最小值,个数")
    print(df.groupby(by = ['class','sex'])[['Tensorflow','Keras']].agg([np.max, np.min, pd.Series.count]))

    # 分组后不同属性应用多种不同统计汇总
    # 对 Python 计算最大值和最小值
    # 对 Keras 计数和计算中位数
    print("分组后不同属性应用多种不同统计汇总")
    print(df.groupby(by = ['class','sex'])[['Python','Keras']].agg(
        {'Python':[('最大值',np.max),('最小值',np.min)],
         'Keras':[('计数',pd.Series.count),('中位数',np.median)]}))

    print(df.pivot_table(values=['Python', 'Keras', 'Tensorflow'],# 要透视分组的值
                   index=['class', 'sex'], # 分组透视指标,相当于之前的 by
                   aggfunc={'Python':[('最大值', np.max)], # 聚合运算
                            'Keras':[('最小值', np.min),('中位数', np.median)],
                            'Tensorflow':[('最小值', np.min),('平均值', np.mean),('计数', count)]}))
test_group1()


def test_vis1():
    df1 = pd.DataFrame(data = np.random.randn(1000, 4),
                       index = pd.date_range(start = '23/1/2022', periods = 1000),
                       columns=list('ABCD'))
    print(df1)
    df1.cumsum().plot()
    plt.show()

def test_vis2():
    df2 = pd.DataFrame(data = np.random.rand(10, 4),
                       columns = list('ABCD'))
    print(df2)
    (df2.plot.bar(stacked = True)) # stacked 堆叠
    (df2.plot.bar(stacked = False))# stacked 不堆叠
    plt.show()


def test_vis3():
    # 饼图用来表示百分比,百分比是自动计算的,颜色可以更换
    df3 = pd.DataFrame(data = np.random.rand(4, 2),
                       index = list('ABCD'),
                       columns = ['One', 'Two'])
    # subplots 表示两个图,多个图
    # figsize 表示尺寸
    df3.plot.pie(subplots = True,figsize = (8, 8))
    plt.show()

def test_vis4():
    # 更换颜色
    df3 = pd.DataFrame(data = np.random.rand(4, 2),
                       index = list('ABCD'),
                       columns = ['One', 'Two'])
    df3.plot.pie(subplots = True,figsize = (8, 8),
                 colors = np.random.random(size = (4, 3)))
    plt.show()

def test_vis5():
    #散点图
    # 横纵坐标,表示两个属性之间的关系
    df4 = pd.DataFrame(np.random.randint(0, 50, size = (50, 4)), columns = list('ABCD'))
    (df4.plot.scatter(x = 'A', y = 'B')) # A和B关系绘制

    df4['F'] = df4['C'].map(lambda x : x + np.random.randint(-5, 5, size = 1)[0])
    df4.plot.scatter(x = 'C', y = 'F')
    plt.show()

def test_vis6():
    df5 = pd.DataFrame(data = np.random.rand(10, 4),
                       columns = list('ABCD'))
    df5.plot.area(stacked = True)  # stacked 堆叠
    df5.plot.area(stacked = False) # stacked 不堆叠
    plt.show()

def test_plot():
    import numpy as np
    x=np.linspace(1,50,100)     #定义x数据范围
    y=3*x+1
    plt.figure()                #定义一个图像窗口
    plt.plot(x,y)               #plot()画出曲线
    plt.show()                  #显示图像

    '''
    plt.figure()为单独图像窗口，语法如下：
    figure(num=None, figsize=None, dpi=None, facecolor=None, edgecolor=None, ……)
    1.num：可选参数。窗口的属性id,即该窗口的身份标识。如果不提供该参数，则创建窗口的时候该参数会自增，如果提供的话则该窗口会以该num为Id存在。
    2.figsize:可选参数。整数元组，默认是无。提供整数元组则会以该元组为长宽。
    3.dpi：可选参数，整数。表示该窗口的分辨率。
    4.facecolor：可选参数，表示窗口的背景颜色，如果没有提供则默认为figure.facecolor。颜色的设置是通过RGB，范围是'#000000'~'#FFFFFF'。
    5.edgecolor:可选参数，表示窗口的边框颜色
    '''
