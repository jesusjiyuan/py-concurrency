import base64
import json
import math
import time
import uuid
import gc
import sys
sys.path.append("/java_web/cloudcs2mon/pyspace/")
import os
os.chdir(os.path.dirname(__file__))
print("1",os.path.dirname(__file__))

import logs
import confhelper
import requests
from playwright.sync_api import Playwright, sync_playwright

import dbmapper
from entity import LinkMonResult, MonLinkBatch

logger = logs.get_logger('jd')

user_data_dir = f"D:\\tmp\\playwright\\userdata"
print(user_data_dir)
wiew_size = {"width": 1080, "height": 2240}
linkpath_prefix = confhelper.confdata().get("linkpath_prefix")+"jd/"
work_dir = confhelper.confdata().get("work_dir")
urls = []
monLinks = []
page_size = 60
picList = []

logger.info("sys.argv: {}".format(sys.argv))
batchNo = sys.argv[1]
#batchNo = time.strftime('%Y%m%d%H%M%S',time.localtime())
browser=""
env = {
    "network.http.use-cache": False,
    "browser.cache.memory.enable": False,
    "browser.cache.disk.enable": False,
    "browser.sessionhistory.max_total_viewers": 3,
    "network.dns.disableIPv6": True,
    "Content.notify.interval": 750000,
    "content.notify.backoffcount": 3,

}
args = ["--browser.cache.memory.enable=False","--browser.cache.disk.enable=False","--browser.sessionhistory.max_total_viewers=3","--network.http.use-cache=False"]
def run(playwright: Playwright) -> None:
    #browser = playwright.firefox.launch(headless=False,slow_mo=2000)
#    browser = playwright.firefox.launch_persistent_context(user_data_dir=user_data_dir,headless=False,slow_mo=2000,args=args,env=env)
    #context = browser.new_context(viewport=wiew_size,storage_state="jd_state.json")
#    context = browser.new_context(screen=wiew_size,viewport=wiew_size,storage_state="jd_state.json")
    # Open new page
#    page = context.new_page()
    #page.set_viewport_size(wiew_size)
    # Go to https://pro.jd.com/mall/active/36yPbWm4JqFrmTgABydz6GkWNkca/index.html
    #page.goto("https://mall.jd.com/index-935158.html?from=pc")
    #page.goto("https://mall.jd.com/index-11388268.html?from=pc")
    i = 0
    for link in monLinks:
        browser = playwright.firefox.launch_persistent_context(user_data_dir=user_data_dir,headless=False,slow_mo=2000,args=args,env=env)
        page = browser.new_page()
        url = link.url
        linkId = link.id
        logger.info("开始遍历 url:{} id:{}".format(url,linkId))
        page.goto(url)
        if page.locator("text=搜本店").count() == 0:
            logger.error("无效店铺: {}".format(url))
            page.close()
            browser.close()
            continue
        if page.locator(".J_giftClose.d-close").count()>0:
            logger.info("出现领券框")
            page.locator(".J_giftClose.d-close").click()
        page.locator("text=搜本店").click()
        #with page.expect_navigation():
        pageTotal = page.locator(".jSearchListArea").locator(".jTotal>em").text_content()
        pageNum = math.ceil(int(pageTotal)/page_size)
        logger.info("url {} pageTotal {} pagenum: {} ".format(url,pageTotal,pageNum))
#        dbmapper.MonLinkBatchMapper.update(MonLinkBatch(goodSum=pageTotal,batchNo=batchNo,linkId=linkId))
        for p_num in range(1,pageNum+1):
            #page.reload();
            if(p_num > 1):
                page.locator("text=下一页").click()
            #print("第"+str(p_num)+"页 url size: "+str(len(pageLinks)))
            pageLinks = page.locator(".jSearchListArea").locator(".jSubObject").all()
            if len(pageLinks) > 0 :
                view_page(p_num,i,page,pageLinks,picList,url,linkId)
        # with open(url_txt_end, "a") as file:
        #     file.write(url)
        #     file.write("\n")
        logger.info("结束遍历 {}".format(url))
        # Close page
        page.workers.clear()
        page.close()
    # ---------------------
    #    context.close()
        browser.background_pages.clear()
        browser.close()

