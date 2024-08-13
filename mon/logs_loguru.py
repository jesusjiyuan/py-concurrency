import sys

from loguru import logger
import os
os.chdir(os.path.dirname(__file__))

# def get_logger(name, plog_conf="logging.conf"):
#     """
#     :param name: logger name
#     :param plog_conf: logging config file path
#     :param write_log_path: write log file path
#     """
#     #if not os.path.exists(write_log_path):
#     #    os.mkdir(write_log_path)
#     #logging.basicConfig(level=logging.DEBUG, encoding="utf-8")
#     logging.config.fileConfig(plog_conf, disable_existing_loggers=False)
#     logger = logging.getLogger(name)
#     return logger



if __name__ == "__main__":
    # from loguru import logger
    # # Remove a previously added handler and stop sending logs to its sink.
    # logger.remove(handler_id=None)  # 清除之前的设置
    # # 设置生成日志文件，utf-8编码，每天0点切割，zip压缩，保留3天，异步写入
    # logger.add(sink='runtime_{time}.log', level='INFO', rotation='00:00', retention='3 days', compression='zip', encoding='utf-8', enqueue=True)
    # logger.add(sink='runtime_{time}.log', level='INFO', rotation='500 MB', retention='30 days', compression='zip', encoding='utf-8', enqueue=True)

# 只输出到控制台
    # 删除默认预定义的的控制台handler
    #logger.remove()
    logger.add(sink=sys.stdout ,format="{time:YYYYMMDD HH:mm:ss.S} [{level}] [{module}] {message}")
    #添加上下文信息：
    #logger.add_context("request_id", "67890")
    logger.add("app.log", rotation="100MB",format="{time:YYYYMMDD HH:mm:ss} [{level}] [{module}] {message}",enqueue=True,level='DEBUG',diagnose=True)
    log = logger
    # # 只输出到文件
    # log = get_logger("crawler")
    # # 同时输出到控制台和文件
    # log = get_logger("root")
    log.debug("test debug")
    log.info("test info")
    log.warning("test warning")
    log.error("test error")
    log.critical("test critical")
    log.info("▁▂▃▄▅▆▇█▇▆▅▄▃▂▁N、特殊符号 §№☆★○●◎◇◆□■△▲※→←↑↓〓＃＆＠＼＾＿")
    str = 'OCR识别结果：[[[[[44.0, 6.0], [173.0, 6.0], [173.0, 29.0], [44.0, 29.0]], (\'京东首页上海\', 0.9988477826118469)], [[[310.0, 6.0], [435.0, 6.0], [435.0, 27.0], [310.0, 27.0]], (\' jd_ujTIahdFj. PLUS\', 0.9405677914619446)], [[[637.0, 8.0], [686.0, 8.0], [686.0, 23.0], [637.0, 23.0]], (\'企业采购\', 0.9995736479759216)], [[[721.0, 6.0], [778.0, 6.0], [778.0, 27.0], [721.0, 27.0]], (\'客户服务\', 0.9997944831848145)], [[[812.0, 8.0], [861.0, 8.0], [861.0, 23.0], [812.0, 23.0]], (\'网站导航\', 0.9998513460159302)], [[[890.0, 6.0], [949.0, 6.0], [949.0, 27.0], [890.0, 27.0]], (\''
    log.info(str)