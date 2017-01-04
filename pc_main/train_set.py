# -*- coding: utf-8 -*-

import argparse
import os
import pandas as pd
import re

from common.training_reader import TrainingReader
from common.feature_engineer_frame import FeatureEngineerFrame


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--load_path',
                        default='%s/../data' % os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument('--save_path',
                        default='%s/../../output/dataset/' % os.path.dirname(os.path.abspath(__file__)))

    # Arguments
    args = parser.parse_args()
    load_path = args.load_path
    save_path = args.save_path

    ####################################################################################################################
    # READ FILES IN SUB-FOLDERS of load_path
    ####################################################################################################################

    # list load_path sub-folders
    regex = re.compile(r'^[0-9]')
    directory_list = [i for i in os.listdir(load_path) if regex.search(i)]

    # initialize empty data frame for results
    concat_features = pd.DataFrame()

    # iteration on sub-folders
    for directory in directory_list:
        # Instantiate FeatureEngineerFrame
        feature_engineer = FeatureEngineerFrame(label=directory)

        file_list = os.listdir(os.path.join(load_path, directory))

        # iteration on audio files in each sub-folder
        for audio_file in file_list:
            file_reader = TrainingReader(os.path.join(load_path, directory, audio_file))
            data, sample_rate = file_reader.read_audio_file()
            avg_features = feature_engineer.feature_engineer(audio_data=data)

            concat_features = pd.concat([concat_features, avg_features]).reset_index(drop=True)

    ####################################################################################################################
    # SAVE
    ####################################################################################################################

    # Save DataFrame
    concat_features.to_csv(os.path.join(save_path, 'dataset.csv'), index=False)


if __name__ == '__main__':
    main()
