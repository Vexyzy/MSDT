"""
Configuration logger file
"""

import os

from loguru import logger
from notifiers.logging import NotificationHandler

params = {
    "token": os.getenv("TELEGRAM_TOKEN"),
    "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
}

# initialize filter

def logger_filter(message):
    """Filter for logger

    Args:
        message (_type_): message of log

    Returns:
        _type_: is log constraint sensitive words or not. If true, this message
        doesn't be logged.
    """
    sensitive_keywords=[
        "password",   "api",      "api_key",
        "secret_key", "passport", "snils"
    ]
    return not any(keyword in message.get("message", "").lower()
                    for keyword in sensitive_keywords)


# inititalize tg hendler
telegram_handler = NotificationHandler("telegram", defaults=params)

# Configurate logger

# All logs
logger.add(
    "logs/all/log_file.log",  # path
    rotation="10:00",  # when file will be rotate
    retention="7 days",  # file time live
    compression="zip",  # compression if rotation
    level="DEBUG",  # level for logging
    filter=logger_filter, # filter
    format="{time} {level} {message}",
)

# Error logs
logger.add(
    "logs/errors/log_error_file.log",  # path
    rotation="17 KB",  # how much log file can be weight
    compression="zip",  # compression if rotation
    level="ERROR",  # level for logging
    filter=logger_filter, # filter
    format="{time} {level} {message}",
)

# send message error to telegram
logger.add(telegram_handler, level="ERROR", filter=logger_filter)