# -*- coding: utf-8 -*-

import re


__all__ = [
    'DefaultPredictor'
]

import logging

class DefaultPredictor:
    """
    Class to classify a new audio signal and determine if it's a baby cry
    """

    def __init__(self, model):
        self.model = model

    def classify(self, new_signal):
        """
        Make prediction with trained model

        :param new_signal: 1d array, 34 features
        :return: 1 (it's baby cry); 0 (it's not a baby cry)
        """
        logging.debug("signal: %s" % str(new_signal))


        category = self.model.predict(new_signal)
        logging.debug("category: %s" % str(category))

        # category is an array of the kind array(['004 - Baby cry'], dtype=object)
        return category[0]
