#! /usr/bin/env python3

from card_color_enum import CardColorEnum
from card_enum import CardEnum
import random

ALL_CARD = []
for card in CardEnum:
    if card not in (CardEnum.QU, CardEnum.JA):
        ALL_CARD.append((CardColorEnum.SPADE, card.value))
        ALL_CARD.append((CardColorEnum.HEART, card.value))
        ALL_CARD.append((CardColorEnum.CLUB, card.value))
        ALL_CARD.append((CardColorEnum.DIAMOND, card.value))
# 加入大小王
ALL_CARD.append((CardColorEnum.SPADE,CardEnum.QU.value))
ALL_CARD.append((CardColorEnum.HEART,CardEnum.JA.value))


ALL_CARD_NO_COLOR = list(map(lambda x:x[1], ALL_CARD))

ALL_UNIQUE_CARD = list()
for card_item in CardEnum:
    ALL_UNIQUE_CARD.append(card_item.value)

CARD_MAP = {
    '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
    'T':10, 'J':11, 'Q':12, 'K':13, 'A':14, '2': 15, 'S': 16, 'B': 17
    }
REV_CARD_MAP = dict()
for k, v in CARD_MAP.items():
    REV_CARD_MAP[v] = k


if __name__  == '__main__':
    #random.shuffle(ALL_CARD)
    #for item in ALL_CARD:
    #    print(item)
    #print(ALL_CARD)
    #for item in ALL_CARD_NO_COLOR:
    #    print(item)
    print(ALL_UNIQUE_CARD)