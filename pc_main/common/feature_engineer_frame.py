# -*- coding: utf-8 -*-

#import feature_engineer as FeatureEngineer
import pandas as pd
from feature_engineer import FeatureEngineer 
__all__ = [
    'FeatureEngineerFrame'
]

class FeatureEngineerFrame(FeatureEngineer):

    def __init__(self, label=None):
        if label is None:
            self.label = ''
        else:
            self.label = label

    def feature_engineer(self, audio_data):
     
        median_feat = super(FeatureEngineerFrame, self).feature_engineer(audio_data)

        features_df = pd.DataFrame(data=median_feat, columns=self.COL, index=None)

        features_df['label'] = self.label

        return features_df
