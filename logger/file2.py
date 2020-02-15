from set_logger import set_logger

logger = set_logger()

def run_file2():
    # Logs
    logger.debug('A debug in file2')
    logger.info('An info in file2')
    logger.warning('Something is not right in file2')
    logger.error('A Major error has happened in file2')
    logger.critical('Fatal error. Cannot continue in file2')
