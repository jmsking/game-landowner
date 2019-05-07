#! /usr/bin/env python3

DEBUG_MODE = False
ENV_DEBUG = False
PARENT_PATH = './ddz/'
MODEL_PATH = PARENT_PATH + 'model/'
MODEL_SAVE_PATH = MODEL_PATH + 'deep_q.ckpt'
MODEL_META_PATH = MODEL_PATH + 'deep_q.ckpt.meta'
LOG_SAVE_PATH = PARENT_PATH + 'logs'
N_INPUT = 30
N_OUTPUT = 1
N_ACTION = 27
GEN_SAMPLE_FILE = False
SCORE_RATIO = 100