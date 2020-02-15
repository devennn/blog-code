import logging

def set_logger(level=logging.WARNING):
    FORMAT = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
    logging.basicConfig(format=FORMAT)
    # Gets or creates a logger
    logger = logging.getLogger(__name__)

    # set log level
    logger.setLevel(level=level)

    # define file handler and set formatter
    formatter = logging.Formatter(FORMAT)
    file_handler = logging.FileHandler('logfile.log')
    file_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(file_handler)

    return logger
