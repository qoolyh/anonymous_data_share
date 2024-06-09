import logging


def init_logger(name, filename):
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(filename, encoding='utf-8')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger