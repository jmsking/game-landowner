#! /usr/bin/env python3

from enum import Enum

class CardEnum(Enum):
    TH = '3'
    FO = '4'
    FI = '5'
    SI = '6'
    SE = '7'
    EI = '8'
    NI = '9'
    T = 'T'
    J = 'J'
    Q = 'Q'
    K = 'K'
    A = 'A'
    TW = '2'
    # small joker
    QU = 'S'
    # big joker
    JO = 'B'

if __name__ == '__main__':
    for item in CardEnum:
        print(item.value)