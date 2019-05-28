#! /usr/bin/env python3

from enum import Enum
from all_card import ALL_UNIQUE_CARD
from card_type_struct import CardTypeStruct
from action_type_enum import ActionTypeEnum


"""
Card Main Group
Ex. 33344, 333 is called Main Group
            44 is called Kicker card
"""
class Primal(Enum):
    SOLO = "Solo"
    PAIR = "Pair"
    TRIO = "Trio"
    FOUR = "Four"
    BOMB = "Bomb"
    ROCKET = "Rocket"
    PASS = "Pass"

"""
Definition of the policy network action
"""
ACTION_DICT = dict()
k = 0
# solo - kicker(No) - chain(No) - cardTypeStruct - card
# quantity(15)
for card_item in ALL_UNIQUE_CARD:
    ACTION_DICT[k] = (Primal.SOLO, False, False, 
                        CardTypeStruct(ActionTypeEnum.ACTION_PUT_ONE, 1, card_item),
                        [card_item])
    k += 1
# solo - kicker(No) - chain(Yes) - cardTypeStruct - card
# quantity(36)
# Remove '2', 'S', 'B'
all_card_tmp = ALL_UNIQUE_CARD[:-3]
for ind in range(len(all_card_tmp)-5 + 1):
    card = all_card_tmp[ind:ind+5]
    ACTION_DICT[k] = (Primal.SOLO, False, True, 
                        CardTypeStruct(ActionTypeEnum.ACTION_PUT_5_CONTINUE, 5, card[-1]),
                        card)
    k += 1




if __name__ == "__main__":
    for item in ACTION_DICT.values():
        print(item[-1])
        











