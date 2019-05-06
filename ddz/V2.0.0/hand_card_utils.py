#! /usr/bin/env python3

from card_type_struct import CardTypeStruct
from card_type_enum import CardTypeEnum
from card_enum import CardEnum
import random

class HandCardUtils(object):


    """ 根据手牌计算得到手牌状态
    """
    @staticmethod
    def obtain_hand_card_status(hand_card_seq):
        hand_card_status = [0 for _ in range(18)]
        for item in hand_card_seq:
            hand_card_status[item] += 1
        return hand_card_status

    """ 查找k连对
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
        rnd = random.randint(0,len(even_pair)-1)
        return even_pair[rnd]

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
        rnd = random.randint(0,len(even_pair)-1)
        return even_pair[rnd]

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
        rnd = random.randint(0,len(contin_pair)-1)
        return contin_pair[rnd]


    # 是否包含连对/飞机
    @staticmethod
    def is_find(hand_card):
        isFind = True
        for k in range(len(hand_card) - 1):
            diff = hand_card[k+1] - hand_card[k]
            if diff != 1:
                isFind = False
                break
        return isFind

    # 针对对子或三带寻找候选出牌序列
    # Ex. [3,4,5,7,8,9]
    # Return [[3,4,5],[7,8,9]]
    # Ex. [3,5,6]
    # Return [[3],[5,6]]
    @staticmethod
    def find_first_sub_seq(hand_card):
        max_seq_len = 1
        seq_len = 1
        start = 0
        end = 0
        seq = list()
        is_contain_tw = False
        # 对2最后出
        if CardEnum.TW.value in hand_card:
            is_contain_tw = True
            hand_card = list(filter(lambda x:x!=CardEnum.TW.value, hand_card))
        if len(hand_card) == 1:
            seq.append(hand_card)
            if is_contain_tw:
                seq.append(([CardEnum.TW.value],1))
            return seq
        for k in range(len(hand_card) - 1):
            diff = hand_card[k+1] - hand_card[k]
            if diff == 1:
                seq_len += 1
            else:
                sub_seq = hand_card[start:end+1]
                seq.append((sub_seq,len(sub_seq)))
                start = end+1
                end = start + 1
                seq_len = 1
            if seq_len > max_seq_len:
                max_seq_len = seq_len
                end = k+1
                start = end - max_seq_len + 1
        sub_seq = hand_card[start:end+1]
        seq.append((sub_seq, len(sub_seq)))
        if is_contain_tw:
            seq.append(([CardEnum.TW.value],1))
        seq = sorted(seq, key=lambda x:x[1], reverse=True)
        seq = list(map(lambda x:x[0], seq))
        return seq

    """ 是否包含炸弹 """
    @staticmethod
    def _is_contain_bomb(hand_card_seq, hand_card_status):
        # 普通炸弹
        bomb_list = list(map(lambda x:x[0],filter(lambda x : x[1] == 4, enumerate(hand_card_status))))
        if len(bomb_list) > 0:
            return True
        # 王炸
        ja_qu_list = {CardEnum.QU.value, CardEnum.JA.value}
        if len(set(hand_card_seq).intersection(ja_qu_list)) == 2:
            return True
        return False

    """ 是否包含连子 
    Returns:
    若存在,则返回该连子最大的值
    否则,返回-1
    """
    @staticmethod
    def _is_contain_continue(hand_card_seq):
        # 去掉2及大小王
        exclude_list = [CardEnum.TW.value, CardEnum.QU.value, CardEnum.JA.value]
        pure_list = list(filter(lambda x:x not in exclude_list, hand_card_seq))
        if len(pure_list) < 5:
            return -1
        tmp_list = pure_list[:1]
        for k in range(len(pure_list)-1):
            if pure_list[k+1] - tmp_list[-1] == 1:
                tmp_list.append(pure_list[k+1])
            elif pure_list[k+1] - tmp_list[-1] > 1:
                tmp_list.clear()
                tmp_list.append(pure_list[k+1])
        if len(tmp_list) >= 5:
            return tmp_list[-1]
        return -1

    """ 根据当前出的牌型判断是否存在大于该牌型的手牌
    """
    @staticmethod
    def is_find_hand_card_type(hand_card_seq, hand_card_status, current_hand_card_type):
        cur_card_type = current_hand_card_type.card_type
        cur_primary_item = current_hand_card_type.primary_item
        if cur_card_type == CardTypeEnum.CT_ONE:
            ans_list = list(filter(lambda x:x>cur_primary_item, hand_card_seq))
            if len(ans_list) > 0:
                return True
            # 炸弹也满足条件
            return HandCardUtils._is_contain_bomb(hand_card_seq, hand_card_status)
        elif cur_card_type == CardTypeEnum.CT_DOU:
            ct_dou = list(map(lambda x:x[0],filter(lambda x : x[1] == 2, enumerate(hand_card_status))))
            ans_list = list(filter(lambda x:x>cur_primary_item, ct_dou))
            if len(ans_list) > 0:
                return True
            # 炸弹也满足条件
            return HandCardUtils._is_contain_bomb(hand_card_seq, hand_card_status)
        elif cur_card_type == CardTypeEnum.CT_CONTINUE:
            ans = HandCardUtils._is_contain_continue(hand_card_seq)
            if ans != -1:
                return True
            return HandCardUtils._is_contain_bomb(hand_card_seq, hand_card_status)
        elif cur_card_type == CardTypeEnum.CT_THREE:
            ct_three = list(map(lambda x:x[0],filter(lambda x : x[1] == 3, enumerate(hand_card_status))))
            ans_list = list(filter(lambda x:x>cur_primary_item, ct_three))
            if len(ans_list) > 0:
                return True
            return HandCardUtils._is_contain_bomb(hand_card_seq, hand_card_status)
        elif cur_card_type == CardTypeEnum.CT_THREE_ONE:
            if len(hand_card_seq) < 4:
                return False
            ct_three = list(map(lambda x:x[0],filter(lambda x : x[1] == 3, enumerate(hand_card_status))))
            ans_list = list(filter(lambda x:x>cur_primary_item, ct_three))
            if len(ans_list) > 0:
                return True
            return HandCardUtils._is_contain_bomb(hand_card_seq, hand_card_status)
        elif cur_card_type == CardTypeEnum.CT_THREE_DOU:
            if len(hand_card_seq) < 5:
                return False
            ct_three = list(map(lambda x:x[0],filter(lambda x : x[1] == 3, enumerate(hand_card_status))))
            ct_two = list(map(lambda x:x[0],filter(lambda x : x[1] == 2, enumerate(hand_card_status))))
            ans_list = list(filter(lambda x:x>cur_primary_item, ct_three))
            if len(ans_list) > 0 and len(ct_two) >= 1:
                return True
            return HandCardUtils._is_contain_bomb(hand_card_seq, hand_card_status)
        elif cur_card_type == CardTypeEnum.CT_FOUR_ONE:
            if len(hand_card_seq) < 6:
                return False
            ct_four = list(map(lambda x:x[0],filter(lambda x : x[1] == 4, enumerate(hand_card_status))))
            ans_list = list(filter(lambda x:x>cur_primary_item, ct_four))
            if len(ans_list) > 0:
                return True
            return HandCardUtils._is_contain_bomb(hand_card_seq, hand_card_status)
        elif cur_card_type == CardTypeEnum.CT_FOUR_DOU:
            if len(hand_card_seq) < 8:
                return False
            ct_four = list(map(lambda x:x[0],filter(lambda x : x[1] == 4, enumerate(hand_card_status))))
            ct_two = list(map(lambda x:x[0],filter(lambda x : x[1] == 2, enumerate(hand_card_status))))
            ans_list = list(filter(lambda x:x>cur_primary_item, ct_four))
            if len(ans_list) > 0 and len(ct_two) >= 2:
                return True
            return HandCardUtils._is_contain_bomb(hand_card_seq, hand_card_status)
        elif cur_card_type == CardTypeEnum.CT_BOMB:
            cur_count = current_hand_card_type.card_count
            # 普通炸弹
            if cur_count == 4:
                ct_bomb = list(map(lambda x:x[0],filter(lambda x : x[1] == 4, enumerate(hand_card_status))))
                ans_list = list(filter(lambda x:x>cur_primary_item, ct_bomb))
                if len(ans_list) > 0:
                    return True
                # 是否有王炸
                ja_qu_list = {CardEnum.QU.value, CardEnum.JA.value}
                if len(set(hand_card_seq).intersection(ja_qu_list)) == 2:
                    return True
            return False
        else:
            raise Exception('current card type error.')
        return False

    @staticmethod
    def value_map(primary_item, card_type, card_count):
        _CONST = 100
        # 单牌
        if card_type == CardTypeEnum.CT_ONE:
            return primary_item / 100
        # 对子
        if card_type == CardTypeEnum.CT_DOU:
            return (primary_item * 2 + 2) / 100
        # 三不带
        if card_type == CardTypeEnum.CT_THREE and card_count == 3:
            return (primary_item * 3 + 3) / 100
        # 三不带飞机
        if card_type == CardTypeEnum.CT_THREE and card_count >= 6:
            return (primary_item * card_count + card_count) / 100 
        # 三带一
        if card_type == CardTypeEnum.CT_THREE_ONE and card_count == 4:
            return (primary_item * 3 + 3) / 100
        # 三带一飞机
        if card_type == CardTypeEnum.CT_THREE_ONE and card_count >= 8:
            return (primary_item * card_count + card_count) / 100
        # 三带一对
        if card_type == CardTypeEnum.CT_THREE_DOU and card_count == 5:
            return (primary_item * 3 + 6) / 100
        # 三带一对飞机
        if card_type == CardTypeEnum.CT_THREE_DOU and card_count >= 10:
            return (primary_item * card_count + card_count + 12 ) / 100      
        # 连子
        if card_type == CardTypeEnum.CT_CONTINUE:
            return (primary_item * (card_count - 3)) / 100
        # 四带两单
        if card_type == CardTypeEnum.CT_FOUR_ONE:
            return (primary_item * 5) / 100
        # 四带两对
        if card_type == CardTypeEnum.CT_FOUR_DOU:
            return (primary_item * 5 + 10) / 100
        # 炸弹(王炸)
        if card_type == CardTypeEnum.CT_BOMB and card_count == 2:
            return 1
        # 炸弹(普通炸弹)
        if card_type == CardTypeEnum and card_count == 4:
            return (primary_item * 6) / 100

        return 0
    


def test_is_find_hand_card_type():
    # case 1：单牌测试
    hand_card_seq = [7,8,9]
    hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card_seq)
    cur_card_type = CardTypeStruct()
    cur_card_type.card_type = CardTypeEnum.CT_ONE
    cur_card_type.card_count = 1
    cur_card_type.primary_item = 8
    ans = HandCardUtils.is_find_hand_card_type(hand_card_seq, hand_card_status, cur_card_type)
    print('单牌:', ans)
    # case 2: 对子测试
    hand_card_seq = [7,8,9,9,10]
    hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card_seq)
    cur_card_type = CardTypeStruct()
    cur_card_type.card_type = CardTypeEnum.CT_DOU
    cur_card_type.card_count = 2
    cur_card_type.primary_item = 4
    ans = HandCardUtils.is_find_hand_card_type(hand_card_seq, hand_card_status, cur_card_type)
    print('对子', ans)
    # case 3: 三不带测试
    hand_card_seq = [7,8,9,9,9]
    hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card_seq)
    cur_card_type = CardTypeStruct()
    cur_card_type.card_type = CardTypeEnum.CT_THREE
    cur_card_type.card_count = 3
    cur_card_type.primary_item = 8
    ans = HandCardUtils.is_find_hand_card_type(hand_card_seq, hand_card_status, cur_card_type)
    print('三不带', ans)
    # case 4: 三带一测试
    hand_card_seq = [7,8,9,9,9]
    hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card_seq)
    cur_card_type = CardTypeStruct()
    cur_card_type.card_type = CardTypeEnum.CT_THREE_ONE
    cur_card_type.card_count = 4
    cur_card_type.primary_item = 8
    ans = HandCardUtils.is_find_hand_card_type(hand_card_seq, hand_card_status, cur_card_type)
    print('三带一', ans)
    # case 5: 三带二测试
    hand_card_seq = [7,8,9,9,9,10,10]
    hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card_seq)
    cur_card_type = CardTypeStruct()
    cur_card_type.card_type = CardTypeEnum.CT_THREE_DOU
    cur_card_type.card_count = 5
    cur_card_type.primary_item = 8
    ans = HandCardUtils.is_find_hand_card_type(hand_card_seq, hand_card_status, cur_card_type)
    print('三带二', ans)
    # case 6: 四带二单测试
    hand_card_seq = [7,8,9,9,9,9]
    hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card_seq)
    cur_card_type = CardTypeStruct()
    cur_card_type.card_type = CardTypeEnum.CT_FOUR_ONE
    cur_card_type.card_count = 6
    cur_card_type.primary_item = 8
    ans = HandCardUtils.is_find_hand_card_type(hand_card_seq, hand_card_status, cur_card_type)
    print('四带二单', ans)
    # case 7: 四带二对测试
    hand_card_seq = [7,7,8,9,9,9,9,10,11]
    hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card_seq)
    cur_card_type = CardTypeStruct()
    cur_card_type.card_type = CardTypeEnum.CT_FOUR_DOU
    cur_card_type.card_count = 8
    cur_card_type.primary_item = 8
    ans = HandCardUtils.is_find_hand_card_type(hand_card_seq, hand_card_status, cur_card_type)
    print('四带二对', ans)
    # case 8: 连子测试
    hand_card_seq = [7,8,9,10,11,16]
    hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card_seq)
    cur_card_type = CardTypeStruct()
    cur_card_type.card_type = CardTypeEnum.CT_CONTINUE
    cur_card_type.card_count = 5
    cur_card_type.primary_item = 8
    ans = HandCardUtils.is_find_hand_card_type(hand_card_seq, hand_card_status, cur_card_type)
    print('连子', ans)
    # case 9: 普通炸弹测试
    hand_card_seq = [7,8,9,9,9,9]
    hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card_seq)
    cur_card_type = CardTypeStruct()
    cur_card_type.card_type = CardTypeEnum.CT_BOMB
    cur_card_type.card_count = 4
    cur_card_type.primary_item = 8
    ans = HandCardUtils.is_find_hand_card_type(hand_card_seq, hand_card_status, cur_card_type)
    print('普通炸弹', ans)
    # case 10: 王炸
    hand_card_seq = [7,8,9,15,15,15,15]
    hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card_seq)
    cur_card_type = CardTypeStruct()
    cur_card_type.card_type = CardTypeEnum.CT_BOMB
    cur_card_type.card_count = 2
    cur_card_type.primary_item = 17
    ans = HandCardUtils.is_find_hand_card_type(hand_card_seq, hand_card_status, cur_card_type)
    print('王炸', ans)

def test_find_first_sub_seq():
    # case 1: 335566
    hand_card = [3,5,6]
    res = HandCardUtils.find_first_sub_seq(hand_card)
    print(res)
    # case 2: 33446677
    hand_card = [3,4,6,7]
    res = HandCardUtils.find_first_sub_seq(hand_card)
    print(res)
    # case 3: 3344557788
    hand_card = [3,4,5,7,8]
    res = HandCardUtils.find_first_sub_seq(hand_card)
    print(res)
    # case 4: 33556677
    hand_card = [3,5,6,7]
    res = HandCardUtils.find_first_sub_seq(hand_card)
    print(res)
    # case 5: 335566778899
    hand_card = [3,5,6,7,8,9]
    res = HandCardUtils.find_first_sub_seq(hand_card)
    print(res)
    # case 5: 22335566778899
    hand_card = [3,5,6,7,8,9,15]
    res = HandCardUtils.find_first_sub_seq(hand_card)
    print(res)


if __name__ == '__main__':
    #test_is_find_hand_card_type()

    test_find_first_sub_seq()