#! /usr/bin/env python3

from card_color_enum import CardColorEnum
from card_enum import CardEnum
import random

ALL_CARD = []
for k in range(CardEnum.TH.value, CardEnum.QU.value, 1):
    ALL_CARD.append((CardColorEnum.SPADE, k))
    ALL_CARD.append((CardColorEnum.HEART, k))
    ALL_CARD.append((CardColorEnum.CLUB, k))
    ALL_CARD.append((CardColorEnum.DIAMOND, k))
# 加入大小王
ALL_CARD.append((CardColorEnum.SPADE,CardEnum.QU.value))
ALL_CARD.append((CardColorEnum.HEART,CardEnum.JA.value))

if __name__  == '__main__':
    random.shuffle(ALL_CARD)
    for item in ALL_CARD:
        print(item)
    #print(ALL_CARD)