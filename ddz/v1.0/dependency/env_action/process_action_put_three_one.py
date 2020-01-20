#! /usr/bin/env python3

from log.log import Logger
import random
import numpy as np

from .base_process_action import BaseProcessAction
from common.hand_card_utils import HandCardUtils
from enums.card_type_enum import CardTypeEnum

logger = Logger.getLog(__file__)

class ProcessThreeOneStrategy(BaseProcessAction):
    """
    E.g. [3334], [4443], [5556], ......
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
        remain_card = self.__flat_card(self.hand_card_status, exist_card)
        if len(remain_card) < k:
            logger.debug('Can not accept the card')
            return None, None, None
        other_card = sorted(random.sample(remain_card, k))
        score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_THREE_DOU, 3*k+k)
        put_card = list(map(lambda x:[x]*3, exist_card))
        put_card = np.reshape(put_card, (1, -1)).tolist()[0]
        put_card.extend(other_card)
        return put_card, score, exist_card[-1]

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
