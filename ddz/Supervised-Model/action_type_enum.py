#! /usr/bin/env python3

from enum import Enum

"""
For Generating Data
"""
class ActionTypeEnum(Enum):
    ACTION_PUT_ONE = '单牌'
    ACTION_PUT_DOU = '对子'
    ACTION_PUT_THREE = '三不带'
    ACTION_PUT_THREE_ONE = '三带一'
    ACTION_PUT_THREE_DOU = '三带一对'
    ACTION_PUT_3_DOU = '三连对'
    ACTION_PUT_4_DOU = '四连对'
    ACTION_PUT_5_DOU = '五连对'
    ACTION_PUT_6_DOU = '六连对'
    ACTION_PUT_7_DOU = '七连对'
    ACTION_PUT_8_DOU = '八连对'
    # 
    ACTION_PUT_2_THREE = '两连三不带'
    # 
    ACTION_PUT_3_THREE = '三连三不带'
    # 
    ACTION_PUT_2_THREE_ONE = '两连三带一'
    # 
    ACTION_PUT_3_THREE_ONE = '三连三带一'
    # 
    ACTION_PUT_2_THREE_DOU = '两连三带一对'
    # 
    ACTION_PUT_3_THREE_DOU = '三连三带一对'
    ACTION_PUT_FOUR_ONE = '四带二单'
    ACTION_PUT_FOUR_DOU = '四带二对'

    ACTION_PUT_5_CONTINUE = '5连子'
    ACTION_PUT_6_CONTINUE = '6连子'
    ACTION_PUT_7_CONTINUE = '7连子'
    ACTION_PUT_8_CONTINUE = '8连子'
    ACTION_PUT_9_CONTINUE = '9连子'
    ACTION_PUT_10_CONTINUE = '10连子'
    ACTION_PUT_11_CONTINUE = '11连子'
    ACTION_PUT_12_CONTINUE = '12连子'

    ACTION_PUT_BOMB = '炸弹'
    ACTION_NO_PUT = '不出'