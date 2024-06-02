import logging
import os


def configure_logging(log_directory='logs', log_filename='test.log'):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")

    file_handler = logging.FileHandler(os.path.join(log_directory, log_filename))
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
