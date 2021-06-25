import boto3, logging, watchtower
from logging.handlers import TimedRotatingFileHandler


class LazadaLogger:
    @staticmethod
    def get_logger(logger_name: str = __name__):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.addHandler(LazadaLogger.__get_cloudwatch_handler())
        return logger

    @staticmethod
    def __get_cloudwatch_handler(s3_profile_name: str = None):
        s3 = boto3.session.Session(profile_name=s3_profile_name)
        handler = watchtower.CloudWatchLogHandler(
            log_group="pvicard", stream_name="cronjob", boto3_session=s3
        )
        handler.setFormatter(LazadaLogger.__get_file_log_formatter())
        return handler

    @staticmethod
    def __get_file_log_formatter():
        formatter = logging.Formatter(
            "%(levelname)s [%(name)s:%(lineno)d]: %(message)s"
        )
        return formatter
