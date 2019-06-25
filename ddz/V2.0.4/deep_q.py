#! /usr/bin/env python3

from __future__ import absolute_import

import config
from O_Net import ONet
from L_Net import LNet
from U_Net import UNet
import threading

"""
Train ONet, LNet, UNet Independent
"""
def train_net(flag):
    if flag == 0:
        agent1 = ONet(n_input=config.N_INPUT, n_output=config.N_OUTPUT)
        agent1.start_train()
    elif flag == 1:
        agent2 = LNet(n_input=config.N_INPUT, n_output=config.N_OUTPUT)
        agent2.start_train()
    else:
        agent3 = UNet(n_input=config.N_INPUT, n_output=config.N_OUTPUT)
        agent3.start_train()

t = list()
for i in range(3):
    t.append(threading.Thread(target=train_net, args=(i,)))

for item in t:
    item.start()

for item in t:
    item.join()