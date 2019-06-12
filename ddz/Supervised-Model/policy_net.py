#! /usr/bin/env python3

import tensorflow as tf
from preproc import PreprocUtils
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import config

class PolicyNet():
    def __init__(self, x_dim=15, y_dim=4, z_dim=3, batch_size = 5,
                n_action=config.N_POLICY_ACTION, n_display=5, 
                learning_rate=0.001, n_epoches=100):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.z_dim = z_dim
        self.batch_size = batch_size
        self.n_action = n_action
        self.n_display = n_display
        self.learning_rate = learning_rate
        self.n_epoches = n_epoches

    """
    Create a convolution layer
    Args:
        input_data: The input of layer
        kernel_h: the heigh of the kernel
        kernel_w: the width of the kernel
        n_kernel: the number of kernel
        dh: the step aside height
        dw: the step aside width
        param_list: trainable params list
        name: the name of this operation
    """
    def conv_op(self, input_data, kernel_h, kernel_w, n_kernel, dh, dw, param_list, name):
        n_in = input_data.get_shape()[-1].value
        with tf.name_scope(name) as scope:
            kernel = tf.get_variable(scope+"W", [kernel_h, kernel_w, n_in, n_kernel],
                        dtype=tf.float32, initializer=tf.contrib.layers.xavier_initializer_conv2d())
            bias_init_value = tf.constant(0, shape=[n_kernel], dtype=tf.float32)
            bias = tf.Variable(bias_init_value, trainable=True, name="bias")

            layer_out = tf.nn.conv2d(input_data, kernel, [1,dh,dw,1], padding="SAME")
            layer_out_add_bias = tf.nn.bias_add(layer_out, bias)
            conv_out = tf.nn.relu(layer_out_add_bias, name=scope)
            param_list += [kernel, bias]
            return conv_out

    """
    Create a fully connect layer
    Args:
        input_data: the input of layer
        n_out: the output size of layer
        param_list: trainale params list
        name: the name of this operation
    """
    def fc_op(self, input_data, n_out, param_list, name):
        n_in = input_data.get_shape()[-1].value
        with tf.name_scope(name) as scope:
            kernel = tf.get_variable(scope+"W", [n_in, n_out], dtype=tf.float32,
                        initializer=tf.contrib.layers.xavier_initializer_conv2d())
            bias_init_value = tf.constant(0.1,shape=[n_out], dtype=tf.float32)
            bias = tf.Variable(bias_init_value, trainable=True, name="bias")
            fc_out = tf.nn.relu_layer(input_data, kernel, bias, name=scope)
            param_list += [kernel, bias]
            return fc_out

    """
    Create a max pooling operation
    Args:
        input_data: the input of layer
        kh: the height of pool
        kw: the width of pool
        dh: the step aside height
        dw: the step aside width
        name: the name of this operation
    """
    def max_pool_op(self, input_data, kh, kw, dh, dw, name):
        return tf.nn.max_pool(input_data, ksize=[1,kh,kw,1], strides=[1,dh,dw,1], 
                            padding="SAME", name=name)

    """
    Build a policy network
    Args:
        input_data: the input of network
    """
    def build_net(self, input_data):
        param_list = list()
        conv_1 = self.conv_op(input_data, 3, 3, 64, 1, 1, param_list, "conv_1")
        pool_1 = self.max_pool_op(conv_1, 2, 2, 1, 1, 'pool_1')
        conv_2 = self.conv_op(pool_1, 3, 3, 128, 1, 1, param_list, "conv_2")
        pool_2 = self.max_pool_op(conv_2, 2, 2, 1, 1, 'pool_2')
        conv_3 = self.conv_op(pool_2, 3, 3, 256, 1, 1, param_list, "conv_3")
        pool_3 = self.max_pool_op(conv_3, 2, 2, 1, 1, 'pool_3')

        shp = pool_3.get_shape()
        flatt_size = shp[1].value * shp[2].value * shp[3].value
        flatt_input = tf.reshape(pool_3, [-1, flatt_size], name="flatt_input")

        fc_out = self.fc_op(flatt_input, self.n_action, param_list, "fc")
        y = tf.nn.softmax(fc_out)
        tf.add_to_collection('net_out', y)
        return y, param_list

    def train_op(self, y_, y, tvar):
        optimizer = tf.train.AdamOptimizer(self.learning_rate)
        loss = -tf.reduce_mean(tf.reduce_sum(y_*tf.log(y)))
        #grad = tf.gradients(loss, tvar)
        #update_grad = optimizer.apply_gradients(zip(grad, tvar))
        update_grad = optimizer.minimize(loss)
        return update_grad, loss

    def build_input(self):
        x = tf.placeholder(tf.float32, 
                        [None, self.x_dim, self.y_dim, self.z_dim], name="x")
        y_ = tf.placeholder(tf.float32, [None, self.n_action], name="y")
        return x, y_

    def obtain_mini_batch(self, input_x, input_y):
        n_samples = input_x.shape[0]
        rnd = np.random.randint(n_samples-self.batch_size+1)
        end = rnd+self.batch_size
        return input_x[rnd:end,:,:,:], input_y[rnd:end,:]

    def start_train(self, input_x, input_y):
        with tf.Session() as sess:
            x, y_ = self.build_input()
            y, tvar = self.build_net(x)
            update_grad, loss = self.train_op(y_, y, tvar)
            init = tf.global_variables_initializer()
            sess.run(init)
            saver = tf.train.Saver()
            for epoch in range(self.n_epoches):
                epoch += 1
                batch_x, batch_y = self.obtain_mini_batch(input_x, input_y)
                cost, _ = sess.run([loss, update_grad], feed_dict={x:batch_x, y_:batch_y})
                if epoch % self.n_display == 0:
                    print_log = "Epoch/Epoches: {}/{} - cost: {}"
                    print(print_log.format(epoch, self.n_epoches, cost))
            predictions = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(y_, 1), tf.argmax(y, 1)), tf.float32))
            accuracy = sess.run(predictions, feed_dict={x:input_x, y_:input_y})
            print('Train Accuracy: {}%'.format(accuracy*100))
            saver.save(sess, config.POLICY_MODEL_SAVE_PATH)
            print('Model Save Success.')
    
    def predict(self, input_data):
        with tf.Session() as sess:
            saver = tf.train.import_meta_graph(config.POLICY_META_SAVE_PATH)
            model_file = tf.train.latest_checkpoint(config.POLICY_MODEL_PARENT_PATH)
            saver.restore(sess, model_file)
            net_out = tf.get_collection('net_out')
            pred = sess.run(net_out, feed_dict={"x:0":input_data})[0][0]
        return np.argmax(pred)

if __name__ == "__main__":
    train_inputs, train_output = PreprocUtils.gen_policy_net_input()
    enc = OneHotEncoder(categories=[[i for i in range(config.N_POLICY_ACTION)]], sparse=False)
    train_output = enc.fit_transform(train_output)
    net = PolicyNet()
    print(train_inputs[0:1,:,:,:].shape)
    net.start_train(train_inputs, train_output)
    pred = net.predict(train_inputs[0:1,:,:,:])
    print(pred)

    
        