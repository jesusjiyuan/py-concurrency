import base64
import json

from selenium import webdriver
from time import sleep
import logs
from PIL import Image
from selenium.webdriver.chrome.options import Options
import requests
logger = logging.getLogger(__name__)
class test:
    window_size_width = 1440
    #第二个输入这个：隐藏式启动谷歌浏览器执行UI测试用例
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    #browser = webdriver.Chrome()
    browser.maximize_window()
    #driver.get('https://www.baidu.com/')
    browser.get('http://epaper.hljnews.cn/hljrb/20181101/388976.html')
    #sleep(2)
    # 截取全屏
    #browser.save_screenshot("pic/demo1.png")

    def get_screenshot_scroll(self, scroll=500, scroll_interval=0.1):
        '''
        滚动截图
        注：必须开启无界面模式，即：--headless
        scroll 默认 100 ，向下滚动的像素数量
        scroll_interval 默认0.1s,滚动间隔
        width 截图的宽度  默认1440
        '''
        try:
            logger.info('开始截图，当前地址：' + self.browser.current_url)
            js_height = "return document.body.clientHeight"
            k = 1
            height = self.browser.execute_script(js_height)
            while True:
                if k * scroll < height:
                    js_move = "window.scrollTo(0,{})".format(k * scroll)
                    self.browser.execute_script(js_move)
                    sleep(scroll_interval)
                    height = self.browser.execute_script(js_height)
                    k += 1
                else:
                    break
                # 截图总高度最大量
                if height > 40000:
                    break
            # 接下来是全屏的关键，用js获取页面的宽高，如果有其他需要用js的部分也可以用这个方法
            width = self.window_size_width
            # width = self.browser.execute_script("return document.body.scrollWidth")
            height = self.browser.execute_script("return document.body.scrollHeight")
            logger.info('----->scroll screenshot width:{} height:{}'.format(width, height))
            # 将浏览器的宽高设置成刚刚获取的宽高
            self.browser.set_window_size(width, height)
            # 截图
            png_file = "../pic/1.png"
            #self.browser.save_screenshot(png_file)
            bytes_content = self.browser.get_screenshot_as_png()
            logger.info('滚动截图完成')
            return bytes_content
        except Exception as e:
            logger.info('-----> get screenshot err:' + e)


def ocr(dict):
    url = "https://mhqym.topwin.net/ppocr/predict/ocr_system"
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
    result = requests.post(url,data=json.dumps(dict),headers= header)
    #print(result.json())
    str = ""
    for i in result.json().get("results")[0]:
        str = str + i.get("text")
    print(str)

png_file = "../pic/1.png"
with open(png_file,"wb+") as f:
    test = test()
    bytes_content = test.get_screenshot_scroll()
    #img = Image.open(bytes_content)
    #img.save(format='PNG')
    f.write(bytes_content)
    f.flush()
    test.browser.quit()
    encoded = base64.b64encode(open(png_file, 'rb').read()).decode("utf-8")
    l = [encoded]
    map = {"images": l}
    #print(json.dumps(map))
    ocr(map)
    