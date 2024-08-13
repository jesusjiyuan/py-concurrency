import time

from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    #browser = playwright.chromium.launch_persistent_context(
    #    # 指定本机用户缓存地址
    #    user_data_dir=r"C:\Users\user\AppData\Local\Google\Chrome\User Data",
    #    # 指定本机google客户端exe的路径
    #    executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    #    # 要想通过这个下载文件这个必然要开  默认是False
    #    accept_downloads=True,
    #    # 设置不是无头模式
    #    headless=False,
    #    bypass_csp=True,
    #    slow_mo=10,
    #    # 跳过检测
    #    args = ['--disable-blink-features=AutomationControlled','--remote-debugging-port=9222']
#
    #)
    #browser = playwright.firefox.launch_persistent_context(
    #    user_data_dir = "D:\\tmp",
    #    executable_path="D:\\ProgramFiles\\browsers\\firefox\\firefox.exe",
    #    headless=False,
    #    bypass_csp=True,
    #    slow_mo=10,
    #    # 跳过检测
    #    #args = ['--disable-blink-features=AutomationControlled','--remote-debugging-port=9222']
    #)
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.yadea.com.cn/
    page.goto("https://www.yadea.com.cn/")

    #time.sleep(1)
    # Click text=VFLY| >> div >> nth=0
    print(page.title())
    page.screenshot(path="../pic/1.png", full_page=True)

    page.locator("header >> text=骑行产品").hover();
    page.locator("header >> text=VFLY").hover();
    # Click text=VFLY GVFLY LVFLY NVFLY 骑兵01 >> img >> nth=0
    with page.expect_popup() as popup_info:
        page.locator("text=VFLY GVFLY LVFLY NVFLY 骑兵01 >> img").first.click()
    page1 = popup_info.value
    print(page1.title())
    page1.screenshot(path="../pic/2.png", full_page=True)

    page.goto("https://www.yadea.com.cn/")
    page.locator("header >> text=骑行产品").hover();
    # Click header >> text=冠能系列
    page.locator("header >> text=冠能系列").hover()

    # Click .car-img >> nth=0
    # with page.expect_navigation(url="https://www.yadea.com.cn/model-details/e10"):
    with page.expect_navigation():
        page.locator(".car-img").first.click()
    print(page.title())
    page.screenshot(path="../pic/3.png", full_page=True)
        # assert page.url == "https://www.yadea.com.cn/model-details/e10"

    page.locator("header >> text=骑行产品").hover();
    # Click text=换电系列
    page.locator("header >> text=换电系列").hover()

    # Click text=雅迪换电兽 01 MAX雅迪换电兽 02 MAX 2023 >> img >> nth=1
    page.locator("text=雅迪换电兽 01 MAX雅迪换电兽 02 MAX 2023 >> img").nth(1).click()
    # assert page.url == "https://www.yadea.com.cn/car-detail/hds02/index.html"

    print(page.title())
    page.screenshot(path="../pic/4.png", full_page=True)


    # Close page
    page1.close()
    # Close page
    page.close()
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
