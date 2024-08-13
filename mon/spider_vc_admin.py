import datetime
import json
import logging
import time

import requests
import schedule

import dmPython
from playwright.sync_api import Playwright, sync_playwright, expect
from urllib3 import Timeout

wiew_size = {"width": 2000, "height": 2240}
result_api = 0
result_page = 0

# 创建一个logger
log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('vc')
consol_handler = logging.StreamHandler()
logger.addHandler(consol_handler)
logger.setLevel(logging.INFO)
# 创建一个输出到文件的handler
file_handler = logging.FileHandler('vc.log',encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(log_format))
consol_handler.setFormatter(logging.Formatter(log_format))
# 将handler添加到logger
logger.addHandler(file_handler)
#logger = logs.get_logger("simple")

pic_dir = "/data/monitor/pagepic/"
#pic_dir = "/java_web/pagecheck/pagepic/"
pic_req_url="/monitor/pagepic/"
save_db_pic = []
token=""

#upload_url="https://spgxpt.shmh.gov.cn/monitor/common/upload"
upload_url="http://127.0.0.1:8000/monitor/common/upload"
class sysPageCruiseEntity():
    def __init__(self,id=None,result=None,pics='',create_time=None):
        self.id = id
        self.result = result
        self.pics = pics
        self.create_time = create_time

def connect() -> object:
    #conn = dmPython.connect(user='MONITOR', password='MONITOR@123.topw', server='32.2.6.214:5236',  port=5236)
    conn = dmPython.connect(user='MONITOR', password='MONITOR@123.net', server='101.227.55.53:15236',  port=15236)
    return conn

def insert_result(entity):
    conn = connect()
    cursor = conn.cursor()
    #"values ('"+link.id+"','"+link.pUrl+"','"+link.url+"','"+link.picPath+"','"+str(datetime.now())+"','"+str(link.batchNo)+"')"
    sql = "insert into sys_page_cruise(id, result, pics) "\
          "values ('{id}','{result}','{pics}')" \
        .format(id=entity.id,result=entity.result,pics=entity.pics)
    logger.info(f"sql: {sql}")
    cursor.execute(sql)
    conn.close()


def check_api(context,token):
    url = "https://spgxpt.shmh.gov.cn/monitor/cameras/resource/search"
    data = {
        "pageSize": 999999,
        "town": "七宝镇"
    }
    headers={"Content-Type":"application/json","token":token}
    response = context.request.post(url=url,data=data,headers=headers)
    resp_data = json.loads(response.body())
    code = resp_data['code']
    msg = resp_data['msg']
    data = resp_data['data']
    logger.info(f"request url {url} ,result {code},{msg}")
    if 200 == code and len(data) > 0:
        global result_api
        result_api += 1
        logger.info(f"request result data {len(data)}")

def save_screenshot(page,file_name,file_subfix=".png"):
    ofile = time.strftime('%Y%m%d%H%M%S') + file_name + file_subfix
    save_db_pic.append(pic_req_url + ofile)
    page.screenshot(path=pic_dir + ofile, full_page=True)

def upload_file(file_path):
    result =""
    files = {'file': open(file_path, 'rb')}
    headers={"token":token}
    response = requests.post(url=upload_url,files=files,headers=headers)
    resp_data = response.json()
    code = resp_data['code']
    msg = resp_data['msg']
    data = resp_data['data']
    logger.info(f"upload_file ,result {code},{msg},{data}")
    if 200 == code and len(data) > 0:
        result = data['fileName']
    return result

def run_admin(playwright: Playwright,url:str) -> None:
    browser = playwright.chromium.launch(headless=False,slow_mo=3000)
    context = browser.new_context(screen=wiew_size, viewport=wiew_size)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    page.goto(url)
    try:
        #session_storage
        session_storage = page.evaluate("() => sessionStorage")
        #print(session_storage['token'])
        global token
        token = session_storage['token']
        check_api(context,session_storage['token'])

        page.get_by_text("视频资源").click(timeout=3000)
        save_screenshot(page,"1")

        page.locator(".tag-list").locator("text=七宝镇").click()
        #page.get_by_role("button", name="").click()
        page.locator(".search-content").locator("button").click()
        save_screenshot(page,"2")

        page.get_by_text("列表展示").click()
        time.sleep(5)
        page_size = page.locator(".el-pagination__total").text_content(timeout=3000)
        save_screenshot(page,"3")

        logger.info(f"page url {url} , page_size {page_size}")
        page.get_by_text("地图展示").click()
        page.get_by_text("点位总数").click()
    except Timeout as e:
        logger.error(f"run_admin {e}")
    except Exception as e:
        global result_page
        result_page += 1
        logger.error(f"run_admin {e}")
    print("----->")

    # ---------------------
    context.tracing.stop(path = "trace.zip")
    context.close()
    browser.close()


def run_user(playwright: Playwright,url:str) -> None:
    browser = playwright.chromium.launch(headless=False,slow_mo=3000)
    context = browser.new_context(screen=wiew_size, viewport=wiew_size)
    page = context.new_page()
    page.goto(url , wait_until='networkidle') # load networkidle
    try:
        #session_storage
        session_storage = page.evaluate("() => sessionStorage")
        #print(session_storage['token'])
        check_api(context,session_storage['token'])


        print(page.get_by_text("视频资源").inner_text())
        page.get_by_text("视频资源").click()
        save_screenshot(page,"1")

        page.locator(".tag-list").locator("text=七宝镇").click()
        page.locator(".search-content").locator("button").click()
        save_screenshot(page,"2")

        page.get_by_text("列表展示").click()
        time.sleep(5)
        page_size = page.locator(".el-pagination__total").text_content()
        save_screenshot(page,"3")

        logger.info(f"page url {url} , page_size {page_size}")
    except Exception as e:
        global result_page
        result_page += 1
        logger.error(f"run_admin {e}")

    print("----->")
    # ---------------------
    context.close()
    browser.close()

def start():
    logger.info("check start")
    start = time.time()
    with sync_playwright() as playwright:
        urls = ['https://spgxpt.shmh.gov.cn/vcweb/#/login?ticket=p11cq9hr5r2z6hmujl'
                ,'https://spgxpt.shmh.gov.cn/vcweb/#/login?ticket=com_p11cq9hr5r2z6hmujl']
        #run_admin(playwright,urls[0])
        run_user(playwright,urls[1])

    entity = sysPageCruiseEntity(id=time.strftime('%Y%m%d%H%M%S',time.localtime()))
    print(str(result_api) +" "+str(result_page))

    logger.info(f"pics: {save_db_pic}")
    #entity.pics = ",".join(save_db_pic)
    save_db_pic1 = []
    for f in save_db_pic:
        #s =  upload_file("/data"+f)

        save_db_pic1.append(f)
    entity.pics = ",".join(save_db_pic1)
    logger.info(f"entity.pics: {entity.pics}")
    if result_api == 1 and result_page == 0:
        entity.result = '0'
    else:
        entity.result = '1'
    insert_result(entity)
    logger.info(f"check end take {time.time()-start}")


#def test_insert_result():
#    print("1")
#    insert_result(sysPageCruiseEntity())
#    print("1")


start()
#def sched():
#    # 清空任务
#    schedule.clear()
#    # 创建一个按3秒间隔执行任务
#    schedule.every(1).minutes.do(start)
#    while True:
#        schedule.run_pending()
#
#sched()