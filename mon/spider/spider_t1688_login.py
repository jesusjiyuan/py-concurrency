import time

from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://login.taobao.com/member/login.jhtml
    page.goto("http://shop1466614953236.1688.com/")

    # Click .iconfont.icon-qrcode
    page.locator(".iconfont.icon-qrcode").click()

    time.sleep(30)
    context.storage_state(path="t1688_state.json")
    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
