#! /usr/bin/env python3

from card_type_struct import CardTypeStruct
from card_enum import CardEnum
import random
import config
from action_type_enum import ActionTypeEnum
from all_card import CARD_MAP

class HandCardUtils(object):

    @staticmethod
    def write_to_file(*data, to_path = config.SAMPLE_SAVE_PATH):
        with open(to_path, 'w') as f:
            f.write(config.ROUND_FLAG_1+data[0])
            f.write('\n')
            f.write(config.ROUND_FLAG_2+data[1])
            f.write('\n')

    """ 根据手牌计算得到手牌状态
    """
    @staticmethod
    def obtain_hand_card_status(hand_card_seq):
        hand_card_status = [0 for _ in range(18)]
        for item in hand_card_seq:
            hand_card_status[CARD_MAP[item]] += 1
        return hand_card_status

    """ 查找k连对(返回最大值)
    """
    @staticmethod
    def find_even_pair(hand_card_status, k):
        assert k > 1
        exist_card = list(map(lambda x:x[0], 
                filter(lambda x: x[1] in (2,3) and x[0] != CardEnum.TW.value, enumerate(hand_card_status))))
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

    """ 查找k连飞机
    """
    @staticmethod
    def find_even_three(hand_card_status, k):
        assert k > 1
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
    查找连子
    """
    @staticmethod
    def find_continues(hand_card_status, k):
        contin_pair = list()
        # 去掉2及大小王
        exclude_list = [CardEnum.TW.value, CardEnum.QU.value, CardEnum.JO.value]
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

if __name__ == '__main__':

   pass