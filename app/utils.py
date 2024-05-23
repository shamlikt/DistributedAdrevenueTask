import  logging
import sys
import os


def setup_logger(name, logger_dir=".", level=logging.DEBUG):

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Terminal handler
    term_handler = logging.StreamHandler(sys.stdout)
    term_handler.setLevel(level)
    term_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s: %(message)s", datefmt='%Y-%m-%d %H:%M:%S'))

    # File handler
    logger_path = os.path.join(logger_dir, 'dask_app.log')
    file_handler = logging.FileHandler(logger_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s %(filename)s:%(lineno)s : %(message)s"))

    #Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(term_handler)

    return logger



