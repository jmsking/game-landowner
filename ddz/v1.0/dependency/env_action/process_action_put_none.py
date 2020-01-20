#! /usr/bin/env python3

from log.log import Logger

from .base_process_action import BaseProcessAction

logger = Logger.getLog(__file__)

class ProcessNoneStrategy(BaseProcessAction):

    def __init__(self, hand_card_status, primary_item, **kwargs):
        super().__init__(hand_card_status, primary_item, **kwargs)

    def run(self):
        logger.debug('** Action No Put **')
        return [], 0, None