import numpy as np
import torch
import os
from torch.utils.data import Dataset, DataLoader
from utils import wav_to_torch

class TextAudioLoader(Dataset):

    def __init__(self, audiopath):
        self.audiopath = audiopath
        self.filenames = os.listdir(audiopath)

    def _filter(self):
        pass

    def get_audio(self):
        print(self.filenames)
        for filename in self.filenames:
            print(os.getcwd() + '/' + filename)
            audio, sampling_rate = wav_to_torch(os.getcwd() + '/data/' + filename)
            print(audio)
            print(audio.size())
            print(sampling_rate)

    def __getitem__(self, index):
        return self.get_audio()