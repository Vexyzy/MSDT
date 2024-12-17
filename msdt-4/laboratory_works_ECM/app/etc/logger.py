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
    format="{extra[ip]} {extra[user]} {time} {level} {message}",
)

# Error logs
logger.add(
    "logs/errors/log_error_file.log",  # path
    rotation="10 MB",  # how much log file can be weight
    compression="zip",  # compression if rotation
    level="ERROR",  # level for logging
    format="{extra[ip]} {extra[user]} {time} {level} {message}",
)

# send message error to telegram
logger.add(telegram_handler, level="ERROR")
