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
    def __init__(self, n_input, n_output, n_hidden=20, discount_rate=0.99, learning_rate=0.001, n_epoch=200,
                batch_size=100, min_grad = 0.1, max_grad = 1, n_action = 27, window = 5):
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
        self.AW1 = tf.Variable(tf.random_normal([self.n_input+self.n_action, self.n_output],mean=0,stddev=1),name='AW1')
        self.target_out = tf.matmul(self.auxi_input_x, self.AW1)

        tf.add_to_collection('net_out', self.net_out)
        #tf.add_to_collection('target_out', self.target_out)

    def learn_grad(self, tvars):
        adam = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        W1_grad = tf.placeholder(tf.float32, name='batch_grad1')
        W2_grad = tf.placeholder(tf.float32, name='batch_grad2')
        W3_grad = tf.placeholder(tf.float32, name='batch_grad3')
        batch_grad = [W1_grad, W2_grad, W3_grad]
        update_grad = adam.apply_gradients(zip(batch_grad, tvars[:-1]))
        return W1_grad, W2_grad, W3_grad, update_grad

    def build_grad(self):
        input_y = tf.placeholder(tf.float32, [None, self.n_output], name='input_y')
        loss = tf.reduce_mean(tf.square(input_y - self.net_out))
        tvars = tf.trainable_variables()
        new_grads = tf.gradients(loss,tvars[:-1])
        new_grads = [tf.clip_by_value(grad, self.min_grad, self.max_grad) for grad in new_grads]
        return input_y, tvars, new_grads, loss
    
    def write2file(self, x, y):
        with open('sample.txt', 'a', encoding='utf-8') as f:
            for ix, item in enumerate(x):
                val = item + [y[ix]]
                text = str(val)
                f.write(text)
                f.write('\n')

    """
    Generate mini-batch sample
    """
    def gen_mini_batch(self, sess, sample_buffer_x, sample_buffer_y):
        X, y = list(), list()
        xs, vs, rs = list(), list(), list()
        env = Env()
        t = 1
        obser = env.reset()
        while t <= self.batch_size:
            xs.append(copy.deepcopy(obser))
            action = np.random.randint(0,self.n_action)
            vs.append(action)
            obser, reward, done, _ = env.step(action)
            rs.append(reward)
            if done:
                if len(xs) >= self.window:
                    mX, my = self.obtain_sample(sess, xs, vs, rs)
                    X.extend(mX)
                    y.extend(my)
                    t += 1
                obser = env.reset()
                xs, vs, rs = list(), list(), list()
        #X = sess.run(tf.nn.l2_normalize(X, axis = 0))
        if config.GEN_SAMPLE_FILE:
            self.write2file(X, y)
        #sample_buffer_x.extend(X)
        #sample_buffer_y.extend(y)
        #if len(sample_buffer_x) > self.max_sample_pool:

        return X, y

    def obtain_sample(self, sess, xs, vs, rs):
        X, y = list(), list()
        for ix in range(len(xs)-1):
            next_x = xs[ix+1]
            #print(next_x)
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
                    auxi_input_x = copy.deepcopy(tmp_x)
                del tmp_x
            Q_value = sess.run(self.target_out, feed_dict={self.auxi_input_x:auxi_input_x})[0][0]
            act = [0]*self.n_action
            act[curr_act] = 1
            new_x = curr_x + act
            new_x = [float(item) for item in new_x]
            X.append(new_x)
            y.append(curr_r + self.discount_rate * Q_value)
        return X, y

    def start_train(self):
        with tf.Session() as sess:
            self.build_net()
            input_y, tvars, new_grads, loss = self.build_grad()
            W1_grad, W2_grad, W3_grad, AW1_grad, update_grad = self.learn_grad(tvars)
            init = tf.global_variables_initializer()
            sess.run(init)
            tf.summary.scalar('loss', loss)
            tf.summary.histogram('W1', self.W1)
            tf.summary.histogram('W2', self.W2)
            tf.summary.histogram('W3', self.W3)
            merged = tf.summary.merge_all()
            #print(merged)
            writer = tf.summary.FileWriter('logs', sess.graph)
            grad_buffer = sess.run(tvars)
            saver = tf.train.Saver()
            for i,grad in enumerate(grad_buffer):
                grad_buffer[i] = grad * 0
            t = 1
            sample_buffer_x = list()
            sample_buffer_y = list()
            while t <= self.n_epoch:
                X, y = self.gen_mini_batch(sess, sample_buffer_x, sample_buffer_y)
                epx = np.vstack(X)
                epy = np.vstack(y)
                t_grad = sess.run(new_grads, feed_dict={self.input_x:epx,input_y:epy})
                cost = sess.run(loss, feed_dict={self.input_x:epx,input_y:epy})
                print('cost for epoch %d : %f.' %(t, cost))
                sess.run(update_grad, feed_dict={W1_grad:t_grad[0], 
                            W2_grad:t_grad[1], W3_grad:t_grad[2], AW1_grad:t_grad[3]})
                log_result = sess.run(merged, feed_dict={self.input_x:epx,input_y:epy})
                writer.add_summary(log_result, t)
                t += 1
            saver.save(sess, config.MODEL_SAVE_PATH)
            print('--------training successful--------')
            

    def predict(self):
        env = Env()
        obser = env.reset()
        print(obser)
        final_action, reward = list(), list()
        with tf.Session() as sess:
            saver = tf.train.import_meta_graph('./model/deep_q.ckpt.meta')
            model_file=tf.train.latest_checkpoint('./model/')
            saver.restore(sess,model_file)
            net_out = tf.get_collection('net_out')
            tvars = tf.trainable_variables()
            #for var in tvars:
            #    print(var.name)
            #    print(var.eval())
            #print(W1.eval())
            is_done = False
            while True:
                order_act_reward = list()
                for action in range(self.n_action):
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