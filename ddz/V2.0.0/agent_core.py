#! /usr/bin/env python3

import numpy as np
import tensorflow as tf
from env import Env
import config

AGENT_DEBUG = config.DEBUG_MODE

"""
Using Policy Network
"""
class AgentCore(object):

    """ 
    Args:
        discount_rate: 衰减因子
    """
    def __init__(self, n_input, n_output, n_hidden=5, discount_rate=0.9, learning_rate=0.001, n_epoch=20,
                batch_size=5, min_grad = 0.5, max_grad = 2):
        self.n_input = n_input
        self.n_output = n_output
        self.n_hidden = n_hidden
        self.discount_rate = discount_rate
        self.learning_rate = learning_rate
        self.n_epoch = n_epoch
        self.batch_size = batch_size
        self.min_grad = min_grad
        self.max_grad = max_grad

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
        self.input_x = tf.placeholder(tf.float32, [None, self.n_input], name='input_x')
        #self.W1 = tf.Variable(tf.random_normal([self.n_input, self.n_hidden],mean=0,stddev=1),name='W1')
        self.W1 = tf.get_variable('W1', shape=[self.n_input, self.n_hidden], 
                                    initializer=tf.contrib.layers.xavier_initializer())
        layer1 = tf.nn.relu(tf.matmul(self.input_x, self.W1))
        #self.W2 = tf.Variable(tf.random_normal([self.n_hidden, self.n_hidden],mean=0,stddev=1),name='W2')
        self.W2 = tf.get_variable('W2', shape=[self.n_hidden, self.n_hidden], 
                                    initializer=tf.contrib.layers.xavier_initializer())
        layer2 = tf.nn.relu(tf.matmul(layer1, self.W2))
        #self.W3 = tf.Variable(tf.random_normal([self.n_hidden, self.n_output],mean=0,stddev=1),name='W3')
        self.W3 = tf.get_variable('W3', shape=[self.n_hidden, self.n_output], 
                                    initializer=tf.contrib.layers.xavier_initializer())
        net_out = tf.matmul(layer2, self.W3)
        self.prob = tf.nn.softmax(net_out)

    def learn_grad(self, tvars):
        adam = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        W1_grad = tf.placeholder(tf.float32, name='batch_grad1')
        W2_grad = tf.placeholder(tf.float32, name='batch_grad2')
        W3_grad = tf.placeholder(tf.float32, name='batch_grad3')
        batch_grad = [W1_grad, W2_grad, W3_grad]
        update_grad = adam.apply_gradients(zip(batch_grad, tvars))
        return W1_grad, W2_grad, W3_grad, update_grad

    def build_grad(self, prob):
        input_y = tf.placeholder(tf.float32, [None, self.n_output], name='input_y')
        expect_reward = tf.placeholder(tf.float32, name='expect_reward')
        loglik = tf.reduce_mean(tf.log(input_y*(input_y-prob)+(1-input_y)*(input_y+prob)),axis=1,keep_dims=True)
        loss = -tf.reduce_mean(expect_reward*loglik)
        tvars = tf.trainable_variables()
        new_grads = tf.gradients(loss,tvars)
        new_grads = [tf.clip_by_value(grad, self.min_grad, self.max_grad) for grad in new_grads]
        return input_y, expect_reward, tvars, new_grads, loss, loglik
    
    def write2file(self, x, y, r):
        with open('sample.txt', 'a', encoding='utf-8') as f:
            f.write('-----------------------------------\n')
            f.write('x')
            f.write('\n')
            for item in x:
                val = item.tolist()
                text = str(val)
                f.write(text)
                f.write('\n')
            f.write('y')
            f.write('\n')
            for item in y:
                val = item.tolist()
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
    Generate target vaule
    """
    def gen_mini_batch(self, sess, xs, rs, ys):
        pass


    def start_train(self):
        env = Env()
        final_action = list()
        with tf.Session() as sess:
            self.build_net()
            input_y, expect_reward, tvars, new_grads, loss, loglik = self.build_grad(self.prob)
            W1_grad, W2_grad, W3_grad, update_grad = self.learn_grad(tvars)
            init = tf.global_variables_initializer()
            sess.run(init)
            grad_buffer = sess.run(tvars)
            for i,grad in enumerate(grad_buffer):
                grad_buffer[i] = grad * 0
            observation = env.reset()
            t = 1
            xs,ys,rs = list(),list(),list()
            reward_sum = 0
            while t <= self.n_epoch:
                obser = np.reshape(observation, [1, self.n_input])
                prob_value = sess.run(self.prob, feed_dict={self.input_x:obser})
                if AGENT_DEBUG:
                    print('prob value {}'.format(prob_value))
                action = tf.argmax(prob_value, 1)
                action_value = action.eval()[0]
                if AGENT_DEBUG:
                    print('start action {}'.format(action_value))
                action_set = [ix for ix in range(self.n_output)]
                avg_p = round(1/(self.n_output-1), 2)
                if avg_p * (self.n_output-1) > 1:
                    avg_p -= 0.01
                another_p = 1 - avg_p * (self.n_output-1)
                action_p = [avg_p]*(self.n_output-1)
                action_p.insert(action_value, another_p)
                target_action = np.random.choice(action_set, 1, p=action_p)[0]
                target = [0]*(self.n_output)
                target[target_action] = 1
                target = np.array(target)
                #print('-------------------------')
                #print(action_value)
                #print(action_p)
                #print(target_action)
                #print(target)
                if AGENT_DEBUG:
                    print('target {}'.format(target))
                xs.append(obser)
                ys.append(target)
                final_action.append(action_value)
                observation, reward, done = env.step(action_value)
                reward_sum += reward
                rs.append(reward)
                if done:
                    t += 1
                    if AGENT_DEBUG:
                        print('reward list {}'.format(rs))
                        print('action list {}'.format(final_action))
                    #self.gen_target(sess, xs, rs, ys)
                    epx = np.vstack(xs)
                    epy = np.vstack(ys)
                    epr = np.vstack(rs)
                    #self.write2file(xs, ys, rs)
                    xs,ys,rs = list(),list(),list()
                    if t <= self.n_epoch:
                        final_action = list()
                    epr = self.obtain_expect_reward(epr)
                    epr -= np.mean(epr)
                    epr /= np.std(epr)
                    print(epr)
                    #epr = np.column_stack((epr for _ in range(self.n_output)))
                    if AGENT_DEBUG:
                        print('epx-shape {}'.format(epx.shape))
                        print('epy-shape {}'.format(epy.shape))
                        print('epr-shape {}'.format(epr.shape))
                    t_grad = sess.run(new_grads, feed_dict={self.input_x:epx,input_y:epy,expect_reward:epr})
                    #loglik_value = sess.run(loglik, feed_dict={self.input_x:epx,input_y:epy})
                    #print('loglik: {}'.format(loglik_value))
                    #print('input_y: {}'.format(epy))
                    #pv = sess.run(self.prob, feed_dict={self.input_x:epx})
                    #print('prob: {}'.format(pv))
                    #print('reward_value: {}'.format(epr))
                    #print("grad_buffer {}".format(grad_buffer))
                    for i, grad in enumerate(t_grad):
                        grad_buffer[i] += grad
                    
                    if t % self.batch_size == 0:
                        cost = sess.run(loss, feed_dict={self.input_x:epx,input_y:epy,expect_reward:epr})
                        print('cost: {}'.format(cost))
                        print('Average reward for epoch %d : %f.' %(t, reward_sum/self.batch_size))
                        sess.run(update_grad, feed_dict={W1_grad:grad_buffer[0], 
                                    W2_grad:grad_buffer[1], W3_grad:grad_buffer[2]})
                    reward_sum = 0
                    observation = env.reset()
        return final_action

if __name__ == '__main__':
    agent = AgentCore(n_input=36, n_output=26)
    final_action = agent.start_train()
    print(final_action)