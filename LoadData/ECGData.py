import wfdb
import numpy as np
import matplotlib.pyplot as plt

class ECGData:
	"""
	Holds the physical signal, segments, and labels from wfdb record
	"""
	def __init__(self, data_path):
		self.record = wfdb.rdrecord(data_path)
		self.channel1 = self.record.p_signal[:, 0]
		self.channel2 = self.record.p_signal[:, 1]
		self.annotation = wfdb.rdann(data_path, 'atr', return_label_elements=['symbol'])
		self.all_labels = np.asarray(self.annotation.symbol)
		self.locations = self.annotation.sample
		self.find_peaks()
		self.find_segments()

	def find_peaks(self):
		# other labels not in this list mark non-beat events
		possible_beat_labels = ['N', 'L', 'R', 'B', 'A', 'a', 'J', 'S', 'V', 'r', 'F', 'e', 'j', 'n', 'E', '/', 'f', 'Q', '?']
		mask = np.isin(self.all_labels, possible_beat_labels)
		self.beat_labels = self.all_labels[mask]
		self.r_peaks = self.locations[mask]

	def find_segments(self):
		"""
		There are the same number of r peaks as there are beat labels.
		This means that there should be the same number of beats as r peaks.
		However, during the semester we treated r peaks as the borders between
		beats, so there would be 2 more segments than r peaks counted.
		This won't work for the number of labels we have, so for this project
		I am going to start the beat exactly halfway between two r peaks.
		"""
		self.segments1 = []
		self.segments2 = []

		self.segments1.append(self.channel1[:(self.r_peaks[0] + self.r_peaks[1])//2])
		self.segments2.append(self.channel2[:(self.r_peaks[0] + self.r_peaks[1])//2])
		for i in range(1, len(self.r_peaks) - 1):
			self.segments1.append(self.channel1[(self.r_peaks[i - 1] + self.r_peaks[i])//2:(self.r_peaks[i] + self.r_peaks[i + 1])//2])
			self.segments2.append(self.channel2[(self.r_peaks[i - 1] + self.r_peaks[i])//2:(self.r_peaks[i] + self.r_peaks[i + 1])//2])
		self.segments1.append(self.channel1[(self.r_peaks[-2] + self.r_peaks[-1])//2:])
		self.segments2.append(self.channel2[(self.r_peaks[-2] + self.r_peaks[-1])//2:])

		if len(self.segments1) != len(self.beat_labels) or len(self.segments2) != len(self.beat_labels):
			print("Mismatched number of segments: {} {} {}".format(len(self.segments1), len(self.segments2), len(self.beat_labels)))

	def plot_segments(self, channel_num):
		"""
		Spaghetti plot (segments overlaid on top of each other)
		"""
		if channel_num == 1:
			segs = self.segments1
		elif channel_num == 2:
			segs = self.segments2
		else:
			print("Please choose a valid channel number (1 or 2)")
			return

		for seg in segs:
			plt.plot(seg)
		plt.show()

	def plot_r_peaks(self, channel_num, anomalies=None):
		"""
		dots on peaks (different color if detected anomalies)
		anomalies - numpy array of 0s and 1s (0 is normal)
		"""
		if channel_num == 1:
			signal = self.channel1
		elif channel_num == 2:
			signal = self.channel2
		else:
			print("Please choose a valid channel number (1 or 2)")
			return

		plt.plot(signal)
		if anomalies:
			mask = anomalies.astype(bool)
			plt.plot(r_peaks[mask], signal[r_peaks[mask]], "ro")
			plt.plot(r_peaks[np.invert(mask)], signal[r_peaks[np.invert(mask)]], "go")

	def get_signal(self, channel_num):
		if channel_num == 1:
			return self.channel1
		elif channel_num == 2:
			return self.channel2
		else:
			print("Please choose a valid channel number (1 or 2)")
			return

	def get_r_peaks(self):
		return self.r_peaks

	def get_beat_labels(self):
		return self.beat_labels

	def get_record(self):
		return self.record

	def get_annotation(self):
		return self.annotation

	def get_segments(self, channel_num):
		if channel_num == 1:
			return self.segments1
		elif channel_num == 2:
			return self.segments2
		else:
			print("Please choose a valid channel number (1 or 2)")
			return
