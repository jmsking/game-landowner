#! /usr/bin/env python3

# debug mode setting
DEBUG_MODE = False
ENV_DEBUG = False
# save path of generated file
O_PARENT_PATH = './gen/o-net/'
L_PARENT_PATH = './gen/l-net/'
U_PARENT_PATH = './gen/u-net/'
O_NET_MODEL_PATH = O_PARENT_PATH + 'model/'
L_NET_MODEL_PATH = L_PARENT_PATH + 'model/'
U_NET_MODEL_PATH = U_PARENT_PATH + 'model/'
O_NET_MODEL_SAVE_PATH = O_NET_MODEL_PATH + 'o_net.ckpt'
O_NET_MODEL_META_PATH = O_NET_MODEL_PATH + 'o_net.ckpt.meta'
L_NET_MODEL_SAVE_PATH = L_NET_MODEL_PATH + 'l_net.ckpt'
L_NET_MODEL_META_PATH = L_NET_MODEL_PATH + 'l_net.ckpt.meta'
U_NET_MODEL_SAVE_PATH = U_NET_MODEL_PATH + 'u_net.ckpt'
U_NET_MODEL_META_PATH = U_NET_MODEL_PATH + 'u_net.ckpt.meta'
O_LOG_SAVE_PATH = O_PARENT_PATH + 'logs'
L_LOG_SAVE_PATH = L_PARENT_PATH + 'logs'
U_LOG_SAVE_PATH = U_PARENT_PATH + 'logs'
#SAMPLE_SAVE_PATH = PARENT_PATH + 'sample.txt'
# deep-q net input-output setting
N_INPUT = 33
N_OUTPUT = 1
N_ACTION = 37
# whether genenate sample file or not
GEN_SAMPLE_FILE = False
# reward ration
SCORE_RATIO = 100