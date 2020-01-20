#! /usr/bin/env python3

from log.log import Logger
import random

from .base_process_action import BaseProcessAction
from common.hand_card_utils import HandCardUtils
from enums.card_type_enum import CardTypeEnum

logger = Logger.getLog(__file__)

class ProcessOneStrategy(BaseProcessAction):
    """
    Single card, e.g. [3], [4], [5], ...
    """
    def __init__(self, hand_card_status, primary_item, **kwargs):
        super().__init__(hand_card_status, primary_item, **kwargs)

    def run(self):
        exist_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[1] >= 1, enumerate(self.hand_card_status))))
        if self.primary_item is not None:
            exist_card = list(filter(lambda x:x > self.primary_item,exist_card))
        if len(exist_card) == 0:
            logger.debug('Can not accept the card')
            return None, None, None
        
        rnd = random.randint(0,len(exist_card)-1)
        put_card = exist_card[rnd]
        score = HandCardUtils.value_map(put_card, CardTypeEnum.CT_ONE, 1)
        return [put_card], score, put_card
            