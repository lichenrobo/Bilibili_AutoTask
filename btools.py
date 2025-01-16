from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time
import logging
import subprocess


# 大会员券列表
vip_privilege_list = [
"     B币券     ",
"  会员购优惠券  ",
"   漫画福利券   ",
"  会员购包邮券  ",
" 漫画商城优惠券 ",
"   装扮体验卡   ",
"   课堂优惠券   "
]


def get_and_save_cookies(driver, output_file):
    cookies = driver.get_cookies()
    with open(output_file, 'w') as f:
        json.dump(cookies, f)

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
    # 7. 开启日志
    logger.info("############################################################################################")
    logger.info("#####################################  任务开始于此处  #####################################")
    logger.info("############################################################################################\n")
    #logger.debug('This is a debug message')
    #logger.info('This is an info message')
    #logger.warning('This is a warning message')
    #logger.error('This is an error message')
    #logger.critical('This is a critical message')

    return logger
################################################################################


########################### 判断信息等级并记录 ##################################
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
    
    # 调用shell脚本，并获取命令的输出结果
    back = subprocess.run(["./script/vip_privilege.sh", str(vp_type)], capture_output=True, text=True)
    time.sleep(3)

    # 将 JSON 字符串解析为 Python 字典
    result = json.loads(back.stdout)
    code = int(result.get("code"))

    # 判断结果是否正常，赋值状态码
    if code == 69801 or code == 0:
        flag = 0            # 领取是成功的
    else:
        flag = 1            # 总之就是出错了

    # 返回输出结果
    return {"result": result, "flag": flag}
################################################################################