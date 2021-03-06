import torch
import numpy as np
from scipy.io.wavfile import read
import os
MAX_WAV_VALUE = 32768.0

def load_wav_to_torch(full_path):
    """
    Loads wavdata into torch array
    """
    sampling_rate, data = read(full_path)
    return torch.FloatTensor(data.astype(np.float32)), sampling_rate


def file_to_list(filename):
    """
    :param filename:
    :return: a list of filenames
    """
    #filename = os.path.join('dataset', filename)
    with open(filename, encoding='utf-8') as f:
        files = f.readlines()

    files = [f.rstrip() for f in files]
    return files


def to_gpu(x):
    x = x.contiguous()

    if torch.cuda.is_available():
        x = x.cuda(non_blocking=True)
    return torch.autograd.Variable(x)


def mu_law_decode(x, mu_quantization=256):
    assert(torch.max(x) <= mu_quantization)
    assert(torch.min(x) >= 0)
    x = x.float()
    mu = mu_quantization - 1.
    # Map values back to [-1, 1].
    signal = 2 * (x / mu) - 1
    # Perform inverse of mu-law transformation.
    magnitude = (1 / mu) * ((1 + mu)**torch.abs(signal) - 1)
    return torch.sign(signal) * magnitude

def mu_law_encode(x, mu_quantization=256):
    assert(torch.max(x) >= -1.0)
    assert(torch.min(x) <= 1.0)
    mu = mu_quantization - 1
    scaling = np.log1p(mu)
    x_mu = torch.sign(x) * torch.log1p(mu * torch.abs(x)) / scaling
    encoding = ((x_mu + 1) / 2 * mu + 0.5).long()
    return encoding
