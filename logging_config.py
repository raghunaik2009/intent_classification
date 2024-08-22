import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file='logs/server.log', max_bytes=10000000, backup_count=3):
    logger = logging.getLogger()
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    handler.setFormatter(log_formatter)
    handler.setLevel(logging.INFO)
    
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
