#! /usr/bin/env python3

from abc import abstractmethod

"""
Base class for all action-class
"""

class BaseProcessAction:
    def __init__(self, hand_card_status, primary_item, **kwargs):
        """
        hand_card_status: 
        ---------------------------------------------------
        Card:  * * * 3 4 5 6 7 8 9 10 J Q K A 2 QUEEN JACK
        ---------------------------------------------------
        Count: 0 0 0 4 4 4 4 4 4 4 4  4 4 4 4 4   1     1
        ---------------------------------------------------
        """
        self.hand_card_status = hand_card_status
        self.primary_item = primary_item
        self.kwargs = kwargs

    @abstractmethod
    def run(self):
        """
        Returns
        -----------------
        put_card: e.g. [3, 4, 5, 6, 7, 8]
        score: the reward for this action
        primary_item: the primary element of the `put_card`
        """
        raise NotImplementedError