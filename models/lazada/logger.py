import logging
from logging.handlers import TimedRotatingFileHandler


class LazadaLogger:
    @staticmethod
    def get_logger(logger_name: str = __name__):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.addHandler(LazadaLogger.__get_file_handler())
        return logger

    @staticmethod
    def __get_file_handler():
        handler = TimedRotatingFileHandler(
            "lazada.log", backupCount=1, when="D", interval=30
        )
        handler.setFormatter(LazadaLogger.__get_file_log_formatter())
        return handler

    @staticmethod
    def __get_file_log_formatter():
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s:%(name)s:%(lineno)d]: %(message)s"
        )
        return formatter
