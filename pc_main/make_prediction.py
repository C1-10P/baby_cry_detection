# -*- coding: utf-8 -*-

import argparse
import os
import sys
import pickle
import logging

#egg_path = '%s/../lib/baby_cry_detection-0.1-py2.7.egg' % os.path.dirname(os.path.abspath(__file__))
#sys.path.append(egg_path)

from common.overlapping_reader import OverlappingReader
from common.default_predictor import DefaultPredictor
from common.feature_engineer import FeatureEngineer
from common.simple_reader import SimpleReader
from common.majority_voter import MajorityVoter


def main():
    logging.basicConfig(filename='make_prediction.log', level=logging.DEBUG)
    logging.info('Start')

    parser = argparse.ArgumentParser()
    parser.add_argument('--recording',
                        default='%s/../recording/%s' % (os.path.dirname(os.path.abspath(__file__)),'signal_9s.wav'))
    parser.add_argument('--load_path_model',
                        default='%s/../model/' % os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument('--prediction',
                        default='%s/../prediction/%s' % (os.path.dirname(os.path.abspath(__file__)),'prediction.txt'))
    parser.add_argument('-q', dest='quiet', action='store_true', default=False)
    parser.add_argument('-o', dest='overlapping', action='store_true', default=False)


    # Arguments
    args = parser.parse_args()
    recording = args.recording
    load_path_model = args.load_path_model
    prediction_file = args.prediction
    quiet_mode = args.quiet
    overlapping_reader_mode = args.overlapping
    
    # Read signal

    if overlapping_reader_mode: 
     file_reader = OverlappingReader(recording)
    else:
     file_reader = SimpleReader(recording)

    play_list = file_reader.read_audio_file()
    
    # Feature extraction
    engineer = FeatureEngineer()

    play_list_processed = list()

    for signal in play_list:
        tmp = engineer.feature_engineer(signal)
        play_list_processed.append(tmp)

    # MAKE PREDICTION
   
    with open((os.path.join(load_path_model, 'model.pkl')), 'rb') as fp:
        model = pickle.load(fp)

    predictor = DefaultPredictor(model)

    predictions = list()

    for signal in play_list_processed:
        tmp = predictor.classify(signal)
        predictions.append(tmp)

    if not quiet_mode:
     print "Predictions: %s" % str(predictions)
    
    # MAJORITY VOTE
   
    majority_voter = MajorityVoter(predictions)
    majority_vote = majority_voter.vote()

    # SAVE
  
    if not quiet_mode:
     print "Majority vote: %s" % majority_vote

    # Save prediction result
    with open(prediction_file, 'wb') as text_file:
        text_file.write("{0}".format(majority_vote))

    logging.info('End')


if __name__ == '__main__':
    main()
