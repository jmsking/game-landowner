#! /usr/bin/env python3

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from hand_card_utils import HandCardUtils



def test_find_even_pair():
    #hand_card = [3,3,4,4,5,6,6,7,7,8,8,10,10,11,12,12,13,13,14,14,15,15,16]
    hand_card_status = [0, 0, 0, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 3, 0, 0, 0, 0]
    k = 2
    #hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card)
    res = HandCardUtils.find_even_pair(hand_card_status, k)
    print(res)

def test_find_even_three():
    hand_card = [3,3,3,4,4,4,5,6,6,6,7,7,7,8,8,8,10,10,10,11,12,12,12,13,13,13,14,14,14]
    k = 3
    hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card)
    res = HandCardUtils.find_even_pair(hand_card_status, k)
    print(res)

def test_find_continues():
    hand_card = [3,3,3,4,4,4,5,6,6,6,7,7,7,8,8,8,10,10,10,11,12,12,12,13,13,13,14,14,14]
    k = 5
    hand_card_status = HandCardUtils.obtain_hand_card_status(hand_card)
    res = HandCardUtils.find_continues(hand_card_status, k)
    print(res)

if __name__ == '__main__':
    #test_find_even_pair()
    #test_find_even_three()
    test_find_continues()
