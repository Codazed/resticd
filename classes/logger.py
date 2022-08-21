import logging

default_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s]: %(message)s', "%Y-%m-%d %H:%M:%S")

class ResticdLogger(logging.Logger):
    def __init__(self):
        super().__init__('resticd', logging.DEBUG)
        self.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = default_formatter
        ch.setFormatter(formatter)

        self.propagate = False
        self.addHandler(ch)

    def log(self, message: str, level: int, sub_name=None):
        if sub_name:
            formatter = logging.Formatter('[%(asctime)s] [%(sub_name)s] [%(levelname)s]: %(message)s', "%Y-%m-%d %H:%M:%S")
        else:
            formatter = default_formatter
        for handler in self.handlers:
                handler.setFormatter(formatter)

        self._log(level, message, None)

    def debug(self, message, sub_name=None):
        self.log(message, logging.DEBUG, sub_name)

    def info(self, message, sub_name=None):
        self.log(message, logging.INFO, sub_name)

    def warn(self, message, sub_name=None):
        self.log(message, logging.WARN, sub_name)

    def error(self, message, sub_name=None):
        self.log(message, logging.ERROR, sub_name)
    
    def critical(self, message, sub_name=None):
        self.log(message, logging.CRITICAL, sub_name)

logger = ResticdLogger()