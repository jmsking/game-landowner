#! /usr/bin/env python3

from log.log import Logger

import tensorflow as tf
import numpy as np
from common.common_utils import CommonUtils
from common.constants import TF_CONST, EXTRA_CONST
from enums.action_type_enum import ActionTypeEnum
from enums.player_role_enum import PlayerRoleEnum
from dataset.mini_batch import MiniBatch

logger = Logger.getLog(__name__)

logger.info(tf.__version__)

"""
Implement of Deep-Q network
"""

class DeepQNet:

    def __init__(self, n_input, layers, role=PlayerRoleEnum.LAND_OWNER,
            lr=0.005, dr=0.05, bs=200, epsilon=0.2, buffer_size=5000,
            n_epoch=500, n_update=500, n_show=100, scope='', 
            model_path=EXTRA_CONST['SAVE_MODEL_PATH'], instance=None):
        """
        Parameters
        -----------------------
        n_input: the number of input features
        role: the role of player
        layers: a list represent the node number of each hidden layer
        lr: learning rate
        dr: discount rate (useless)
        bs: batch size
        epsilon: epsilon-greedy
        buffer_size: the max size of buffer to save samples
        n_epoch: the times of training process
        n_update: the number to update target network
        n_show: the number to show training information
        scope: the scope of all variables
        """
        self.n_input = n_input
        self.layers = layers
        self.role = role
        self.lr = lr
        self.dr = dr
        self.bs = bs
        self.epsilon = epsilon
        self.buffer_size = buffer_size
        self.n_epoch = n_epoch
        self.n_update = n_update
        self.n_show = n_show
        self.scope = scope
        self.model_path = model_path
        self.graph = tf.Graph()
        self.sess = tf.compat.v1.Session(graph=self.graph)
        #self.batcher = None
        self.batcher = MiniBatch(self.bs, self.role, self.epsilon, net=instance)

    def __build_net_struct(self, name):
        """
        Build the struct of two networks
        one is value network and
        another is target network
        """
        input_x_op = tf.compat.v1.placeholder(tf.float32, [None, self.n_input], name=f'{name}_input_x')
        target_op = tf.compat.v1.placeholder(tf.float32, [None, 1], name=f'{name}_target')
        weight = []
        bias = []
        n_pre_hidden = self.n_input
        h_out = input_x_op
        for idx, n_hidden in enumerate(self.layers):
            with tf.compat.v1.variable_scope(f'{self.scope}_{name}', reuse=tf.compat.v1.AUTO_REUSE):
                w_tmp = tf.compat.v1.get_variable(f'w_{idx}', shape=[n_pre_hidden, n_hidden],
                                        initializer=tf.contrib.layers.xavier_initializer())
                bias_tmp = tf.compat.v1.get_variable(f'bias_{idx}', shape=(1,),
                                        initializer=tf.zeros_initializer())
                weight.append(w_tmp)
                bias.append(bias_tmp)
            n_pre_hidden = n_hidden

            h_out = tf.add(tf.matmul(h_out, w_tmp), bias_tmp)
            h_out = tf.nn.relu(h_out)
        with tf.compat.v1.variable_scope(f'{self.scope}_{name}', reuse=tf.compat.v1.AUTO_REUSE):
            final_w = tf.compat.v1.get_variable(f'w_{len(self.layers)}', shape=[self.layers[-1], 1],
                                        initializer=tf.contrib.layers.xavier_initializer())
            weight.append(final_w)
        net_out = tf.matmul(h_out, final_w)
        return input_x_op, target_op, net_out, weight, bias

    def build_value_network(self):
        """
        Build a value network struct
        """
        self.value_input_x_op, self.value_target_op, self.value_net_out, \
        self.value_weight, self.value_bias = self.__build_net_struct('value')

    def build_target_network(self):
        """
        Build a target network struct
        """
        self.target_input_x_op, _, self.target_net_out, \
        self.target_weight, self.target_bias = self.__build_net_struct('target')

    def init_variables(self):
        self.init_op = tf.compat.v1.global_variables_initializer()

    def obtain_mini_batch(self):
        """
        Obtain mini-batch samples from sample buffer
        Containing batch_x and batch_target
        """
        batch_x, batch_target = self.batcher.next()
        return batch_x, batch_target

    def collect_grad(self, y, target_op):
        """
        Collect the gradient in training process 
        to update target network
        """
        loss = tf.reduce_mean(tf.square(y - target_op))
        tvars = tf.compat.v1.trainable_variables()
        tvars_size = len(tvars)
        value_net_tvars = tvars[:tvars_size//2]
        value_net_grads = tf.gradients(loss, value_net_tvars)
        return loss, value_net_grads

    def update_weight(self, grad, net_name='value'):
        """
        Update weight and bias for all networks
        grad: the gradient list for each trainable parameter
        """
        optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=self.lr)
        tvars = tf.compat.v1.trainable_variables()
        tvars_size = len(tvars)
        mid = tvars_size // 2
        if net_name == 'value':
            # update parameters of value network
            tvars = tvars[:mid]
        else:
            # update parameters of target network
            tvars = tvars[mid:]
        update_grad = optimizer.apply_gradients(zip(grad, tvars))
        return update_grad

    def __save_model(self, sess, input_op, net_out):
        builder = tf.saved_model.builder.SavedModelBuilder(self.model_path)
        inputs = {TF_CONST['INPUT_KEY']: tf.saved_model.utils.build_tensor_info(input_op)}
        outputs = {TF_CONST['OUTPUT_KEY']: tf.saved_model.utils.build_tensor_info(net_out)}
        signature = tf.saved_model.build_signature_def(inputs, outputs, TF_CONST['METHOD_NAME'])
        builder.add_meta_graph_and_variables(sess, [TF_CONST['MODEL_TAG']], {TF_CONST['SIGNATURE_KEY']: signature})
        builder.save()
        logger.info('*** save model success ***')

    def train(self):
        """
        step = 1
        For episode in n_episode:
            For t in timestep:
                If random < epsilon:
                    At, Rt, St = random-action
                Else:
                    Input (St-1, Ak) to value network
                    Output (At, Rt, St)
                Collect (St-1, At, Rt, St) into Buffer
                Obtain batch-size X
                Input batch-size X into target network
                Obtain target value for batch-size X 
                Train value network
                If step % n_update = 0:
                    Set target network equal to value network
        """
        with self.graph.as_default():
            self.build_value_network()
            self.build_target_network()
            self.init_variables()
            self.sess.run(self.init_op)
            grad_collection = []
            for epoch in range(1, self.n_epoch+1, 1):
                batch_x, batch_target = self.obtain_mini_batch()
                #print(batch_x.shape)
                #print(batch_target.shape)
                #net_out = self.sess.run(self.value_net_out, feed_dict={self.value_input_x_op:batch_x})
                #print(net_out.shape)
                #print(self.value_target_op.shape)
                loss, batch_grad = self.collect_grad(self.value_net_out, self.value_target_op)
                cost, grad = self.sess.run([loss, batch_grad], feed_dict={
                                        self.value_input_x_op: batch_x,
                                        self.value_target_op: batch_target
                                    })
                print(len(grad))
                for item in grad:
                    print(item.shape)
                break
                grad_collection.append(grad)
                # update value network parameters
                self.update_weight(grad)
                # update target network parameters
                if epoch % self.n_update == 0:
                    sum_grad = np.sum(grad_collection, axis=0)
                    self.update_weight(sum_grad, net_name='target')
                if epoch % self.n_show == 0:
                    logger.info(f'Epoch: {epoch}/{self.n_epoch} -- loss: {cost}')

            #self.__save_model(self.sess, self.value_input_x_op, self.value_net_out)