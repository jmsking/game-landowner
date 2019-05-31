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
    oneP

    main_agent_status, low_agent_status, up_agent_status = _gen_agent(player_cards_1, player_cards_2, player_cards_3)
    env = Env()
    put_card_status = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    last_action = None
    curr_flag = "o" # 'o', 'l', 'u'
    while False:
        obser = env.specify_env(main_agent_status, put_card_status)
        action = ActionTypeEnum.ACTION_NO_PUT.value
        if last_action and curr_flag != 'o':
            while True:
                action = np.random.choice(
                    [last_action, 
                    ActionTypeEnum.ACTION_PUT_BOMB.value, 
                    ActionTypeEnum.ACTION_NO_PUT.value], 1)[0]
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
        _, done, info = env.step(action)
        put_card = info['put_card']
        if put_card:
            put_card = ''.join(put_card)
        card_process.append("0," + put_card)
        main_agent_status = env.hand_card_status
        put_card_status = env.put_card_status
        last_action = action
        if done:
            break
            obser = env.specify_env(low_agent_status, put_card_status, low_role)
            xs_l.append(copy.deepcopy(obser))
            action = ActionTypeEnum.ACTION_DEFAULT.value
            if last_action and curr_flag != 'l':
                while True:
                    action = np.random.choice(
                        [last_action, 
                        ActionTypeEnum.ACTION_PUT_BOMB.value, 
                        ActionTypeEnum.ACTION_NO_PUT.value], 1)[0]
                    obser, reward, done, info = env.step(action)
                    err = info['error']
                    if not err:
                        env.restore()
                        break
                    env.restore() 
            else:
                while True:
                    #agent_card_status = self._get_next_agent_status(env.hand_card_status, env.put_card_status)
                    action = np.random.randint(0,self.n_action-1)
                    #card_count = sum(env.hand_card_status)
                    obser, reward, done, info = env.step(action)
                    err = info['error']
                    if not err:
                        env.restore()
                        break
                    env.restore()
            # reward decay of low_agent
            if last_action and action not in [ActionTypeEnum.ACTION_NO_PUT.value, ActionTypeEnum.ACTION_PUT_BOMB.value]:
                rs_o[-1] -= 0.1
            if action != ActionTypeEnum.ACTION_NO_PUT.value:
                curr_flag = 'l'
                last_action = action
            obser, reward, done, info = env.step(action)
            low_agent_status = env.hand_card_status
            put_card_status = env.put_card_status
            vs_l.append(action)
            last_action = action
            primary_item = info['primary_item']
            #is_find = HandCardUtils.is_find_hand_card_type(agent_card_status, primary_item, action)
            #reward = self._process_reward(reward, main_role, is_find, action, card_count)
            rs_l.append(reward)
            if done:
                if len(xs_o) >= self.window:
                    #rs_o = list(map(lambda x:x-1,rs_o))
                    rs_o[-1] = rs_o[-1] - 10
                    mX, mR, mAX = self.obtain_sample(sess, xs_o, vs_o, rs_o)
                    buffer_X.extend(mX)
                    buffer_R.extend(mR)
                    buffer_AX.extend(mAX)
                if len(xs_l) >= self.window:
                    #rs_l = list(map(lambda x:x+1,rs_l))
                    mX, mR, mAX = self.obtain_sample(sess, xs_l, vs_l, rs_l)
                    #buffer_X.extend(mX)
                    #buffer_R.extend(mR)
                    #buffer_AX.extend(mAX)
                if len(xs_u) >= self.window:
                    #rs_u = list(map(lambda x:x+1,rs_u))
                    mX, mR, mAX = self.obtain_sample(sess, xs_u, vs_u, rs_u)
                    #buffer_X.extend(mX)
                    #buffer_R.extend(mR)
                    #buffer_AX.extend(mAX)
                break
            obser = env.specify_env(up_agent_status, put_card_status, up_role)
            xs_u.append(copy.deepcopy(obser))
            action = ActionTypeEnum.ACTION_DEFAULT.value
            if last_action and curr_flag != 'u':
                while True:
                    action = np.random.choice(
                        [last_action, 
                        ActionTypeEnum.ACTION_PUT_BOMB.value, 
                        ActionTypeEnum.ACTION_NO_PUT.value], 1)[0]
                    obser, reward, done, info = env.step(action)
                    err = info['error']
                    if not err:
                        env.restore()
                        break
                    env.restore() 
            else:
                while True:
                    #agent_card_status = self._get_next_agent_status(env.hand_card_status, env.put_card_status)
                    action = np.random.randint(0,self.n_action-1)
                    #card_count = sum(env.hand_card_status)
                    obser, reward, done, info = env.step(action)
                    err = info['error']
                    if not err:
                        env.restore()
                        break
                    env.restore()
            # reward decay of up_agent
            is_decay = False
            if last_action and action not in [ActionTypeEnum.ACTION_NO_PUT.value, ActionTypeEnum.ACTION_PUT_BOMB.value]:
                is_decay = True
            if action != ActionTypeEnum.ACTION_NO_PUT.value:
                curr_flag = 'u'
                last_action = action
            obser, reward, done, info = env.step(action)
            up_agent_status = env.hand_card_status
            put_card_status = env.put_card_status
            vs_u.append(action)
            last_action = action
            primary_item = info['primary_item']
            #is_find = HandCardUtils.is_find_hand_card_type(agent_card_status, primary_item, action)
            #reward = self._process_reward(reward, main_role, is_find, action, card_count)
            if is_decay:
                reward -= 0.1
            rs_u.append(reward)
            if done:
                if len(xs_o) >= self.window:
                    #rs_o = list(map(lambda x:x-1,rs_o))
                    mX, mR, mAX = self.obtain_sample(sess, xs_o, vs_o, rs_o)
                    buffer_X.extend(mX)
                    buffer_R.extend(mR)
                    buffer_AX.extend(mAX)
                if len(xs_l) >= self.window:
                    #rs_l = list(map(lambda x:x+1,rs_l))
                    #rs_l[-1] = rs_l[-1] + 10
                    mX, mR, mAX = self.obtain_sample(sess, xs_l, vs_l, rs_l)
                    #buffer_X.extend(mX)
                    #buffer_R.extend(mR)
                    #buffer_AX.extend(mAX)
                if len(xs_u) >= self.window:
                    #rs_u = list(map(lambda x:x+1,rs_u))
                    mX, mR, mAX = self.obtain_sample(sess, xs_u, vs_u, rs_u)
                    #buffer_X.extend(mX)
                    #buffer_R.extend(mR)
                    #buffer_AX.extend(mAX)
                break
        
        #X = sess.run(tf.nn.l2_normalize(X, axis = 0))
        #if config.GEN_SAMPLE_FILE:
        #    self.write2file(X, y)
        if len(buffer_X) > self.max_sample_pool:
            diff_len = len(buffer_X) - self.max_sample_pool
            buffer_X = buffer_X[diff_len:]
            buffer_R = buffer_R[diff_len:]
            buffer_AX = buffer_AX[diff_len:]
        if len(buffer_X) > self.batch_size:    
            start = np.random.randint(0,len(buffer_X)-self.batch_size+1)
            end = start + self.batch_size
            return buffer_X[start:end], buffer_R[start:end], buffer_AX[start:end]
        return buffer_X, buffer_R, buffer_AX

    def obtain_sample(self, sess, xs, vs, rs):
        X, curr_reward, auxi_X = list(), list(), list()
        for ix in range(len(xs)-1):
            next_x = xs[ix+1]
            curr_x, curr_act, curr_r = xs[ix], vs[ix], rs[ix]
            # look through all actions
            max_reward = -1e10
            auxi_input_x = 0
            for action in range(self.n_action):
                act = [0] * self.n_action
                act[action] = 1
                tmp_x = copy.deepcopy(next_x)
                tmp_x.extend(act)
                tmp_x = np.array(tmp_x)
                tmp_x = np.reshape(tmp_x, [1, self.n_input+self.n_action])
                expect_value = sess.run(self.net_out, feed_dict={self.input_x:tmp_x})[0][0]
                if expect_value > max_reward:
                    max_reward = expect_value
                    auxi_input_x = next_x + act
                del tmp_x
            act = [0]*self.n_action
            act[curr_act] = 1
            new_x = curr_x + act
            new_x = [float(item) for item in new_x]
            X.append(new_x)
            curr_reward.append(curr_r)
            auxi_X.append(auxi_input_x)
        return X, curr_reward, auxi_X