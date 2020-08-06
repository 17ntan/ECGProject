import wfdb
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join('LoadData')))
sys.path.append(os.path.abspath(os.path.join('WaveletScattering')))
sys.path.append(os.path.abspath(os.path.join('Modeling')))
from ECGData import ECGData
from WaveletScattering import wavelet_scattering, process_wavelet_coeffs
from anomalyDetection import anomaly_detection, test_thresh

# # load data (Record 100)
data_path = 'LoadData/Data/100'
# record = wfdb.rdrecord(data_path)
# ecg_signal = record.p_signal[:, 0]

# annotation = wfdb.rdann(data_path, 'atr', return_label_elements=['symbol'])
# ann = annotation.symbol
# true_anomaly = np.where(np.asanyarray(ann) != "N")
# print("true label index:", true_anomaly)

data = ECGData(data_path)
# data.plot_segments(1)
ecg_signal = data.get_signal(1)

# calculate scattering wavelet coefficients
[Sx, order0, order1, order2] = wavelet_scattering(ecg_signal, plot_coeffs=False)

# calculate dissimilarity of each beat
dissimilarity = process_wavelet_coeffs(Sx)
anomaly_detection(record, annotation, dissimilarity, plot=False)
# test_thresh(record, annotation, dissimilarity, true_anomaly)