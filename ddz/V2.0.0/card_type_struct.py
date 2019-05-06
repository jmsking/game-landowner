#! /usr/bin/env python3

from card_type_enum import CardTypeEnum

"""
打出的牌型结构
"""

class CardTypeStruct(object):
    def __init__(self):
        # 该牌型所属类型
        self._card_type = CardTypeEnum.CT_ERR
        # 该牌型含有的牌的个数
        self._card_count = -1
        # 该牌型的主因子(即决定该牌型大小的元素)
        self._primary_item = -1
        # 该牌型的价值
        self._card_score = -1

    @property
    def card_type(self):
        return self._card_type
    @property
    def card_count(self):
        return self._card_count
    @property
    def primary_item(self):
        return self._primary_item
    @property
    def card_score(self):
        return self._card_score

    @card_type.setter
    def card_type(self, value):
        assert isinstance(value, CardTypeEnum), 'the value cannot cast to <CardTypeEnum>'
        self._card_type = value
    @card_count.setter
    def card_count(self, value):
        self._card_count = value
    @primary_item.setter
    def primary_item(self, value):
        self._primary_item = value
    @card_score.setter
    def card_score(self, value):
        self._card_score = value