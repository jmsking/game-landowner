#! /usr/bin/env python3

#TODO remove in production environment
import sys
base_path = 'd:/study/me/game-landowner/ddz/V3.0.0'
sys.path.append(base_path)

import copy
import random
import numpy as np

from log.log import Logger
from dependency.env import Env
from agent.player import Player
from enums.player_role_enum import PlayerRoleEnum
from enums.action_type_enum import ActionTypeEnum, ALL_ACTIONS, ALL_ACTION_VALUES
from common.hand_card_utils import HandCardUtils
from common.common_utils import CommonUtils

#from network.net import Net

logger = Logger.getLog(__file__)

"""
Every time we will get mini-batch samples from `Experience Buffer`
For classical DQN, the `Experience Buffer` store data like (St-1, At, Rt, St)
"""

MAX_BUFFER_SIZE = 1e4

class MiniBatch:

    def __init__(self, batch_size=None, role=None, epsilon=1, net=None):
        self.bs = batch_size
        self.role = role
        self.epsilon = epsilon
        self.buffer = []
        self.net = net
        #self.net = Net()

    def next(self):
        # add random to obatain new experience
        if random.random() >= 0.5:
            self.__generate()
        while len(self.buffer) < self.bs:
            self.__generate()
        return self.postprocess()

    def postprocess(self):
        """
        Generate a valid input of network and target of network
        """
        logger.info('*** Obtain mini-batch input and mini-batch target of network ***')
        batch_x = []
        batch_target = []
        batches = self.buffer[:self.bs]
        for idx, item in enumerate(batches):
            state, _, action, reward, next_state = copy.deepcopy(item)
            if idx == len(batches)-1:
                break
            action_onehot = CommonUtils.onehot(ALL_ACTION_VALUES)
            state.extend(action_onehot[action.value])
            batch_x.append(state)
            next_avaliable_actions = batches[idx+1][1]
            max_target_out = -1e10
            for act in next_avaliable_actions:
                target_inputs = next_state.copy()
                target_inputs.extend(action_onehot[act.value])
                target_inputs = np.reshape(target_inputs, (1, -1))
                #TODO use double-DQN
                target_net_out = self.net.predict(target_inputs, is_target=True)
                if target_net_out > max_target_out:
                    max_target_out = target_net_out
            batch_target.append(reward + max_target_out)

        return np.array(batch_x), np.reshape(batch_target, (-1,1))

    def __agent(self):
        # initialize three player
        lo = Player('player-01', role=PlayerRoleEnum.LAND_OWNER)
        ulo = Player('player-02', role=PlayerRoleEnum.UP_LAND_OWNER)
        llo = Player('player-03', role=PlayerRoleEnum.LOW_LAND_OWNER)
        lo_cards = lo.obtain_init_card()
        exclude_card = copy.deepcopy(lo_cards)
        ulo_cards = ulo.obtain_init_card(exclude_card=exclude_card)
        exclude_card.extend(ulo_cards)
        llo_cards = llo.obtain_init_card(exclude_card=exclude_card)
        lo_cards = list(map(lambda x:x[1], lo_cards))
        ulo_cards = list(map(lambda x:x[1], ulo_cards))
        llo_cards = list(map(lambda x:x[1], llo_cards))
        logger.info(f'Land owner cards: {lo_cards}')
        logger.info(f'Upper land owner cards: {ulo_cards}')
        logger.info(f'Lower land owner cards: {llo_cards}')
        lo_card_status = HandCardUtils.obtain_hand_card_status(lo_cards)
        ulo_card_status = HandCardUtils.obtain_hand_card_status(ulo_cards)
        llo_card_status = HandCardUtils.obtain_hand_card_status(llo_cards)
        return lo_card_status, ulo_card_status, llo_card_status

    def __generate(self):
        """
        Generate a episode sample for each player role
        """
        logger.info('Generate samples for training')
        lo_card_status, ulo_card_status, llo_card_status = self.__agent()
        env = Env(lo_card_status, llo_card_status, ulo_card_status)
        state = env.state
        # show a active agent
        active_agent = PlayerRoleEnum.LAND_OWNER
        card_status = lo_card_status
        action, primary_item = None, None
        episode = []
        is_end = False
        current_agent_generator = self.__current_agent()
        while not is_end:
            current_agent = next(current_agent_generator)
            logger.info(f'Current Agent is {current_agent}')
            if action != ActionTypeEnum.ACTION_NO_PUT:
                pre_action = action
                pre_primary_item = primary_item
            elif active_agent == current_agent:
                pre_action, pre_primary_item = None, None
            avaliable_act = self.obtain_avaliable_act(env, card_status, 
                                            pre_action, pre_primary_item)
            action = self.__choose_a_action(state, avaliable_act, current_agent)
            logger.info(f'Choose action -> {action}')
            kwargs = {'pre_primary_item':pre_primary_item}
            reward, new_state, info = env.step(action, **kwargs)
            # wheather finish a episode
            is_end = info['is_end']
            primary_item = info['primary_item']
            # recode the avaliable actions of each state for each agent
            # to obtain target network output
            # because an agent may not be able to lookthrough all actions
            # at a state
            episode.append([state, avaliable_act, action, reward, new_state])
            state = new_state
            card_status = env.hand_card_status
            logger.info(f'Next agent card status -> {card_status}')
            if action != ActionTypeEnum.ACTION_NO_PUT:
                active_agent = current_agent
        logger.info('*** Finish a episode ***')

        self.__split_by_role(episode)

    def __split_by_role(self, episode):
        """
        Split the episode samples by current agent role
        To collect experience of current agent
        And this will focus on current agent
        E.g. we collect experience samples for land-owner,
        so we will observe the state change of land-owner,
        and we will get some sequence like [St, At, Rt, St+1]
        for land-owner, show that in t-time the state of land-owner
        is `St`, when he adopt action `At` in t-time, then he
        will obtain reward `Rt` and transfer to next state `St+1`,
        and in (t+1)-time the state of land-owner is `St+1`, and when
        he adopt action `At+1` and so on.
        Note: we add `avaliable_actions` after each state
        so each record like [St, AAt, At, Rt, St+1], and `AAt` represent
        avaliable actions in t-time
        """
        start = 0
        if self.role == PlayerRoleEnum.LOW_LAND_OWNER:
            start = 1
        elif self.role == PlayerRoleEnum.UP_LAND_OWNER:
            start = 2
        episode = episode[start:]
        for idx, item in enumerate(episode):
            if idx % 3 == 0:
                #TODO fix the effecience and adopt LRU algorithm?
                if len(self.buffer) == MAX_BUFFER_SIZE:
                    del self.buffer[0]
                self.buffer.append(item)

    def obtain_avaliable_act(self, env, card_status,
                        pre_action=None, pre_primary_item=None):
        avaliable_act = []
        actions = [ActionTypeEnum.ACTION_NO_PUT, ActionTypeEnum.ACTION_PUT_BOMB]
        if pre_action is None:
            actions = copy.deepcopy(ALL_ACTIONS)
            actions.remove(ActionTypeEnum.ACTION_NO_PUT)
        else:
            if pre_action not in actions:
                actions.append(pre_action)
        for act in actions:
            if env.check_action(card_status, act, pre_primary_item)[0]:
                avaliable_act.append(act)
        return avaliable_act


    def __choose_a_action(self, state, avaliable_actions, role):
        """
        Exploration or Exploitation
        Choose a action from `avaliable_actions` base on current `state`
        """
        if random.random() < self.epsilon:
            # exploration
            action = random.choice(avaliable_actions)
            return action
        # exploitation
        oh_map = CommonUtils.onehot(ALL_ACTION_VALUES)
        max_out = -1e10
        action = None
        for act in avaliable_actions:
            inputs = copy.deepcopy(state)
            inputs.extend(oh_map[act.value])
            inputs = np.expand_dims(inputs, axis=0)
            net_out = self.net.predict(inputs)
            if net_out > max_out:
                action = act
                max_out = net_out
        return action

    def __current_agent(self):
        """
        Return current player role in order
        """
        while True:
            yield PlayerRoleEnum.LAND_OWNER
            yield PlayerRoleEnum.LOW_LAND_OWNER
            yield PlayerRoleEnum.UP_LAND_OWNER


if __name__ == '__main__':
    mini_batch = MiniBatch(batch_size=10, role=PlayerRoleEnum.LAND_OWNER)
    batch_x = mini_batch.next()
    logger.info(batch_x)


