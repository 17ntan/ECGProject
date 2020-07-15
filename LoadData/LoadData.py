import wfdb
import numpy as np

# It's actually super easy to load the data!! All we need is wfdb
# This file is really just a "how to use wfdb"


# list of files that we got from the data base
# I typed all of them out and then I realized it's provided 
# in txt file called RECORDS :(
files = ["100", "101", "102", "103", "104", "105", "106", "107", "108", "109",
	"111", "112", "113", "114", "115", "116", "117", "118", "119", "121", "122", 
	"123", "124", "200", "201", "202", "203", "205", "207", "208", "209", "210", 
	"212", "213", "214", "215", "217", "219", "220", "221", "222", "223", "228", 
	"230", "231", "232", "233", "234"]

# load the data
# Input: file name. No need for .dat or .hea or whatever. 
# Output: wfdb record
record = wfdb.rdrecord('Data/100')

# get numpy array out of wfdb record
# Input: wfdb record
# Output: numpy array of signal Mx2 (2 ECG channels I think?)
arr = record.p_signal

# plot both signals
# Input: wfdb record, string for title
# Output: plot
wfdb.plot_wfdb(record=record, title='Record 100 from MIT-BIH Arrhythmia Database')
