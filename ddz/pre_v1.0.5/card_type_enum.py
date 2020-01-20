#! /usr/bin/env python3

from enum import Enum

"""
牌型枚举类
"""

class CardTypeEnum(Enum):
    # 错误牌型
    CT_ERR = -1
    # 不出
    CT_NO = 0
    # 单牌
    CT_ONE = 1
    # 对子
    CT_DOU = 2
    # 三带一单
    CT_THREE_ONE = 3
    # 三带一对
    CT_THREE_DOU = 4
    # 连子
    CT_CONTINUE = 5
    # 四带两单
    CT_FOUR_ONE = 6
    # 四带两对
    CT_FOUR_DOU = 7
    # 三不带
    CT_THREE = 8
    # 炸弹
    CT_BOMB = 9