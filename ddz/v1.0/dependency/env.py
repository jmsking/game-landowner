#! /usr/bin/env python3

from __future__ import absolute_import

import random
import numpy as np
import copy

from enums.card_type_enum import CardTypeEnum
from enums.action_type_enum import ActionTypeEnum
from enums.card_enum import CardEnum
from enums.player_role_enum import PlayerRoleEnum
from common.hand_card_utils import HandCardUtils
from common.common_utils import CommonUtils
from config import config
from log.log import Logger
from .env_action import *

logger = Logger.getLog(__file__)

ACTION_MAP = {
    ActionTypeEnum.ACTION_PUT_ONE: (ProcessOneStrategy, {}),
    ActionTypeEnum.ACTION_PUT_DOU: (ProcessDouStrategy, {}),
    ActionTypeEnum.ACTION_PUT_3_DOU: (ProcessDouStrategy, {'k': 3}),
    ActionTypeEnum.ACTION_PUT_4_DOU: (ProcessDouStrategy, {'k': 4}),
    ActionTypeEnum.ACTION_PUT_5_DOU: (ProcessDouStrategy, {'k': 5}),
    ActionTypeEnum.ACTION_PUT_6_DOU: (ProcessDouStrategy, {'k': 6}),
    ActionTypeEnum.ACTION_PUT_7_DOU: (ProcessDouStrategy, {'k': 7}),
    ActionTypeEnum.ACTION_PUT_8_DOU: (ProcessDouStrategy, {'k': 8}),
    ActionTypeEnum.ACTION_PUT_9_DOU: (ProcessDouStrategy, {'k': 9}),
    ActionTypeEnum.ACTION_PUT_10_DOU: (ProcessDouStrategy, {'k': 10}),
    ActionTypeEnum.ACTION_PUT_THREE: (ProcessThreeStrategy, {}),
    ActionTypeEnum.ACTION_PUT_2_THREE: (ProcessThreeStrategy, {'k': 2}),
    ActionTypeEnum.ACTION_PUT_3_THREE: (ProcessThreeStrategy, {'k': 3}),
    ActionTypeEnum.ACTION_PUT_4_THREE: (ProcessThreeStrategy, {'k': 4}),
    ActionTypeEnum.ACTION_PUT_5_THREE: (ProcessThreeStrategy, {'k': 5}),
    ActionTypeEnum.ACTION_PUT_6_THREE: (ProcessThreeStrategy, {'k': 6}),
    ActionTypeEnum.ACTION_PUT_THREE_ONE: (ProcessThreeOneStrategy, {}),
    ActionTypeEnum.ACTION_PUT_2_THREE_ONE: (ProcessThreeOneStrategy, {'k': 2}),
    ActionTypeEnum.ACTION_PUT_3_THREE_ONE: (ProcessThreeOneStrategy, {'k': 3}),
    ActionTypeEnum.ACTION_PUT_4_THREE_ONE: (ProcessThreeOneStrategy, {'k': 4}),
    ActionTypeEnum.ACTION_PUT_5_THREE_ONE: (ProcessThreeOneStrategy, {'k': 5}),
    ActionTypeEnum.ACTION_PUT_THREE_DOU: (ProcessThreeDouStrategy, {}),
    ActionTypeEnum.ACTION_PUT_2_THREE_DOU: (ProcessThreeDouStrategy, {'k': 2}),
    ActionTypeEnum.ACTION_PUT_3_THREE_DOU: (ProcessThreeDouStrategy, {'k': 3}),
    ActionTypeEnum.ACTION_PUT_4_THREE_DOU: (ProcessThreeDouStrategy, {'k': 4}),
    ActionTypeEnum.ACTION_PUT_FOUR_ONE: (ProcessFourOneStrategy, {}),
    ActionTypeEnum.ACTION_PUT_FOUR_DOU: (ProcessFourDouStrategy, {}),
    ActionTypeEnum.ACTION_PUT_5_CONTINUE: (ProcessContinueStrategy, {'k': 5}),
    ActionTypeEnum.ACTION_PUT_6_CONTINUE: (ProcessContinueStrategy, {'k': 6}),
    ActionTypeEnum.ACTION_PUT_7_CONTINUE: (ProcessContinueStrategy, {'k': 7}),
    ActionTypeEnum.ACTION_PUT_8_CONTINUE: (ProcessContinueStrategy, {'k': 8}),
    ActionTypeEnum.ACTION_PUT_9_CONTINUE: (ProcessContinueStrategy, {'k': 9}),
    ActionTypeEnum.ACTION_PUT_10_CONTINUE: (ProcessContinueStrategy, {'k': 10}),
    ActionTypeEnum.ACTION_PUT_11_CONTINUE: (ProcessContinueStrategy, {'k': 11}),
    ActionTypeEnum.ACTION_PUT_12_CONTINUE: (ProcessContinueStrategy, {'k': 12}),
    ActionTypeEnum.ACTION_PUT_BOMB: (ProcessBombStrategy, {}),
    ActionTypeEnum.ACTION_NO_PUT: (ProcessNoneStrategy, {}),
}

