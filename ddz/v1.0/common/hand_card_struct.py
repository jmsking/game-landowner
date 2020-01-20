#! /usr/bin/env python3

from hand_card_utils import HandCardUtils
from card_enum import CARD_MAP

"""
手牌结构类
"""
class HandCardStruct(object):

    def __init__(self):
        # 手牌价值
        self._hand_card_value = -1
        # 手牌个数
        self._hand_card_count = -1
        # 手牌需要几轮可以打完
        self._n_epochs = -1
        # 手牌序列(无花色,升序排列)
        self._hand_card_seq = None
        # 手牌序列(有花色,升序排列)
        self._hand_card_color_seq = None
        # 手牌序列颜色
        self._color_seq = None
        # 手牌各单牌的数量,例如手牌为:3489TKKA2
        # 则各单牌的数量列表为:[0,0,0,1,1,0,0,0,1,1,1,0,0,2,1,1,0,0]
        # 其固定长度为18,其中前三个位置固定为0(因为斗地主从3开始)
        self._hand_card_status = None

    @property
    def hand_card_value(self):
        return self._hand_card_value

    @property
    def hand_card_count(self):
        return self._hand_card_count

    @property
    def n_epochs(self):
        return self._n_epochs

    @property
    def hand_card_seq(self):
        repr_hand_card_seq = list()
        for item in self._hand_card_seq:
            if item > 10:
                repr_hand_card_seq.append(CARD_MAP[item])
            else:
                repr_hand_card_seq.append(item)
        return repr_hand_card_seq

    @property
    def hand_card_color_seq(self):
        return self._hand_card_color_seq

    @property
    def color_seq(self):
        return self._color_seq

    @property
    def hand_card_status(self):
        return self._hand_card_status

    '''
    color_seq: [(color1, item1), (color2, item2), ...]
    '''
    @hand_card_color_seq.setter
    def hand_card_color_seq(self, color_seq):
        self._hand_card_color_seq = sorted(color_seq, key=lambda x : x[1], reverse=False)
        # 将有花色序列转换为无花色序列
        self._hand_card_seq = list(map(lambda x:x[1], self._hand_card_color_seq))
        self._color_seq = list(map(lambda x:x[0], self._hand_card_color_seq))
        # 记录每张牌的状态
        self._hand_card_status = HandCardUtils.obtain_hand_card_status(self._hand_card_seq)
        # 记录每张牌的个数
        self._hand_card_count = sum(self._hand_card_status)
        # 得到手牌的初始价值
        self._hand_card_value = HandCardUtils.hand_card_init_value(self._hand_card_seq)

if __name__ == '__main__':
    from card_color_enum import CardColorEnum
    handCardStruct = HandCardStruct()
    color_seq = [(CardColorEnum.SPADE, 5), (CardColorEnum.HEART, 3), (CardColorEnum.CLUB, 10), (CardColorEnum.DIAMOND, 3)]
    handCardStruct.hand_card_color_seq = color_seq
    sort_hand_card_color_seq = handCardStruct.hand_card_color_seq
    sort_hand_card_seq = handCardStruct.hand_card_seq
    print(sort_hand_card_color_seq)
    print(sort_hand_card_seq)