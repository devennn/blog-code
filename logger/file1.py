import logging
from set_logger import set_logger
from file2 import run_file2

logger = set_logger(level=logging.CRITICAL)

# Logs
logger.debug('A debug in file1')
logger.info('An info in file1')
logger.warning('Something is not right in file1')
logger.error('A Major error has happened in file1')
logger.critical('Fatal error. Cannot continue in file1')

run_file2()
