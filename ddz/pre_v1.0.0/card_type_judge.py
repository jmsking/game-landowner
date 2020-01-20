#! /usr/bin/env python3

from card_type_struct import CardTypeStruct
from card_type_enum import CardTypeEnum
from card_enum import CardEnum
import numpy as np
from hand_card_utils import HandCardUtils

"""
牌型判断
"""
class CardTypeJudge(object):
    
    def __init__(self):
        pass

    """ 根据手牌状态得到手牌牌型 """
    def judge_card_type(self, hand_card):
        assert len(hand_card) == 18, 'the size of hand card status must be 18.'
        cardTypeStruct = CardTypeStruct()
        card_count = sum(hand_card)
        cardTypeStruct.card_count = card_count
        find_one = list(map(lambda x:x[0],filter(lambda x : x[1] == 1, enumerate(hand_card))))
        find_two = list(map(lambda x:x[0],filter(lambda x : x[1] == 2, enumerate(hand_card))))
        find_three = list(map(lambda x:x[0],filter(lambda x : x[1] == 3, enumerate(hand_card))))
        find_four = list(map(lambda x:x[0],filter(lambda x : x[1] == 4, enumerate(hand_card))))
        # 单牌
        if card_count == 1:
            assert len(find_one) == 1, 'hand card status error.'
            cardTypeStruct.card_type = CardTypeEnum.CT_ONE
            cardTypeStruct.primary_item = find_one[0]
            # 分值[-7,7]
            cardTypeStruct.card_score = HandCardUtils.value_map(find_one[0], CardTypeEnum.CT_ONE, card_count)
        # 对子(包含连对)
        if card_count % 2 == 0 and card_count > 0 and len(find_two) >= 1:
            # 列表中只含对子且对子中不含2
            if len(find_two) * 2 == card_count and CardEnum.TW.value not in find_two:
                if HandCardUtils.is_find(find_two):
                    cardTypeStruct.card_type = CardTypeEnum.CT_DOU
                    cardTypeStruct.primary_item = find_two[-1]
                    # 分值[-7,7]
                    cardTypeStruct.card_score = HandCardUtils.value_map(find_two[-1], 
                                                    CardTypeEnum.CT_DOU, card_count)
        #三带一单(连三带一单)
        if card_count % 4 == 0 and card_count > 0 and len(find_three) >= 1:
            # 三带一单
            if len(find_three) == 1 and len(find_one) == 1:
                cardTypeStruct.card_type = CardTypeEnum.CT_THREE_ONE
                cardTypeStruct.primary_item = find_three[0]
                # 分值[-7,7]
                cardTypeStruct.card_score = HandCardUtils.value_map(find_three[0],
                                                    CardTypeEnum.CT_THREE_ONE, card_count)
            elif len(find_three) * 3 + len(find_one) == card_count and CardEnum.TW.value not in find_three:
                if HandCardUtils.is_find(find_three):
                    cardTypeStruct.card_type = CardTypeEnum.CT_THREE_ONE
                    cardTypeStruct.primary_item = find_three[-1]
                    # 分值[0.5,7.5]
                    cardTypeStruct.card_score = HandCardUtils.value_map(find_three[-1],
                                                    CardTypeEnum.CT_THREE_ONE, card_count)
        #三带一对(连三带一对)
        if card_count % 5 == 0 and card_count > 0 and len(find_three) >= 1:
            # 三带一对
            if len(find_two) == 1 and len(find_three) == 1:
                cardTypeStruct.card_type = CardTypeEnum.CT_THREE_DOU
                cardTypeStruct.primary_item = find_three[0]
                # 分值 [-7,7]
                cardTypeStruct.card_score = HandCardUtils.value_map(find_three[0],
                                                    CardTypeEnum.CT_THREE_DOU, card_count)
            elif len(find_three) * 3 + len(find_two) * 2 == card_count and CardEnum.TW.value not in find_three:
                if HandCardUtils.is_find(find_three):
                    cardTypeStruct.card_type = CardTypeEnum.CT_THREE_DOU
                    cardTypeStruct.primary_item = find_three[-1]
                    # 分值[0.5,7.5]
                    cardTypeStruct.card_score = HandCardUtils.value_map(find_three[-1],
                                                    CardTypeEnum.CT_THREE_DOU, card_count)
        # 连子
        if card_count >= 5:
            # 必须都是单牌
            if len(find_one) == card_count:
                arr = set(find_one)
                exclude_arr = {CardEnum.TW.value, CardEnum.JA.value, CardEnum.QU.value}
                # 连子中不能包含2和大小王
                if len(list(arr.intersection(exclude_arr))) == 0:
                    if HandCardUtils.is_find(find_one):
                        cardTypeStruct.card_type = CardTypeEnum.CT_CONTINUE
                        cardTypeStruct.primary_item = find_one[-1]
                        # 分值[-6,8]
                        cardTypeStruct.card_score = HandCardUtils.value_map(find_one[-1],
                                                    CardTypeEnum.CT_CONTINUE, card_count)
        # 四带两单
        if card_count == 6 and len(find_four) >= 1:
            if len(find_four) == 1 and len(find_one) == 2:
                cardTypeStruct.card_type = CardTypeEnum.CT_FOUR_ONE
                cardTypeStruct.primary_item = find_four[0]
                # 分值[0,7]
                cardTypeStruct.card_score = HandCardUtils.value_map(find_four[0],
                                                    CardTypeEnum.CT_FOUR_ONE, card_count)
        # 四带两对
        if card_count == 8 and len(find_four) >= 1:
            if len(find_four) == 1 and len(find_two) == 2:
                cardTypeStruct.card_type = CardTypeEnum.CT_FOUR_DOU
                cardTypeStruct.primary_item = find_four[0]
                # 分值[0,7]
                cardTypeStruct.card_score = HandCardUtils.value_map(find_four[0],
                                                    CardTypeEnum.CT_FOUR_DOU, card_count)
        # 三不带(连三不带)
        if card_count % 3 == 0 and card_count > 0 and len(find_three) >= 1:
            if len(find_three) == 1:
                cardTypeStruct.card_type = CardTypeEnum.CT_THREE
                cardTypeStruct.primary_item = find_three[0]
                # 分值[-7,7]
                cardTypeStruct.card_score = HandCardUtils.value_map(find_three[0],
                                                    CardTypeEnum.CT_THREE, card_count)
            # 连三不带里面不能包含2
            elif len(find_three) * 3 == card_count and CardEnum.TW.value not in find_three:
                if HandCardUtils.is_find(find_three):
                    cardTypeStruct.card_type = CardTypeEnum.CT_THREE
                    cardTypeStruct.primary_item = find_three[-1]
                    # 分值[0.5,7.5]
                    cardTypeStruct.card_score = HandCardUtils.value_map(find_three[-1],
                                                    CardTypeEnum.CT_THREE, card_count)
        # 炸弹(王炸)
        if card_count == 2:
            if len(find_one) == 2 and find_one[0] == CardEnum.QU.value and find_one[1] == CardEnum.JA.value:
                cardTypeStruct.card_type = CardTypeEnum.CT_BOMB
                cardTypeStruct.primary_item = find_one[-1]
                # 分值 25
                cardTypeStruct.card_score = HandCardUtils.value_map(find_one[-1], CardTypeEnum.CT_BOMB,card_count)
        # 炸弹(普通炸弹)
        if card_count == 4 and len(find_four) >= 1:
            if len(find_four) == 1:
                cardTypeStruct.card_type = CardTypeEnum.CT_BOMB
                cardTypeStruct.primary_item = find_four[0]
                # 分值[7,21]
                cardTypeStruct.card_score = HandCardUtils.value_map(find_four[0],
                                                    CardTypeEnum.CT_BOMB, card_count)
        return cardTypeStruct


