import datetime
# 引用B站工具包
import btools
# 引用定时计划包 apscheduler
from apscheduler.schedulers.blocking import BlockingScheduler                 # 单线程任务  
from apscheduler.schedulers.background import BackgroundScheduler             # 多线程任务池

def vip_privilege(p_list, retry_count=0, max_retries=2):

    logger.info("######################################################################################\n")
    # 领取状态码
    status_flag = 0

    for p_item in p_list:
        try:
            # 调用自动领取大会员领取程序
            p_result = btools.receive_vip_privilege(p_item)
            btools.vip_privilege_log_result(logger, p_item, p_result["result"])
            p_flag = p_result["flag"]

            if p_flag > 0:          # 任何一个券领取失败都会导致状态码改变
                status_flag = 1

        except Exception as e:
            #print(f"登录发生错误: {e}")
            status_flag = 1
            logger.critical("领取权益 " + str(p_item) + " 出现错误： " + str(e))


    logger.info("######################################################################################\n\n\n\n\n\n\n\n")

    if status_flag == 0:
        return 0
    elif status_flag > 0 and retry_count < max_retries:
        logger.error("*******************此次领取任务出现错误，需要重试！！！*******************")
        retry_count += 1
        # 添加一次重试任务
        scheduler.add_job(vip_privilege, trigger='date', run_date=datetime.datetime.now() + datetime.timedelta(minutes=15), args=[p_list, retry_count, max_retries])
        return 1
    else:
        # 
        logger.critical("*******************          出大事了！！！          *******************")
        return -1



def task_summary():

    #logger.info("这是一次总结，状态码： ")
    return 0
    



if __name__ == '__main__':

    # 初始化 Log 记录
    logger = btools.logger_init("./log/bilibili_autotask.log");

    # 初始化脚本参数
    p_list = [1, 2, 3]                  # 每月领取的权益代码 list




    # 多线程任务设置
    scheduler = BackgroundScheduler(daemon=True, logger=logger)                                                     # 创建任务管理器 ;daemon=True 程序关闭时后台进程也停止 
    scheduler.add_job(vip_privilege, 'cron', minute='0,10,20,30,40,50', max_instances=1,  args=[p_list, 0, 2])      # 添加自动领取大会员权益任务
    #scheduler.add_job(vip_privilege, 'cron', minute='*/20', max_instances=1,  args=[p_list, 0, 2]) 
    scheduler.start()                                                                                               # 启动多线程任务

    # 代码调试区 使用时全部注释
    vip_privilege_flag = vip_privilege(p_list, 0, 2)
    #

    # 维持脚本运行，并定期总结
    summary = BlockingScheduler(daemon=True, logger=logger)
    #summary.add_job(task_summary, 'interval', seconds=10)
    summary.add_job(task_summary, 'cron', minute='55', max_instances=1)
    summary.start()

    """
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
    """
    """
    scheduler = BlockingScheduler()
    #scheduler.add_job(print("hello"), 'interval', minutes=10)
    scheduler.add_job(vip_privilege, 'cron', minute='0,10,20,30,40,50', max_instances=1)
    scheduler.start()
    """