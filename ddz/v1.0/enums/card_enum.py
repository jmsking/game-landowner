#! /usr/bin/env python3

from enum import Enum

class CardEnum(Enum):
    TH = 3
    FO = 4
    FI = 5
    SI = 6
    SE = 7
    EI = 8
    NI = 9
    T = 10
    J = 11
    Q = 12
    K = 13
    A = 14
    TW = 15
    # Queen, 小王
    QU = 16
    # Jack, 大王
    JA = 17

if __name__ == '__main__':
    print(CardEnum.A)
    print(CardEnum.TW.value)
    print(CardEnum.QU.value)
    print(CardEnum.JA.value)