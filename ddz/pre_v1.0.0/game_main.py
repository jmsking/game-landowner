#! /usr/bin/env python3

from player import Player
from card_type_struct import CardTypeStruct
import time
import random
from hand_card_struct import HandCardStruct
import all_card
from player_role_enum import PlayerRoleEnum

"""
游戏主体类
"""

class GameMain(object):
    def __init__(self):
        # 地主ID
        self._land_owner_id = -1
        # 当前叫分
        self._score = 0
        # 三张底牌
        self._bottom_card = list()
        # 当前玩家
        self._players = dict()
        # 已经打出去的牌
        self._all_out_card = list()
        # 三名玩家已经打出去的牌
        self._player_out_card = dict()
        # 三名玩家剩余的手牌个数
        self._player_remain_card_count = dict()
        # 当前打出的牌型
        self._current_put_card_type = None
        # 当前游戏是否结束
        self._game_is_over = False

    """ 发牌
    """
    def deal_card(self, c):
        if c == 1:
            return all_card.ALL_CARD[:17]
        elif c == 2:
            return all_card.ALL_CARD[17:34]
        elif c == 3:
            return all_card.ALL_CARD[34:51]
        else:
            return all_card.ALL_CARD[51:]

    """ 随机一个玩家开始叫地主 """
    def call_by(self, player_ids):
        rnd = random.randint(3)
        return rnd, player_ids[rnd]

    """ 设置玩家角色 """
    def set_player_role(self, owner_ind, player_ids):
        # 地主上家
        up_player = ((owner_ind - 1) + 3) % 3
        # 地主下家
        low_player = (owner_ind + 1) % 3
        self._players[owner_ind].player_role = PlayerRoleEnum.LAND_OWNER
        self._players[up_player].player_role = PlayerRoleEnum.UP_LAND_OWNER
        self._players[low_player].player_role = PlayerRoleEnum.LOW_LAND_OWNER
        
    """ 开始游戏
    """
    def game_start(self):
        # 第一个玩家是第二个玩家的上家
        # 第二个玩家是第三个玩家的上家
        # 第三个玩家是第一个玩家的上家
        player1 = Player('001')
        id1 = player1.player_id
        print('玩家[ID=%s]进入了游戏' %id1)
        player2 = Player('002')
        id2 = player2.player_id
        print('玩家[ID=%s]进入了游戏' %id2)
        player3 = Player('003')
        id3 = player3.player_id
        print('玩家[ID=%s]进入了游戏' %id3)
        self._players[id1] = player1
        self._players[id2] = player2
        self._players[id3] = player3
        sleep_time = 1
        print('游戏%s后开始...' %sleep_time)
        for k in range(sleep_time):
            print(sleep_time-k)
            time.sleep(1)
        print('-----------------游戏开始---------------')
        random.shuffle(all_card.ALL_CARD)
        time.sleep(1)
        print('开始为玩家[ID=%s]发牌' %id1)
        hand_card = self.deal_card(1)
        hcs1 = HandCardStruct()
        hcs1.hand_card_color_seq = hand_card
        print('玩家[ID=%s]的手牌为\n%s' %(id1, hcs1.hand_card_seq))
        time.sleep(1)
        print('开始为玩家[ID=%s]发牌' %id2)
        hand_card = self.deal_card(2)
        hcs2 = HandCardStruct()
        hcs2.hand_card_color_seq = hand_card
        print('玩家[ID=%s]的手牌为\n%s' %(id2, hcs2.hand_card_seq))
        time.sleep(1)
        print('开始为玩家[ID=%s]发牌' %id3)
        hand_card = self.deal_card(3)
        hcs3 = HandCardStruct()
        hcs3.hand_card_color_seq = hand_card
        print('玩家[ID=%s]的手牌为\n%s' %(id3, hcs3.hand_card_seq))
        time.sleep(1)
        # TO DO: 目前是随机一个玩家为地主,后续需要添加抢地主环节
        rnd, self._land_owner_id = self.call_by([id1,id2,id3])
        # 设置玩家角色
        self.set_player_role(rnd, [id1,id2,id3])
        
        



if __name__ == '__main__':
    game = GameMain()
    game.game_start()