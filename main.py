import wfdb
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join('WaveletScattering')))
from WaveletScattering import wavelet_scattering

# load data (Record 100)
record = wfdb.rdrecord('LoadData/Data/100')
ecg_signal = record.p_signal[:, 0]

wavelet_scattering(ecg_signal, plot_coeffs=True)
