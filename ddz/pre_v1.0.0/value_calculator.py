#! /usr/bin/env python3

from card_type_enum import CardTypeEnum
from card_type_judge import CardTypeJudge
from hand_card_utils import HandCardUtils

"""
手牌价值得分计算
"""

count = 0

class ValueCalculator(object):
    def __init__(self):
        pass

    def _write2file(self, data):
        with open('solution', 'w', encoding='utf-8') as f:
            for key, value in data.items():
                f.write(key+':'+'\t')
                f.write(str(value))
                f.write('\n')

    # hand_card: [[item1], [item2], ...]
    def _calc_put_card_seq_score(self, hand_card):
        ctj = CardTypeJudge()
        score = 0
        for item in hand_card:
            hand_card_status = HandCardUtils.obtain_hand_card_status(item)
            cts = ctj.judge_card_type(hand_card_status)
            one_hand_score = HandCardUtils.value_map(cts.primary_item, cts.card_type, cts.card_count)
            score += one_hand_score
        return score

    def calc_hand_card_value(self, hand_card_seq, hand_card_status):
        put_card_queue = list()
        best_put_card_queue = list()
        solution = dict()
        max_value = [-100]
        n_epoch = -1
        for item in CardTypeEnum:
            if item in (CardTypeEnum.CT_ERR, CardTypeEnum.CT_NO):
                continue
            self._calc_hand_card_value_core(
                hand_card_seq, hand_card_status, put_card_queue, max_value, solution, best_put_card_queue, item)
        n_epoch = len(best_put_card_queue)
        self._write2file(solution)
        return max_value, n_epoch, best_put_card_queue

    def _calc_hand_card_value_core(self, hand_card_seq, hand_card_status, put_card_queue, max_value, solution, best_put_card_queue, put_type):
        # 是一手牌,直接返回该牌型的分值
        cts = CardTypeJudge().judge_card_type(hand_card_status)
        if cts.card_type != CardTypeEnum.CT_ERR:
            global count
            tmp_put_card_queue = put_card_queue.copy()
            tmp_put_card_queue.extend([hand_card_seq])
            solution[str(count)] = tmp_put_card_queue
            score = self._calc_put_card_seq_score(tmp_put_card_queue)
            if score > max_value[0]:
                max_value.clear()
                max_value.append(score)
                best_put_card_queue.clear()
                best_put_card_queue.extend(tmp_put_card_queue)
            count += 1
            return

        if put_type == CardTypeEnum.CT_ONE:
            #print('come into one...')
            for ind, item in enumerate(hand_card_seq):
                #print('----%d---' %ind)
                put_card_queue.append([item])
                new_hand_card_seq = hand_card_seq.copy()
                del new_hand_card_seq[ind]
                new_hand_card_status = hand_card_status.copy()
                new_hand_card_status[item] -= 1
                self._calc_hand_card_value_core(new_hand_card_seq, 
                        new_hand_card_status, put_card_queue, max_value, 
                        solution, best_put_card_queue, CardTypeEnum.CT_ONE)
                if len(new_hand_card_seq) >= 2:
                    self._calc_hand_card_value_core(new_hand_card_seq, 
                        new_hand_card_status, put_card_queue, max_value, 
                        solution, best_put_card_queue, CardTypeEnum.CT_DOU)
                del put_card_queue[-1]
                
        if put_type == CardTypeEnum.CT_DOU:
            #print('come into two...')
            find_two = list(map(lambda x:x[0],filter(lambda x : x[1] == 2, enumerate(hand_card_status))))
            if isinstance(find_two, int):
                find_two = [find_two]
            # 获取不同出法(保证最大连对出法)
            #find_two = HandCardUtils.find_first_sub_seq(find_two)
            for item in find_two:
                #append_val = list()
                #for val in item:
                #    append_val.extend([val, val])
                #put_card_queue.append(append_val)
                put_card_queue.append([item, item])
                #cur_value = self.value_map()
                new_hand_card_seq = list(filter(lambda x:x != item, hand_card_seq))
                new_hand_card_status = hand_card_status.copy()
                #for val in item:
                new_hand_card_status[item] -= 2
                self._calc_hand_card_value_core(new_hand_card_seq, 
                            new_hand_card_status,put_card_queue,max_value, 
                            solution, best_put_card_queue, CardTypeEnum.CT_ONE)
                #del put_card_queue[-1]
                if len(new_hand_card_seq) >= 2:
                    self._calc_hand_card_value_core(new_hand_card_seq, 
                            new_hand_card_status,put_card_queue,max_value, 
                            solution, best_put_card_queue, CardTypeEnum.CT_DOU)
                del put_card_queue[-1]

        if put_type == CardTypeEnum.CT_THREE:
            #print('come into two...')
            find_three = list(map(lambda x:x[0],filter(lambda x : x[1] == 3, enumerate(hand_card_status))))
            if isinstance(find_three, int):
                find_two = [find_three]
            # 获取不同出法(保证最大连对出法)
            #find_two = HandCardUtils.find_first_sub_seq(find_two)
            for item in find_three:
                #append_val = list()
                #for val in item:
                #    append_val.extend([val, val])
                #put_card_queue.append(append_val)
                put_card_queue.append([item, item, item])
                #cur_value = self.value_map()
                new_hand_card_seq = list(filter(lambda x:x != item, hand_card_seq))
                new_hand_card_status = hand_card_status.copy()
                #for val in item:
                new_hand_card_status[item] -= 3
                self._calc_hand_card_value_core(new_hand_card_seq, 
                            new_hand_card_status,put_card_queue,max_value, 
                            solution, best_put_card_queue, CardTypeEnum.CT_ONE)
                #del put_card_queue[-1]
                if len(new_hand_card_seq) >= 2:
                    self._calc_hand_card_value_core(new_hand_card_seq, 
                            new_hand_card_status,put_card_queue,max_value, 
                            solution, best_put_card_queue, CardTypeEnum.CT_DOU)
                del put_card_queue[-1]

        if put_type == CardTypeEnum.CT_THREE_ONE:
            find_three = list(map(lambda x:x[0],filter(lambda x : x[1] == 3, enumerate(hand_card_status))))
            find_one = list(map(lambda x:x[0],filter(lambda x : x[1] == 1, enumerate(hand_card_status))))
            if isinstance(find_three, int):
                find_three = [find_three]
            if isinstance(find_one, int):
                find_one = [find_one]
            for item in find_three:
                new_hand_card_seq = None
                new_hand_card_status = None
                if len(find_one) > 0:
                    put_card_queue.append([item, item, item, find_one[0]])
                    new_hand_card_seq = list(filter(lambda x:x not in [item,find_one[0]], hand_card_seq))
                    new_hand_card_status = hand_card_status.copy()
                    new_hand_card_status[item] -= 3
                    new_hand_card_status[find_one[0]] -= 1
                else:
                    find_number = list(map(lambda x:x[0],filter(lambda x : x[1] != item, enumerate(hand_card_status))))
                    if len(find_number) > 0:
                        put_card_queue.append([item, item, item, find_number[0]])
                        new_hand_card_seq = list(filter(lambda x:x != item, hand_card_seq))
                        fir_ind = new_hand_card_seq.index(find_number[0])
                        del new_hand_card_seq[fir_ind]
                        new_hand_card_status = hand_card_status.copy()
                        new_hand_card_status[item] -= 3
                        new_hand_card_status[find_number[0]] -= 1
                    else:
                        return
                self._calc_hand_card_value_core(new_hand_card_seq, 
                            new_hand_card_status,put_card_queue,max_value, 
                            solution, best_put_card_queue, CardTypeEnum.CT_ONE)
                if len(new_hand_card_seq) >= 2:
                    self._calc_hand_card_value_core(new_hand_card_seq, 
                            new_hand_card_status,put_card_queue,max_value, 
                            solution, best_put_card_queue, CardTypeEnum.CT_DOU)
                del put_card_queue[-1]

        if put_type == CardTypeEnum.CT_THREE_DOU:
            find_three = list(map(lambda x:x[0],filter(lambda x : x[1] == 3, enumerate(hand_card_status))))
            find_two = list(map(lambda x:x[0],filter(lambda x : x[1] == 2, enumerate(hand_card_status))))
            if isinstance(find_three, int):
                find_three = [find_three]
            if isinstance(find_two, int):
                find_two = [find_two]
            for item in find_three:
                new_hand_card_seq = None
                new_hand_card_status = None
                if len(find_two) > 0:
                    put_card_queue.append([item, item, item, find_two[0], find_two[0]])
                    new_hand_card_seq = list(filter(lambda x:x not in [item,find_two[0]], hand_card_seq))
                    new_hand_card_status = hand_card_status.copy()
                    new_hand_card_status[item] -= 3
                    new_hand_card_status[find_two[0]] -= 2
                else:
                    return
                self._calc_hand_card_value_core(new_hand_card_seq, 
                            new_hand_card_status,put_card_queue,max_value, 
                            solution, best_put_card_queue, CardTypeEnum.CT_ONE)
                if len(new_hand_card_seq) >= 2:
                    self._calc_hand_card_value_core(new_hand_card_seq, 
                            new_hand_card_status,put_card_queue,max_value, 
                            solution, best_put_card_queue, CardTypeEnum.CT_DOU)
                del put_card_queue[-1]

if __name__ == '__main__':
    hand_card_seq = [3,4,5,5,6,7,7]
    hand_card_status = [0, 0, 0, 1, 1, 2, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    vc = ValueCalculator()
    score, n_epoch, best_put_hand_card = vc.calc_hand_card_value(
        hand_card_seq, hand_card_status)
    print(score)
    print(n_epoch)
    print(best_put_hand_card)
