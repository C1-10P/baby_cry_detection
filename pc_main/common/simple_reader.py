# -*- coding: utf-8 -*-

import librosa
# import re
# import pydub
# import os

__all__ = [
    'SimpleReader'
]

# new style class
class SimpleReader(object):
    """
    Read input audio file
    file_name: 'path/to/file/filename.mp3'
    """

    def __init__(self, file_name):
        self.file_name = file_name
        pass

    def read_audio_file(self):
        """
        Read audio file using librosa package. librosa allows resampling to desired sample rate and convertion to mono.

        :return:
        * play_list: a list of audio_data as numpy.ndarray.
        """

        play_list = list()
        audio_data, _ = librosa.load(self.file_name, sr=44100, mono=True)
        play_list.append(audio_data)

        return play_list
