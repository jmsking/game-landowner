#! /usr/bin/env python3

import logging

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Logger:

    @staticmethod
    def getLog(name):
        logger = logging.getLogger(name)
        return logger