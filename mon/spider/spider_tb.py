import math
import time

import os
os.chdir(os.path.dirname(__file__))

from asyncio import InvalidStateError
from playwright.sync_api import Playwright, sync_playwright

import logs
import confhelper
#logging.config.fileConfig('logging.ini')
#logger = logging.getLogger('tb')
logger = logs.get_logger('tb')

wiew_size = {"width": 1080, "height": 2240}
linkpath_prefix = confhelper.confdata().get("linkpath_prefix")+"tb/"
work_dir = confhelper.confdata().get("work_dir")
path_prefix = "d:/tmp/pic/taobao/"
page_size = 24
picList = []

def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False,slow_mo=2000)

    #context = browser.new_context(viewport=wiew_size,storage_state="tb_state.json")
    #context = browser.new_context(storage_state="tb_state.json")
    context = browser.new_context(screen=wiew_size, viewport=wiew_size,storage_state="tb_state.json")

    # Open new page
    page = context.new_page()

    # Go to https://shop64356781.taobao.com/
    #page.goto("https://shop64356781.taobao.com/")
    #page.mouse.wheel(0,10000)
    #page.goto("https://lz888888.taobao.com/category.htm?spm=a1z10.1-c-s.w5001-21305331213.10.27d24163Si2GnA&search=y&v=1&scene=taobao_shop")

    i = 0
    for url in urls:
        # 排除已爬取过的url
        if url in urls_end:
            continue
        logger.info("开始遍历 {}".format(url))
        page.goto(url)

        if page.locator(".sufei-dialog-close").count()> 0:
            page.locator(".sufei-dialog-close").click()

        #
        if page.locator(".J_SearchForm").locator("text=搜本店").count() > 0 :
            page.locator(".J_SearchForm").locator("text=搜本店").click()
        elif page.locator(".all-cats.popup-container").locator("text=所有分类").count() > 0 :
            page.locator(".all-cats.popup-container").locator("text=所有分类").click()
        elif page.locator("text=全部宝贝").count() > 0 :
            page.locator("text=全部宝贝").click()

        while page.locator(".captcha-tips").count() >0:
            logger.info("全部宝贝 出现图形验证等待5秒")
            #send_email("spidetb","出现图形验证等待5秒")
            #time.sleep(5)
            page.wait_for_timeout(5000)
        if page.locator(".sufei-dialog-close").count()> 0:
            page.locator(".sufei-dialog-close").click()
        #with page.expect_navigation():

        pageTotal = page.locator(".pagination.pagination-mini").locator(".page-info").text_content()
        pageNum = int(pageTotal.split("/")[1])
        logger.info("url {} pageTotal {} pagenum: {} ".format(url,pageTotal,pageNum))

        for p_num in range(1,pageNum+1):
            page.reload()
            logger.info("第{}页".format(p_num))
            if(p_num > 1):
                try:
                    page.locator(".pagination.pagination-mini").locator("text=下一页").click()
                except Exception as e:
                    logger.exception("next page traceback is:{}".format(e))
                    continue
            #print("第"+str(p_num)+"页 url size: "+str(len(pageLinks)))
            pageLinks = page.locator(".item3line1").locator(".item").all()
            if len(pageLinks) > 0 :
                view_page(p_num,i,page,pageLinks,picList)
        with open(url_txt_end, "a") as file:
            file.write(url)
            file.write("\n")
        logger.info("结束遍历 {}".format(url))
    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


def view_page(p_num:int,i:int,page,pageLinks,picList):
    for p in pageLinks:
        i = i + 1
        j = 0
        try:
            #page.wait_for_load_state('networkidle')
            with page.expect_popup(timeout=60000) as popup_info:
                p.first.click()
                logger.info("enabled: {}, visible: {}, url: {}".format(p.is_enabled(),p.is_visible(),""))
            page1 = popup_info.value
            #page1.mouse.wheel(0,10000)
            while page1.locator("text=Sorry").count() >0:
                logger.info("出现图形验证等待5秒")
                #time.sleep(5)
                #send_email("spidetb","出现图形验证等待5秒")
                page1.wait_for_timeout(5000)


            if page1.locator("text=宝贝详情").count() > 0 :

                if page1.locator("text=Sorry").count() == 0:
                    pic = path_prefix +str(p_num)+"-"+str(i)+"-"+str(j)+page1.title().replace("*","").replace("/","#").replace(" ","")[0:30]+".png"
                    #time.sleep(2)
                    page1.wait_for_timeout(2000)
                    if page1.locator(".baxia-dialog-close").count()> 0:
                        page1.locator(".baxia-dialog-close").click()
                    page1.screenshot(path=pic,full_page=True)
                    picList.append(pic)
                else:
                    logger.info("出现图形验证进入60秒睡眠")
                    #time.sleep(60)
                    page1.wait_for_timeout(6000)
            else:
                while page1.locator("text=宝贝详情").count() == 0:
                    logger.info("出现图形验证小弹框等待5秒")
                    #time.sleep(5)
                    #send_email("spidetb","出现图形验证等待5秒")
                    page1.wait_for_timeout(5000)

            page1.close()
        except UnboundLocalError as e:
            logger.exception("UnboundLocalError traceback is:{}".format(e))
        except InvalidStateError as e:
            logger.exception("InvalidStateError traceback is:{}".format(e))
        except TimeoutError as e:
            logger.exception("TimeoutError traceback is:{}".format(e))
        except Exception as e:
            logger.info("exception {} url:{}".format(i,page1.url))
            logger.exception("exception traceback is:{}".format(e))
            page1.close()

url_txt = "txt/tb_url.txt"
url_txt_end = "txt/tb_url_end.txt"
def read_urls(file_path:str):
    urls = []
    with open(file_path, 'r') as f:
        line = f.readline()
        urls.append(line.replace("\n",""))
        while line:
            line = f.readline().replace("\n","")
            urls.append(line)
    return urls

os.chdir(os.path.dirname(__file__))
urls = read_urls(url_txt)
urls_end = read_urls(url_txt_end)

with sync_playwright() as playwright:
    run(playwright)