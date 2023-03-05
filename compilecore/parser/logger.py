

import logging



class Logger(object):

    def __init__(self) -> None:

        # 创建一个名为 "my_logger" 的 Logger 对象
        self.logger = logging.getLogger("CompileCore logger")
        self.logger.setLevel(logging.INFO)

        # 创建一个将日志记录到终端的 StreamHandler 对象
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # 添加处理器到 Logger 对象
        self.logger.addHandler(console_handler)

    def debug(self):
        self.logger.setLevel(logging.DEBUG)

    def log(self, info):
        
        self.logger.debug(info)