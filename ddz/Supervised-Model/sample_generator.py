#! /usr/bin/env python3

from all_card import ALL_CARD_NO_COLOR
import random

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
Sample Generator
"""
def generate_data():
    random.shuffle(ALL_CARD_NO_COLOR)
    player_1 = _deal_card(1)
    player_2 = _deal_card(2)
    player_3 = _deal_card(3)
    bottom_card = _deal_card(0)
    xs_o, vs_o, rs_o = list(), list(), list()
    xs_l, vs_l, rs_l = list(), list(), list()
    xs_u, vs_u, rs_u = list(), list(), list()
    main_agent_status, low_agent_status, up_agent_status = self._gen_agent()
    env = Env()
    put_card_status = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    main_role = PlayerRoleEnum.LAND_OWNER
    low_role = PlayerRoleEnum.LOW_LAND_OWNER
    up_role = PlayerRoleEnum.UP_LAND_OWNER
    last_action = None
    curr_flag = "o" # 'o', 'l', 'u'
    while True:
        obser = env.specify_env(main_agent_status, put_card_status, main_role)
        xs_o.append(copy.deepcopy(obser))
        action = ActionTypeEnum.ACTION_DEFAULT.value
        if last_action and curr_flag != 'o':
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
            if last_action and action not in [ActionTypeEnum.ACTION_NO_PUT.value, ActionTypeEnum.ACTION_PUT_BOMB.value]:
                rs_u[-1] -= 0.1
            if action != ActionTypeEnum.ACTION_NO_PUT.value:
                curr_flag = 'o'
                last_action = action
            obser, reward, done, info = env.step(action)
            main_agent_status = env.hand_card_status
            put_card_status = env.put_card_status
            vs_o.append(action)
            last_action = action
            rs_o.append(reward)
            if done:
                if len(xs_o) >= self.window:
                    #rs_o = list(map(lambda x:x+1,rs_o))
                    
                    mX, mR, mAX = self.obtain_sample(sess, xs_o, vs_o, rs_o)
                    buffer_X.extend(mX)
                    buffer_R.extend(mR)
                    buffer_AX.extend(mAX)
                if len(xs_l) >= self.window:
                    #rs_l = list(map(lambda x:x-1,rs_l))
                    mX, mR, mAX = self.obtain_sample(sess, xs_l, vs_l, rs_l)
                    #buffer_X.extend(mX)
                    #buffer_R.extend(mR)
                    #buffer_AX.extend(mAX)
                if len(xs_u) >= self.window:
                    #rs_u = list(map(lambda x:x-1,rs_u))
                    #rs_u[-1] = rs_u[-1] - 10
                    mX, mR, mAX = self.obtain_sample(sess, xs_u, vs_u, rs_u)
                    #buffer_X.extend(mX)
                    #buffer_R.extend(mR)
                    #buffer_AX.extend(mAX)
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