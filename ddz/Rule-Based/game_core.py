#! /usr/bin/env python3

from card_enum import CARD_MAP
from hand_card_utils import HandCardUtils
from player_role_enum import PlayerRoleEnum
from action_type_enum import ActionTypeEnum
from hand_card_struct import HandCardStruct
from env import Env

"""
游戏核心类
"""

class GameCore():
    def __init__(self):
        self._game_is_over = False
    

    """
    获取候选的动作
    """
    def _obtain_candidate_action(self):
        return []

    """
    获取出牌
    Args:
      player: 当前玩家
      obser: 可观察到的环境信息
      last_player_role: 上一个玩家的角色
      last_card_type_struct: 上一个玩家所出牌型结构
      last_action: 上一个玩家的出牌类型
    """
    def obtain_put_card(self, player, obser, last_player_role, last_card_type_struct=None, last_action=None):
        env = Env()
        env.specify_env(None, None)
        action_reward = self._obtain_candidate_action()
        order_action = list(map(lambda x: x[0], sorted(action_reward, key=lambda x:x[1], reverse=True)))
        last_primary_item = None
        if last_card_type_struct is not None:
            last_action = last_card_type_struct.card_type
            last_primary_item = last_card_type_struct.primary_item
            order_action = list(filter(lambda x: x == last_action or x == ActionTypeEnum.ACTION_PUT_BOMB.value, order_action))
        else:
            order_action.remove(ActionTypeEnum.ACTION_NO_PUT.value)
        #print('可出牌型: {}'.format(order_action))
        can_accept = False
        accpet_action = None
        action = order_action[0]
        obser, _, done, info = env.step(action, None, last_primary_item, last_action)
        if done:
            self._game_is_over = True
        can_accept = True
        accpet_action = action
        put_card = []
        primary_item = 0
        if can_accept:
            put_card = info['put_card']
            primary_item = info['primary_item']
            self._update_curr_player(player, put_card)
        return accpet_action, put_card, primary_item

    """
    更新当前玩家信息
    Args:
      player: 当前玩家
      put_card: 当前玩家的出牌
      has_put_card_status: 当前玩家已出牌的状态
    """
    def _update_curr_player(self, player, put_card):
        hcs = HandCardStruct()
        hand_card_color_seq = player.hand_card_struct.hand_card_color_seq
        for item in put_card:
            for ix, val in enumerate(hand_card_color_seq):
                if val is not None and item == val[1]:
                    hand_card_color_seq[ix] = None
                    break

        new_seq = list(filter(lambda x:x is not None, hand_card_color_seq))
        hcs.hand_card_color_seq = new_seq
        player.hand_card_struct = hcs
