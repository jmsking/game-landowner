#! /usr/bin/env python3

from player import Player
from card_type_struct import CardTypeStruct
import time
import random
from hand_card_struct import HandCardStruct
import all_card
from player_role_enum import PlayerRoleEnum
import tensorflow as tf
import copy
from env import Env
import numpy as np
from action_type_enum import ActionTypeEnum
import config
from hand_card_utils import HandCardUtils
from card_color_enum import CardColorEnum
from card_enum import CARD_MAP

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
        # 所有玩家
        self._players = dict()
        # 已经打出去的牌
        self._all_out_card = list()
        # 记录当前打出去牌的个数(初始时没有一张牌打出去)
        self._put_card_status = [0]*18
        # 三名玩家已经打出去的牌
        self._player_out_card = dict()
        # 三名玩家剩余的手牌个数
        self._player_remain_card_count = dict()
        # 当前打出的牌型
        self._current_put_card_type = None
        # 当前游戏是否结束
        self._game_is_over = False

        # 延迟时间
        self._sleep_time = 0

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

    """ 玩家开始叫地主 """
    def call_by(self, player_ids):
        rnd = random.randint(0,2)
        player1 = self._players[player_ids[0]]
        player2 = self._players[player_ids[1]]
        player3 = self._players[player_ids[2]]
        # 0: 不抢
        # 1: 抢地主
        # 2: 加倍
        # 3: 超级加倍
        curr_call_ind = rnd
        next_call_ind = rnd
        grab_level = 0
        is_grab = [True]*3
        while True:
            grab_ind_list = list(map(lambda x:x[0], filter(lambda x:x[1], enumerate(is_grab))))
            if len(grab_ind_list) == 1:
                curr_call_ind = grab_ind_list[0]
                return curr_call_ind, player_ids[curr_call_ind]
            if next_call_ind == 0 and is_grab[0]:
                curr_grab_level = input('玩家[ID=%s]是否抢地主(需要大于%d).[0: 不抢, 1: 抢地主, 2: 加倍, 3: 超级加倍]' %(player1.player_id, grab_level))
                curr_grab_level = int(curr_grab_level)
                if curr_grab_level == 3:
                    curr_call_ind = 0
                    return curr_call_ind, player_ids[curr_call_ind]
                if curr_grab_level > grab_level:
                    curr_call_ind = 0
                    grab_level = curr_grab_level
                else:
                    is_grab[0] = False
                next_call_ind = 1
            elif next_call_ind == 1 and is_grab[1]:
                init_value = player2.hand_card_struct.hand_card_value
                print(player2.player_id)
                print(init_value)  
                if init_value < 0.1:
                    print('玩家[ID=%s]不抢' %player2.player_id)
                    is_grab[1] = False
                elif init_value >= 0.1 and init_value < 0.5:
                    if grab_level == 0:
                        print('玩家[ID=%s]抢地主' %player2.player_id)
                        grab_level = 1
                        curr_call_ind = 1
                    else:
                        print('玩家[ID=%s]不抢' %player2.player_id)
                        is_grab[1] = False
                elif init_value >= 0.5 and init_value < 1:
                    if grab_level <= 1:
                        print('玩家[ID=%s]加倍' %player2.player_id)
                        grab_level = 2
                    else:
                        print('玩家[ID=%s]不抢' %player2.player_id)
                        is_grab[1] = False
                elif init_value >= 1:
                    print('玩家[ID=%s]超级加倍' %player2.player_id)
                    grab_level = 3
                    return curr_call_ind, player_ids[curr_call_ind]
                next_call_ind = 2
            elif next_call_ind == 2 and is_grab[2]:
                init_value = player3.hand_card_struct.hand_card_value
                print(player3.player_id)
                print(init_value)  
                if init_value < 0.1:
                    print('玩家[ID=%s]不抢' %player3.player_id)
                    is_grab[2] = False
                elif init_value >= 0.1 and init_value < 0.5:
                    if grab_level == 0:
                        print('玩家[ID=%s]抢地主' %player3.player_id)
                        grab_level = 1
                    else:
                        print('玩家[ID=%s]不抢' %player3.player_id)
                        is_grab[2] = False
                elif init_value >= 0.5 and init_value < 1:
                    if grab_level <= 1:
                        print('玩家[ID=%s]加倍' %player3.player_id)
                        grab_level = 2
                    else:
                        print('玩家[ID=%s]不抢' %player3.player_id)
                        is_grab[2] = False
                elif init_value >= 1:
                    print('玩家[ID=%s]超级加倍' %player3.player_id)
                    grab_level = 3
                    return curr_call_ind, player_ids[curr_call_ind]
                next_call_ind = 0
            else:
                print('请重新开局')
                return None, None

    """ 设置玩家角色 """
    def set_player_role(self, owner_ind, player_ids):
        owner_player_id = player_ids[owner_ind]
        # 地主上家
        up_player = ((owner_ind - 1) + 3) % 3
        up_player_id = player_ids[up_player]
        # 地主下家
        low_player = (owner_ind + 1) % 3
        low_player_id = player_ids[low_player]
        self._players[owner_player_id].player_role = PlayerRoleEnum.LAND_OWNER
        self._players[up_player_id].player_role = PlayerRoleEnum.UP_LAND_OWNER
        self._players[low_player_id].player_role = PlayerRoleEnum.LOW_LAND_OWNER

    human_player_id = None

    def human_agent_battle(self):
        global human_player_id
        human_name = input('请输入人类玩家名称:')
        human_name = "灭霸" if len(human_name) == 0 else human_name
        human_player_id = human_name
        player1 = Player(human_name)
        id1 = player1.player_id
        print('玩家[ID=%s]进入了游戏' %id1)
        player2 = Player('机器人-狗蛋')
        id2 = player2.player_id
        print('玩家[ID=%s]进入了游戏' %id2)
        player3 = Player('机器人-猫屎')
        id3 = player3.player_id
        print('玩家[ID=%s]进入了游戏' %id3)
        self._players[id1] = player1
        self._players[id2] = player2
        self._players[id3] = player3
        sleep_time = 3
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
        player1.hand_card_struct = hcs1
        print('玩家[ID=%s]的手牌为\n%s' %(id1, hcs1.hand_card_seq))
        time.sleep(1)
        print('开始为玩家[ID=%s]发牌' %id2)
        hand_card = self.deal_card(2)
        hcs2 = HandCardStruct()
        hcs2.hand_card_color_seq = hand_card
        player2.hand_card_struct = hcs2
        print('玩家[ID=%s]的手牌为\n%s' %(id2, hcs2.hand_card_seq))
        time.sleep(1)
        print('开始为玩家[ID=%s]发牌' %id3)
        hand_card = self.deal_card(3)
        hcs3 = HandCardStruct()
        hcs3.hand_card_color_seq = hand_card
        player3.hand_card_struct = hcs3
        print('玩家[ID=%s]的手牌为\n%s' %(id3, hcs3.hand_card_seq))
        time.sleep(1)
        # 叫地主
        land_rnd, self._land_owner_id = self.call_by([id1,id2,id3])
        print('地主被玩家[ID=%s]抢到' %self._land_owner_id)
        # 设置玩家角色
        self.set_player_role(land_rnd, [id1,id2,id3])
        for player in self._players.values():
            if player.player_role == PlayerRoleEnum.LAND_OWNER:
                print('玩家[ID=%s]为地主' %player.player_id)
            elif player.player_role == PlayerRoleEnum.UP_LAND_OWNER:
                print('玩家[ID=%s]为地主上家' %player.player_id)
            elif player.player_role == PlayerRoleEnum.LOW_LAND_OWNER:
                print('玩家[ID=%s]为地主下家' %player.player_id)
            else:
                print('Game running error')
                return
        self._bottom_card = self.deal_card(0)
        print('三张底牌为 %s' %self._bottom_card)
        land_hand_card = self.deal_card(land_rnd+1)
        land_hand_card += self._bottom_card
        land_hcs = HandCardStruct()
        land_hcs.hand_card_color_seq = land_hand_card
        land_player = self._players[self._land_owner_id]
        land_player.hand_card_struct = land_hcs
        print('地主[ID=%s]的手牌为\n%s' %(land_player.player_id, land_hcs.hand_card_seq))

    def set_game_env_test(self):
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
        sleep_time = 3
        print('游戏%s后开始...' %sleep_time)
        for k in range(sleep_time):
            print(sleep_time-k)
            time.sleep(1)
        print('-----------------游戏开始---------------')
        random.shuffle(all_card.ALL_CARD)
        time.sleep(1)
        print('开始为玩家[ID=%s]发牌' %id1)
        hand_card = [(CardColorEnum.SPADE,3), (CardColorEnum.SPADE,3), 
            (CardColorEnum.SPADE,4), (CardColorEnum.SPADE,4), 
            (CardColorEnum.SPADE,6), (CardColorEnum.SPADE,7), 
            (CardColorEnum.SPADE,7), (CardColorEnum.SPADE,7), 
            (CardColorEnum.SPADE,8), (CardColorEnum.SPADE,10), 
            (CardColorEnum.SPADE,10), (CardColorEnum.SPADE,11), 
            (CardColorEnum.SPADE,11), (CardColorEnum.SPADE,12), 
            (CardColorEnum.SPADE,12), (CardColorEnum.SPADE,12), 
            (CardColorEnum.SPADE,12), (CardColorEnum.SPADE,15), 
            (CardColorEnum.SPADE,15), (CardColorEnum.SPADE,16)]
        hcs1 = HandCardStruct()
        hcs1.hand_card_color_seq = hand_card
        player1.hand_card_struct = hcs1
        print('玩家[ID=%s]的手牌为\n%s' %(id1, hcs1.hand_card_seq))
        time.sleep(1)
        print('开始为玩家[ID=%s]发牌' %id2)
        hand_card = [(CardColorEnum.SPADE,3), (CardColorEnum.SPADE,3), 
            (CardColorEnum.SPADE,4), (CardColorEnum.SPADE,5), 
            (CardColorEnum.SPADE,8), (CardColorEnum.SPADE,8), 
            (CardColorEnum.SPADE,8), (CardColorEnum.SPADE,9), 
            (CardColorEnum.SPADE,9), (CardColorEnum.SPADE,10), 
            (CardColorEnum.SPADE,11), (CardColorEnum.SPADE,13), 
            (CardColorEnum.SPADE,13), (CardColorEnum.SPADE,13), 
            (CardColorEnum.SPADE,14), (CardColorEnum.SPADE,14), (CardColorEnum.SPADE,15)]
        hcs2 = HandCardStruct()
        hcs2.hand_card_color_seq = hand_card
        player2.hand_card_struct = hcs2
        print('玩家[ID=%s]的手牌为\n%s' %(id2, hcs2.hand_card_seq))
        time.sleep(1)
        print('开始为玩家[ID=%s]发牌' %id3)
        hand_card = [(CardColorEnum.SPADE,4), (CardColorEnum.SPADE,5), 
            (CardColorEnum.SPADE,5), (CardColorEnum.SPADE,5), 
            (CardColorEnum.SPADE,6), (CardColorEnum.SPADE,6), 
            (CardColorEnum.SPADE,6), (CardColorEnum.SPADE,7), 
            (CardColorEnum.SPADE,9), (CardColorEnum.SPADE,9),
            (CardColorEnum.SPADE,10), (CardColorEnum.SPADE,11), 
            (CardColorEnum.SPADE,13), (CardColorEnum.SPADE,14), 
            (CardColorEnum.SPADE,14), (CardColorEnum.SPADE,15), (CardColorEnum.SPADE,17)]
        hcs3 = HandCardStruct()
        hcs3.hand_card_color_seq = hand_card
        player3.hand_card_struct = hcs3
        print('玩家[ID=%s]的手牌为\n%s' %(id3, hcs3.hand_card_seq))
        time.sleep(1)
        # TO DO: 目前是随机一个玩家为地主,后续需要添加抢地主环节
        land_rnd, self._land_owner_id = 0, id1
        print('地主被玩家[ID=%s]抢到' %self._land_owner_id)
        # 设置玩家角色
        self.set_player_role(land_rnd, [id1,id2,id3])
        for player in self._players.values():
            if player.player_role == PlayerRoleEnum.LAND_OWNER:
                print('玩家[ID=%s]为地主' %player.player_id)
            elif player.player_role == PlayerRoleEnum.UP_LAND_OWNER:
                print('玩家[ID=%s]为地主上家' %player.player_id)
            elif player.player_role == PlayerRoleEnum.LOW_LAND_OWNER:
                print('玩家[ID=%s]为地主下家' %player.player_id)
            else:
                print('Game running error')
                return
        #self._bottom_card = self.deal_card(0)
        #print('三张底牌为 %s' %self._bottom_card)
        #land_hand_card = self.deal_card(land_rnd+1)
        #land_hand_card += self._bottom_card
        #land_hcs = HandCardStruct()
        #land_hcs.hand_card_color_seq = land_hand_card
        #land_player = self._players[self._land_owner_id]
        #land_player.hand_card_struct = land_hcs
        #print('地主[ID=%s]的手牌为\n%s' %(land_player.player_id, land_hcs.hand_card_seq))

    def set_game_env(self):
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
        sleep_time = self._sleep_time
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
        player1.hand_card_struct = hcs1
        print('玩家[ID=%s]的手牌为\n%s' %(id1, hcs1.hand_card_seq))
        time.sleep(1)
        print('开始为玩家[ID=%s]发牌' %id2)
        hand_card = self.deal_card(2)
        hcs2 = HandCardStruct()
        hcs2.hand_card_color_seq = hand_card
        player2.hand_card_struct = hcs2
        print('玩家[ID=%s]的手牌为\n%s' %(id2, hcs2.hand_card_seq))
        time.sleep(1)
        print('开始为玩家[ID=%s]发牌' %id3)
        hand_card = self.deal_card(3)
        hcs3 = HandCardStruct()
        hcs3.hand_card_color_seq = hand_card
        player3.hand_card_struct = hcs3
        print('玩家[ID=%s]的手牌为\n%s' %(id3, hcs3.hand_card_seq))
        time.sleep(1)
        # TO DO: 目前是随机一个玩家为地主,后续需要添加抢地主环节
        land_rnd, self._land_owner_id = self.call_by([id1,id2,id3])
        print('地主被玩家[ID=%s]抢到' %self._land_owner_id)
        # 设置玩家角色
        self.set_player_role(land_rnd, [id1,id2,id3])
        for player in self._players.values():
            if player.player_role == PlayerRoleEnum.LAND_OWNER:
                print('玩家[ID=%s]为地主' %player.player_id)
            elif player.player_role == PlayerRoleEnum.UP_LAND_OWNER:
                print('玩家[ID=%s]为地主上家' %player.player_id)
            elif player.player_role == PlayerRoleEnum.LOW_LAND_OWNER:
                print('玩家[ID=%s]为地主下家' %player.player_id)
            else:
                print('Game running error')
                return
        self._bottom_card = self.deal_card(0)
        print('三张底牌为 %s' %self._bottom_card)
        land_hand_card = self.deal_card(land_rnd+1)
        land_hand_card += self._bottom_card
        land_hcs = HandCardStruct()
        land_hcs.hand_card_color_seq = land_hand_card
        land_player = self._players[self._land_owner_id]
        land_player.hand_card_struct = land_hcs
        print('地主[ID=%s]的手牌为\n%s' %(land_player.player_id, land_hcs.hand_card_seq))

    """
    得到玩家顺序
    地主出牌 -> 地主下家出牌 -> 地主上家出牌
    """
    def get_player_order(self):
        order_player_ids = ['0']*3
        for player_id, player in self._players.items():
            if player.player_role == PlayerRoleEnum.LAND_OWNER:
                order_player_ids[0] = player_id
            elif player.player_role == PlayerRoleEnum.UP_LAND_OWNER:
                order_player_ids[2] = player_id
            elif player.player_role == PlayerRoleEnum.LOW_LAND_OWNER:
                order_player_ids[1] = player_id
            else:
                print('Game running error')
        return order_player_ids

    """
    获取玩家 title
    """
    def get_player_role_title(self, curr_player_id):
        player = self._players[curr_player_id]
        if player.player_role == PlayerRoleEnum.LAND_OWNER:
            return "地主"
        elif player.player_role == PlayerRoleEnum.UP_LAND_OWNER:
            return "上家"
        elif player.player_role == PlayerRoleEnum.LOW_LAND_OWNER:
            return "下家"
        else:
            return ""


    """
    更新当前玩家信息
    """
    def _update_curr_player(self, curr_player_id, put_card):
        player = self._players[curr_player_id]
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
        for item in put_card:
            self._put_card_status[item] += 1

    """
    当前玩家出牌过程
    Args: 
    curr_player_id -> 当前出牌玩家ID
    net_out -> 网络输出的最大期望奖励值
    last_card_type_struct -> 上家出的牌型结构
    """
    def put_card_process(self, sess, env, curr_player_id, net_out, last_card_type_struct=None, last_action=None):
        curr_player = self._players[curr_player_id]
        print('玩家[ID=%s ROLE=%s]当前手牌: %s' %(curr_player_id, self.get_player_role_title(curr_player_id), curr_player.hand_card_struct.hand_card_seq))
        if curr_player_id == None:
        #if curr_player_id == human_player_id:
            while True:
                input_card = input('请玩家[ID=%s]出牌(多张牌以空格分隔)' %(curr_player_id))
                if len(input_card) == 0 and last_action is not None:
                    return None, [], None
                input_card = input_card.split()

                input_card_temp = []
                new_dict = {v : k for k, v in CARD_MAP.items()}
                for card in input_card:
                    card_temp = card.capitalize()
                    if card_temp in new_dict:
                        input_card_temp.append(new_dict[card_temp])
                    elif card.isdigit() and int(card) >= 0 and int(card) <= 10:
                        input_card_temp.append(int(card))

                input_card = list(map(lambda x:int(x), input_card_temp))
                print(input_card)
                
                is_contain = HandCardUtils.is_contain_card(curr_player.hand_card_struct.hand_card_status, input_card)
                is_find, cts = HandCardUtils.is_one_hand(input_card)
                is_meet = True
                print(is_contain)
                print(is_find)
                print(is_meet)
                if is_contain and is_find and last_action:
                    is_meet = False
                    last_primary_item = last_card_type_struct.primary_item
                    card_type = cts.card_type
                    primary_item = cts.primary_item
                    card_count = cts.card_count
                    if last_action == ActionTypeEnum.ACTION_PUT_BOMB.value:
                        if card_type == last_action and card_count == 2:
                            is_meet = True
                        elif card_type == last_action and card_count == 4 and primary_item > last_primary_item:
                            is_meet = True
                    else:
                        if card_type == ActionTypeEnum.ACTION_PUT_BOMB.value:
                            is_meet = True
                        elif card_type == last_action and primary_item > last_primary_item:
                            is_meet = True
                if is_contain and is_find and is_meet:
                    self._update_curr_player(curr_player_id, input_card)
                    if len(curr_player.hand_card_struct.hand_card_seq) == 0:
                        self._game_is_over = True
                    return cts.card_type, input_card, cts.primary_item
                else:
                    print('所出牌型不合理')    
        action_reward = list()
        n_action = 27
        n_input = config.N_INPUT
        hcs = curr_player.hand_card_struct
        hand_card_status = hcs.hand_card_status
        # 判断是否是一手牌
        #if HandCardUtils.is_one_hand(hand_card_status):

        put_card_status = self._put_card_status
        obser = env.specify_env(hand_card_status, put_card_status, curr_player.player_role)
        #print('curr obser:{}'.format(obser))
        for action in range(n_action):
            act = [0] * n_action
            act[action] = 1
            x = copy.deepcopy(obser)
            x.extend(act)
            x = np.reshape(x, [1, n_input+n_action])
            out = sess.run(net_out, feed_dict={'input_x:0': x})[0][0]
            action_reward.append((action, out))
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
        for action in order_action:
            obser, _, done, info = env.step(action, last_primary_item, last_action)
            error = info['error']
            if not error:
                if done:
                    self._game_is_over = True
                can_accept = True
                accpet_action = action
                break
            env.restore()
        put_card = []
        primary_item = 0
        if can_accept:
            put_card = info['put_card']
            primary_item = info['primary_item']
            self._update_curr_player(curr_player_id, put_card)
        return accpet_action, put_card, primary_item

    """ 开始游戏
    """
    def game_start(self):
        self.set_game_env_test()
        #self.human_agent_battle()
        order_player_ids = self.get_player_order()
        env = Env()
        k = 0
        with tf.Session() as sess:
            saver = tf.train.import_meta_graph(config.MODEL_META_PATH)
            model_file=tf.train.latest_checkpoint(config.MODEL_PATH)
            saver.restore(sess,model_file)
            net_out = tf.get_collection('net_out')
            lcts = None
            last_action = None
            # 当前获有牌权的玩家ID
            curr_master_id = order_player_ids[k]
            while not self._game_is_over:
                curr_player_id = order_player_ids[k]
                # 进行主动出牌
                if curr_player_id == curr_master_id:
                    lcts = None
                    last_action = None
                # 当前玩家出牌
                action, put_card, primary_item = self.put_card_process(sess, env, curr_player_id, net_out, lcts, last_action)
                if len(put_card) > 0:
                    put_card_temp = []
                    time.sleep(self._sleep_time)
                    for x in put_card:
                        if x in CARD_MAP:
                            put_card_temp.append(CARD_MAP[x])
                        else:
                            put_card_temp.append(x)

                    print('玩家[ID=%s]出牌 -> %s \n' %(curr_player_id, put_card_temp))
                    curr_master_id = order_player_ids[k]
                    lcts = CardTypeStruct()
                    lcts.card_type = action
                    lcts.card_count = len(put_card)
                    lcts.primary_item = primary_item
                    last_action = action
                else:
                    time.sleep(self._sleep_time)
                    print('玩家[ID=%s]要不起 \n' %(curr_player_id))
                # 轮到下一个玩家
                k = (k + 1) % 3
        time.sleep(self._sleep_time)
        print('Game over \n')
        



if __name__ == '__main__':
    game = GameMain()
    game.game_start()