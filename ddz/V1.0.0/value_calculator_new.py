#! /usr/bin/env python3

from card_type_enum import CardTypeEnum
from card_type_judge import CardTypeJudge
from card_type_struct import CardTypeStruct

"""
手牌价值得分计算
"""
class ValueCalculator(object):
    def __init__(self):
        pass

    def calc_hand_card_value(self, hand_card_seq, hand_card_status):
        best_put_card_queue = None
        max_value = -100
        n_epoch = -1
        for item in CardTypeEnum:
            self._calc_hand_card_value_core(hand_card_seq, hand_card_status, best_put_card_queue, max_value, CardTypeEnum.CT_ONE)
            if cur_max_value > max_value:
                max_value = cur_max_value
                best_put_card_queue = put_card_queue
            break
        if best_put_card_queue is not None:
            n_epoch = len(best_put_card_queue)
        return max_value, best_put_card_queue

    def _calc_hand_card_value_core(self, hand_card_seq, hand_card_status):
        # 是一手牌,直接返回该牌型的分值
        cts = CardTypeJudge().judge_card_type(hand_card_status)
        if cts.card_type != CardTypeEnum.CT_ERR:
            return cts.card_score, [hand_card_seq]
        
        if put_type == CardTypeEnum.CT_ONE:
            print('come into one...')
            print(hand_card_seq)
            for ind, item in enumerate(hand_card_seq):
                #put_card_queue = list()
                #put_card_queue.append([item])
                best_put_card_queue.extend([item])
                max_value += self.value_map()
                new_hand_card_seq = hand_card_seq.copy()
                del new_hand_card_seq[ind]
                new_hand_card_status = hand_card_status.copy()
                new_hand_card_status[item] -= 1
                self._calc_hand_card_value_core(new_hand_card_seq, new_hand_card_status, CardTypeEnum.CT_ONE)
                if len(hand_card_seq) >= 2:
                    self._calc_hand_card_value_core(new_hand_card_seq, new_hand_card_status, CardTypeEnum.CT_DOU)
                remain_score = [score1, score2]
                remain_queue = [queue1, queue2]
                max_remain_value = max(remain_score)
                best_ind = remain_score.index(max_remain_value)
                best_queue = remain_queue[best_ind]
                cur_max_value = cur_value + max_remain_value
                if cur_max_value > max_value:
                    max_value = cur_max_value
                if len(best_queue) > 0:
                    put_card_queue.extend(best_queue)
                print(max_value)
                print(put_card_queue)
                put_card_queue.clear()
                #return cur_max_value, put_card_queue
        if put_type == CardTypeEnum.CT_DOU:
            print('come into two...')
            print(hand_card_seq)
            find_two = list(map(lambda x:x[0],filter(lambda x : x[1] == 2, enumerate(hand_card_status))))
            if isinstance(find_two, int):
                find_two = [find_two]
            for item in find_two:
                put_card_queue.append([item, item])
                cur_value = self.value_map()
                new_hand_card_seq = list(filter(lambda x:x!=item, hand_card_seq))
                new_hand_card_status = hand_card_status.copy()
                new_hand_card_status[item] -= 2
                self._calc_hand_card_value_core(new_hand_card_seq, new_hand_card_status, CardTypeEnum.CT_ONE)
                self._calc_hand_card_value_core(new_hand_card_seq, new_hand_card_status, CardTypeEnum.CT_DOU)
                remain_score = [score1, score2]
                remain_queue = [queue1, queue2]
                max_remain_value = max(remain_score)
                best_ind = remain_score.index(max_remain_value)
                best_queue = remain_queue[best_ind]
                cur_max_value = cur_value + max_remain_value
                if cur_max_value > max_value:
                    max_value = cur_max_value
                if len(best_queue) > 0:
                    put_card_queue.extend(best_queue)
                print(max_value)
                print(put_card_queue)
                put_card_queue.clear()
                #return cur_max_value, put_card_queue
        return

    def value_map(self):
        return 2

if __name__ == '__main__':
    hand_card_seq = [3,7]
    hand_card_status = [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
    vc = ValueCalculator()
    score, put_hand_card = vc.calc_hand_card_value(hand_card_seq, hand_card_status)
    print(score)
    print(put_hand_card)