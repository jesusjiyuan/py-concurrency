import os
os.chdir(os.path.dirname(__file__))

from asyncio import InvalidStateError
from playwright.sync_api import Playwright, sync_playwright

import logs
import confhelper
logger = logs.get_logger('tb')

wiew_size = {"width": 1080, "height": 2240}
linkpath_prefix = confhelper.confdata().get("linkpath_prefix")+"t1688/"
work_dir = confhelper.confdata().get("work_dir")
path_prefix = "d:/tmp/pic/t1688/"
page_size = 24
picList = []

def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False,slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()
    #url = "https://rightint001.1688.com/"
    url = "https://shop1395075526323.1688.com/"
    page.goto(url)

    with page.expect_popup() as page1_info:
        page.get_by_text("全部商品").click()
    page1 = page1_info.value
    page_size =  page1.locator("#bd_1_container_0 > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > label:nth-child(1)").inner_text()
    logger.info(page_size)

    pageLinks = page1.locator(".main-picture").all()
    logger.info(pageLinks)
    if len(pageLinks) > 0:
        for url in pageLinks:
            logger.info(url.inner_html())
            url.first.click()
    page.close()
    page1.close()

    # ---------------------
    context.close()
    browser.close()

os.chdir(os.path.dirname(__file__))
with sync_playwright() as playwright:
    run(playwright)
