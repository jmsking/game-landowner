#! /usr/bin/env python3

#TODO remove in production environment
import sys, os
base_path = 'd:/study/me/game-landowner/ddz/V3.0.0'
sys.path.append(base_path)
from log.log import Logger

import copy
import numpy as np
from network.net import Net
from agent.player import Player
from common.common_utils import CommonUtils
from common.hand_card_utils import HandCardUtils
from enums.player_role_enum import PlayerRoleEnum
from enums.action_type_enum import ActionTypeEnum, ALL_ACTIONS, ALL_ACTION_VALUES
from dependency.env import Env

logger = Logger.getLog(__name__)

class Application:

    def __init__(self):
        pass

    def __obtain_actions(self, env, card_status, pre_action, pre_primary_item):
        available_act = []
        available_put_cards = []
        actions = [ActionTypeEnum.ACTION_NO_PUT, ActionTypeEnum.ACTION_PUT_BOMB]
        if pre_action is None:
            actions = copy.deepcopy(ALL_ACTIONS)
            actions.remove(ActionTypeEnum.ACTION_NO_PUT)
        else:
            if pre_action not in actions:
                actions.append(pre_action)
        for act in actions:
            is_valid, put_cards, _ = env.check_action(card_status, act, pre_primary_item)
            if is_valid:
                available_act.append(act)
                available_put_cards.append(put_cards)
        return available_act, available_put_cards

    def __preprocess(self, pre_put_cards, hand_card_status):
        env = Env(hand_card_status, hand_card_status, hand_card_status)
        pre_action, pre_primary_item = None, None
        if pre_put_cards:
            pre_card_status = HandCardUtils.obtain_hand_card_status(pre_put_cards)
            for act in ALL_ACTIONS:
                is_valid, put_cards, pre_primary_item = env.check_action(pre_card_status, act)
                if is_valid and \
                    np.sum(np.equal(pre_put_cards, put_cards)) == len(pre_put_cards):
                    pre_action = act
                    break
        available_actions, available_put_cards = self.__obtain_actions(env, hand_card_status,
            pre_action, pre_primary_item)
        return available_actions, available_put_cards

    def __postprocess(self, net, state, available_actions, available_put_cards):
        rewards = []
        action_onehot = CommonUtils.onehot(ALL_ACTION_VALUES)
        for action in available_actions:
            state_copy = copy.deepcopy(state)
            hand_card_status = state_copy[:18]
            desk_card_status = state_copy[18:]
            inputs = []
            inputs.extend(hand_card_status[3:])
            inputs.extend(desk_card_status[3:])
            inputs.extend(action_onehot[action.value])
            inputs = np.reshape(inputs, (1,-1))
            score = net.predict(inputs)
            rewards.append(score)
        max_idx = np.argmax(rewards)
        current_put_cards = available_put_cards[max_idx]
        return current_put_cards

    def train_net(self):
        logger.info('*** Start training network, this may cost some time ***')
        net = Net()
        net.train()

    def predict(self, state, **kwargs):
        """
        state : contain `hand_card_status`, `desk_card_status` and `player_role onehot`
        """
        logger.info('*** Start predicting ***')
        # obtain the put card of other player
        put_cards = kwargs.pop('put_cards', None)
        hand_card_status = state[:15]
        available_actions, available_put_cards = self.__preprocess(put_cards, hand_card_status)
        net = Net(is_infer=True)
        current_put_cards = self.__postprocess(net, state, available_actions, available_put_cards)
        return current_put_cards


def test_data():
    player = Player('agent', role=PlayerRoleEnum.LAND_OWNER)
    player_cards = player.obtain_init_card()
    player_cards = list(map(lambda x:x[1], player_cards))
    logger.info(f'player cards: {player_cards}')
    player_card_status = HandCardUtils.obtain_hand_card_status(player_cards)
    desk_card_status = [0]*18
    role_onehot = [1, 0, 0]
    state = []
    state.extend(player_card_status)
    state.extend(desk_card_status)
    state.extend(role_onehot)
    pre_put_cards = None
    return state, pre_put_cards

    
if __name__ == '__main__':
    application = Application()
    #application.train_net()
    state, pre_put_cards = test_data()
    logger.info(state)
    put_cards = application.predict(state, put_cards=pre_put_cards)
    logger.info(put_cards)