import numpy as np
from kymatio.numpy import Scattering1D
import matplotlib.pyplot as plt
from sklearn import preprocessing

def wavelet_scattering(x, plot_coeffs=False):
	"""
	Following this tutorial: https://www.kymat.io/gallery_1d/plot_real_signal.html#sphx-glr-gallery-1d-plot-real-signal-py

	Input: 1d numpy array
	Output: scattering coefficients, list of numpy arrays
	"""

	# normalize
	x = x / np.max(np.abs(x))

	T = x.shape[-1]
	J = 6 # the largest filter will be concentrated in a time interval of size 2**J.
	Q = 16 # the number of wavelets per octave in the first-order filter bank. The larger the value, the narrower these filters are in the frequency domain and the wider they are in the time domain
	scattering = Scattering1D(J, T, Q)

	Sx = scattering(x)

	meta = scattering.meta()
	order0 = np.where(meta['order'] == 0)
	order1 = np.where(meta['order'] == 1)
	order2 = np.where(meta['order'] == 2)

	if plot_coeffs:
		plt.figure(figsize=(8, 2))
		plt.plot(x)
		plt.title('Original signal')
		plt.figure(figsize=(8, 8))
		plt.subplot(3, 1, 1)
		plt.plot(Sx[order0][0])
		plt.title('Zeroth-order scattering')
		plt.subplot(3, 1, 2)
		plt.imshow(Sx[order1], aspect='auto')
		plt.title('First-order scattering')
		plt.subplot(3, 1, 3)
		plt.imshow(Sx[order2], aspect='auto')
		plt.title('Second-order scattering')
		plt.show()

	return [Sx, order0, order1, order2]

def wavelet_scattering_segments(segments):
	"""
	Input: list of numpy arrays (list of segments)
	Output: list of lists of numpy arrays (scattering coeffs for each segment)
	"""
	coeffs = []
	for segment in segments:
		coeffs.append(wavelet_scattering(segment))
	return coeffs

def process_wavelet_coeffs(Sx):
	"""
	Standardize and shift scattering coefficients. Return dissimilarity of each segment.

	Sx: scattering coefficients, 1d numpy array
	Output: S_hat: processed scattering coefficients, list of numpy arrays
	"""
	# remove bias introduced by the varying range of the scattering coefficients
	S_standard = preprocessing.scale(Sx)
	# shift data to origin
	S_hat = S_standard
	# dissimilarity
	d = np.linalg.norm(S_hat)
	# d1 = d.reshape((d.shape[0],1))
	return d

def process_wavelet_coeffs_segments(Sx_lst):
	"""
	Input: list of Sx (one for each segment)
	Output: list of dissimilarities (one for each segment)
	"""
	d_lst = []
	for Sx in Sx_lst:
		ravel = [np.ravel(layer) for layer in Sx]
		vector = np.concatenate(ravel)
		d_lst.append(process_wavelet_coeffs(vector))
	return d_lst
