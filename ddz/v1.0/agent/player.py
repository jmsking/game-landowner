#! /usr/bin/env python3

import random

from log.log import Logger
from enums.player_role_enum import PlayerRoleEnum
from common.card_utils import CardUtil

logger = Logger.getLog(__file__)

class Player:

    def __init__(self, name, role=PlayerRoleEnum.DEFAULT):
        """
        name : a specified name for current player
        role : the role of player
        """
        if role == PlayerRoleEnum.DEFAULT:
            raise Exception('Please specified the role of this player,' \
                        'ref <PlayerRoleEnum>')
        logger.info(f'Current Player is [{name}({role.value})]')
        self.name = name
        self.role = role

    def obtain_init_card(self, exclude_card=None):
        """
        Obatain cards at first time in one episode
        """
        card_num = 17
        if self.role == PlayerRoleEnum.LAND_OWNER:
            card_num = 20
        cards = CardUtil.get_card(card_num, exclude_card)
        return cards