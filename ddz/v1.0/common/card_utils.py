#! /usr/bin/env python3

#TODO remove in production environment
import sys
base_path = 'd:/study/me/game-landowner/ddz/V3.0.0'
sys.path.append(base_path)

from enums.card_color_enum import CardColorEnum
from enums.card_enum import CardEnum
import random


CARD_MAP = {
    '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
    'T':10, 'J':11, 'Q':12, 'K':13, 'A':14, '2': 15, 'S': 16, 'B': 17
}

class CardUtil:

    @staticmethod
    def all_card():
        cards = []
        for card in CardEnum:
            if card not in (CardEnum.QU, CardEnum.JA):
                cards.append((CardColorEnum.SPADE, card.value))
                cards.append((CardColorEnum.HEART, card.value))
                cards.append((CardColorEnum.CLUB, card.value))
                cards.append((CardColorEnum.DIAMOND, card.value))
        # add Queen and Jack
        cards.append((CardColorEnum.SPADE,CardEnum.QU.value))
        cards.append((CardColorEnum.HEART,CardEnum.JA.value))
        return cards

    @staticmethod
    def all_plain_card():
        cards = CardUtil.all_card()
        plain_cards = list(map(lambda x:x[1], cards))
        return plain_cards

    @staticmethod
    def get_card(card_num=17, exclude_card=None, is_plain=False):
        assert card_num >= 1 and card_num <= 20
        cards = CardUtil.all_card()
        if is_plain:
            cards = CardUtil.all_plain_card()
        cards = CardUtil.__shuffle_card(cards)   
        remain_cards = cards
        if exclude_card:
            remain_cards = list(set(cards) - set(exclude_card))
        if len(remain_cards) < card_num:
            raise Exception(f'Size of avaliable card is {len(remain_cards)}, but need {card_num}')
        remain_cards = remain_cards[:card_num]
        if is_plain:
            remain_cards = sorted(remain_cards)
        else:
            remain_cards = sorted(remain_cards, key=lambda x: x[1])
        return remain_cards

    @staticmethod
    def __shuffle_card(cards):
        random.shuffle(cards)
        return cards

if __name__  == '__main__':
    cards = CardUtil.get_card(card_num=20, is_plain=True)
    print(cards)