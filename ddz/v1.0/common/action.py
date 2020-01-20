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
Definition of the value network (O-Net, L-Net, U-Net) action
"""
POLICY_ACTION_DICT = dict()
k = 0
# solo - kicker(No) - chain(No) - cardTypeStruct - card
# quantity(15)
for card_item in ALL_UNIQUE_CARD:
    POLICY_ACTION_DICT[k] = (Primal.SOLO, False, False, 
                        CardTypeStruct(ActionTypeEnum.ACTION_PUT_ONE, 1, card_item),
                        [card_item])
    k += 1
# solo - kicker(No) - chain(Yes) - cardTypeStruct - card
# quantity(36)
# Remove '2', 'S', 'B'
all_card_tmp = ALL_UNIQUE_CARD[:-3]
for card_count in range(5, 13, 1):
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
        POLICY_ACTION_DICT[k] = (Primal.SOLO, False, True, 
                            CardTypeStruct(action_type, card_count, card[-1]),
                            card)
        k += 1

# pair - kicker(No) - chain(No) - cardTypeStruct - card
# quantity(13)
# Remove 'S', 'B'
for card_item in ALL_UNIQUE_CARD[:-2]:
    POLICY_ACTION_DICT[k] = (Primal.PAIR, False, False, 
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
        POLICY_ACTION_DICT[k] = (Primal.PAIR, False, True, 
                            CardTypeStruct(action_type, card_count*2, card[-1]),
                            card_comb)
        k += 1

# trio - kicker(No) - chain(No) - cardTypeStruct - card
# quantity(13)
# Remove 'S', 'B'
for card_item in ALL_UNIQUE_CARD[:-2]:
    POLICY_ACTION_DICT[k] = (Primal.TRIO, False, False, 
                        CardTypeStruct(ActionTypeEnum.ACTION_PUT_THREE, 3, card_item),
                        [card_item, card_item, card_item])
    k += 1

# trio - kicker(No) - chain(Yes) - cardTypeStruct - card
# quantity(45)
# Remove '2', 'S', 'B'
for card_count in range(2, 7, 1):
    action_type = ActionTypeEnum.ACTION_PUT_2_THREE
    if card_count == 3:
        action_type = ActionTypeEnum.ACTION_PUT_3_THREE
    elif card_count == 4:
        action_type = ActionTypeEnum.ACTION_PUT_4_THREE
    elif card_count == 5:
        action_type = ActionTypeEnum.ACTION_PUT_5_THREE
    elif card_count == 6:
        action_type = ActionTypeEnum.ACTION_PUT_6_THREE
    for ind in range(len(all_card_tmp)-card_count + 1):
        card = all_card_tmp[ind:ind+card_count]
        card_comb = list()
        for item in card:
            card_comb.extend([item, item, item])
        POLICY_ACTION_DICT[k] = (Primal.TRIO, False, True, 
                            CardTypeStruct(action_type, card_count*3, card[-1]),
                            card_comb)
        k += 1

# trio - kicker(Yes) - chain(No) - cardTypeStruct - card
# quantity(13)
# Remove 'S', 'B'
for card_item in ALL_UNIQUE_CARD[:-2]:
    POLICY_ACTION_DICT[k] = (Primal.TRIO, True, False, 
                        CardTypeStruct(ActionTypeEnum.ACTION_PUT_THREE_ONE, 4, card_item),
                        [card_item, card_item, card_item])
    k += 1

# trio - kicker(Yes) - chain(Yes) - cardTypeStruct - card
# quantity(38)
# Remove '2', 'S', 'B'
for card_count in range(2, 6, 1):
    action_type = ActionTypeEnum.ACTION_PUT_2_THREE_ONE
    if card_count == 3:
        action_type = ActionTypeEnum.ACTION_PUT_3_THREE_ONE
    elif card_count == 4:
        action_type = ActionTypeEnum.ACTION_PUT_4_THREE_ONE
    elif card_count == 5:
        action_type = ActionTypeEnum.ACTION_PUT_5_THREE_ONE
    for ind in range(len(all_card_tmp)-card_count + 1):
        card = all_card_tmp[ind:ind+card_count]
        card_comb = list()
        for item in card:
            card_comb.extend([item, item, item])
        POLICY_ACTION_DICT[k] = (Primal.TRIO, True, True, 
                            CardTypeStruct(action_type, card_count*3 + card_count, card[-1]),
                            card_comb)
        k += 1

# trio - kicker(Yes) - chain(No) - cardTypeStruct - card
# quantity(13)
# Remove 'S', 'B'
for card_item in ALL_UNIQUE_CARD[:-2]:
    POLICY_ACTION_DICT[k] = (Primal.TRIO, True, False, 
                        CardTypeStruct(ActionTypeEnum.ACTION_PUT_THREE_DOU, 5, card_item),
                        [card_item, card_item, card_item])
    k += 1

# trio - kicker(Yes) - chain(Yes) - cardTypeStruct - card
# quantity(30)
# Remove '2', 'S', 'B'
for card_count in range(2, 5, 1):
    action_type = ActionTypeEnum.ACTION_PUT_2_THREE_DOU
    if card_count == 3:
        action_type = ActionTypeEnum.ACTION_PUT_3_THREE_DOU
    elif card_count == 4:
        action_type = ActionTypeEnum.ACTION_PUT_4_THREE_DOU
    for ind in range(len(all_card_tmp)-card_count + 1):
        card = all_card_tmp[ind:ind+card_count]
        card_comb = list()
        for item in card:
            card_comb.extend([item, item, item])
        POLICY_ACTION_DICT[k] = (Primal.TRIO, True, True, 
                            CardTypeStruct(action_type, card_count*3 + card_count*2, card[-1]),
                            card_comb)
        k += 1

# four - kicker(Yes) - chain(No) - cardTypeStruct - card
# quantity(13)
# Remove 'S', 'B'
for card_item in ALL_UNIQUE_CARD[:-2]:
    POLICY_ACTION_DICT[k] = (Primal.TRIO, True, False, 
                        CardTypeStruct(ActionTypeEnum.ACTION_PUT_FOUR_ONE, 6, card_item),
                        [card_item, card_item, card_item, card_item])
    k += 1

# four - kicker(Yes) - chain(No) - cardTypeStruct - card
# quantity(13)
# Remove 'S', 'B'
for card_item in ALL_UNIQUE_CARD[:-2]:
    POLICY_ACTION_DICT[k] = (Primal.TRIO, True, False, 
                        CardTypeStruct(ActionTypeEnum.ACTION_PUT_FOUR_DOU, 8, card_item),
                        [card_item, card_item, card_item, card_item])
    k += 1

# bomb - kicker(No) - chain(No) - cardTypeStruct - card
# quantity(13)
# Remove 'S', 'B'
for card_item in ALL_UNIQUE_CARD[:-2]:
    POLICY_ACTION_DICT[k] = (Primal.BOMB, False, False, 
                        CardTypeStruct(ActionTypeEnum.ACTION_PUT_BOMB, 4, card_item),
                        [card_item, card_item, card_item, card_item])
    k += 1

# rocket - kicker(No) - chain(No) - cardTypeStruct - card
# quantity(1)
POLICY_ACTION_DICT[k] = (Primal.BOMB, False, False, 
                        CardTypeStruct(ActionTypeEnum.ACTION_PUT_BOMB, 2, ALL_UNIQUE_CARD[-1]),
                        ALL_UNIQUE_CARD[-2:])
k += 1

# pass - kicker(No) - chain(No) - cardTypeStruct - card
# quantity(1)
POLICY_ACTION_DICT[k] = (Primal.PASS, False, False, 
                        CardTypeStruct(ActionTypeEnum.ACTION_NO_PUT, 0, None), ['PASS'])

k += 1

"""
Definition of the kicker network action
"""
KICKER_ACTION_DICT = dict()
k = 0
for card_item in ALL_UNIQUE_CARD:
    KICKER_ACTION_DICT[k] = (Primal.SOLO, [card_item])
    k += 1

for card_item in ALL_UNIQUE_CARD[:-2]:
    KICKER_ACTION_DICT[k] = (Primal.PAIR, [card_item, card_item])
    k += 1


if __name__ == "__main__":
    for item in KICKER_ACTION_DICT.values():
        print(item[-1])
        











