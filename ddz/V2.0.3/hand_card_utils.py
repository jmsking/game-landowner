#! /usr/bin/env python3

from card_type_struct import CardTypeStruct
from card_type_enum import CardTypeEnum
from card_enum import CardEnum
import random
import config
from action_type_enum import ActionTypeEnum

class HandCardUtils(object):

    def write2file(self, x, y):
        with open(config.SAMPLE_SAVE_PATH, 'a', encoding='utf-8') as f:
            for ix, item in enumerate(x):
                val = item + [y[ix]]
                text = str(val)
                f.write(text)
                f.write('\n')

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

    @staticmethod
    def is_contain_card(hand_card_status, put_card_seq):
        put_card_status = HandCardUtils.obtain_hand_card_status(put_card_seq)
        copy_status = hand_card_status.copy()
        for ix in range(len(hand_card_status)):
            copy_status[ix] -= put_card_status[ix]
        neg = list(filter(lambda x:x<0, copy_status))
        return len(neg) == 0

    """ 根据手牌状态判断是否是一手牌 """
    @staticmethod
    def is_one_hand(hand_card_seq):
        hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card_seq)
        assert len(hand_card_status) == 18, 'the size of hand card status must be 18.'
        cts = CardTypeStruct()
        card_count = sum(hand_card_status)
        cts.card_count = card_count
        find_one = list(map(lambda x:x[0],filter(lambda x : x[1] == 1, enumerate(hand_card_status))))
        find_two = list(map(lambda x:x[0],filter(lambda x : x[1] == 2, enumerate(hand_card_status))))
        find_three = list(map(lambda x:x[0],filter(lambda x : x[1] == 3, enumerate(hand_card_status))))
        find_four = list(map(lambda x:x[0],filter(lambda x : x[1] == 4, enumerate(hand_card_status))))
        find_one = [find_one] if isinstance(find_one, int) else find_one
        find_two = [find_two] if isinstance(find_two, int) else find_two
        find_three = [find_three] if isinstance(find_three, int) else find_three
        find_four = [find_four] if isinstance(find_four, int) else find_four
        # 单牌
        if card_count == 1:
            cts.card_type = ActionTypeEnum.ACTION_PUT_ONE.value
            cts.primary_item = hand_card_seq[0]
            return True, cts
        # 对子(包含连对)
        if card_count % 2 == 0 and card_count > 0 and len(find_two) >= 1:
            if card_count == 2 and len(find_two) == 1:
                cts.primary_item = find_two[-1]
                cts.card_type = ActionTypeEnum.ACTION_PUT_DOU.value
                return True, cts
            # 列表中只含对子且对子中不含2
            if len(find_two) * 2 == card_count and CardEnum.TW.value not in find_two:
                if HandCardUtils.is_find(find_two):
                    cts.primary_item = find_two[-1]
                    size = len(find_two)
                    if size == 2:
                        cts.card_type = ActionTypeEnum.ACTION_PUT_2_DOU.value
                    elif size == 3:
                        cts.card_type = ActionTypeEnum.ACTION_PUT_2_DOU.value
                    elif size == 4:
                        cts.card_type = ActionTypeEnum.ACTION_PUT_2_DOU.value
                    elif size == 5:
                        cts.card_type = ActionTypeEnum.ACTION_PUT_2_DOU.value
                    return True, cts
        #三带一单(连三带一单)
        if card_count % 4 == 0 and card_count > 0 and len(find_three) >= 1:
            # 三带一单
            if len(find_three) == 1 and len(find_one) == 1:
                cts.primary_item = find_three[-1]
                cts.card_type = ActionTypeEnum.ACTION_PUT_THREE_ONE.value
                return True, cts
            elif len(find_three) * 3 + len(find_one) == card_count and CardEnum.TW.value not in find_three:
                if HandCardUtils.is_find(find_three):
                    cts.primary_item = find_three[-1]
                    size = len(find_three)
                    if size == 2:
                        cts.card_type == ActionTypeEnum.ACTION_PUT_2_THREE_ONE.value
                    elif size == 3:
                        cts.card_type == ActionTypeEnum.ACTION_PUT_3_THREE_ONE.value
                    return True, cts
        #三带一对(连三带一对)
        if card_count % 5 == 0 and card_count > 0 and len(find_three) >= 1:
            # 三带一对
            if len(find_two) == 1 and len(find_three) == 1:
                cts.primary_item = find_three[-1]
                cts.card_type = ActionTypeEnum.ACTION_PUT_THREE_DOU.value
                return True, cts
            elif len(find_three) * 3 + len(find_two) * 2 == card_count and CardEnum.TW.value not in find_three:
                if HandCardUtils.is_find(find_three):
                    cts.primary_item = find_three[-1]
                    size = len(find_three)
                    if size == 2:
                        cts.card_type == ActionTypeEnum.ACTION_PUT_2_THREE_DOU.value
                    elif size == 3:
                        cts.card_type == ActionTypeEnum.ACTION_PUT_3_THREE_DOU.value
                    return True, cts
        # 连子
        if card_count >= 5:
            # 必须都是单牌
            if len(find_one) == card_count:
                arr = set(find_one)
                exclude_arr = {CardEnum.TW.value, CardEnum.JA.value, CardEnum.QU.value}
                # 连子中不能包含2和大小王
                if len(list(arr.intersection(exclude_arr))) == 0:
                    if HandCardUtils.is_find(find_one):
                        cts.primary_item = find_one[-1]
                        size = len(find_one)
                        if size == 5:
                            cts.card_type = ActionTypeEnum.ACTION_PUT_5_CONTINUE.value
                        elif size == 6:
                            cts.card_type = ActionTypeEnum.ACTION_PUT_6_CONTINUE.value                            
                        elif size == 7:
                            cts.card_type = ActionTypeEnum.ACTION_PUT_7_CONTINUE.value
                        elif size == 8:
                            cts.card_type = ActionTypeEnum.ACTION_PUT_8_CONTINUE.value
                        elif size == 9:
                            cts.card_type = ActionTypeEnum.ACTION_PUT_9_CONTINUE.value
                        elif size == 10:
                            cts.card_type = ActionTypeEnum.ACTION_PUT_10_CONTINUE.value
                        elif size == 11:
                            cts.card_type = ActionTypeEnum.ACTION_PUT_11_CONTINUE.value
                        elif size == 12:
                            cts.card_type = ActionTypeEnum.ACTION_PUT_12_CONTINUE.value
                        return True, cts
        # 四带两单
        if card_count == 6 and len(find_four) >= 1:
            if len(find_four) == 1 and len(find_one) == 2:
                cts.primary_item = find_four[-1]
                cts.card_type = ActionTypeEnum.ACTION_PUT_FOUR_ONE.value
                return True, cts
        # 四带两对
        if card_count == 8 and len(find_four) >= 1:
            if len(find_four) == 1 and len(find_two) == 2:
                cts.primary_item = find_four[-1]
                cts.card_type = ActionTypeEnum.ACTION_PUT_FOUR_DOU.value
                return True, cts
        # 三不带(连三不带)
        if card_count % 3 == 0 and card_count > 0 and len(find_three) >= 1:
            if len(find_three) == 1:
                cts.primary_item = find_three[-1]
                cts.card_type = ActionTypeEnum.ACTION_PUT_THREE.value
                return True, cts
            # 连三不带里面不能包含2
            elif len(find_three) * 3 == card_count and CardEnum.TW.value not in find_three:
                if HandCardUtils.is_find(find_three):
                    cts.primary_item = find_three[-1]
                    size = len(find_three)
                    if size == 2:
                        cts.card_type = ActionTypeEnum.ACTION_PUT_2_THREE.value
                    elif size == 3:
                        cts.card_type = ActionTypeEnum.ACTION_PUT_3_THREE.value
                    return True, cts
        # 炸弹(王炸)
        if card_count == 2:
            if len(find_one) == 2 and find_one[0] == CardEnum.QU.value and find_one[1] == CardEnum.JA.value:
                cts.primary_item = find_one[-1]
                cts.card_type = ActionTypeEnum.ACTION_PUT_BOMB.value
                return True, cts
        # 炸弹(普通炸弹)
        if card_count == 4 and len(find_four) >= 1:
            if len(find_four) == 1:
                cts.primary_item = find_four[-1]
                cts.card_type = ActionTypeEnum.ACTION_PUT_BOMB.value
                return True, cts
        return False, None

    """ 根据当前出的牌型判断是否存在大于该牌型的手牌
    """
    @staticmethod
    def is_find_hand_card_type(hand_card_status, primary_item, action):
        # 单牌
        if action == ActionTypeEnum.ACTION_PUT_ONE.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] >= 1, enumerate(hand_card_status))))
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
        # 对子
        elif action == ActionTypeEnum.ACTION_PUT_DOU.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] == 2, enumerate(hand_card_status))))
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
        # 三不带
        elif action == ActionTypeEnum.ACTION_PUT_THREE.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] == 3, enumerate(hand_card_status))))
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
        # 三带一
        elif action == ActionTypeEnum.ACTION_PUT_THREE_ONE.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] == 3, enumerate(hand_card_status)))) 
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                other_exist_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[1] >= 1 and x[0] != put_card, enumerate(hand_card_status))))
                if isinstance(other_exist_card, int):
                    other_exist_card = [other_exist_card]
                if len(other_exist_card) == 0:
                    return False
        # 三带一对
        elif action == ActionTypeEnum.ACTION_PUT_THREE_DOU.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] == 3, enumerate(hand_card_status)))) 
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                other_exist_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[1] >= 2 and x[0] != put_card, enumerate(hand_card_status))))
                if isinstance(other_exist_card, int):
                    other_exist_card = [other_exist_card]
                if len(other_exist_card) == 0:
                    return False
        # 两连对
        elif action == ActionTypeEnum.ACTION_PUT_2_DOU.value:
            K = 2
            exist_card = HandCardUtils.find_even_pair(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
        # 三连对
        elif action == ActionTypeEnum.ACTION_PUT_3_DOU.value:
            K = 3
            exist_card = HandCardUtils.find_even_pair(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
        # 四连对
        elif action == ActionTypeEnum.ACTION_PUT_4_DOU.value:
            K = 4
            exist_card = HandCardUtils.find_even_pair(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
        # 五连对
        elif action == ActionTypeEnum.ACTION_PUT_5_DOU.value:
            K = 5
            exist_card = HandCardUtils.find_even_pair(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
        # 两连三不带
        elif action == ActionTypeEnum.ACTION_PUT_2_THREE.value:
            K = 2
            exist_card = HandCardUtils.find_even_three(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
        # 三连三不带
        elif action == ActionTypeEnum.ACTION_PUT_3_THREE.value:
            K = 3
            exist_card = HandCardUtils.find_even_three(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
        # 两连三带一
        elif action == ActionTypeEnum.ACTION_PUT_2_THREE_ONE.value:
            K = 2
            exist_card = HandCardUtils.find_even_three(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                other_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[0] not in exist_card, enumerate(hand_card_status))))
                if len(other_card) < K:
                    return False
        # 三连三带一
        elif action == ActionTypeEnum.ACTION_PUT_3_THREE_ONE.value:
            K = 3
            exist_card = HandCardUtils.find_even_three(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                other_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[0] not in exist_card, enumerate(hand_card_status))))
                if len(other_card) < K:
                    return False
        # 两连三带一对
        elif action == ActionTypeEnum.ACTION_PUT_2_THREE_DOU.value:
            K = 2
            exist_card = HandCardUtils.find_even_three(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                other_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[0] not in exist_card and x[1] == 2, enumerate(hand_card_status))))
                if len(other_card) < K:
                    return False
        # 三连三带一对
        elif action == ActionTypeEnum.ACTION_PUT_3_THREE_DOU.value:
            K = 3
            exist_card = HandCardUtils.find_even_three(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                other_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[0] not in exist_card and x[1] == 2, enumerate(hand_card_status))))
                if len(other_card) < K:
                    return False
        # 四带二单
        elif action == ActionTypeEnum.ACTION_PUT_FOUR_ONE.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] == 4, enumerate(hand_card_status)))) 
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                other_exist_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[1] >= 1 and x[0] != put_card, enumerate(hand_card_status))))
                if isinstance(other_exist_card, int):
                    other_exist_card = [other_exist_card]
                if len(other_exist_card) <= 1:
                    return False
        # 四带二对
        elif action == ActionTypeEnum.ACTION_PUT_FOUR_DOU.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] == 4, enumerate(hand_card_status)))) 
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                other_exist_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[1] >= 2 and x[0] != put_card, enumerate(hand_card_status))))
                if isinstance(other_exist_card, int):
                    other_exist_card = [other_exist_card]
                if len(other_exist_card) <= 1:
                    return False
        # 连子(5)
        elif action == ActionTypeEnum.ACTION_PUT_5_CONTINUE.value:
            K = 5
            exist_card = HandCardUtils.find_continues(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
        # 连子(6)
        elif action == ActionTypeEnum.ACTION_PUT_6_CONTINUE.value:
            K = 6
            exist_card = HandCardUtils.find_continues(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False

        # 连子(7)
        elif action == ActionTypeEnum.ACTION_PUT_7_CONTINUE.value:
            K = 7
            exist_card = HandCardUtils.find_continues(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
            
        # 连子(8)
        elif action == ActionTypeEnum.ACTION_PUT_8_CONTINUE.value:
            K = 8
            exist_card = HandCardUtils.find_continues(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
           
        # 连子(9)
        elif action == ActionTypeEnum.ACTION_PUT_9_CONTINUE.value:
            K = 9
            exist_card = HandCardUtils.find_continues(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
            
        # 连子(10)
        elif action == ActionTypeEnum.ACTION_PUT_10_CONTINUE.value:
            K = 10
            exist_card = HandCardUtils.find_continues(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
            
        # 连子(11)
        elif action == ActionTypeEnum.ACTION_PUT_11_CONTINUE.value:
            K = 11
            exist_card = HandCardUtils.find_continues(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
           
        # 连子(12)
        elif action == ActionTypeEnum.ACTION_PUT_12_CONTINUE.value:
            K = 12
            exist_card = HandCardUtils.find_continues(hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                return False
            
        # 炸弹
        elif action == ActionTypeEnum.ACTION_PUT_BOMB.value:
            qu_ja = [CardEnum.QU.value, CardEnum.JA.value]
            comm_bomb = list(map(lambda x:x[0], filter(lambda x: x[1] == 4, enumerate(hand_card_status))))
            master_bomb = list(map(lambda x:x[0], filter(lambda x: x[0] in qu_ja and x[1] == 1, enumerate(hand_card_status))))
            if isinstance(comm_bomb, int):
                comm_bomb = [comm_bomb]
            if isinstance(master_bomb, int):
                master_bomb = [master_bomb]
            if primary_item is not None:
                comm_bomb = list(filter(lambda x:x > primary_item,comm_bomb))
                if isinstance(comm_bomb, int):
                    comm_bomb = [comm_bomb]
            if len(comm_bomb) == 0 and len(master_bomb) < 2:
                return False
            
        # 不出
        elif action == ActionTypeEnum.ACTION_NO_PUT.value:
            return False

        return True

    """
    手牌初始价值
    """
    @staticmethod
    def hand_card_init_value(hand_card_seq):
        hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card_seq)
        value_ratio = [0.1,0.2,0.3,0.3,0.4,1]
        value = []
        # 单牌价值
        single_value = 0
        for item in hand_card_seq:
            single_value += (item-10)
        single_value /= 67
        value.append(single_value*value_ratio[0])
        # 对子数
        dou_value = 0
        dou_num = list(filter(lambda x:x[1] == 2, enumerate(hand_card_status)))
        dou_num = dou_num if isinstance(dou_num, int) else len(dou_num)
        dou_value = dou_num * 2 * 0.1
        value.append(dou_value*value_ratio[1])
        # 三带数
        tri_value = 0
        tri_num = list(filter(lambda x:x[1] == 3, enumerate(hand_card_status)))
        tri_num = tri_num if isinstance(tri_num, int) else len(tri_num)
        tri_value = tri_num * 3 * 0.1
        value.append(tri_value*value_ratio[2])
        # 连子数
        cont_value = 0
        cont_num_list = []
        for k in (5,6,7,8,9,10,11,12,13,14,15,16,17):
            cont_num = HandCardUtils.find_continues(hand_card_status, k)
            cont_num = cont_num if isinstance(cont_num, int) else len(cont_num)
            cont_num_list.append(cont_num)
        p = 1 / len(cont_num_list) if len(cont_num_list) > 0 else 0
        cont_num = sum(list(map(lambda x:x*p, cont_num_list)))
        cont_value = cont_num * 0.1
        value.append(cont_value*value_ratio[3])
        # 炸弹数
        bomb_value = 0
        comm_bomb_num = list(filter(lambda x:x[1] == 4, enumerate(hand_card_status)))
        comm_bomb_num = comm_bomb_num if isinstance(comm_bomb_num, int) else len(comm_bomb_num)    
        master_bomb = list(filter(lambda x:x in [CardEnum.QU.value, CardEnum.JA.value], 
                    hand_card_seq))
        is_contain_master_bomb = False
        if not isinstance(master_bomb, int) and len(master_bomb) == 2:
            is_contain_master_bomb = True
        bomb_value = comm_bomb_num * 0.4
        if is_contain_master_bomb:
            bomb_value += 5
        value.append(bomb_value*value_ratio[4])
        return sum(value)

    @staticmethod
    def value_map(primary_item, card_type, card_count):
        _CONST = 100
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
            return (primary_item * 5 + 10) / _CONST
        # 炸弹(王炸)
        if card_type == CardTypeEnum.CT_BOMB and card_count == 2:
            return 1
        # 炸弹(普通炸弹)
        if card_type == CardTypeEnum and card_count == 4:
            return (primary_item * 6) / _CONST

        return 0


if __name__ == '__main__':

   pass