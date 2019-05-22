#! /usr/bin/env python3

from __future__ import absolute_import, print_function, division
import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from abstract_value_calculator import AbstractValueCalculator
import random
from hand_card_utils import HandCardUtils
from card_type_enum import CardTypeEnum
from action_type_enum import ActionTypeEnum
from card_enum import CardEnum
import numpy as np
import copy
import all_card
from player_role_enum import PlayerRoleEnum

"""
单牌奖赏计算器
"""
class P_1_CardCalc(AbstractValueCalculator):
    
    @staticmethod
    def obtain_reward(hand_card_status, surround, *args):
        not_afford = False
        last_player_role, last_card_type_struct, last_action = args[0], args[1], args[2]
        if len(args) != 3:
            last_player_role, last_card_type_struct, last_action = None, None, None
        primary_item = None
        if last_card_type_struct is not None:
            primary_item = last_card_type_struct.primary_item
        exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] >= 1, enumerate(hand_card_status))))
        if isinstance(exist_card, int):
            exist_card = [exist_card]
        if primary_item is not None:
            exist_card = list(filter(lambda x:x > primary_item,exist_card))
            if isinstance(exist_card, int):
                exist_card = [exist_card]
        if len(exist_card) == 0:
            not_afford = True
        else:
            rnd = random.randint(0,len(exist_card)-1)
            put_card = exist_card[rnd]
            score = HandCardUtils.value_map(put_card, CardTypeEnum.CT_ONE, 1)
            self.observation[put_card] -= 1
            self.observation[18+put_card] += 1
            self.hand_card_status[put_card] -= 1
            self.put_card_status[put_card] += 1
            info['put_card'] = [put_card]
            info['primary_item'] = put_card
            if ENV_DEBUG:
                print('Put card %s' %put_card)


if __name__ == "__main__":
    P_1_CardCalc.obtain_reward(None, None)