def view_page(p_num:int,i:int,page,pageLinks,picList,linkUrl,linkId):
    for p in pageLinks:
        i = i + 1
        j = 0
        try:
            page.wait_for_load_state('networkidle')
            with page.expect_popup(timeout=60000) as popup_info:
                p.first.click()
                logger.info("enabled: {}, visible: {}".format(p.is_enabled(),p.is_visible()))
            page1 = popup_info.value
            #page1.wait_for_load_state('networkidle')
            #subpageLinks = page1.locator(".jSubObject").all()
            #print("suburl size: "+str(len(subpageLinks)))
            #if len(subpageLinks) > 0 :
            #    view_page(i,page1,subpageLinks,picList)
            while page1.locator("text=验证").count() >0:
                logger.info("出现图形验证等待5秒")
                #time.sleep(5)
                page1.wait_for_timeout(5000)
            if page1.locator("text=商品介绍").count() > 0 :
                if page1.locator("text=验证").count() == 0:
                    pic = linkpath_prefix +str(p_num)+"-"+str(i)+"-"+str(j)+page1.title().replace("*","").replace("/","#").replace(" ","")[0:30]+".png"
                    #page1.screenshot(path=pic,full_page=True)
                    #picList.append(pic)
                    #linkMonResult = LinkMonResult(str(uuid.uuid4().int),linkUrl,page1.url,"/profile"+pic.replace(work_dir,""),batchNo,linkId=linkId)
                    #count = dbmapper.LinkMonResultMapper.count(linkMonResult)
                    #if int(count) > 0:
                    #    linkMonResult.status=0
                    #    linkMonResult.ocrStr=""
                    #    dbmapper.LinkMonResultMapper.update(linkMonResult)
                    #else:
                    #    dbmapper.LinkMonResultMapper.insert(linkMonResult)
                else:
                    logger.info("出现图形验证进入60秒睡眠")
                    #time.sleep(60)
                    page1.wait_for_timeout(60000)
                #time.sleep(2)

                #page1.locator("text=规格与包装").click()
                #j = j+1
                #pic1 = linkpath_prefix +str(i)+"-"+str(j)+page1.title().replace("/","#")[0:40]+".png"
                #page1.screenshot(path=pic1)
                #picList.append(pic1)
                #time.sleep(2)
                page1.close()
        except Exception as e:
            logger.info("exception {} url:{}".format(i,page1.url))
            logger.exception("exception traceback is:{}".format(e))
            page1.close()
            #pageList.append(popup_info.value)
        #finally:
        #    page1.close()

def ocr(png_file):
    encoded = base64.b64encode(open(png_file, 'rb').read()).decode("utf-8")
    l = [encoded]
    map = {"images": l}
    #print(json.dumps(map))
    url = "https://mhqym.topwin.net/ppocr/predict/ocr_system"
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
    result = requests.post(url,data=json.dumps(map),headers= header)
    #print(result.json())
    str = ""
    for i in result.json().get("results")[0]:
        str = str + i.get("text")
    print(str)
    return str


os.chdir(os.path.dirname(__file__))
# 通过db加载url
monTask = dbmapper.MonTaskMapper.get_by_batchno(batchNo=batchNo)
if monTask is not None and monTask.typea == '0':
    monLink = dbmapper.MonLinkMapper.list_by_ids(monTask.targetIds.split(","),'jd')
    if len(monLink) > 0:
        #urls = [link.url for link in monLink]
        monLinks = monLink

# 通过文件加载url
#url_txt = "txt/jd_url.txt"
#url_txt_end = "txt/jd_url_end.txt"
#with open(url_txt, 'r') as f:
#    line = f.readline()
#    urls.append(line.replace("\n",""))
#    while line:
#        line = f.readline().replace("\n","")
#        urls.append(line)
logger.info("待监测的url %s",[(link.id,link.url) for link in monLinks])
if len(monLinks) > 0:
    with sync_playwright() as playwright:
        run(playwright)
