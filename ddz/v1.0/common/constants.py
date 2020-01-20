#! /usr/bin/env python3

import tensorflow as tf

TF_CONST = {
    'INPUT_KEY': 'input',
    'OUTPUT_KEY': 'output',
    'METHOD_NAME': tf.saved_model.PREDICT_METHOD_NAME,
    'SIGNATURE_KEY': tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY,
    'MODEL_TAG': tf.saved_model.SERVING,
}

EXTRA_CONST = {
    'SAVE_MODEL_PATH': 'models',
}
