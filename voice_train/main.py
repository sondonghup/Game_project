import time
import os
import subprocess
import shutil
import base64
from dataset import TextAudioLoader

if __name__ == '__main__':
    train_data = TextAudioLoader('./data')
    train_data.get_audio()