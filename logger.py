from datetime import datetime
import os
from loguru import logger as logging

log_path = './log/runtime.log'
logging.add(log_path, rotation="2048 MB", retention=3, level='DEBUG', format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>', backtrace=True, diagnose=True, enqueue=False, catch=True)
