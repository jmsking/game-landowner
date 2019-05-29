#! /usr/bin/env python3

from all_card import ALL_CARD_NO_COLOR
import random
from action_type_enum import ActionTypeEnum, ALL_ACTION_TYPE
from env import Env
from hand_card_utils import HandCardUtils
import numpy as np

"""
Deal Card
"""
def _deal_card(c):
    if c == 1:
        return ALL_CARD_NO_COLOR[:17]
    elif c == 2:
        return ALL_CARD_NO_COLOR[17:34]
    elif c == 3:
        return ALL_CARD_NO_COLOR[34:51]
    else:
        return ALL_CARD_NO_COLOR[51:]
"""
Obtain initialized status
"""
def _obtain_init_status(cards1, cards2, cards3, bottom_cards):
    card1 = ''.join(cards1)
    card2 = ''.join(cards2)
    card3 = ''.join(cards3)
    bcards = ''.join(bottom_cards)
    cards = "cards: " + card1 + ";" + card2 + ";" + card3 + ";" + bcards
    return cards

def _gen_agent(cards1, cards2, cards3):
    main_agent_status = HandCardUtils.obtain_hand_card_status(cards1)
    low_agent_status = HandCardUtils.obtain_hand_card_status(cards2)
    up_agent_status = HandCardUtils.obtain_hand_card_status(cards3)
    return main_agent_status, low_agent_status, up_agent_status


"""
Sample Generator
"""
def generate_data():
    random.shuffle(ALL_CARD_NO_COLOR)
    player_cards_1 = _deal_card(1)
    player_cards_2 = _deal_card(2)
    player_cards_3 = _deal_card(3)
    bottom_cards = _deal_card(0)
    cards = _obtain_init_status(player_cards_1, player_cards_2, player_cards_3, bottom_cards)
    print(cards)

    card_process = list()

    main_agent_status, low_agent_status, up_agent_status = _gen_agent(player_cards_1, player_cards_2, player_cards_3)
    env = Env()
    put_card_status = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    last_action = None
    last_primary = None
    curr_flag = "o" # 'o', 'l', 'u'
    while True:
        obser = env.specify_env(main_agent_status, put_card_status)
        action = ActionTypeEnum.ACTION_NO_PUT.value
        if last_action and curr_flag != 'o':
            while True:
                action = np.random.choice(
                    [last_action, 
                    ActionTypeEnum.ACTION_PUT_BOMB.value, 
                    ActionTypeEnum.ACTION_NO_PUT.value], 1)[0]
                if action == last_action:
                    _, done, info = env.step(action, last_primary)
                else:
                    _, done, info = env.step(action)
                err = info['error']
                if not err:
                    env.restore()
                    break
                env.restore() 
        else:
            while True:
                size = len(ALL_ACTION_TYPE)
                rnd = np.random.randint(size)
                action = ALL_ACTION_TYPE[rnd]
                if action == ActionTypeEnum.ACTION_NO_PUT.value:
                    continue
                _, done, info = env.step(action)
                err = info['error']
                if not err:
                    env.restore()
                    break
                env.restore()
        if action != ActionTypeEnum.ACTION_NO_PUT.value:
            curr_flag = 'o'
            last_action = action
            _, done, info = env.step(action, last_primary)
            put_card = info['put_card']
            print(action)
            print(put_card)
            print(info)
            if put_card:
                put_card = ''.join(put_card)
            card_process.append("0," + put_card)
            main_agent_status = env.hand_card_status
            put_card_status = env.put_card_status
            last_primary = info['primary_item']
        else:
            card_process.append("0,PASS")
        if done:
            break
        obser = env.specify_env(low_agent_status, put_card_status)
        action = ActionTypeEnum.ACTION_DEFAULT.value
        if last_action and curr_flag != 'l':
            while True:
                action = np.random.choice(
                    [last_action, 
                    ActionTypeEnum.ACTION_PUT_BOMB.value, 
                    ActionTypeEnum.ACTION_NO_PUT.value], 1)[0]
                if action == last_action:
                    _, done, info = env.step(action, last_primary)
                else:
                    _, done, info = env.step(action)
                err = info['error']
                if not err:
                    env.restore()
                    break
                env.restore() 
        else:
            while True:
                size = len(ALL_ACTION_TYPE)
                rnd = np.random.randint(size)
                action = ALL_ACTION_TYPE[rnd]
                if action == ActionTypeEnum.ACTION_NO_PUT.value:
                    continue
                _, done, info = env.step(action)
                err = info['error']
                if not err:
                    env.restore()
                    break
                env.restore()
        if action != ActionTypeEnum.ACTION_NO_PUT.value:
            curr_flag = 'l'
            last_action = action
            _, done, info = env.step(action, last_primary)
            put_card = info['put_card']
            if put_card:
                put_card = ''.join(put_card)
            card_process.append("1," + put_card)
            low_agent_status = env.hand_card_status
            put_card_status = env.put_card_status
            last_primary = info['primary_item']
        else:
            card_process.append("1,PASS")
        if done:
            break
        obser = env.specify_env(up_agent_status, put_card_status)
        action = ActionTypeEnum.ACTION_DEFAULT.value
        if last_action and curr_flag != 'u':
            while True:
                action = np.random.choice(
                    [last_action, 
                    ActionTypeEnum.ACTION_PUT_BOMB.value, 
                    ActionTypeEnum.ACTION_NO_PUT.value], 1)[0]
                if action == last_action:
                    _, done, info = env.step(action, last_primary)
                else:
                    _, done, info = env.step(action)
                err = info['error']
                if not err:
                    env.restore()
                    break
                env.restore() 
        else:
            while True:
                size = len(ALL_ACTION_TYPE)
                rnd = np.random.randint(size)
                action = ALL_ACTION_TYPE[rnd]
                if action == ActionTypeEnum.ACTION_NO_PUT.value:
                    continue
                _, done, info = env.step(action)
                err = info['error']
                if not err:
                    env.restore()
                    break
                env.restore()
        if action != ActionTypeEnum.ACTION_NO_PUT.value:
            curr_flag = 'u'
            last_action = action
            _, done, info = env.step(action, last_primary)
            put_card = info['put_card']
            if put_card:
                put_card = ''.join(put_card)
            card_process.append("2," + put_card)
            up_agent_status = env.hand_card_status
            put_card_status = env.put_card_status
            last_primary = info['primary_item']
        else:
            card_process.append("2,PASS")
        if done:
            break
    return card_process

if __name__ == "__main__":
    card_process = generate_data()
    print(card_process)