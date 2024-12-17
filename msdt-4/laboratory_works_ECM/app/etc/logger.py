"""
Configuration logger file
"""

from loguru import logger

# Configurate logger

# All logs
logger.add(
    'app/logs/all/log_file.log', # path
    rotation="10:00", # when file will be rotate
    retention="7 days", # file time live
    compression="zip", # compression if rotation
    level="DEBUG" # level for logging
)

# Error logs
logger.add(
    'app/logs/errors/log_error_file.log', # path
    rotation="10 MB", # how much log file can be weight
    compression="zip", # compression if rotation
    level="ERROR" # level for logging 
)
