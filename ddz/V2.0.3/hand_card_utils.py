#! /usr/bin/env python3

from card_type_struct import CardTypeStruct
from card_type_enum import CardTypeEnum
from card_enum import CardEnum
import random
import config

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

    """ 是否包含连对/飞机 """
    @staticmethod
    def is_find(hand_card):
        isFind = True
        for k in range(len(hand_card) - 1):
            diff = hand_card[k+1] - hand_card[k]
            if diff != 1:
                isFind = False
                break
        return isFind

    """ 根据手牌状态判断是否是一手牌 """
    @staticmethod
    def is_one_hand(self, hand_card_status):
        assert len(hand_card_status) == 18, 'the size of hand card status must be 18.'
        card_count = sum(hand_card_status)
        find_one = list(map(lambda x:x[0],filter(lambda x : x[1] == 1, enumerate(hand_card_status))))
        find_two = list(map(lambda x:x[0],filter(lambda x : x[1] == 2, enumerate(hand_card_status))))
        find_three = list(map(lambda x:x[0],filter(lambda x : x[1] == 3, enumerate(hand_card_status))))
        find_four = list(map(lambda x:x[0],filter(lambda x : x[1] == 4, enumerate(hand_card_status))))
        # 单牌
        if card_count == 1:
            return True
        # 对子(包含连对)
        if card_count % 2 == 0 and card_count > 0 and len(find_two) >= 1:
            # 列表中只含对子且对子中不含2
            if len(find_two) * 2 == card_count and CardEnum.TW.value not in find_two:
                if HandCardUtils.is_find(find_two):
                    return True
        #三带一单(连三带一单)
        if card_count % 4 == 0 and card_count > 0 and len(find_three) >= 1:
            # 三带一单
            if len(find_three) == 1 and len(find_one) == 1:
                return True
            elif len(find_three) * 3 + len(find_one) == card_count and CardEnum.TW.value not in find_three:
                if HandCardUtils.is_find(find_three):
                    return True
        #三带一对(连三带一对)
        if card_count % 5 == 0 and card_count > 0 and len(find_three) >= 1:
            # 三带一对
            if len(find_two) == 1 and len(find_three) == 1:
                return True
            elif len(find_three) * 3 + len(find_two) * 2 == card_count and CardEnum.TW.value not in find_three:
                if HandCardUtils.is_find(find_three):
                   return True
        # 连子
        if card_count >= 5:
            # 必须都是单牌
            if len(find_one) == card_count:
                arr = set(find_one)
                exclude_arr = {CardEnum.TW.value, CardEnum.JA.value, CardEnum.QU.value}
                # 连子中不能包含2和大小王
                if len(list(arr.intersection(exclude_arr))) == 0:
                    if HandCardUtils.is_find(find_one):
                        return True
        # 四带两单
        if card_count == 6 and len(find_four) >= 1:
            if len(find_four) == 1 and len(find_one) == 2:
                return True
        # 四带两对
        if card_count == 8 and len(find_four) >= 1:
            if len(find_four) == 1 and len(find_two) == 2:
                return True
        # 三不带(连三不带)
        if card_count % 3 == 0 and card_count > 0 and len(find_three) >= 1:
            if len(find_three) == 1:
                return True
            # 连三不带里面不能包含2
            elif len(find_three) * 3 == card_count and CardEnum.TW.value not in find_three:
                if HandCardUtils.is_find(find_three):
                    return True
        # 炸弹(王炸)
        if card_count == 2:
            if len(find_one) == 2 and find_one[0] == CardEnum.QU.value and find_one[1] == CardEnum.JA.value:
                return True
        # 炸弹(普通炸弹)
        if card_count == 4 and len(find_four) >= 1:
            if len(find_four) == 1:
                return True
        return False

    @staticmethod
    def value_map(primary_item, card_type, card_count):
        _CONST = config.SCORE_RATIO
        _BASE_SCORE = 10
        diff = (primary_item - _BASE_SCORE)
        #score = [0 for i in range(9)]
        #random.seed(primary_item+card_type.value)
        #random.shuffle(score)
        # 单牌
        if card_type == CardTypeEnum.CT_ONE:
            reward = 0
            if diff >= 0:
                reward = (primary_item) / _CONST
            else:
                reward = (primary_item - diff) / _CONST
            return reward
        # 对子
        if card_type == CardTypeEnum.CT_DOU:
            reward = 0
            if diff >= 0:
                reward = (primary_item) / _CONST
            else:
                reward = (primary_item - diff + 1) / _CONST
            return reward
        # 三不带
        if card_type == CardTypeEnum.CT_THREE and card_count == 3:
            reward = 0
            if diff >= 0:
                reward = (primary_item) / _CONST
            else:
                reward = (primary_item - diff + 2) / _CONST
            return reward
        # 三不带飞机
        if card_type == CardTypeEnum.CT_THREE and card_count >= 6:
            reward = 0
            if diff >= 0:
                reward = (primary_item) / _CONST
            else:
                reward = (primary_item - diff + 2) / _CONST
            return reward
        # 三带一
        if card_type == CardTypeEnum.CT_THREE_ONE and card_count == 4:
            reward = 0
            if diff >= 0:
                reward = (primary_item) / _CONST
            else:
                reward = (primary_item - diff + 2) / _CONST
            return reward
        # 三带一飞机
        if card_type == CardTypeEnum.CT_THREE_ONE and card_count >= 8:
            reward = 0
            if diff >= 0:
                reward = (primary_item) / _CONST
            else:
                reward = (primary_item - diff + 2) / _CONST
            return reward
        # 三带一对
        if card_type == CardTypeEnum.CT_THREE_DOU and card_count == 5:
            reward = 0
            if diff >= 0:
                reward = (primary_item) / _CONST
            else:
                reward = (primary_item - diff + 2) / _CONST
            return reward
        # 三带一对飞机
        if card_type == CardTypeEnum.CT_THREE_DOU and card_count >= 10:
            reward = 0
            if diff >= 0:
                reward = (primary_item) / _CONST
            else:
                reward = (primary_item - diff + 2) / _CONST
            return reward
        # 连子
        if card_type == CardTypeEnum.CT_CONTINUE:
            reward = 0
            if diff >= 0:
                reward = (primary_item) / _CONST
            else:
                reward = (primary_item - diff) / _CONST
            return reward
        # 四带两单
        if card_type == CardTypeEnum.CT_FOUR_ONE:
            return (primary_item / 4) / _CONST
        # 四带两对
        if card_type == CardTypeEnum.CT_FOUR_DOU:
            return (primary_item / 4) / _CONST
        # 炸弹(王炸)
        if card_type == CardTypeEnum.CT_BOMB and card_count == 2:
            return 1.0 / 4
        # 炸弹(普通炸弹)
        if card_type == CardTypeEnum.CT_BOMB and card_count == 4:
            return (primary_item / 4) / _CONST

        return 0


if __name__ == '__main__':

   pass