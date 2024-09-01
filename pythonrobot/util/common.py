import logging
import os

from pythonrobot.util.config import dir_path


class Logger:
    def __init__(self ,name,level=logging.DEBUG):
        # 创建日志器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 创建控制台处理器
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # 创建格式器并将其添加到处理器中
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # 将处理器添加到日志器
        self.logger.addHandler(ch)
        log_file = dir_path / 'log' / 'server_api.txt'
        if log_file:
            # 确保日志目录存在
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            fh = logging.FileHandler(log_file)
            fh.setLevel(level)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)