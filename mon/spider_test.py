import time

from playwright.sync_api import Playwright, sync_playwright, expect

pic_dir = "/java_web/pagecheck/pagepic/"


def run(playwright: Playwright) -> None:
    #browser = playwright.chromium.launch(headless=True,args=["--webgl.force-enabled=true","--webgl.disabled=false","--webgl.enable-webgl2=false"])
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://get.webgl.org/")
    time.sleep(5)
    ofile = pic_dir+"1.png"
    page.screenshot(path=ofile,full_page=True)
    page.goto("chrome://gpu")
    ofile = pic_dir+"2.png"
    page.screenshot(path=ofile,full_page=True)
    page.goto("https://gis.shmh.gov.cn/mh_map/")
    ofile = pic_dir+"3.png"
    time.sleep(10)
    page.screenshot(path=ofile,full_page=True)

    page.goto("https://spgxpt.shmh.gov.cn/vcweb/#/login?ticket=p11cq9hr5r2z6hmujl")
    ofile = pic_dir+"4.png"
    time.sleep(120)
    page.screenshot(path=ofile,full_page=True)

    page.goto("https://spgxpt.shmh.gov.cn/vcweb/#/login?ticket=com_p11cq9hr5r2z6hmujl")
    page.get_by_text("视频资源").click()
    ofile = pic_dir+"5.png"
    time.sleep(120)
    page.screenshot(path=ofile,full_page=True)

    page.locator(".tag-list").locator("text=七宝镇").click()
    page.locator(".search-content").locator("button").click()
    ofile = pic_dir+"6.png"
    time.sleep(120)
    page.screenshot(path=ofile,full_page=True)

    page.get_by_text("列表展示").click()
    page_size = page.locator(".el-pagination__total").text_content()
    print(f"page_size : {page_size}")
    ofile = pic_dir+"7.png"
    time.sleep(120)
    page.screenshot(path=ofile,full_page=True)




    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
