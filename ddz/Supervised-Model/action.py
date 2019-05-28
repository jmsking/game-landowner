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
for card_count in range(5, 13, 1):
    print(card_count)
    action_type = ActionTypeEnum.ACTION_PUT_5_CONTINUE
    if card_count == 6:
        action_type = ActionTypeEnum.ACTION_PUT_6_CONTINUE
    elif card_count == 7:
        action_type = ActionTypeEnum.ACTION_PUT_7_CONTINUE
    elif card_count == 8:
        action_type = ActionTypeEnum.ACTION_PUT_8_CONTINUE
    elif card_count == 9:
        action_type = ActionTypeEnum.ACTION_PUT_9_CONTINUE
    elif card_count == 10:
        action_type = ActionTypeEnum.ACTION_PUT_10_CONTINUE
    elif card_count == 11:
        action_type = ActionTypeEnum.ACTION_PUT_11_CONTINUE
    elif card_count == 12:
        action_type = ActionTypeEnum.ACTION_PUT_12_CONTINUE
    for ind in range(len(all_card_tmp)-card_count + 1):
        card = all_card_tmp[ind:ind+card_count]
        ACTION_DICT[k] = (Primal.SOLO, False, True, 
                            CardTypeStruct(action_type, card_count, card[-1]),
                            card)
        k += 1

# pair - kicker(No) - chain(No) - cardTypeStruct - card
# quantity(13)
# Remove 'S', 'B'
for card_item in ALL_UNIQUE_CARD[:-2]:
    ACTION_DICT[k] = (Primal.PAIR, False, False, 
                        CardTypeStruct(ActionTypeEnum.ACTION_PUT_DOU, 2, card_item),
                        [card_item, card_item])
    k += 1

# pair - kicker(No) - chain(Yes) - cardTypeStruct - card
# quantity(52)
# Remove '2', 'S', 'B'
for card_count in range(3, 11, 1):
    action_type = ActionTypeEnum.ACTION_PUT_3_DOU
    if card_count == 4:
        action_type = ActionTypeEnum.ACTION_PUT_6_DOU
    elif card_count == 5:
        action_type = ActionTypeEnum.ACTION_PUT_7_DOU
    elif card_count == 6:
        action_type = ActionTypeEnum.ACTION_PUT_8_DOU
    elif card_count == 7:
        action_type = ActionTypeEnum.ACTION_PUT_9_DOU
    elif card_count == 8:
        action_type = ActionTypeEnum.ACTION_PUT_10_DOU
    elif card_count == 9:
        action_type = ActionTypeEnum.ACTION_PUT_10_DOU
    elif card_count == 10:
        action_type = ActionTypeEnum.ACTION_PUT_10_DOU
    for ind in range(len(all_card_tmp)-card_count + 1):
        card = all_card_tmp[ind:ind+card_count]
        card_comb = list()
        for item in card:
            card_comb.extend([item, item])
        ACTION_DICT[k] = (Primal.PAIR, False, True, 
                            CardTypeStruct(action_type, card_count*2, card[-1]),
                            card_comb)
        k += 1


if __name__ == "__main__":
    #print(k)
    for item in ACTION_DICT.values():
        print(item[-1])
        











