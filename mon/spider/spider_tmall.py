from operator import contains
import os
os.chdir(os.path.dirname(__file__))

from asyncio import InvalidStateError
from playwright.sync_api import Playwright, sync_playwright

import logs
import confhelper
logger = logs.get_logger('tb')

wiew_size = {"width": 1080, "height": 2240}
linkpath_prefix = confhelper.confdata().get("linkpath_prefix")+"tmall/"
work_dir = confhelper.confdata().get("work_dir")
path_prefix = "d:/tmp/pic/tmall/"
page_size = 24
picList = []

def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False,slow_mo=2000)
    context = browser.new_context(screen=wiew_size, viewport=wiew_size,storage_state="tmall_state.json")
    # Open new page
    page = context.new_page()
    #url = 'http://shop112752036.taobao.com/'
    #url = 'http://shop64886789.taobao.com/'
    #url = 'http://shop163109165.taobao.com/'
    url = 'http://shop112841437.taobao.com/'
    logger.info("开始遍历 {}".format(url))
    page.goto(url)
    while page.locator(".captcha-tips").count() >0:
        logger.info("全部宝贝 出现图形验证等待5秒")
        #send_email("spidetb","出现图形验证等待5秒")
        #time.sleep(5)
        page.wait_for_timeout(5000)
    all_flag = 0
    all_flag = page.locator("text=所有商品").count()
    if all_flag > 0:
        page.locator("text=所有商品").click()
    try:
        all_flag = page.locator(".banner-box").locator("area:nth-child(2)").wait_for(timeout=10).first.get_attribute("href").count()
        if all_flag > 0:
            page.locator(".banner-box").locator("area:nth-child(2)").first.click()
    except Exception as e:
        print(e)

    #with page.expect_request(p,timeout=60000) as info:
    #    page1 = info.value
    #html.ks-gecko120.ks-gecko.ks-firefox120.ks-firefox.w1190 body div#page.shop-tmall div#content.eshop.head-expand.tb-shop div#bd div.layout.grid-m0.J_TLayout div.col-main div.main-wrap.J_TRegion div#shop22869710746.J_TModule div#TmshopSrchNav.skin-box.tb-module.tshop-pbsm.tshop-pbsm-tmall-srch-list div#J_ShopSearchResult div.skin-box-bd div.filter.clearfix.J_TFilter p.ui-page-s b.ui-page-s-len
    logger.info(page.locator(".J_TFilter").locator("b.ui-page-s-len").inner_text())
    page_num_str = page.locator(".J_TFilter").locator("b.ui-page-s-len").inner_text()
    page_size = 0
    if contains(page_num_str,"/") :
        page_size = int(page_num_str.split("/")[1])
    print(page_size)

    pageLinks = page.locator(".J_TGoldData").all()
    print(pageLinks)
    if len(pageLinks) > 0:
        for url in pageLinks:
            logger.info(url.inner_html())
            url.first.click()
    # ---------------------
    page.close()
    context.close()
    browser.close()

os.chdir(os.path.dirname(__file__))
with sync_playwright() as playwright:
    run(playwright)