class Env:
    def __init__(self, lo_card_status, llo_card_status, ulo_card_status):
        logger.info('Start init game environment')
        self.lo_card_status = lo_card_status
        self.llo_card_status = llo_card_status
        self.ulo_card_status = ulo_card_status
        self.role_generator = self.__current_agent()
        self.role = next(self.role_generator)
        self.desk_card_status = [0]*18
        self.current_state = self.__state(self.lo_card_status, self.desk_card_status)
        

    def step(self, action, **kwargs):
        """
        From a `state` to a new state by `action`
        """
        pre_primary_item = kwargs.pop('pre_primary_item', None)
        action_strategy_info = ACTION_MAP[action]
        params = action_strategy_info[1]
        strategy = action_strategy_info[0](self.hand_card_status,
                                    pre_primary_item, **params)
        put_cards, reward, primary_item, = strategy.run()
        logger.info(f'Put cards -> {put_cards}, reward -> {reward}, primary_item -> {primary_item}')
        self.__update_hand_card_status(put_cards)
        info = {'primary_item': primary_item, 'is_end': self.__is_end()}
        self.role = next(self.role_generator)
        new_state = self.__state(self.hand_card_status, self.desk_card_status)
        return reward, new_state, info

    def check_action(self, hand_card_status, action, primary_item=None):
        """
        Check the validation of `action` according to `hand_card_status`
        """
        action_strategy_info = ACTION_MAP[action]
        kwargs = action_strategy_info[1]
        strategy = action_strategy_info[0](hand_card_status, primary_item, **kwargs)
        put_cards, _, pi, = strategy.run()
        if put_cards is not None:
            return True, put_cards, pi
        return False, put_cards, pi

    @property
    def state(self):
        return self.current_state

    @property
    def hand_card_status(self):
        if self.role == PlayerRoleEnum.LAND_OWNER:
            return self.lo_card_status
        if self.role == PlayerRoleEnum.LOW_LAND_OWNER:
            return self.llo_card_status
        if self.role == PlayerRoleEnum.UP_LAND_OWNER:
            return self.ulo_card_status
        logger.error('Invalid parameter `role`, Please reference [PlayerRoleEnum]')
        return None

    def __is_end(self):
        """
        Wheather the episode is finished
        """
        if sum(self.hand_card_status) == 0:
            return True
        return False

    def __update_hand_card_status(self, put_cards):
        for card in put_cards:
            if self.role == PlayerRoleEnum.LAND_OWNER:
                self.lo_card_status[card] -= 1
            if self.role == PlayerRoleEnum.LOW_LAND_OWNER:
                self.llo_card_status[card] -= 1
            if self.role == PlayerRoleEnum.UP_LAND_OWNER:
                self.ulo_card_status[card] -= 1
            self.desk_card_status[card] += 1
    
    def __current_agent(self):
        """
        Return current player role in order
        """
        while True:
            yield PlayerRoleEnum.LAND_OWNER
            yield PlayerRoleEnum.LOW_LAND_OWNER
            yield PlayerRoleEnum.UP_LAND_OWNER

    def __state(self, hand_card_status, desk_card_status):
        # first 0,1,2 is useless
        state = hand_card_status[3:]
        state.extend(desk_card_status[3:])
        role_oh = CommonUtils.onehot()[self.role.value]
        state.extend(role_oh)
        return state
