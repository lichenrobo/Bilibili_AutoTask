from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time
import logging
import requests
import subprocess

# 参数设置
csrf_path = "./config/csrf"
SESSDATA_path = "./config/SESSDATA"

# 大会员福利券列表
vip_privilege_list = [
"     B币券     ",
"  会员购优惠券  ",
"   漫画福利券   ",
"  会员购包邮券  ",
" 漫画商城优惠券 ",
"   装扮体验卡   ",
"   课堂优惠券   "
]


# 获取并保存 cookie
def get_and_save_cookies(driver, output_file):
    cookies = driver.get_cookies()
    with open(output_file, 'w') as f:
        json.dump(cookies, f)

# 装载 cookie
def load_cookies(driver, cookie_file):
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)


############################# 初始配置 logger ###################################
def logger_init(log_file):                          # log_file 指定log文件存放路径

    # 1. 配置日志记录器
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # 设置最低日志级别为 DEBUG
    # 2. 创建 FileHandler 对象，将日志写入文件
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)  # 设置文件 Handler 的日志级别
    # 3. 创建 StreamHandler 对象，将日志输出到控制台
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO) # 设置控制台 Handler 的日志级别
    # 4. 创建 Formatter 对象，定义日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # 5. 将 Formatter 对象添加到 Handler
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    # 6. 将 Handler 添加到 Logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    # 7. 开启日志并返回logger
    #logger.debug('This is a debug message')
    #logger.info('This is an info message')
    #logger.warning('This is a warning message')
    #logger.error('This is an error message')
    #logger.critical('This is a critical message')
    return logger
################################################################################



############################# 每日领大会员经验 ###################################
def vip_experience(logger):
    # 状态码初始化
    flag = 0
    # 领取大会员经验的 api 
    url = "https://api.bilibili.com/x/vip/experience/add"
    # 必须更改 header 为常用浏览器，否则默认的 python-requests header 会被 B站 风控拒绝访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # 获取 csrf 和 SESSDATA 参数
    try:
        file = open(csrf_path, 'r', encoding='utf-8')
        csrf = file.read()
    finally:
        file.close()
    try:
        file = open(SESSDATA_path, 'r', encoding='utf-8')
        SESSDATA = file.read()
    finally:
        file.close()

    # 构建 data 参数
    data = {
        "csrf": csrf
    }
    # 将 data 参数进行 URL 编码
    # requests.post 会自动把 data 内容编码为 urlencode 格式，所以不需要多余的操作，自己转码反而会产生错误。

    # 构建 cookies
    cookies = {
        "SESSDATA": SESSDATA
    }

    # 发送 POST 请求
    try:
        response = requests.post(url, headers=headers, data=data, cookies=cookies)
        # 检查响应状态码
        if response.status_code == 200:
            result = response.json()          # 解析 json 为字典
            code = int(result.get("code"))
            message = result.get("message")
            logger.info("***************************** 领取大会员每日经验 *****************************" )    
            if code == 0 :
                logger.info("Code    : " + str(code))
                logger.info("Message : " + message)
            elif code > 0:
                logger.warning("Code    : " + str(code))
                logger.warning("Message : " + message)
            else:
                logger.error("Code    : " + str(code))
                logger.error("Message : " + message)    
            logger.info(result)
            logger.info("******************************************************************************\n")
            # 判断结果是否正常，赋值状态码
            if code != 69198 and code != 0:
                flag = 1            # 总之就是出错了


        else:
            logger.error("请求失败，状态码：" + str(response.status_code))
            logger.error(response.text)
            flag = 1
    except requests.exceptions.RequestException as e:
        logger.critical("请求发生错误: " + str(e))
        flag = 1

    # 返回任务状态码
    return flag

################################################################################


############################ 领取单个大会员权益 ##################################
def single_privilege(vp_type):
    # 状态码初始化
    flag = 0
    # 领取大会员福利券的 api 
    url = "https://api.bilibili.com/x/vip/privilege/receive"
    # 必须更改 header 为常用浏览器，否则默认的 python-requests header 会被 B站 风控拒绝访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # 获取 csrf 和 SESSDATA 参数
    try:
        file = open(csrf_path, 'r', encoding='utf-8')
        csrf = file.read()
    finally:
        file.close()
    try:
        file = open(SESSDATA_path, 'r', encoding='utf-8')
        SESSDATA = file.read()
    finally:
        file.close()

    # 构建 data 参数
    data = {
        "type":vp_type,
        "platform":"web",
        "csrf": csrf
    }
    # 将 data 参数进行 URL 编码
    # requests.post 会自动把 data 内容编码为 urlencode 格式，所以不需要多余的操作，自己转码反而会产生错误。

    # 构建 cookies
    cookies = {
        "SESSDATA": SESSDATA
    }

    # 发送 POST 请求
    try:
        response = requests.post(url, headers=headers, data=data, cookies=cookies)
        # 检查响应状态码
        if response.status_code == 200:
            result = response.json()          # 解析 json 为字典
        else:
            #logger.error("请求失败，状态码：" + str(response.status_code))
            #logger.error(response.text)
            flag = 1
    except requests.exceptions.RequestException as e:
        #logger.critical("请求发生错误: " + str(e))
        flag = 1
    
    return result

################################################################################

####################### 判断大会员权益信息等级并记录 ##############################
def vip_privilege_log_result(logger, vp_type, result):

    code = int(result.get("code"))
    message = result.get("message")
    #ttl = result.get("ttl")
    #data = result.get("data")

    logger.info("****************************** " + vip_privilege_list[(vp_type -1)] +" ******************************" )    
    if code == 0 :
        logger.info("Code    : " + str(code))
        logger.info("Message : " + message)
    elif code > 0:
        logger.warning("Code    : " + str(code))
        logger.warning("Message : " + message)
    else:
        logger.error("Code    : " + str(code))
        logger.error("Message : " + message)
    
    logger.info(result)
    logger.info("******************************************************************************\n")

    return result
################################################################################


########################### 每月自动领取大会员权益 ###############################
def receive_vip_privilege(vp_type):
    
    # 调用单个权益领取函数，并获取输出结果
    result = single_privilege(vp_type)
    time.sleep(3)

    code = int(result.get("code"))

    # 判断结果是否正常，赋值状态码
    if code == 69801 or code == 0:
        flag = 0            # 领取是成功的
    else:
        flag = 1            # 总之就是出错了

    # 返回输出结果
    return {"result": result, "flag": flag}
################################################################################