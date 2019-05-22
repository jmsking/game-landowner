#! /usr/bin/env python3

from enum import Enum

"""
玩家角色枚举类
"""

class PlayerRoleEnum(Enum):
    # 未确认
    DEFAULT = -1
    # 地主
    LAND_OWNER = 1
    # 地主上家
    UP_LAND_OWNER = 2
    # 地主下家
    LOW_LAND_OWNER = 3