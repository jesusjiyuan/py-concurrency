from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://mall.jd.com/index-935158.html?from=pc
    page.goto("https://mall.jd.com/index-935158.html?from=pc")

    # Click .d-content a:nth-child(4) >> nth=0
    # with page.expect_navigation(url="https://cfe.m.jd.com/privatedomain/risk_handler/03101900/?returnurl=https%3A%2F%2Fitem.jd.com%2F10083040818536.html&rqhost=https%3A%2F%2Fapi.m.jd.com&rpid=rp-188065206-10435-1694142975956&evtype=3&evapi=color_pc_detailpage_wareBusiness&source=1&forceCurrentView=1&lgid=2193"):
    with page.expect_navigation():
        with page.expect_popup() as popup_info:
            page.locator(".d-content a:nth-child(4)").first.click()
        page1 = popup_info.value

    # Close page
    page1.close()

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
