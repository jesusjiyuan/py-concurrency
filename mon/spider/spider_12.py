from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.yadea.com.cn/
    page.goto("https://www.yadea.com.cn/")

    # Click text=VFLY GVFLY LVFLY NVFLY 骑兵01 >> img >> nth=0
    with page.expect_popup() as popup_info:
        page.locator("text=VFLY GVFLY LVFLY NVFLY 骑兵01 >> img").first.click()
    page1 = popup_info.value

    # Click header >> text=冠能系列
    page.locator("header >> text=冠能系列").click()

    # Click .car-img >> nth=0
    # with page.expect_navigation(url="https://www.yadea.com.cn/model-details/e10"):
    with page.expect_navigation():
        page.locator(".car-img").first.click()
    # assert page.url == "https://www.yadea.com.cn/model-details/e10"

    # Click text=雅迪换电兽 01 MAX雅迪换电兽 02 MAX 2023 >> img >> nth=1
    page.locator("text=雅迪换电兽 01 MAX雅迪换电兽 02 MAX 2023 >> img").nth(1).click()
    # assert page.url == "https://www.yadea.com.cn/car-detail/hds02/index.html"

    # Close page
    page1.close()

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
