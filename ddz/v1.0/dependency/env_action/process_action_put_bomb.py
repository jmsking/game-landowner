#! /usr/bin/env python3

from log.log import Logger
import random

from .base_process_action import BaseProcessAction
from common.hand_card_utils import HandCardUtils
from enums.card_type_enum import CardTypeEnum
from enums.card_enum import CardEnum
from enums.action_type_enum import ActionTypeEnum

logger = Logger.getLog(__file__)

class ProcessBombStrategy(BaseProcessAction):
    """
    E.g. [4444], [9999], [QUEEN JACK]
    """

    def __init__(self, hand_card_status, primary_item, **kwargs):
        super().__init__(hand_card_status, primary_item, **kwargs)

    def run(self):
        qu_ja = [CardEnum.QU.value, CardEnum.JA.value]
        comm_bomb = list(map(lambda x:x[0], filter(lambda x: x[1] == 4, enumerate(self.hand_card_status))))
        master_bomb = list(map(lambda x:x[0], filter(lambda x: x[0] in qu_ja and x[1] == 1, enumerate(self.hand_card_status))))
        if self.primary_item:
            comm_bomb = list(filter(lambda x:x > self.primary_item,comm_bomb))
        if len(comm_bomb) == 0 and len(master_bomb) < 2:
            logger.debug('Can not accept the card')
            return None, None, None
        comm_bomb.append('master')
        rnd = random.randint(0, len(comm_bomb)-1)
        one_card = comm_bomb[rnd]
        if one_card == 'master':
            put_card = qu_ja
            score = HandCardUtils.value_map(put_card[-1], CardTypeEnum.CT_BOMB, 2)
            return put_card, score, put_card[-1]
        put_card = [one_card]*4
        score = HandCardUtils.value_map(put_card[-1], CardTypeEnum.CT_BOMB, 4)
        return put_card, score, put_card[-1]
