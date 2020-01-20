#! /usr/bin/env python3

class CommonUtils:

    @staticmethod
    def onehot(category=[1,2,3]):
        size = len(category)
        result = {}
        for idx, item in enumerate(category):
            oh = [0]*size
            oh[idx] = 1
            result[item] = oh
        return result