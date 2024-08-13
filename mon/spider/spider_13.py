import base64
import json
import time

import image
import requests
from PIL import Image
from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=True,slow_mo=100)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.yadea.com.cn/
    page.goto("https://www.yadea.com.cn/")

    # Click span:has-text("骑行产品")
    page.locator("span:has-text(\"骑行产品\")").hover()
    # Click text=VFLY| >> div >> nth=0
    page.locator("text=VFLY| >> div").first.hover()

    # Click text=VFLY G
    with page.expect_popup() as popup_info:
        page.locator("text=VFLY G").click()
    page1 = popup_info.value

    time.sleep(3)
    print(page.title())
    out1 = "./pic/1.png"
    page.screenshot(path=out1,full_page=True)
    ocr(out1)

    # Click header >> text=冠能系列
    page.locator("span:has-text(\"骑行产品\")").hover()
    page.locator("header >> text=冠能系列").hover()

    # Click header >> text=雅迪冠能 探索E10
    # with page.expect_navigation(url="https://www.yadea.com.cn/model-details/e10"):
    with page.expect_navigation():
        page.locator("header >> text=雅迪冠能 探索E10").click()
    # assert page.url == "https://www.yadea.com.cn/model-details/e10"

    time.sleep(3)
    print(page.title())
    out2 = "./pic/2.png"
    page.screenshot(path=out2,full_page=True)
    ocr(out2)

    # Click header >> text=换电系列
    page.locator("span:has-text(\"骑行产品\")").hover()
    page.locator("header >> text=换电系列").hover()

    # Click text=雅迪换电兽 01 MAX
    page.locator("text=雅迪换电兽 01 MAX").click()
    # assert page.url == "https://www.yadea.com.cn/car-detail/hds01/index.html"

    time.sleep(3)
    print(page.title())
    out3 = "./pic/3.png"
    page.screenshot(path=out3,full_page=True)
    ocr(out3)

    # Close page
    page.close()

    # Close page
    page1.close()

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

with sync_playwright() as playwright:
    run(playwright)
