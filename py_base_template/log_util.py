import os
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler


class TimeAndFileRotatingHandler(TimedRotatingFileHandler, RotatingFileHandler):
    """
    自定义日志处理器
    根据时间和文件大小分割
    """

    def doRollover(self):
        """
        TODO 分割日志的方法
        """
        pass

    def shouldRollover(self, record):
        """
        TODO 判断是否需要分割日志
        """
        pass

    def getFilesToDelete(self):
        """
        TODO 删除策略
        """
        pass
