# 引用B站工具包
import btools
# 引用定时计划包 apscheduler
from apscheduler.schedulers.blocking import BlockingScheduler                # 单线程任务  
from apscheduler.schedulers.background import BackgroundScheduler             # 多线程任务池

def vip_privilege(p_list):

    logger.info("######################################################################################\n")

    for p_item in p_list:
        try:
            # 调用自动领取大会员领取程序
            p_result = btools.receive_vip_privilege(p_item)
            btools.vip_privilege_log_result(logger, p_item, p_result["result"])
            p_flag = p_result["flag"]

        except Exception as e:
            #print(f"登录发生错误: {e}")
            logger.critical("领取权益 " + str(p_item) + " 出现错误： " + str(e))


    logger.info("######################################################################################\n\n\n\n\n\n\n\n")


def task_summary():

    logger.info("这是一次总结，状态码： ")
    



if __name__ == '__main__':

    # 初始化 Log 记录
    logger = btools.logger_init("./log/latest.log");

    # 初始化脚本参数
    p_list = [1, 2, 3]                  # 每月领取的权益代码 list

    # 代码调试区 使用时全部注释
    vip_privilege_flag = vip_privilege(p_list)
    #


    # 多线程任务设置
    scheduler = BackgroundScheduler(daemon=True, logger=logger)                                                 # 创建任务管理器 ;daemon=True 程序关闭时后台进程也停止 
    scheduler.add_job(vip_privilege, 'cron', minute='0,10,20,30,40,50', max_instances=1,  args=[p_list])        # 添加自动领取大会员权益任务
    scheduler.start()                                                                                           # 启动多线程任务

    # 维持脚本运行，并定期总结
    summary = BlockingScheduler(daemon=True, logger=logger)
    #summary.add_job(task_summary, 'interval', seconds=10)
    summary.add_job(task_summary, 'cron', minute='*/1', max_instances=1)
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