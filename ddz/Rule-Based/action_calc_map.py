#! /usr/bin/env python3

from action_type_enum import ActionTypeEnum
from value_calculator.p_1_card_calc import P_1_CardCalc

"""
Action - ValueCalculator 映射字典
"""
ACTION_CALC_DICT = {
    # 单牌
    ActionTypeEnum.ACTION_PUT_ONE.value: P_1_CardCalc,
    # 对子
    ActionTypeEnum.ACTION_PUT_DOU.value: P_1_CardCalc,
    # 三不带
    ActionTypeEnum.ACTION_PUT_THREE.value: P_1_CardCalc,
    # 三带一
    ActionTypeEnum.ACTION_PUT_THREE_ONE.value: P_1_CardCalc,
    # 三带一对
    ActionTypeEnum.ACTION_PUT_THREE_DOU.value: P_1_CardCalc,
    # 两连对
    ActionTypeEnum.ACTION_PUT_2_DOU.value: P_1_CardCalc,
    # 三连对
    ActionTypeEnum.ACTION_PUT_3_DOU.value: P_1_CardCalc,
    # 四连对
    ActionTypeEnum.ACTION_PUT_4_DOU.value: P_1_CardCalc,
    # 五连对
    ActionTypeEnum.ACTION_PUT_5_DOU.value: P_1_CardCalc,
    # 两连三不带
    ActionTypeEnum.ACTION_PUT_2_THREE.value: P_1_CardCalc,
    # 三连三不带
    ActionTypeEnum.ACTION_PUT_3_THREE.value: P_1_CardCalc,
    # 两连三带一
    ActionTypeEnum.ACTION_PUT_2_THREE_ONE.value: P_1_CardCalc,
    # 三连三带一
    ActionTypeEnum.ACTION_PUT_3_THREE_ONE.value: P_1_CardCalc,
    # 两连三带一对
    ActionTypeEnum.ACTION_PUT_2_THREE_DOU.value: P_1_CardCalc,
    # 三连三带一对
    ActionTypeEnum.ACTION_PUT_3_THREE_DOU.value: P_1_CardCalc,
    # 四带二单
    ActionTypeEnum.ACTION_PUT_FOUR_ONE.value: P_1_CardCalc,
    # 四带二对
    ActionTypeEnum.ACTION_PUT_FOUR_DOU.value: P_1_CardCalc,
    # 连子(5)
    ActionTypeEnum.ACTION_PUT_5_CONTINUE.value: P_1_CardCalc,
    # 连子(6)
    ActionTypeEnum.ACTION_PUT_6_CONTINUE.value: P_1_CardCalc,
    # 连子(7)
    ActionTypeEnum.ACTION_PUT_7_CONTINUE.value: P_1_CardCalc,
    # 连子(8)
    ActionTypeEnum.ACTION_PUT_8_CONTINUE.value: P_1_CardCalc,
    # 连子(9)
    ActionTypeEnum.ACTION_PUT_9_CONTINUE.value: P_1_CardCalc,
    # 连子(10)
    ActionTypeEnum.ACTION_PUT_10_CONTINUE.value: P_1_CardCalc,
    # 连子(11)
    ActionTypeEnum.ACTION_PUT_11_CONTINUE.value: P_1_CardCalc,
    # 连子(12)
    ActionTypeEnum.ACTION_PUT_12_CONTINU.value: P_1_CardCalc,
    # 炸弹
    ActionTypeEnum.ACTION_PUT_BOMB.value: P_1_CardCalc,
    # 不出
    ActionTypeEnum.ACTION_NO_PUT.value: P_1_CardCalc
}