#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import numpy as np
import os

def readraw(name):
	"""Read file with floating point temperature values."""
	if os.path.getsize(name) >= 76800:
		shape = (120,160)
	else:
		shape = (60,80)

	d = np.fromfile(name, np.float32, count=shape[0]*shape[1])
	d.shape = shape

	return d


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Display raw temperature file for exploring interactively')
	parser.add_argument('--cmap', dest='cmap', default='coolwarm')
	parser.add_argument('--title', '-t', dest='t')
	parser.add_argument('filename')
	args = parser.parse_args()
	plt.imshow(readraw(args.filename))
	plt.colorbar()
	if args.t:
		plt.title(args.t)
	plt.set_cmap(args.cmap)
	plt.show()
