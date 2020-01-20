#! /usr/bin/env python3

from log.log import Logger
import random
import numpy as np

from .base_process_action import BaseProcessAction
from common.hand_card_utils import HandCardUtils
from enums.card_type_enum import CardTypeEnum

logger = Logger.getLog(__file__)

class ProcessThreeStrategy(BaseProcessAction):
    """
    E.g. [333], [444], [555], ......
    """

    def __init__(self, hand_card_status, primary_item, **kwargs):
        super().__init__(hand_card_status, primary_item, **kwargs)

    def run(self):
        k = self.kwargs.pop('k', 1)
        exist_card = HandCardUtils.find_even_three(self.hand_card_status, k=k)
        if self.primary_item is not None:
            exist_card = list(filter(lambda x:x > self.primary_item,exist_card))
        if len(exist_card) == 0:
           logger.debug('Can not accept the card')
           return None, None, None
        rnd = random.randint(0,len(exist_card)-1)
        one_card = exist_card[rnd]
        exist_card = [one_card - ix for ix in reversed(range(k))]
        score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_THREE, 6)
        put_card = list(map(lambda x:[x]*3, exist_card))
        put_card = np.reshape(put_card, (1, -1)).tolist()[0]
        return put_card, score, exist_card[-1]