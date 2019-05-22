#! /usr/bin/env python3

"""
出牌奖赏接口
"""
class AbstractValueCalculator(object):

    @staticmethod
    def obtain_reward(hand_card_status, surround, *args):
        raise NotImplementedError("Not Implemented.")