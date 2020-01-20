#! /usr/bin/env python3

from enum import Enum

class ActionTypeEnum(Enum):
    ACTION_DEFAULT = -1
    # 单牌
    ACTION_PUT_ONE = 0
    # 对子
    ACTION_PUT_DOU = 1
    # 三不带
    ACTION_PUT_THREE = 2
    # 三带一
    ACTION_PUT_THREE_ONE = 3
    # 三带一对
    ACTION_PUT_THREE_DOU = 4
    # 两连对
    ACTION_PUT_2_DOU = 5
    # 三连对
    ACTION_PUT_3_DOU = 6
    # 四连对
    ACTION_PUT_4_DOU = 7
    # 五连对
    ACTION_PUT_5_DOU = 8
    # 两连三不带
    ACTION_PUT_2_THREE = 9
    # 三连三不带
    ACTION_PUT_3_THREE = 10
    # 两连三带一
    ACTION_PUT_2_THREE_ONE = 11
    # 三连三带一
    ACTION_PUT_3_THREE_ONE = 12
    # 两连三带一对
    ACTION_PUT_2_THREE_DOU = 13
    # 三连三带一对
    ACTION_PUT_3_THREE_DOU = 14
    # 四带二单
    ACTION_PUT_FOUR_ONE = 15
    # 四带二对
    ACTION_PUT_FOUR_DOU = 16
    # 连子(5)
    ACTION_PUT_5_CONTINUE = 17
    # 连子(6)
    ACTION_PUT_6_CONTINUE = 18
    # 连子(7)
    ACTION_PUT_7_CONTINUE = 19
    # 连子(8)
    ACTION_PUT_8_CONTINUE = 20
    # 连子(9)
    ACTION_PUT_9_CONTINUE = 21
    # 连子(10)
    ACTION_PUT_10_CONTINUE = 22
    # 连子(11)
    ACTION_PUT_11_CONTINUE = 23
    # 连子(12)
    ACTION_PUT_12_CONTINUE = 24
    # 炸弹
    ACTION_PUT_BOMB = 25
    # 不出
    ACTION_NO_PUT = 26