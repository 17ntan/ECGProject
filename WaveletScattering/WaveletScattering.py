import numpy as np
from kymatio.numpy import Scattering1D
import matplotlib.pyplot as plt

def wavelet_scattering(x, plot_coeffs=False):
	"""
	Following this tutorial: https://www.kymat.io/gallery_1d/plot_real_signal.html#sphx-glr-gallery-1d-plot-real-signal-py

	Input: 1d numpy array
	Output: scattering coefficients, list of numpy arrays
	"""

	# normalize
	x = x / np.max(np.abs(x))

	T = x.shape[-1]
	J = 6
	Q = 16
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

	return [order0, order1, order2]