if __name__ == '__main__':
    judge = CardTypeJudge()
    # case 1: A
    hand_card = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 2: KK
    hand_card = [0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 3: KKK3
    hand_card = [0,0,0,1,0,0,0,0,0,0,0,0,0,3,0,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 4: KKK33
    hand_card = [0,0,0,2,0,0,0,0,0,0,0,0,0,3,0,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 5: 45678
    hand_card = [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 6: 23456(Error)
    hand_card = [0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 7: 35678(Error)
    hand_card = [0,0,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 8: KKKK34
    hand_card = [0,0,0,1,1,0,0,0,0,0,0,0,0,4,0,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 9: KKKK3344
    hand_card = [0,0,0,2,2,0,0,0,0,0,0,0,0,4,0,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 10: KKK
    hand_card = [0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 11: KKAA
    hand_card = [0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 12: AA22(Error)
    hand_card = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 13: KKKK
    hand_card = [0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 14: (QU)(JA)
    hand_card = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 15: KKKAAA
    hand_card = [0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 16: AAA222(Error)
    hand_card = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 17: KKKAAA345(Error)
    hand_card = [0,0,0,1,1,1,0,0,0,0,0,0,0,3,3,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 18: KKKAAA34
    hand_card = [0,0,0,1,1,0,0,0,0,0,0,0,0,3,3,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 19: KKKAAA3344
    hand_card = [0,0,0,2,2,0,0,0,0,0,0,0,0,3,3,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)
    # case 20: KKKAAA33445(Error)
    # case 19: KKKAAA3344
    hand_card = [0,0,0,2,2,1,0,0,0,0,0,0,0,3,3,0,0,0]
    card_type = judge.judge_card_type(hand_card)
    log_str = 'card-type: [%s] - primary-value: [%s]' %(card_type.card_type, card_type.primary_item)
    print(log_str)