#! /usr/bin/env python3

from log.log import Logger
import random

from .base_process_action import BaseProcessAction
from common.hand_card_utils import HandCardUtils
from enums.card_type_enum import CardTypeEnum

logger = Logger.getLog(__file__)

class ProcessFourOneStrategy(BaseProcessAction):
    """
    E.g. [333345], [333344], [555534], ......
    """

    def __init__(self, hand_card_status, primary_item, **kwargs):
        super().__init__(hand_card_status, primary_item, **kwargs)

    def run(self):
        exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] == 4, enumerate(self.hand_card_status)))) 
        if self.primary_item is not None:
            exist_card = list(filter(lambda x:x > self.primary_item,exist_card))
        if len(exist_card) == 0:
            logger.debug('Can not accept the card')
            return None, None, None
        rnd = random.randint(0,len(exist_card)-1)
        one_card = exist_card[rnd]
        remain_card = self.__flat_card(self.hand_card_status, [one_card])
        if len(remain_card) <= 1:
            logger.debug('Can not accept the card')
            return None, None, None
        other_card = sorted(random.sample(remain_card, 2))
        score = HandCardUtils.value_map(one_card, CardTypeEnum.CT_FOUR_ONE, 6)
        put_card = [one_card]*4
        put_card.extend(other_card)
        return put_card, score, one_card

    def __flat_card(self, card_status, exclude_card):
        """
        Flatten these card
        E.g.
        card status is [0,0,0,1,3,2,2,2,0,0,0,0,0,0,0,0,1,0]
        then flatten this is [3,4,4,4,5,5,6,6,7,7,QUEEN]
        """
        flat_card = []
        for card, count in enumerate(card_status):
            if card in exclude_card:
                count -= 3
            if count > 0:
                flat_card.extend([card]*count)
        return flat_card