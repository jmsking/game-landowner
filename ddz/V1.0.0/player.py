#! /usr/bin/env python3

from player_role_enum import PlayerRoleEnum
from hand_card_struct import HandCardStruct
from card_type_struct import CardTypeStruct
from card_type_enum import CardTypeEnum

"""
玩家定义类
"""

class Player(object):
    def __init__(self, player_id):
        # 玩家ID
        self._player_id = player_id
        # 玩家角色
        self._player_role = PlayerRoleEnum.DEFAULT
        # 手牌结构
        self._hand_card_struct = None
        # 要打出去的牌型
        self._put_card_type = CardTypeStruct()
        # 要打出去的牌(无花色)
        self._put_card = list()
        # 要打出去的牌(有花色)
        self._put_color_card = list()

    @property
    def player_id(self):
        return self._player_id

    @property
    def player_role(self):
        return self._player_role

    @player_role.setter
    def player_role(self, value):
        self._player_role = value

    """ 清空出牌序列 """
    def clear_put_card_seq(self):
        self._put_card.clear()
        self._put_color_card.clear()
        self._put_card_type = CardTypeStruct()

    """ 出一组牌 
    Args:
    current_put_card_type: 当前出牌牌型
    """
    def put_cards(self, current_put_card_type, isPassive=True):
        # 被动出牌
        if isPassive:
            pass
            # 是否存在大于该牌型的手牌
            # 找到出某个牌型后,剩余牌型的价值
            # 返回剩余牌型最大价值的方案

    """ 根据当前出的牌型进行被动出牌
    Args:
        current_put_card: class <CardTypeStruct>
    """
    def put_cards_passive(self, current_put_card):
        assert isinstance(current_put_card, CardTypeStruct), 'args must be type <CardTypeStruct>'
        # 单牌
        if current_put_card.card_type == CardTypeEnum.CT_ONE:
            pass


    """ 主动出牌 """
    def put_card_active(self):
        pass