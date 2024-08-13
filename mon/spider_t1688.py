from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False,slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rightint001.1688.com/")

    with page.expect_popup() as page1_info:
        page.get_by_text("全部商品").click()
    page1 = page1_info.value
    page_size =  page1.locator("#bd_1_container_0 > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > label:nth-child(1)").inner_text()
    print(page_size)

    pageLinks = page1.locator(".main-picture").all()
    print(pageLinks)
    if len(pageLinks) > 0:
        for url in pageLinks:
            url.first.click()
    page.close()
    page1.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
