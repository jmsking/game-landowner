#! /usr/bin/env python3

"""
所能观察的信息类
"""
class Obser():
    def __init__(self):
        # 已出的牌
        self._has_put_card_status = [0]*18

    @property
    def has_put_card_status(self):
        return self._has_put_card_status

    @has_put_card_status.setter
    def has_put_card_status(self, value):
        self._has_put_card_status = value