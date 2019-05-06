#! /usr/bin/env python3

import numpy as np
import tensorflow as tf
from env import Env
import config
import copy

AGENT_DEBUG = config.DEBUG_MODE

"""
Using Deep-Q Network
"""
class AgentCore(object):

    """ 
    Args:
        discount_rate: 衰减因子
    """
    def __init__(self, n_input, n_output, n_hidden=5, discount_rate=0.9, learning_rate=0.001, n_epoch=500,
                batch_size=100, min_grad = 0.5, max_grad = 2, n_action = 27, window = 3):
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

    def obtain_expect_reward(self, rewards):
        """ 获取期望价值 
        Args: rewards -> [r1, r2, r3, ...], 出某个牌型的奖励
        """
        expect_rewards = list(np.zeros_like(rewards))
        running_add = 0
        for k in reversed(range(len(rewards))):
            running_add = running_add * self.discount_rate + rewards[k]
            expect_rewards[k] = running_add
        return np.array(expect_rewards)

    def build_net(self):
        self.input_x = tf.placeholder(tf.float32, [None, self.n_input+self.n_action], name='input_x')
        #self.W1 = tf.Variable(tf.random_normal([self.n_input, self.n_hidden],mean=0,stddev=1),name='W1')
        self.W1 = tf.get_variable('W1', shape=[self.n_input+self.n_action, self.n_hidden], 
                                    initializer=tf.contrib.layers.xavier_initializer())
        layer1 = tf.nn.relu(tf.matmul(self.input_x, self.W1))
        #self.W2 = tf.Variable(tf.random_normal([self.n_hidden, self.n_hidden],mean=0,stddev=1),name='W2')
        self.W2 = tf.get_variable('W2', shape=[self.n_hidden, self.n_hidden], 
                                    initializer=tf.contrib.layers.xavier_initializer())
        layer2 = tf.nn.relu(tf.matmul(layer1, self.W2))
        #self.W3 = tf.Variable(tf.random_normal([self.n_hidden, self.n_output],mean=0,stddev=1),name='W3')
        self.W3 = tf.get_variable('W3', shape=[self.n_hidden, self.n_output], 
                                    initializer=tf.contrib.layers.xavier_initializer())
        self.net_out = tf.matmul(layer2, self.W3)

    def learn_grad(self, tvars):
        adam = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        W1_grad = tf.placeholder(tf.float32, name='batch_grad1')
        W2_grad = tf.placeholder(tf.float32, name='batch_grad2')
        W3_grad = tf.placeholder(tf.float32, name='batch_grad3')
        batch_grad = [W1_grad, W2_grad, W3_grad]
        update_grad = adam.apply_gradients(zip(batch_grad, tvars))
        return W1_grad, W2_grad, W3_grad, update_grad

    def build_grad(self):
        input_y = tf.placeholder(tf.float32, [None, self.n_output], name='input_y')
        loss = tf.reduce_mean(tf.square(input_y - self.net_out))
        tvars = tf.trainable_variables()
        new_grads = tf.gradients(loss,tvars)
        new_grads = [tf.clip_by_value(grad, self.min_grad, self.max_grad) for grad in new_grads]
        return input_y, tvars, new_grads, loss
    
    def write2file(self, x, y, r):
        with open('sample.txt', 'a', encoding='utf-8') as f:
            f.write('-----------------------------------\n')
            f.write('x')
            f.write('\n')
            for item in x:
                val = item
                text = str(val)
                f.write(text)
                f.write('\n')
            f.write('y')
            f.write('\n')
            for item in y:
                val = item
                text = str(val)
                f.write(text)
                f.write('\n')
            f.write('r')
            f.write('\n')
            for item in r:
                text = str(item)
                f.write(text)
                f.write('\n')
    """
    Generate mini-batch sample
    """
    def gen_mini_batch(self, sess):
        X, y = list(), list()
        xs, vs, rs = list(), list(), list()
        env = Env()
        t = 1
        obser = env.reset()
        while t <= self.batch_size:
            xs.append(copy.deepcopy(obser))
            action = np.random.randint(0,self.n_action-1)
            vs.append(action)
            obser, reward, done = env.step(action)
            rs.append(reward)
            if done:
                if len(xs) >= self.window:
                    #if AGENT_DEBUG:
                    #    print('Average reward for epoch %d : %f.' %(t, sum(rs)/len(rs)))
                    mX, my = self.obtain_sample(sess, xs, vs, rs)
                    X.extend(mX)
                    y.extend(my)
                    t += 1
                obser = env.reset()
                xs, vs, rs = list(), list(), list()
        X = sess.run(tf.nn.l2_normalize(X, axis = 0))
        self.write2file(X, y, rs)
        return X, y

    def obtain_sample(self, sess, xs, vs, rs):
        X, y = list(), list()
        for ix in range(len(xs)-1):
            next_x = xs[ix+1]
            #print(next_x)
            curr_x, curr_act, curr_r = xs[ix], vs[ix], rs[ix]
            # look through all actions
            max_reward = -1e10
            for action in range(self.n_action):
                act = [0] * self.n_action
                act[action] = 1
                tmp_x = copy.deepcopy(next_x)
                tmp_x.extend(act)
                tmp_x = np.array(tmp_x)
                tmp_x = np.reshape(tmp_x, [1, self.n_input+self.n_action])
                expect_value = sess.run(self.net_out, feed_dict={self.input_x:tmp_x})[0][0]
                max_reward = expect_value if expect_value > max_reward else max_reward
                del tmp_x
            act = [0]*self.n_action
            act[curr_act] = 1
            new_x = curr_x + act
            new_x = [float(item) for item in new_x]
            X.append(new_x)
            y.append(curr_r + self.discount_rate * max_reward)
        return X, y

    def start_train(self):
        with tf.Session() as sess:
            self.build_net()
            input_y, tvars, new_grads, loss = self.build_grad()
            W1_grad, W2_grad, W3_grad, update_grad = self.learn_grad(tvars)
            init = tf.global_variables_initializer()
            sess.run(init)
            grad_buffer = sess.run(tvars)
            for i,grad in enumerate(grad_buffer):
                grad_buffer[i] = grad * 0
            t = 1
            while t <= self.n_epoch:
                X, y = self.gen_mini_batch(sess)
                epx = np.vstack(X)
                epy = np.vstack(y)
                t_grad = sess.run(new_grads, feed_dict={self.input_x:epx,input_y:epy})
                cost = sess.run(loss, feed_dict={self.input_x:epx,input_y:epy})
                print('cost for epoch %d : %f.' %(t, cost))
                sess.run(update_grad, feed_dict={W1_grad:t_grad[0], 
                            W2_grad:t_grad[1], W3_grad:t_grad[2]})
                t += 1
            print('--------training successful--------')
            self.predict(sess)

    def predict(self, sess):
        env = Env()
        obser = env.reset()
        final_action, reward = list(), list()
        while True:
            max_reward = -1e10
            max_action = -1
            for action in range(self.n_action):
                act = [0] * self.n_action
                act[action] = 1
                x = copy.deepcopy(obser)
                x.extend(act)
                x = np.reshape(x, [1, self.n_input+self.n_action])
                out = sess.run(self.net_out, feed_dict={self.input_x: x})
                if out > max_reward:
                    max_reward = out
                    max_action = action
            obser, rew, done = env.step(max_action)
            final_action.append(max_action)
            reward.append(rew)
            if done:
                break
        print('final action: {}'.format(final_action))
        print('reward: {}'.format(reward))

if __name__ == '__main__':
    agent = AgentCore(n_input=33, n_output=1)
    agent.start_train()