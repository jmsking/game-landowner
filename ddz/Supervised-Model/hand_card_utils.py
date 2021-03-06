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

    @staticmethod
    def read_from_file(from_path = config.SAMPLE_SAVE_PATH):
        records = list()
        with open(from_path, 'r') as f:
            _ = f.readline()
            card_process = f.readline()
            records.append(card_process.split(":")[1])
        return records

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

    """ 是否包含连对/飞机 """
    @staticmethod
    def _is_find(hand_card):
        isFind = True
        for k in range(len(hand_card) - 1):
            diff = hand_card[k+1] - hand_card[k]
            if diff != 1:
                isFind = False
                break
        return isFind

    """ Decode the put card 
        Returns:
          (policy net action, kicker net action, {card:card_num})
          Ex. 
            Input: TTT
            Output: (8, {'T': 3})
    """
    @staticmethod
    def decode_put_card(put_card):
        # 不出
        if put_card is None or len(put_card) == 0:
            return 308, None, {}
        hand_card_status = HandCardUtils.obtain_hand_card_status(put_card)
        assert len(hand_card_status) == 18, 'the size of hand card status must be 18.'
        card_count = sum(hand_card_status)
        find_one = list(map(lambda x:x[0],filter(lambda x : x[1] == 1, enumerate(hand_card_status))))
        find_two = list(map(lambda x:x[0],filter(lambda x : x[1] == 2, enumerate(hand_card_status))))
        find_three = list(map(lambda x:x[0],filter(lambda x : x[1] == 3, enumerate(hand_card_status))))
        find_four = list(map(lambda x:x[0],filter(lambda x : x[1] == 4, enumerate(hand_card_status))))
        find_one = [find_one] if isinstance(find_one, int) else find_one
        find_two = [find_two] if isinstance(find_two, int) else find_two
        find_three = [find_three] if isinstance(find_three, int) else find_three
        find_four = [find_four] if isinstance(find_four, int) else find_four
        card_record = dict()
        for card in find_one:
            card_record[card] = 1
        for card in find_two:
            card_record[card] = 2
        for card in find_three:
            card_record[card] = 3
        for card in find_four:
            card_record[card] = 4
        # 单牌-15
        # 0-14
        if card_count == 1:
            primary_item = find_one[-1]
            return primary_item-3, None, card_record
        # 连子-36
        # 15-22 (5)
        # 23-29 (6)
        # 30-35 (7)
        # 36-40 (8)
        # 41-44 (9)
        # 45-47 (10)
        # 48-49 (11)
        # 50 (12)
        if card_count >= 5:
            # 必须都是单牌
            if len(find_one) == card_count:
                arr = set(find_one)
                exclude_arr = {CardEnum.TW.value, CardEnum.JA.value, CardEnum.QU.value}
                # 连子中不能包含2和大小王
                if len(list(arr.intersection(exclude_arr))) == 0:
                    if HandCardUtils._is_find(find_one):
                        primary_item = find_one[-1]
                        count = len(find_one)
                        policy_action = -1
                        if count == 5:
                            policy_action = primary_item+8
                        if count == 6:
                            policy_action = primary_item+15
                        if count == 7:
                            policy_action = primary_item+21
                        if count == 8:
                            policy_action = primary_item+26
                        if count == 9:
                            policy_action = primary_item+30
                        if count == 10:
                            policy_action = primary_item+33
                        if count == 11:
                            policy_action = primary_item+35
                        if count == 12:
                            policy_action = 50
                        return policy_action, None, card_record
        # 对子(包含连对)-65
        # 51-63 (1)
        # 64-73 (3)
        # 74-82 (4)
        # 83-90 (5)
        # 91-97 (6)
        # 98-103 (7)
        # 104-108 (8)
        # 109-112 (9)
        # 113-115 (10)
        if card_count % 2 == 0 and card_count > 0 and len(find_two) >= 1:
            if card_count == 2 and len(find_two) == 1:
                primary_item = find_two[-1]
                return primary_item+48, None, card_record
            # 列表中只含对子且对子中不含2
            if len(find_two) * 2 == card_count and CardEnum.TW.value not in find_two:
                if HandCardUtils._is_find(find_two):
                    primary_item = find_two[-1]
                    count = len(find_two)
                    policy_action = -1
                    if count == 3:
                        policy_action = primary_item+59
                    if count == 4:
                        policy_action = primary_item+68
                    if count == 5:
                        policy_action = primary_item+76
                    if count == 6:
                        policy_action = primary_item+83
                    if count == 7:
                        policy_action = primary_item+89
                    if count == 8:
                        policy_action = primary_item+94
                    if count == 9:
                        policy_action = primary_item+98
                    if count == 10:
                        policy_action = primary_item+101
                    return policy_action, None, card_record
        # 三不带(连三不带)-58
        # 116-128 (1)
        # 129-139 (2)
        # 140-149 (3)
        # 150-158 (4)
        # 159-166 (5)
        # 167-173 (6)
        if card_count % 3 == 0 and card_count > 0 and len(find_three) >= 1:
            if len(find_three) == 1:
                primary_item = find_three[-1]
                return primary_item+113, None, card_record
            # 连三不带里面不能包含2
            elif len(find_three) * 3 == card_count and CardEnum.TW.value not in find_three:
                if HandCardUtils._is_find(find_three):
                    primary_item = find_three[-1]
                    count = len(find_three)
                    policy_action = -1
                    if count == 2:
                        policy_action = primary_item+125
                    if count == 3:
                        policy_action = primary_item+135
                    if count == 4:
                        policy_action = primary_item+144
                    if count == 5:
                        policy_action = primary_item+152
                    if count == 6:
                        policy_action = primary_item+159
                    return policy_action, None, card_record
        #三带一单(连三带一单)-51
        # 174-186 (1)
        # 187-197 (2)
        # 198-207 (3)
        # 208-216 (4)
        # 217-224 (5)
        if card_count % 4 == 0 and card_count > 0 and len(find_three) >= 1:
            # 三带一单
            if len(find_three) == 1 and len(find_one) == 1:
                primary_item = find_three[-1]
                kicker_action = list(map(lambda x:x-3, find_one))
                return primary_item+171, kicker_action, card_record
            elif len(find_three) * 3 + len(find_one) == card_count and CardEnum.TW.value not in find_three:
                if HandCardUtils._is_find(find_three):
                    primary_item = find_three[-1]
                    count = len(find_three)
                    policy_action = -1
                    kicker_action = list(map(lambda x:x-3, find_one))
                    if count == 2:
                        policy_action = primary_item+183
                    if count == 3:
                        policy_action = primary_item+193
                    if count == 4:
                        policy_action = primary_item+202
                    if count == 5:
                        policy_action = primary_item+210
                    return policy_action, kicker_action, card_record
        #三带一对(连三带一对)-43
        # 225-237 (1)
        # 238-248 (2)
        # 249-258 (3)
        # 259-267 (4)
        if card_count % 5 == 0 and card_count > 0 and len(find_three) >= 1:
            # 三带一对
            if len(find_two) == 1 and len(find_three) == 1:
                primary_item = find_three[-1]
                kicker_action = list(map(lambda x:x+12, find_one))
                return primary_item+222, kicker_action, card_record
            elif len(find_three) * 3 + len(find_two) * 2 == card_count and CardEnum.TW.value not in find_three:
                if HandCardUtils._is_find(find_three):
                    primary_item = find_three[-1]
                    count = len(find_three)
                    policy_action = -1
                    kicker_action = list(map(lambda x:x+12, find_one))
                    if count == 2:
                        policy_action = primary_item+234
                    if count == 3:
                        policy_action = primary_item+244
                    if count == 4:
                        policy_action = primary_item+253
                    return policy_action, kicker_action, card_record
        # 四带两单-13
        # 268-280
        if card_count == 6 and len(find_four) >= 1:
            if len(find_four) == 1 and len(find_one) == 2:
                primary_item = find_four[-1]
                kicker_action = list(map(lambda x:x-3, find_one))
                return primary_item+265, kicker_action, card_record
        # 四带两对-13
        # 281-293
        if card_count == 8 and len(find_four) >= 1:
            if len(find_four) == 1 and len(find_two) == 2:
                primary_item = find_four[-1]
                kicker_action = list(map(lambda x:x+12, find_one))
                return primary_item+278, kicker_action, card_record
        # 炸弹(普通炸弹)-13
        # 294-306
        if card_count == 4 and len(find_four) >= 1:
            if len(find_four) == 1:
                primary_item = find_four[-1]
                return primary_item+291, card_record
        # 炸弹(王炸)-1
        # 307
        if card_count == 2:
            if len(find_one) == 2 and find_one[0] == CardEnum.QU.value and find_one[1] == CardEnum.JA.value:
                return 307, card_record
       
        return 308, None, {}

if __name__ == '__main__':

   pass