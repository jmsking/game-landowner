#! /usr/bin/env python3

# debug mode setting
DEBUG_MODE = False
ENV_DEBUG = False
# save path of generated file
PARENT_PATH = './gen/'
MODEL_PATH = PARENT_PATH + 'model/'
MODEL_SAVE_PATH = MODEL_PATH + 'deep_q.ckpt'
MODEL_META_PATH = MODEL_PATH + 'deep_q.ckpt.meta'
LOG_SAVE_PATH = PARENT_PATH + 'logs'
SAMPLE_SAVE_PATH = PARENT_PATH + 'sample.txt'
# deep-q net input-output setting
N_INPUT = 33
N_OUTPUT = 1
N_ACTION = 37
# whether genenate sample file or not
GEN_SAMPLE_FILE = False
# reward ration
SCORE_RATIO = 100