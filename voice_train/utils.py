import torch
import numpy as np
from scipy.io.wavfile import read

# def load_filepaths(filename):
#     with open(filename, encoding='utf-8')as f:
#         filepaths = [line.strip().split()]

def wav_to_torch(full_path):
    sampling_rate, data = read(full_path)
    return torch.FloatTensor(data.astype(np.float32)), sampling_rate

def sepctogram_torch(y, n_fft, sampling_rate, hop_size, win_size, center=False):
    pass