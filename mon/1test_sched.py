
import schedule
import time
def job(name):
    print("I'm working...",name)

name = "张三"
schedule.every(1).seconds.do(job,name)
schedule.every(10).minutes.do(job,name)
schedule.every().hour.do(job,name)
schedule.every().day.at("10:30").do(job,name)
schedule.every(5).to(10).minutes.do(job,name)
schedule.every().monday.do(job,name)
schedule.every().wednesday.at("13:15").do(job,name)
schedule.every().minute.at(":17").do(job,name)
while True:
   schedule.run_pending()
   #time.sleep(1)



import schedule
from datetime import datetime
def task():
    now = datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    print(ts)
def test_task2():
    now = datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    print(ts + '666!')
def func():
    # 清空任务
    schedule.clear()
    # 创建一个按3秒间隔执行任务
    schedule.every(3).seconds.do(task)
    # 创建一个按2秒间隔执行任务
    schedule.every(2).seconds.do(task2)
    while True:
        schedule.run_pending()

task()