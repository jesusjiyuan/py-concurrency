import base64
import json
import time

import requests
from playwright.sync_api import Playwright, sync_playwright

wiew_size = {"width": 1200, "height": 4240}

def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False,slow_mo=2000)
    context = browser.new_context()

    # Open new page
    page = context.new_page()
    page.set_viewport_size(wiew_size)

    # Go to https://pro.jd.com/mall/active/36yPbWm4JqFrmTgABydz6GkWNkca/index.html
    page.goto("https://pro.jd.com/mall/active/36yPbWm4JqFrmTgABydz6GkWNkca/index.html")

    # Click text=家庭量贩
    with page.expect_popup() as popup_info:
        page.locator("text=家庭量贩").click()
    time.sleep(2)
    page2 = popup_info.value
    page2.mouse.wheel(0,10000)
    page2.set_viewport_size(wiew_size)
    time.sleep(2)
    out1 = "./pic/家庭量贩.png"
    page2.screenshot(path=out1,full_page=True)
    print(out1+":")
    start = time.time()
    ret = ocr(out1)
    print("cost time: " + str(time.time()-start))
    print("查询 ‘天天特价’ :")
    index = ret.find("天天特价")
    if index != -1:
        print("天天特价存在")

    # Click text=京东生鲜
    with page2.expect_popup() as popup_info:
        page2.locator("text=京东生鲜").click()
    page3 = popup_info.value
    page3.set_viewport_size(wiew_size)
    page3.mouse.wheel(0,10000)
    #time.sleep(5)
    out2 = "./pic/京东生鲜.png"
    #page3.screenshot(path=out2,full_page=True)
    #print(out2+":")
    #ocr(out2)



# Click text=品牌特卖
#    with page.expect_popup() as popup_info:
#        page.locator("text=品牌特卖").click()
#    #time.sleep(2)
#    page4 = popup_info.value
#    page4.set_viewport_size(wiew_size)
#    page4.mouse.wheel(0,10000)
#    time.sleep(2)
#    out3 = "./pic/品牌特卖.png"
#    page4.screenshot(path=out3,full_page=True)
#    print(out3+":")
#    ocr(out3)



    # Close page
    page.close()

    # Close page
#    page4.close()

    # Close page
    page2.close()

    # Close page
    page3.close()


    # ---------------------
    context.close()
    browser.close()


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


with sync_playwright() as playwright:
    run(playwright)
