#! /usr/bin/env python3

from enum import Enum

"""
牌的颜色枚举类
"""

class CardColorEnum(Enum):
    # 黑桃
    SPADE = 1,'黑桃'
    # 红桃
    HEART = 2,'红桃'
    # 梅花
    CLUB = 3,'梅花'
    # 方片
    DIAMOND = 4,'方片'