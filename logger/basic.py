import logging
logging.basicConfig(level=logging.CRITICAL)

def add_this(a, b):
    logging.debug("In function add this debug")
    logging.info("In function add this info")
    logging.error("In function add this error")
    logging.warning("In function add this warning")
    logging.critical("In function add this critical")
    return a + b

logging.info("Start program")
ans = add_this(1, 3)
logging.info(" Ans is {}".format(ans))
