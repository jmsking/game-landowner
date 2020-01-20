#! /usr/bin/env python3

import random
from enums.card_type_enum import CardTypeEnum
from enums.card_enum import CardEnum
from enums.action_type_enum import ActionTypeEnum
from config import config

class HandCardUtils(object):

    """ 根据手牌计算得到手牌状态
    """
    @staticmethod
    def obtain_hand_card_status(hand_card_seq):
        hand_card_status = [0 for _ in range(18)]
        for item in hand_card_seq:
            hand_card_status[item] += 1
        return hand_card_status

    """ 查找k连对(返回最大值)
    """
    @staticmethod
    def find_even_pair(hand_card_status, k):
        assert k >= 1
        if k == 1:
            exist_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[1] >= 2, enumerate(hand_card_status))))
            return exist_card
        exist_card = list(map(lambda x:x[0],
                filter(lambda x: x[1] in (2,3) and x[0] != CardEnum.TW.value, enumerate(hand_card_status))))
        even_pair = list()
        if len(exist_card) == 1:
            return even_pair
        for ix in range(len(exist_card)-k+1):
            tmp = list()
            curr_item = exist_card[ix]
            tmp.append(curr_item)
            for nx in range(k-1):
                next_item = exist_card[ix+nx+1]
                if next_item - curr_item == nx+1:
                    tmp.append(next_item)
            if len(tmp) == k:
                even_pair.append(tmp)
        if len(even_pair) == 0:
            return even_pair
        even_pair = list(map(lambda x:x[-1], even_pair))
        return even_pair

    """ 查找k连飞机(最大值)
    """
    @staticmethod
    def find_even_three(hand_card_status, k):
        assert k >= 1
        if k == 1:
            exist_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[1] >= 3, enumerate(hand_card_status))))
            return exist_card
        exist_card = list(map(lambda x:x[0], 
                filter(lambda x: x[1] == 3 and x[0] != CardEnum.TW.value, enumerate(hand_card_status))))
        even_pair = list()
        if isinstance(exist_card, int):
            exist_card = [exist_card]
        if len(exist_card) == 1:
            return even_pair
        for ix in range(len(exist_card)-k+1):
            tmp = list()
            curr_item = exist_card[ix]
            tmp.append(curr_item)
            for nx in range(k-1):
                next_item = exist_card[ix+nx+1]
                if next_item - curr_item == nx+1:
                    tmp.append(next_item)
            if len(tmp) == k:
                even_pair.append(tmp)
        if len(even_pair) == 0:
            return even_pair
        even_pair = list(map(lambda x:x[-1], even_pair))
        return even_pair

    """
    查找连子(最大值)
    """
    @staticmethod
    def find_continues(hand_card_status, k):
        contin_pair = list()
        # 去掉2及大小王
        exclude_list = [CardEnum.TW.value, CardEnum.QU.value, CardEnum.JA.value]
        pure_list = list(map(lambda x:x[0],
                    filter(lambda x:x[0] not in exclude_list and x[1] >= 1, enumerate(hand_card_status))))
        if len(pure_list) < 5:
            return contin_pair
        for ix in range(len(pure_list)-4):
            base = pure_list[ix]
            tmp = [base]
            iy = ix + 1
            while iy < len(pure_list):
                if pure_list[iy] - base == 1:
                    tmp.append(pure_list[iy])
                    base += 1
                else:
                    break
                if len(tmp) == k:
                    contin_pair.append(tmp.copy())
                    tmp.clear()
                    break
                iy += 1
        if len(contin_pair) == 0:
            return contin_pair
        contin_pair = list(map(lambda x:x[-1], contin_pair))
        return contin_pair

    @staticmethod
    def value_map(primary_item, card_type, card_count):
        _CONST = 90
        # 单牌
        if card_type == CardTypeEnum.CT_ONE:
            return primary_item / _CONST
        # 对子
        if card_type == CardTypeEnum.CT_DOU:
            return (primary_item * 2 + 2) / _CONST
        # 三不带
        if card_type == CardTypeEnum.CT_THREE and card_count == 3:
            return (primary_item * 3 + 3) / _CONST
        # 三不带飞机
        if card_type == CardTypeEnum.CT_THREE and card_count >= 6:
            return (primary_item * 3 + card_count) / _CONST 
        # 三带一
        if card_type == CardTypeEnum.CT_THREE_ONE and card_count == 4:
            return (primary_item * 3 + 3 + 1) / _CONST
        # 三带一飞机
        if card_type == CardTypeEnum.CT_THREE_ONE and card_count >= 8:
            return (primary_item * 3 + card_count + 1) / _CONST
        # 三带一对
        if card_type == CardTypeEnum.CT_THREE_DOU and card_count == 5:
            return (primary_item * 3 + 6) / _CONST
        # 三带一对飞机
        if card_type == CardTypeEnum.CT_THREE_DOU and card_count >= 10:
            return (primary_item * 3 + card_count + 12 ) / _CONST      
        # 连子
        if card_type == CardTypeEnum.CT_CONTINUE:
            return (primary_item * (card_count - 3)) / _CONST
        # 四带两单
        if card_type == CardTypeEnum.CT_FOUR_ONE:
            return (primary_item * 5) / _CONST
        # 四带两对
        if card_type == CardTypeEnum.CT_FOUR_DOU:
            return (primary_item * 5) / _CONST
        # 炸弹(王炸)
        if card_type == CardTypeEnum.CT_BOMB and card_count == 2:
            return 1
        # 炸弹(普通炸弹)
        if card_type == CardTypeEnum and card_count == 4:
            return (primary_item * 6) / _CONST

        return 0


if __name__ == '__main__':

   pass