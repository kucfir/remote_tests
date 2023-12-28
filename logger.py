import logging


class Logger(logging.Logger):

    def __init__(self, name, log_file_name):
        self.name = name
        self.log_file_name = log_file_name
        self.level = logging.DEBUG
        logging.Logger.__init__(self, self.name, self.level)
        self.logger = logging.getLogger(self.name)
        self.c_handler = logging.StreamHandler()
        self.f_handler = logging.FileHandler(self.log_file_name + ".log")
        self.c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.c_handler.setFormatter(self.c_format)
        self.f_handler.setFormatter(self.f_format)
        self.logger.addHandler(self.c_handler)
        self.logger.addHandler(self.f_handler)
        self.logger.setLevel(self.level)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg=msg)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg=msg)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg=msg)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg=msg)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg=msg)

