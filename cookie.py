from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
import json

import btools


if __name__ == '__main__':

    # 远程 WebDriver 服务器的地址和端口
    remote_server_url = "http://192.168.123.100:4444/wd/hub"
    # 脚本参数
    bilibili_url = "https://www.bilibili.com/"                      # bilibili 首页
    package_url = "https://account.bilibili.com/account/big/myPackage"               # 目标页面
    cookie_file = "cookie.json"
    # 设置浏览器选项 (使用 Options 类，推荐)
    chrome_options = Options()
#   chrome_options.add_argument("--headless")                       # 无头模式运行
    chrome_options.add_argument('--no-sandbox')                     # 禁用沙箱模式，在信任安全的环境下禁用可以一定程度提高效率
    chrome_options.add_argument("--disable-gpu")                    # 禁用 gpu 相关项
    chrome_options.add_argument("--incognito")                      # 隐私窗口，用来获取长期可用的 cookie
    # 创建 webdriver.Remote 实例 (使用 Options 类)
    driver = webdriver.Remote(
        command_executor=remote_server_url,
        options=chrome_options
    )


    #t = time.localtime()
    #print(t.tm_hour, t.tm_min, t.tm_sec)

    try:
        # 登录状态进入目标页面
        driver.get(bilibili_url)                                      # 打开首页
        time.sleep(30)                                             # 首次获取登录信息
        btools.get_and_save_cookies(driver, "cookie.json")

        btools.load_cookies(driver, cookie_file)                    # 载入 cookie
        driver.get(bilibili_url) 

        time.sleep(3)  

        # 获取网页标题
        title = driver.title
        logger.info("网页标题: " + title)



    except Exception as e:
        #print(f"登录发生错误: {e}")
        logger.error("登录发生错误： " + str(e))
    
    finally:
        # 关闭浏览器
        driver.quit()
