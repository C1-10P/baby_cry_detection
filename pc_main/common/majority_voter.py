# -*- coding: utf-8 -*-

__all__ = [
    'MajorityVoter'
]

from collections import Counter

class MajorityVoter:
    """
    Class to make a majority vote over multiple classifications
    """

    def __init__(self, prediction_list):
        self.predictions = prediction_list

    def vote(self):
        #@see http://stackoverflow.com/questions/1518522/python-most-common-element-in-a-list
        data = Counter(self.predictions)
        return data.most_common(1)[0][0]
