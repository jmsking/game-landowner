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
    # 三连对
    ACTION_PUT_3_DOU = 5
    # 四连对
    ACTION_PUT_4_DOU = 6
    # 五连对
    ACTION_PUT_5_DOU = 7
    # 六连对
    ACTION_PUT_6_DOU = 8
    # 七连对
    ACTION_PUT_7_DOU = 9
    # 八连对
    ACTION_PUT_8_DOU = 10
    # 九连对
    ACTION_PUT_9_DOU = 11
    # 十连对
    ACTION_PUT_10_DOU = 12
    # 两连三不带
    ACTION_PUT_2_THREE = 13
    # 三连三不带
    ACTION_PUT_3_THREE = 14
    # 四连三不带
    ACTION_PUT_4_THREE = 15
    # 五连三不带
    ACTION_PUT_5_THREE = 16
    # 六连三不带
    ACTION_PUT_6_THREE = 17
    # 两连三带一
    ACTION_PUT_2_THREE_ONE = 18
    # 三连三带一
    ACTION_PUT_3_THREE_ONE = 19
    # 四连三带一
    ACTION_PUT_4_THREE_ONE = 20
    # 五连三带一
    ACTION_PUT_5_THREE_ONE = 21
    # 两连三带一对
    ACTION_PUT_2_THREE_DOU = 22
    # 三连三带一对
    ACTION_PUT_3_THREE_DOU = 23
    # 四连三带一对
    ACTION_PUT_4_THREE_DOU = 24
    # 四带二单
    ACTION_PUT_FOUR_ONE = 25
    # 四带二对
    ACTION_PUT_FOUR_DOU = 26
    # 连子(5)
    ACTION_PUT_5_CONTINUE = 27
    # 连子(6)
    ACTION_PUT_6_CONTINUE = 28
    # 连子(7)
    ACTION_PUT_7_CONTINUE = 29
    # 连子(8)
    ACTION_PUT_8_CONTINUE = 30
    # 连子(9)
    ACTION_PUT_9_CONTINUE = 31
    # 连子(10)
    ACTION_PUT_10_CONTINUE = 32
    # 连子(11)
    ACTION_PUT_11_CONTINUE = 33
    # 连子(12)
    ACTION_PUT_12_CONTINUE = 34
    # 炸弹
    ACTION_PUT_BOMB = 35
    # 不出
    ACTION_NO_PUT = 36