#! /usr/bin/env python3

import random
from hand_card_utils import HandCardUtils
from card_type_enum import CardTypeEnum
from action_type_enum import ActionTypeEnum
from card_enum import CardEnum
import config
import numpy as np
import copy

ENV_DEBUG = config.ENV_DEBUG

class Env(object):
    def __init__(self):
        pass

    def reset(self):
        # 3,3,4,4,5,5,6,7,8,9,10,11,12,12,13,13,13
        # 3-17
        while True:
            rnd_card = list(np.random.choice(5,13,[0.24,0.24,0.24,0.24,0.04]))
            qu_ja = list(np.random.choice(2,2,[0.7,0.3]))
            self.hand_card_status = [0,0,0] + rnd_card + qu_ja
            if sum(self.hand_card_status) in [17,20]:
                break
        # card put
        self.put_card_status = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        # player role
        # [1,0,0] upper of landowner
        # [0,1,0] landowner
        # [0,0,1] lower of landowner
        #player_role = [0,1,0]
        # merge
        self.observation = list()
        self.observation.extend(self.hand_card_status)
        self.observation.extend(self.put_card_status)

        self.pre_hand_card_status = copy.deepcopy(self.hand_card_status)
        self.pre_put_card_status = copy.deepcopy(self.put_card_status)
        self.pre_observation = copy.deepcopy(self.observation)

        #self.observation.extend(player_role)
        #print('Current card {}'.format(self.hand_card_status[3:]))
        return self.hand_card_status[3:] + self.put_card_status[3:]

    """
    指定当前环境
    Args:
    hand_card_status: 当前玩家手牌状态
    put_card_status: 已出牌的状态
    """
    def specify_env(self, hand_card_status, put_card_status):
        self.hand_card_status = hand_card_status
        self.put_card_status = put_card_status
        self.observation = list()
        self.observation.extend(self.hand_card_status)
        self.observation.extend(self.put_card_status)

        self.pre_hand_card_status = copy.deepcopy(self.hand_card_status)
        self.pre_put_card_status = copy.deepcopy(self.put_card_status)
        self.pre_observation = copy.deepcopy(self.observation)

        return self.hand_card_status[3:] + self.put_card_status[3:]

    def restore(self):
        self.hand_card_status = copy.deepcopy(self.pre_hand_card_status)
        self.put_card_status = copy.deepcopy(self.pre_put_card_status)
        self.observation = copy.deepcopy(self.pre_observation)

    # action: 0 -> single card; 1 -> double; 2 -> triple
    def step(self, action, primary_item = None, last_action = None):

        self.pre_hand_card_status = copy.deepcopy(self.hand_card_status)
        self.pre_put_card_status = copy.deepcopy(self.put_card_status)
        self.pre_observation = copy.deepcopy(self.observation)

        score = 0
        ERR_CARD_SCORE = 0
        done = False
        info = {'error:':False, 'put_card':[], 'primary_item':None}
        if ENV_DEBUG:
            print('Action: {}'.format(action))
        # 单牌
        if action == ActionTypeEnum.ACTION_PUT_ONE.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] >= 1, enumerate(self.hand_card_status))))
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                score = HandCardUtils.value_map(put_card, CardTypeEnum.CT_ONE, 1)
                self.observation[put_card] -= 1
                self.observation[18+put_card] += 1
                self.hand_card_status[put_card] -= 1
                info['put_card'] = [put_card]
                info['primary_item'] = put_card
                if ENV_DEBUG:
                    print('Put card %s' %put_card)
        # 对子
        elif action == ActionTypeEnum.ACTION_PUT_DOU.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] == 2, enumerate(self.hand_card_status))))
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                score = HandCardUtils.value_map(put_card, CardTypeEnum.CT_DOU, 2)
                self.observation[put_card] -= 2
                self.observation[18+put_card] += 2
                self.hand_card_status[put_card] -= 2
                info['put_card'] = [put_card,put_card]
                info['primary_item'] = put_card
                if ENV_DEBUG:
                    print('Put card %s,%s' %(put_card,put_card))
        # 三不带
        elif action == ActionTypeEnum.ACTION_PUT_THREE.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] == 3, enumerate(self.hand_card_status))))
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                score = HandCardUtils.value_map(put_card, CardTypeEnum.CT_THREE, 3)
                self.observation[put_card] -= 3
                self.observation[18+put_card] += 3
                self.hand_card_status[put_card] -= 3
                info['put_card'] = [put_card,put_card,put_card]
                info['primary_item'] = put_card
                if ENV_DEBUG:
                    print('Put card %s,%s,%s' %(put_card,put_card,put_card))
        # 三带一
        elif action == ActionTypeEnum.ACTION_PUT_THREE_ONE.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] == 3, enumerate(self.hand_card_status)))) 
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                other_exist_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[1] >= 1 and x[0] != put_card, enumerate(self.hand_card_status))))
                if isinstance(other_exist_card, int):
                    other_exist_card = [other_exist_card]
                if len(other_exist_card) == 0:
                    score = ERR_CARD_SCORE
                    done = True
                    if ENV_DEBUG:
                        print('Can not accept the card')
                else:
                    rnd = random.randint(0,len(other_exist_card)-1)
                    other_put_card = other_exist_card[rnd]
                    score = HandCardUtils.value_map(put_card, CardTypeEnum.CT_THREE_ONE, 4)
                    self.observation[put_card] -= 3
                    self.observation[18+put_card] += 3
                    self.hand_card_status[put_card] -= 3
                    self.observation[other_put_card] -= 1
                    self.observation[18+other_put_card] += 1
                    self.hand_card_status[other_put_card] -= 1
                    info['put_card'] = [put_card,put_card,put_card,other_put_card]
                    info['primary_item'] = put_card
                    if ENV_DEBUG:
                        print('Put card %s,%s,%s,%s' %(put_card,put_card,put_card,other_put_card))
        # 三带一对
        elif action == ActionTypeEnum.ACTION_PUT_THREE_DOU.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] == 3, enumerate(self.hand_card_status)))) 
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                other_exist_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[1] >= 2 and x[0] != put_card, enumerate(self.hand_card_status))))
                if isinstance(other_exist_card, int):
                    other_exist_card = [other_exist_card]
                if len(other_exist_card) == 0:
                    score = ERR_CARD_SCORE
                    done = True
                    if ENV_DEBUG:
                        print('Can not accept the card')
                else:
                    rnd = random.randint(0,len(other_exist_card)-1)
                    other_put_card = other_exist_card[rnd]
                    score = HandCardUtils.value_map(put_card, CardTypeEnum.CT_THREE_DOU, 5)
                    self.observation[put_card] -= 3
                    self.observation[18+put_card] += 3
                    self.hand_card_status[put_card] -= 3
                    self.observation[other_put_card] -= 2
                    self.observation[18+other_put_card] += 2
                    self.hand_card_status[other_put_card] -= 2
                    info['put_card'] = [put_card,put_card,put_card,other_put_card,other_put_card]
                    info['primary_item'] = put_card
                    if ENV_DEBUG:
                        print('Put card %s,%s,%s,%s,%s' %(put_card,put_card,put_card,other_put_card,other_put_card))
        # 两连对
        elif action == ActionTypeEnum.ACTION_PUT_2_DOU.value:
            K = 2
            exist_card = HandCardUtils.find_even_pair(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_DOU, 4)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 2
                    self.observation[18+put_card] += 2
                    self.hand_card_status[put_card] -= 2
                    log_put.extend([put_card,put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s' %tuple(log_put))
        # 三连对
        elif action == ActionTypeEnum.ACTION_PUT_3_DOU.value:
            K = 3
            exist_card = HandCardUtils.find_even_pair(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:    
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_DOU, 6)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 2
                    self.observation[18+put_card] += 2
                    self.hand_card_status[put_card] -= 2
                    log_put.extend([put_card,put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 四连对
        elif action == ActionTypeEnum.ACTION_PUT_4_DOU.value:
            K = 4
            exist_card = HandCardUtils.find_even_pair(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_DOU, 8)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 2
                    self.observation[18+put_card] += 2
                    self.hand_card_status[put_card] -= 2
                    log_put.extend([put_card,put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 五连对
        elif action == ActionTypeEnum.ACTION_PUT_5_DOU.value:
            K = 5
            exist_card = HandCardUtils.find_even_pair(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_DOU, 10)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 2
                    self.observation[18+put_card] += 2
                    self.hand_card_status[put_card] -= 2
                    log_put.extend([put_card,put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 两连三不带
        elif action == ActionTypeEnum.ACTION_PUT_2_THREE.value:
            K = 2
            exist_card = HandCardUtils.find_even_three(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_THREE, 6)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 3
                    self.observation[18+put_card] += 3
                    self.hand_card_status[put_card] -= 3
                    log_put.extend([put_card,put_card,put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 三连三不带
        elif action == ActionTypeEnum.ACTION_PUT_3_THREE.value:
            K = 3
            exist_card = HandCardUtils.find_even_three(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_THREE, 9)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 3
                    self.observation[18+put_card] += 3
                    self.hand_card_status[put_card] -= 3
                    log_put.extend([put_card,put_card,put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 两连三带一
        elif action == ActionTypeEnum.ACTION_PUT_2_THREE_ONE.value:
            K = 2
            exist_card = HandCardUtils.find_even_three(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                other_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[0] not in exist_card, enumerate(self.hand_card_status))))
                if len(other_card) < K:
                    score = ERR_CARD_SCORE
                    done = True
                    if ENV_DEBUG:
                        print('Can not accept the card')
                else:
                    tmp = list()
                    for _ in range(K):
                        rnd = random.randint(0,len(other_card)-1)
                        tmp_card = other_card[rnd]
                        tmp.append(tmp_card)
                        self.observation[tmp_card] -= 1
                        self.observation[18+tmp_card] += 1
                        self.hand_card_status[tmp_card] -= 1
                    score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_THREE_ONE, 3*K+K)
                    log_put = list()
                    for put_card in exist_card:
                        self.observation[put_card] -= 3
                        self.observation[18+put_card] += 3
                        self.hand_card_status[put_card] -= 3
                        log_put.extend([put_card,put_card,put_card])
                    log_put.extend(tmp)
                    info['put_card'] = log_put
                    info['primary_item'] = exist_card[-1]
                    if ENV_DEBUG:
                        print('Put card %s,%s,%s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 三连三带一
        elif action == ActionTypeEnum.ACTION_PUT_3_THREE_ONE.value:
            K = 3
            exist_card = HandCardUtils.find_even_three(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                other_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[0] not in exist_card, enumerate(self.hand_card_status))))
                if len(other_card) < K:
                    score = ERR_CARD_SCORE
                    done = True
                    if ENV_DEBUG:
                        print('Can not accept the card')
                else:
                    tmp = list()
                    for _ in range(K):
                        rnd = random.randint(0,len(other_card)-1)
                        tmp_card = other_card[rnd]
                        tmp.append(tmp_card)
                        self.observation[tmp_card] -= 1
                        self.observation[18+tmp_card] += 1
                        self.hand_card_status[tmp_card] -= 1
                    score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_THREE_ONE, 3*K+K)
                    log_put = list()
                    for put_card in exist_card:
                        self.observation[put_card] -= 3
                        self.observation[18+put_card] += 3
                        self.hand_card_status[put_card] -= 3
                        log_put.extend([put_card,put_card,put_card])
                    log_put.extend(tmp)
                    info['put_card'] = log_put
                    info['primary_item'] = exist_card[-1]
                    if ENV_DEBUG:
                        print('Put card %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 两连三带一对
        elif action == ActionTypeEnum.ACTION_PUT_2_THREE_DOU.value:
            K = 2
            exist_card = HandCardUtils.find_even_three(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                other_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[0] not in exist_card and x[1] == 2, enumerate(self.hand_card_status))))
                if len(other_card) < K:
                    score = ERR_CARD_SCORE
                    done = True
                    if ENV_DEBUG:
                        print('Can not accept the card')
                else:
                    tmp = list()
                    for _ in range(K):
                        rnd = random.randint(0,len(other_card)-1)
                        tmp_card = other_card[rnd]
                        tmp.extend([tmp_card,tmp_card])
                        self.observation[tmp_card] -= 2
                        self.observation[18+tmp_card] += 2
                        self.hand_card_status[tmp_card] -= 2
                    score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_THREE_DOU, 3*K+2*K)
                    log_put = list()
                    for put_card in exist_card:
                        self.observation[put_card] -= 3
                        self.observation[18+put_card] += 3
                        self.hand_card_status[put_card] -= 3
                        log_put.extend([put_card,put_card,put_card])
                    log_put.extend(tmp)
                    info['put_card'] = log_put
                    info['primary_item'] = exist_card[-1]
                    if ENV_DEBUG:
                        print('Put card %s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 三连三带一对
        elif action == ActionTypeEnum.ACTION_PUT_3_THREE_DOU.value:
            K = 3
            exist_card = HandCardUtils.find_even_three(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                other_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[0] not in exist_card and x[1] == 2, enumerate(self.hand_card_status))))
                if len(other_card) < K:
                    score = ERR_CARD_SCORE
                    done = True
                    if ENV_DEBUG:
                        print('Can not accept the card')
                else:
                    tmp = list()
                    for _ in range(K):
                        rnd = random.randint(0,len(other_card)-1)
                        tmp_card = other_card[rnd]
                        tmp.extend([tmp_card,tmp_card])
                        self.observation[tmp_card] -= 2
                        self.observation[18+tmp_card] += 2
                        self.hand_card_status[tmp_card] -= 2
                    score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_THREE_DOU, 3*K+2*K)
                    log_put = list()
                    for put_card in exist_card:
                        self.observation[put_card] -= 3
                        self.observation[18+put_card] += 3
                        self.hand_card_status[put_card] -= 3
                        log_put.extend([put_card,put_card,put_card])
                    log_put.extend(tmp)
                    info['put_card'] = log_put
                    info['primary_item'] = exist_card[-1]
                    if ENV_DEBUG:
                        print('Put card %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 四带二单
        elif action == ActionTypeEnum.ACTION_PUT_FOUR_ONE.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] == 4, enumerate(self.hand_card_status)))) 
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                other_exist_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[1] >= 1 and x[0] != put_card, enumerate(self.hand_card_status))))
                if isinstance(other_exist_card, int):
                    other_exist_card = [other_exist_card]
                if len(other_exist_card) <= 1:
                    score = ERR_CARD_SCORE
                    done = True
                    if ENV_DEBUG:
                        print('Can not accept the card')
                else:
                    score = HandCardUtils.value_map(put_card, CardTypeEnum.CT_FOUR_ONE, 6)
                    self.observation[put_card] -= 4
                    self.observation[18+put_card] += 4
                    self.hand_card_status[put_card] -= 4
                    pre = -1
                    t = 0
                    tmp = list()
                    while t < 2:
                        rnd = random.randint(0,len(other_exist_card)-1)
                        while True:
                            if rnd != pre:
                                pre = rnd
                                break
                            rnd = random.randint(0,len(other_exist_card)-1)
                        other_put_card = other_exist_card[rnd]
                        tmp.append(other_put_card)
                        self.observation[other_put_card] -= 1
                        self.observation[18+other_put_card] += 1
                        self.hand_card_status[other_put_card] -= 1
                        t += 1
                    log_put = [put_card]*4
                    log_put.extend(tmp)
                    info['put_card'] = log_put
                    info['primary_item'] = put_card
                    if ENV_DEBUG:
                        print('Put card %s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 四带二对
        elif action == ActionTypeEnum.ACTION_PUT_FOUR_DOU.value:
            exist_card = list(map(lambda x:x[0], filter(lambda x: x[1] == 4, enumerate(self.hand_card_status)))) 
            if isinstance(exist_card, int):
                exist_card = [exist_card]
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                other_exist_card = list(map(lambda x:x[0], 
                    filter(lambda x: x[1] >= 2 and x[0] != put_card, enumerate(self.hand_card_status))))
                if isinstance(other_exist_card, int):
                    other_exist_card = [other_exist_card]
                if len(other_exist_card) <= 1:
                    score = ERR_CARD_SCORE
                    done = True
                    if ENV_DEBUG:
                        print('Can not accept the card')
                else:
                    score = HandCardUtils.value_map(put_card, CardTypeEnum.CT_FOUR_DOU, 8)
                    self.observation[put_card] -= 4
                    self.observation[18+put_card] += 4
                    self.hand_card_status[put_card] -= 4
                    pre = -1
                    t = 0
                    tmp = list()
                    while t < 2:
                        rnd = random.randint(0,len(other_exist_card)-1)
                        while True:
                            if rnd != pre:
                                pre = rnd
                                break
                            rnd = random.randint(0,len(other_exist_card)-1)
                        other_put_card = other_exist_card[rnd]
                        tmp.extend([other_put_card,other_put_card])
                        self.observation[other_put_card] -= 2
                        self.observation[18+other_put_card] += 2
                        self.hand_card_status[other_put_card] -= 2
                        t += 1
                    log_put = [put_card]*4
                    log_put.extend(tmp)
                    info['put_card'] = log_put
                    info['primary_item'] = put_card
                    if ENV_DEBUG:
                        print('Put card %s,%s,%s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 连子(5)
        elif action == ActionTypeEnum.ACTION_PUT_5_CONTINUE.value:
            K = 5
            exist_card = HandCardUtils.find_continues(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_CONTINUE, K)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 1
                    self.observation[18+put_card] += 1
                    self.hand_card_status[put_card] -= 1
                    log_put.extend([put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s,%s' %tuple(log_put))
        # 连子(6)
        elif action == ActionTypeEnum.ACTION_PUT_6_CONTINUE.value:
            K = 6
            exist_card = HandCardUtils.find_continues(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_CONTINUE, K)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 1
                    self.observation[18+put_card] += 1
                    self.hand_card_status[put_card] -= 1
                    log_put.extend([put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s,%s,%s' %tuple(log_put))

        # 连子(7)
        elif action == ActionTypeEnum.ACTION_PUT_7_CONTINUE.value:
            K = 7
            exist_card = HandCardUtils.find_continues(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_CONTINUE, K)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 1
                    self.observation[18+put_card] += 1
                    self.hand_card_status[put_card] -= 1
                    log_put.extend([put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s,%s,%s,%s' %tuple(log_put))

        # 连子(8)
        elif action == ActionTypeEnum.ACTION_PUT_8_CONTINUE.value:
            K = 8
            exist_card = HandCardUtils.find_continues(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_CONTINUE, K)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 1
                    self.observation[18+put_card] += 1
                    self.hand_card_status[put_card] -= 1
                    log_put.extend([put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s,%s,%s,%s,%s' %tuple(log_put))

        # 连子(9)
        elif action == ActionTypeEnum.ACTION_PUT_9_CONTINUE.value:
            K = 9
            exist_card = HandCardUtils.find_continues(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_CONTINUE, K)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 1
                    self.observation[18+put_card] += 1
                    self.hand_card_status[put_card] -= 1
                    log_put.extend([put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s,%s,%s,%s,%s,%s' %tuple(log_put))

        # 连子(10)
        elif action == ActionTypeEnum.ACTION_PUT_10_CONTINUE.value:
            K = 10
            exist_card = HandCardUtils.find_continues(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_CONTINUE, K)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 1
                    self.observation[18+put_card] += 1
                    self.hand_card_status[put_card] -= 1
                    log_put.extend([put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 连子(11)
        elif action == ActionTypeEnum.ACTION_PUT_11_CONTINUE.value:
            K = 11
            exist_card = HandCardUtils.find_continues(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_CONTINUE, K)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 1
                    self.observation[18+put_card] += 1
                    self.hand_card_status[put_card] -= 1
                    log_put.extend([put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 连子(12)
        elif action == ActionTypeEnum.ACTION_PUT_12_CONTINUE.value:
            K = 12
            exist_card = HandCardUtils.find_continues(self.hand_card_status, k=K)
            if primary_item is not None:
                exist_card = list(filter(lambda x:x > primary_item,exist_card))
                if isinstance(exist_card, int):
                    exist_card = [exist_card]
            if len(exist_card) == 0:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = random.randint(0,len(exist_card)-1)
                put_card = exist_card[rnd]
                exist_card = [put_card - ix for ix in reversed(range(K))]
                score = HandCardUtils.value_map(exist_card[-1], CardTypeEnum.CT_CONTINUE, K)
                log_put = list()
                for put_card in exist_card:
                    self.observation[put_card] -= 1
                    self.observation[18+put_card] += 1
                    self.hand_card_status[put_card] -= 1
                    log_put.extend([put_card])
                info['put_card'] = log_put
                info['primary_item'] = exist_card[-1]
                if ENV_DEBUG:
                    print('Put card %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %tuple(log_put))
        # 炸弹
        elif action == ActionTypeEnum.ACTION_PUT_BOMB.value:
            qu_ja = [CardEnum.QU.value, CardEnum.JA.value]
            comm_bomb = list(map(lambda x:x[0], filter(lambda x: x[1] == 4, enumerate(self.hand_card_status))))
            master_bomb = list(map(lambda x:x[0], filter(lambda x: x[0] in qu_ja and x[1] == 1, enumerate(self.hand_card_status))))
            if isinstance(comm_bomb, int):
                comm_bomb = [comm_bomb]
            if isinstance(master_bomb, int):
                master_bomb = [master_bomb]
            if primary_item is not None and last_action == ActionTypeEnum.ACTION_PUT_BOMB.value:
                comm_bomb = list(filter(lambda x:x > primary_item,comm_bomb))
                if isinstance(comm_bomb, int):
                    comm_bomb = [comm_bomb]
            if len(comm_bomb) == 0 and len(master_bomb) < 2:
                score = ERR_CARD_SCORE
                done = True
                if ENV_DEBUG:
                    print('Can not accept the card')
            else:
                rnd = len(comm_bomb)
                put_card = qu_ja
                if len(comm_bomb) >= 1 and len(master_bomb) == 2:
                    rnd = random.randint(0,len(comm_bomb))
                elif len(comm_bomb) >= 1:
                    rnd = random.randint(0,len(comm_bomb)-1)
                if rnd < len(comm_bomb):
                    put_card = comm_bomb[rnd]
                card_count = 4 if isinstance(put_card, int) else 2
                if card_count == 2:
                    score = HandCardUtils.value_map(put_card[-1], CardTypeEnum.CT_BOMB, card_count)
                    for item in put_card:
                        self.observation[item] -= 1
                        self.observation[18+item] += 1
                        self.hand_card_status[item] -= 1
                    info['put_card'] = put_card
                    info['primary_item'] = put_card[-1]
                    if ENV_DEBUG:
                        print('Put card %s,%s' %tuple(put_card))
                else:
                    score = HandCardUtils.value_map(put_card, CardTypeEnum.CT_BOMB, card_count)
                    self.observation[put_card] -= 4
                    self.observation[18+put_card] += 4
                    self.hand_card_status[put_card] -= 4
                    info['put_card'] = [put_card,put_card,put_card,put_card]
                    info['primary_item'] = put_card
                    if ENV_DEBUG:
                        print('Put card %s,%s,%s,%s' %(put_card,put_card,put_card,put_card))
        # 不出
        elif action == ActionTypeEnum.ACTION_NO_PUT.value:
            if ENV_DEBUG:
                print('Not put card')

        #if self._is_done():
        #    score += 1
        if ENV_DEBUG:
            print('Current card: %s' %self.hand_card_status)
            print('Current env: %s' %self.observation)
            print('is game over: %s' %(self._is_done() or done))
        #neg = list(filter(lambda x:x<0, self.hand_card_status))
        #if isinstance(neg, int) or len(neg) > 0:
        #    exit
        info['error'] = done
        return self.observation[3:18]+self.observation[21:], score, self._is_done() or done, info

    def _is_done(self):
        return sum(self.hand_card_status) == 0

if __name__ == '__main__':
    env = Env()
    obser = env.reset()
    print(obser)
    print(env.hand_card_status)
    done = False
    t = 1
    print('------------------start [{}]'.format(t))
    while t <= 10:
        action = random.randint(0,26)
        _, _, done, info = env.step(action)
        if done:
            obser = env.reset()
            t += 1
            print('------------------start [{}]'.format(t))