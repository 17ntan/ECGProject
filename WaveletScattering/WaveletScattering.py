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
	J = 8 # the largest filter will be concentrated in a time interval of size 2**J.
	Q = 128 # the number of wavelets per octave in the first-order filter bank. The larger the value, the narrower these filters are in the frequency domain and the wider they are in the time domain
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

def process_wavelet_coeffs(Sx):
	"""
	Standardize and shift scattering coefficients. Return dissimilarity of each segment.

	Sx: scattering coefficients, list of numpy arrays
	Output: S_hat: processed scattering coefficients, list of numpy arrays
	"""
	# remove bias introduced by the varying range of the scattering coefficients
	S_standard = preprocessing.scale(Sx)
	# shift data to origin
	S_hat = S_standard
	# dissimilarity
	d = np.linalg.norm(S_hat, axis=1)
	# d1 = d.reshape((d.shape[0],1))
	return d
