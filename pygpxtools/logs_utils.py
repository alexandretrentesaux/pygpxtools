# -*- encoding: utf-8 -*-
import logging.config


def initialize_logger():
    """Logger initialization"""

    logger = logging.getLogger('pygpxtools')
    logger.setLevel(logging.DEBUG)
    sh = logging.handlers.SysLogHandler()
    sh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    shFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    chFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(shFormatter)
    ch.setFormatter(chFormatter)
    # add the handlers to the logger
    logger.addHandler(sh)
    logger.addHandler(ch)
    return logger
