#!/usr/bin/env python3

import numpy as np
import os
import sys

def readdat(name):
	"""Read DIY-Thermocam dat-files and return thermal data als array."""
	if os.path.getsize(name) >= 38400:
		shape = (120,160)
	else:
		shape = (60,80)

	d = np.fromfile(name, np.dtype('>i2'), count=shape[0]*shape[1])
	d.shape = shape

	return d

def info(name):
	img = readdat(name)
	print(name, img.shape, "coldest:", img.min(), "hottest:", img.max())

if __name__ == "__main__":
	for name in sys.argv[1:]:
		info(name)
