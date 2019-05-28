#! /usr/bin/env python3

from enum import Enum

"""
牌的颜色枚举类
"""

class CardColorEnum(Enum):
    # 黑桃
    SPADE = '黑桃'
    # 红桃
    HEART = '红桃'
    # 梅花
    CLUB = '梅花'
    # 方片
    DIAMOND = '方片'