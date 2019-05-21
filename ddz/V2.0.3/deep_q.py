#! /usr/bin/env python3

from __future__ import absolute_import

import numpy as np
import tensorflow as tf
from env import Env
import config
import copy
from player_role_enum import PlayerRoleEnum
import all_card
import random
from hand_card_utils import HandCardUtils
from action_type_enum import ActionTypeEnum
import all_card

AGENT_DEBUG = config.DEBUG_MODE

"""
Using Deep-Q Network
"""
class AgentCore(object):

    """ 
    Args:
        discount_rate: 衰减因子
    """
    def __init__(self, n_input, n_output, n_hidden=50, discount_rate=0.99, learning_rate=0.001, n_epoch=5000,
                batch_size=20, min_grad = 0.1, max_grad = 1, n_action = 27, window = 2,
                max_sample_pool = 100000, tau = 0.001):
        self.n_input = n_input
        self.n_output = n_output
        self.n_hidden = n_hidden
        self.discount_rate = discount_rate
        self.learning_rate = learning_rate
        self.n_epoch = n_epoch
        self.batch_size = batch_size
        self.min_grad = min_grad
        self.max_grad = max_grad
        self.n_action = n_action
        self.window = window
        self.max_sample_pool = max_sample_pool
        self.tau = tau

    def build_net(self):
        self.input_x = tf.placeholder(tf.float32, [None, self.n_input+self.n_action], name='input_x')
        #self.W1 = tf.Variable(tf.random_normal([self.n_input, self.n_hidden],mean=0,stddev=1),name='W1')
        self.W1 = tf.get_variable('W1', shape=[self.n_input+self.n_action, self.n_hidden], 
                                    initializer=tf.contrib.layers.xavier_initializer())
        #layer1 = tf.nn.relu(tf.matmul(self.input_x, self.W1))
        layer1 = tf.sigmoid(tf.matmul(self.input_x, self.W1))
        #self.W2 = tf.Variable(tf.random_normal([self.n_hidden, self.n_hidden],mean=0,stddev=1),name='W2')
        self.W2 = tf.get_variable('W2', shape=[self.n_hidden, self.n_hidden], 
                                    initializer=tf.contrib.layers.xavier_initializer())
        #layer2 = tf.nn.relu(tf.matmul(layer1, self.W2))
        layer2 = tf.sigmoid(tf.matmul(layer1, self.W2))
        #self.W3 = tf.Variable(tf.random_normal([self.n_hidden, self.n_output],mean=0,stddev=1),name='W3')
        self.W3 = tf.get_variable('W3', shape=[self.n_hidden, self.n_output], 
                                    initializer=tf.contrib.layers.xavier_initializer())
        self.net_out = tf.matmul(layer2, self.W3)

        # 辅助网络确定目标Q值,保证目标Q值的稳定
        self.auxi_input_x = tf.placeholder(tf.float32, [None, self.n_input+self.n_action], name='auxi_input_x')
        self.AW1 = tf.get_variable('AW1', shape=[self.n_input+self.n_action, self.n_hidden], 
                                    initializer=tf.contrib.layers.xavier_initializer())
        layer1 = tf.sigmoid(tf.matmul(self.auxi_input_x, self.AW1))
        self.AW2 = tf.get_variable('AW2', shape=[self.n_hidden, self.n_hidden], 
                                    initializer=tf.contrib.layers.xavier_initializer())
        layer2 = tf.sigmoid(tf.matmul(layer1, self.AW2))
        self.AW3 = tf.get_variable('AW3', shape=[self.n_hidden, self.n_output], 
                                    initializer=tf.contrib.layers.xavier_initializer())
        self.target_out = tf.matmul(layer2, self.AW3)

        tf.add_to_collection('net_out', self.net_out)
        #tf.add_to_collection('target_out', self.target_out)

    def learn_grad(self, tvars):
        adam = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        W1_grad = tf.placeholder(tf.float32, name='batch_grad1')
        W2_grad = tf.placeholder(tf.float32, name='batch_grad2')
        W3_grad = tf.placeholder(tf.float32, name='batch_grad3')
        batch_grad = [W1_grad, W2_grad, W3_grad]
        total_var = len(tvars)
        update_grad = adam.apply_gradients(zip(batch_grad, tvars[:total_var//2]))
        return W1_grad, W2_grad, W3_grad, update_grad

    def build_grad(self):
        input_y = tf.placeholder(tf.float32, [None, self.n_output], name='input_y')
        loss = tf.reduce_mean(tf.square(input_y - self.net_out))
        tvars = tf.trainable_variables()
        total_var = len(tvars)
        new_grads = tf.gradients(loss,tvars[:total_var//2])
        #new_grads = [tf.clip_by_value(grad, self.min_grad, self.max_grad) for grad in new_grads]
        return input_y, tvars, new_grads, loss

    def _gen_agent(self):
        random.shuffle(all_card.ALL_CARD_NO_COLOR)
        #main_agent = all_card.ALL_CARD_NO_COLOR[:20]
        #low_agent = all_card.ALL_CARD_NO_COLOR[20:38]
        #up_agent = all_card.ALL_CARD_NO_COLOR[38:]
        main_agent = [3, 3, 4, 4, 6, 7, 7, 7, 8, 10, 10, 11, 11, 12, 12, 12, 12, 15, 15, 16]
        low_agent = [3, 3, 4, 5, 8, 8, 8, 9, 9, 10, 11, 13, 13, 13, 14, 14, 15]
        up_agent =  [4, 5, 5, 5, 6, 6, 6, 7, 9, 9, 10, 11, 13, 14, 14, 15, 17]
        main_agent_status = HandCardUtils.obtain_hand_card_status(main_agent)
        low_agent_status = HandCardUtils.obtain_hand_card_status(low_agent)
        up_agent_status = HandCardUtils.obtain_hand_card_status(up_agent)
        return main_agent_status, low_agent_status, up_agent_status

    """
    Generate mini-batch sample
    """
    def gen_mini_batch(self, sess, buffer_X, buffer_R, buffer_AX):
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
                    buffer_X.extend(mX)
                    buffer_R.extend(mR)
                    buffer_AX.extend(mAX)
                if len(xs_u) >= self.window:
                    #rs_u = list(map(lambda x:x-1,rs_u))
                    rs_u[-1] = rs_u[-1] - 10
                    mX, mR, mAX = self.obtain_sample(sess, xs_u, vs_u, rs_u)
                    buffer_X.extend(mX)
                    buffer_R.extend(mR)
                    buffer_AX.extend(mAX)
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
                    buffer_X.extend(mX)
                    buffer_R.extend(mR)
                    buffer_AX.extend(mAX)
                if len(xs_u) >= self.window:
                    #rs_u = list(map(lambda x:x+1,rs_u))
                    mX, mR, mAX = self.obtain_sample(sess, xs_u, vs_u, rs_u)
                    buffer_X.extend(mX)
                    buffer_R.extend(mR)
                    buffer_AX.extend(mAX)
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
                    rs_l[-1] = rs_l[-1] + 10
                    mX, mR, mAX = self.obtain_sample(sess, xs_l, vs_l, rs_l)
                    buffer_X.extend(mX)
                    buffer_R.extend(mR)
                    buffer_AX.extend(mAX)
                if len(xs_u) >= self.window:
                    rs_u = list(map(lambda x:x+1,rs_u))
                    mX, mR, mAX = self.obtain_sample(sess, xs_u, vs_u, rs_u)
                    buffer_X.extend(mX)
                    buffer_R.extend(mR)
                    buffer_AX.extend(mAX)
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

    def update_auxi_net_var(self, tvars, sess):
        total_var = len(tvars)
        op_holder = list()
        mid = total_var // 2
        for ix, var in enumerate(tvars[:mid]):
            op = tvars[ix+mid].assign(self.tau * var.value() + (1-self.tau) * tvars[ix+mid].value())
            op_holder.append(op)
    
        for op in op_holder:
            sess.run(op)

    def start_train(self):
        with tf.Session() as sess:
            self.build_net()
            input_y, tvars, new_grads, loss = self.build_grad()
            W1_grad, W2_grad, W3_grad, update_grad = self.learn_grad(tvars)
            init = tf.global_variables_initializer()
            sess.run(init)
            tf.summary.scalar('loss', loss)
            tf.summary.histogram('W1', self.W1)
            tf.summary.histogram('W2', self.W2)
            tf.summary.histogram('W3', self.W3)
            tf.summary.histogram('AW1', self.AW1)
            tf.summary.histogram('AW2', self.AW2)
            tf.summary.histogram('AW3', self.AW3)
            merged = tf.summary.merge_all()
            writer = tf.summary.FileWriter(config.LOG_SAVE_PATH, sess.graph)
            saver = tf.train.Saver()
            t = 1
            buffer_X, buffer_R, buffer_AX = list(), list(), list()
            while t <= self.n_epoch:
                batch_x, batch_r, batch_ax = self.gen_mini_batch(sess, buffer_X, buffer_R, buffer_AX)
                self.update_auxi_net_var(tvars, sess)
                target_value = sess.run(self.target_out, feed_dict={self.auxi_input_x: batch_ax})
                batch_y = list()
                for ix, r in enumerate(batch_r):
                    batch_y.append(r + self.discount_rate*target_value[ix][0])
                epx = np.vstack(batch_x)
                epy = np.vstack(batch_y)
                t_grad = sess.run(new_grads, feed_dict={self.input_x:epx,input_y:epy})
                cost = sess.run(loss, feed_dict={self.input_x:epx,input_y:epy})
                print('cost for epoch %d : %f.' %(t, cost))
                sess.run(update_grad, feed_dict={W1_grad:t_grad[0], 
                            W2_grad:t_grad[1], W3_grad:t_grad[2]})
                log_result = sess.run(merged, feed_dict={self.input_x:epx,input_y:epy})
                writer.add_summary(log_result, t)
                #self.update_auxi_net_var(tvars, sess)
                t += 1
            saver.save(sess, config.MODEL_SAVE_PATH)
            print('--------training successful--------')
            

    def predict(self):
        env = Env()
        obser = env.reset()
        print(obser)
        final_action, reward = list(), list()
        with tf.Session() as sess:
            saver = tf.train.import_meta_graph(config.MODEL_META_PATH)
            model_file=tf.train.latest_checkpoint(config.MODEL_PATH)
            saver.restore(sess,model_file)
            net_out = tf.get_collection('net_out')
            is_done = False
            while True:
                order_act_reward = list()
                for action in range(self.n_action-1):
                    act = [0] * self.n_action
                    act[action] = 1
                    x = copy.deepcopy(obser)
                    x.extend(act)
                    x = np.reshape(x, [1, self.n_input+self.n_action])
                    out = sess.run(net_out, feed_dict={'input_x:0': x})[0][0][0]
                    order_act_reward.append((action, out))
                order_act_reward = sorted(order_act_reward, key=lambda x:x[1], reverse=True)
                for a, _ in order_act_reward:
                    obser, rew, done, info = env.step(a)
                    error = info['error']
                    if not error:
                        final_action.append(a)
                        reward.append(rew)
                        if done:
                            is_done = done
                        break
                    env.restore()
                if is_done:
                    break
        print('final action: {}'.format(final_action))
        print('reward: {}'.format(reward))

if __name__ == '__main__':
    agent = AgentCore(n_input=config.N_INPUT, n_output=config.N_OUTPUT)
    agent.start_train()
    #agent.predict()