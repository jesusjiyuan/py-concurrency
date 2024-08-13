# coding: utf-8
import logging.config
import sys

logging.config.fileConfig('../logging.conf')

# create logger
logger = logging.getLogger('simple')

def test():
    # 'application' code
    logger.debug("debug message {}".format("你好"))
    logger.info("info message %s",list(range(1,4)))
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')
    print(sys.argv)