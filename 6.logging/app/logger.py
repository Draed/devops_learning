"""
Application logging configuration
"""
import sys
from loguru import logger
from app.settings import Settings, LogOutput, LogLevel

def build_logger(settings: Settings) -> logger :
    ## Remove any previously added handlers (important on reloads)
    logger.remove()

    ## Custom logging format
    custom_log_fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <7}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    # Choose the destination (console or file) according to the app settings
    if settings.log_output == LogOutput.STDOUT:
        logger.add(
            sink=sys.stdout,
            level=settings.log_level.value,
            format=custom_log_fmt,
            colorize=True,
            backtrace=True,
            diagnose=True,
            enqueue=True,
        )
    elif settings.log_output == LogOutput.FILE:
        logger.add(
            sink=settings.log_file,
            level=settings.log_level.value,
            format=custom_log_fmt,
            colorize=True,
            backtrace=True,
            diagnose=True,
            enqueue=True,
            encoding="utf-8",
        )
    return logger