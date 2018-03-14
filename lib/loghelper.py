import logging
import os,inspect,time

from lib.filehelper import FileHelper
from lib.platformhelper import PlatformHelper

class LogHelper(object):
    logger = None
    fmt_option = {}
    remove_newline = False

    @classmethod
    def create_logger(cls, path, level="DEBUG", fmt="%(asctime)s %(levelname)s %(message)s",
                      fmt_date='%Y-%m-%dT%H:%M:%S', gmtime=True, remove_newline=True):

        cls.remove_newline = remove_newline
        log_level = cls.__resolve_log_level(level)
        log_name = os.path.basename(path)
        cls.logger = logging.getLogger(log_name)
        cls.logger.setLevel(log_level)

        cls.logger.handlers = [h for h in cls.logger.handlers if not isinstance(h, logging.StreamHandler)]
        cls.logger.removeHandler(cls.logger.handlers)

        # create a file handler

        if not FileHelper.dir_exist(FileHelper.get_dir(path)):
            FileHelper.create_directory(FileHelper.get_dir(path))

        handler = logging.FileHandler(path, mode='a', delay=False)

        handler.setLevel(log_level)

        # add the handlers to the logger
        cls.logger.addHandler(handler)

        cls.logger = logging.getLogger(log_name)

        cls.fmt_option["fmt"] = fmt
        cls.fmt_option['fmt_date'] = fmt_date
        cls.fmt_option['gmtime'] = gmtime
        cls.set_format("%s %s" % (cls.fmt_option['fmt'], cls.__get_call_back()), cls.fmt_option['fmt_date'],
                       cls.fmt_option['gmtime'])

        return cls.logger

    @classmethod
    def get_logger(cls, log_file_path, formatter, level="DEBUG"):
        if cls.logger is None:
            LogHelper.create_logger(log_file_path, formatter, level)
        return cls.logger

    @classmethod
    def __resolve_log_level(cls, level):

        expected_level = level.upper()
        level = logging.INFO

        if "DEBUG" == expected_level:
            level = logging.DEBUG
        elif "INFO" == expected_level:
            level = logging.INFO
        elif "WARN" == expected_level:
            level = logging.WARN
        elif "ERROR" == expected_level:
            level = logging.ERROR
        elif "FATAL" == expected_level:
            level = logging.FATAL

        return level

    @classmethod
    def __get_call_back(cls):
        caller_info = inspect.getframeinfo(inspect.stack()[2][0])
        file_path = str(caller_info.filename)
        file_line_number = str(caller_info.lineno)
        file_name = os.path.basename(file_path)
        call_backup_str = "%s:%s" % (file_name, file_line_number)

        return call_backup_str

    @classmethod
    def info(cls, log_message):
        if cls.logger is None:
            cls.__create_default_logger()

        cls.set_format("%s %s" % (cls.fmt_option['fmt'], cls.__get_call_back()), cls.fmt_option['fmt_date'],
                       cls.fmt_option['gmtime'])
        if cls.remove_newline and log_message:
            log_message = log_message.replace("\n", " ")

        cls.logger.info(log_message)

    @classmethod
    def debug(cls, log_message):
        if cls.logger is None:
            cls.__create_default_logger()

        cls.set_format("%s %s" % (cls.fmt_option['fmt'], cls.__get_call_back()), cls.fmt_option['fmt_date'],
                       cls.fmt_option['gmtime'])
        if cls.remove_newline and log_message:
            log_message = log_message.replace("\n", " ")

        cls.logger.debug(log_message)

    @classmethod
    def error(cls, log_message):
        if cls.logger is None:
            cls.__create_default_logger()

        cls.set_format("%s %s" % (cls.fmt_option['fmt'], cls.__get_call_back()), cls.fmt_option['fmt_date'],
                       cls.fmt_option['gmtime'])
        if cls.remove_newline and log_message:
            log_message = log_message.replace("\n", " ")

        cls.logger.error(log_message)

    @classmethod
    def critical(cls, log_message):
        if cls.logger is None:
            cls.__create_default_logger()

        cls.set_format("%s %s" % (cls.fmt_option['fmt'], cls.__get_call_back()), cls.fmt_option['fmt_date'],
                       cls.fmt_option['gmtime'])

        if cls.remove_newline and log_message:
            log_message = log_message.replace("\n", " ")

        cls.logger.critical(log_message)

    @classmethod
    def warn(cls, log_message):
        if cls.logger is None:
            cls.__create_default_logger()

        cls.set_format("%s %s" % (cls.fmt_option['fmt'], cls.__get_call_back()), cls.fmt_option['fmt_date'],
                       cls.fmt_option['gmtime'])

        if cls.remove_newline and log_message:
            log_message = log_message.replace("\n", " ")

        cls.logger.warn(log_message)

    @classmethod
    def set_format(cls, fmt=None, datefmt=None, gmtime=True):
        fmt = cls.__create_formatter(fmt, datefmt, gmtime)
        for handler in cls.logger.handlers:
            result = handler.setFormatter(fmt)

        return result

    @classmethod
    def __create_formatter(cls, formatter_str, datefmt=None, gmtime=True):
        formatter = logging.Formatter(formatter_str, datefmt)
        if gmtime:
            formatter.converter = time.gmtime
        return formatter

    @classmethod
    def __create_default_logger(cls):
        if PlatformHelper.is_Linux():
            logger_path = os.path.join("/", "tmp")
        elif PlatformHelper.is_win():
            logger_path = os.path.join("c:", "tmp")
        elif PlatformHelper.is_mac():
            logger_path = os.path.join("/", "tmp")

        log_filepath = os.path.join(logger_path, "automation.log")

        return cls.create_logger(log_filepath)

