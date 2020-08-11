import wfdb
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join('LoadData')))
sys.path.append(os.path.abspath(os.path.join('WaveletScattering')))
sys.path.append(os.path.abspath(os.path.join('Modeling')))
from ECGData import ECGData
from WaveletScattering import wavelet_scattering_segments, process_wavelet_coeffs_segments
from anomalyDetection import anomaly_detection, test_thresh
from Metrics import calculate_metrics

# load data (Record 100)
data_path = 'LoadData/Data/100'
data = ECGData(data_path)
# data.plot_segments(1)
ecg_signal = data.get_signal(1)
segments = data.get_segments(1)
record = data.get_record()
annotation = data.get_annotation()
labels = data.get_beat_labels()

# print(len(labels), len(segments))

# calculate scattering wavelet coefficients for each segment
wavelet_coeff_lst = wavelet_scattering_segments(segments)

# calculate dissimilarity of each beat
dissimilarity = process_wavelet_coeffs_segments(wavelet_coeff_lst)
print(len(dissimilarity))
x = anomaly_detection(dissimilarity)
# np.savetxt("result.txt", x)
# x = np.loadtxt("result.txt")

# data.plot_r_peaks(1, anomalies=x)
accuracy, sensitivity, positive_predictivity = calculate_metrics(x, labels)
print(accuracy, sensitivity, positive_predictivity)
