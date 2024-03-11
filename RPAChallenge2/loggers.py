import logging

def setup_logger(log_file, log_level=logging.INFO):
    """
    Set up a logger to log messages to a file.
    """
    logger = logging.getLogger()
    logger.setLevel(log_level)

    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(log_level)

    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
    file_handler.setFormatter(log_formatter)

    logger.addHandler(file_handler)

    return logger
