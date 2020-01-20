#! /usr/bin/env python3

from log.log import Logger
import numpy as np
import tensorflow as tf
import copy
from network.deep_q_net import DeepQNet
from enums.player_role_enum import PlayerRoleEnum
from common.constants import TF_CONST, EXTRA_CONST

logger = Logger.getLog(__name__)

is_first = True


class Model:
    def __init__(self, is_load_model=False, model_path=EXTRA_CONST['SAVE_MODEL_PATH'], **kwargs):
        self.is_load_model = is_load_model
        if is_load_model: 
            self.__load_model(model_path)
        else:
            self.graph = kwargs.pop('graph')
            self.sess = kwargs.pop('sess')

    def __load_model(self, model_path):
        try:
            self.graph = tf.Graph()
            self.sess = tf.compat.v1.Session(graph=self.graph)
            meta_graph = tf.compat.v1.saved_model.loader.load(self.sess, [TF_CONST['MODEL_TAG']], model_path)
            signature_def = meta_graph.signature_def[TF_CONST['SIGNATURE_KEY']]
            input_tensor_info = signature_def.inputs[TF_CONST['INPUT_KEY']]
            output_tensor_info = signature_def.outputs[TF_CONST['OUTPUT_KEY']]
            self.input_op = self.graph.get_tensor_by_name(input_tensor_info.name)
            self.net_out = self.graph.get_tensor_by_name(output_tensor_info.name)
            return True
        except Exception as e:
            logger.error(f'Load model error -> {e}')
        
        return False

    def predict(self, inputs, is_target, **kwargs):
        if not self.is_load_model:
            self.input_op = None
            self.net_out = None
            with self.graph.as_default():
                if is_target:
                    self.input_op = kwargs.pop('target_input_x_op')
                    self.net_out = kwargs.pop('target_net_out')
                else:
                    self.input_op = kwargs.pop('value_input_x_op')
                    self.net_out = kwargs.pop('value_net_out')
        result = self.sess.run(self.net_out, 
                feed_dict={self.input_op: inputs})
        return result.tolist()[0][0]

"""
Netowrk model for agents
"""
class Net(DeepQNet):

    """ 
    Args:
        discount_rate: 衰减因子
    """
    def __init__(self, n_input=33+37, layers=[50], 
            lr=0.005, dr=0.05, bs=10, epsilon=0.2, buffer_size=5000,
            n_epoch=10, n_update=500, n_show=1, 
            model_path=EXTRA_CONST['SAVE_MODEL_PATH'], is_infer=False):
        super().__init__(n_input, layers, PlayerRoleEnum.LAND_OWNER,
            lr, dr, bs, epsilon, buffer_size,
            n_epoch, n_update, n_show, scope='Net', model_path=model_path, instance=self)
        params = {
            'graph': self.graph,
            'sess': self.sess,
        }
        self.is_infer = is_infer
        self.model = Model(is_infer, **params)
        
    def predict(self, inputs, is_target=False):
        """
        inputs : hand_card_status + desk_card_status + player_role + action_onehot
        is_target : wheather use value network or target network
        """
        params = {}
        if not self.is_infer:
            params['value_input_x_op'] = self.value_input_x_op
            params['value_net_out'] = self.value_net_out
            params['target_input_x_op'] = self.target_input_x_op
            params['target_net_out'] = self.target_net_out
        
        result = self.model.predict(inputs, is_target, **params)
        return result