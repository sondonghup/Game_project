import argparse
import torch
from torch.nn import functional as F

parser = argparse.ArgumentParser()
parser.add_argument('--save_every', type=int, required=True, default=1, help='save every')
parser.add_argument('--epoch', type=int, required=True, default=10, help='total epoch')
parser.add_argument('--pretrainG', type=str, default='', help='Pretrained Generator path')
parser.add_argument('--pretrainD', type=str, default='', help='Pretrained Discriminator path')
parser.add_argument('--gpus', type=str, default='0', help='split by ')
parser.add_argument('--batch_size', type=int, required=True, default=10, help='batch size')
parser.add_argument('--experiment_dir', type=str, required=True, help='experiment dir')
parser.add_argument('--sample_rate', type=str, required=True, help='sample rate, 32k/40k/48k')
parser.add_argument('--version', type=str, required=True, help='model version')
parser.add_argument('--if_f0', type=int, required=True, help='use f0 as one of the inputs of the model, 1 or 0')
parser.add_argument('--if_latest', type=int, required=True, help='if only save the latest G/D pth file, 1 or 0')
parser.add_argument('--if_cache_data_in_gpu', type=int, required=True, help='if caching the dataset in GPU memory, 1 or 0')

args = parser.parse_args()

