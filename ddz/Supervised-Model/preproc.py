#! /usr/bin/env python

"""
Preprocess Utils
"""

"""
Generate state-action pair based the process of putting card
Ref. Table 1 of paper
Args:
  card_process: the process of putting card
    Ex. 0,33;1,55;2,66...
  target: labeled target
    Ex. 0 or 1 or 2
"""
def gen_state_action_pair(card_process, target=1):
    samples = list()
    one_sample = list()
    put_seq = card_process.split(";")
    for item in put_seq:
        one_sample.append(item)
        player, _ = item.strip().split(",")
        if player == str(target):
            if len(one_sample) > 1:
                samples.append(one_sample.copy())
           
    return samples

if __name__ == "__main__":
    card_process = "0,33;1,55;2,66;0,77;1,AA;1,6;2,T;0,J;1,K;0,2;2,S;2,44;" \
            "0,KK;2,22;2,89TJQK;2,QQ;0,AA;0,56789;1,789TJ;1,3;2,5"
    samples = gen_state_action_pair(card_process, target=0)
    print(samples)