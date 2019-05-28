#! /usr/bin/env python3

from card_color_enum import CardColorEnum
from card_enum import CardEnum
import random

ALL_CARD = []
for card in CardEnum:
    if card not in (CardEnum.QU, CardEnum.JO):
        ALL_CARD.append((CardColorEnum.SPADE, card.value))
        ALL_CARD.append((CardColorEnum.HEART, card.value))
        ALL_CARD.append((CardColorEnum.CLUB, card.value))
        ALL_CARD.append((CardColorEnum.DIAMOND, card.value))
# 加入大小王
ALL_CARD.append((CardColorEnum.SPADE,CardEnum.QU.value))
ALL_CARD.append((CardColorEnum.HEART,CardEnum.JO.value))


ALL_CARD_NO_COLOR = list(map(lambda x:x[1], ALL_CARD))

ALL_UNIQUE_CARD = list()
for card_item in CardEnum:
    ALL_UNIQUE_CARD.append(card_item.value)


if __name__  == '__main__':
    #random.shuffle(ALL_CARD)
    #for item in ALL_CARD:
    #    print(item)
    #print(ALL_CARD)
    #for item in ALL_CARD_NO_COLOR:
    #    print(item)
    print(ALL_UNIQUE_CARD)