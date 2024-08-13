import os
import logging
import logging.config
import os
os.chdir(os.path.dirname(__file__))

def test_123():
    # 创建一个logger
    logger = logging.getLogger('vc')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    # 创建一个输出到文件的handler
    file_handler = logging.FileHandler('vc.log',encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    # 将handler添加到logger
    logger.addHandler(file_handler)
    #logger = logs.get_logger("simple")


def get_logger(name, plog_conf="logging.conf"):
    """
    :param name: logger name
    :param plog_conf: logging config file path
    :param write_log_path: write log file path
    """
    #if not os.path.exists(write_log_path):
    #    os.mkdir(write_log_path)
    #logging.basicConfig(level=logging.DEBUG, encoding="utf-8")
    logging.config.fileConfig(plog_conf, disable_existing_loggers=False)
    logger = logging.getLogger(name)
    return logger



if __name__ == "__main__":
    # 只输出到控制台
    log = get_logger("debug")
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