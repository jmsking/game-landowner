#! /usr/bin/env python3

from log.log import Logger
import random

from .base_process_action import BaseProcessAction
from common.hand_card_utils import HandCardUtils
from enums.card_type_enum import CardTypeEnum

logger = Logger.getLog(__file__)

class ProcessContinueStrategy(BaseProcessAction):
    """
    E.g. [34567], [456789], [89TJQKA], ...
    """
    def __init__(self, hand_card_status, primary_item, **kwargs):
        super().__init__(hand_card_status, primary_item, **kwargs)

    def run(self):
        k = self.kwargs.pop('k', 5)
        exist_card = HandCardUtils.find_continues(self.hand_card_status, k=k)
        if self.primary_item is not None:
            exist_card = list(filter(lambda x:x > self.primary_item,exist_card))
        if len(exist_card) == 0:
            logger.debug('Can not accept the card')
            return None, None, None
        rnd = random.randint(0,len(exist_card)-1)
        one_card = exist_card[rnd]
        put_card = [one_card - ix for ix in reversed(range(k))]
        score = HandCardUtils.value_map(put_card[-1], CardTypeEnum.CT_CONTINUE, k)
        return put_card, score, put_card[-1]