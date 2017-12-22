#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
from math import sqrt

def readraw(name):
	"""Read file with floating point temperature values."""
	if os.path.getsize(name) >= 76800:
		shape = (120,160)
	else:
		shape = (60,80)

	d = np.fromfile(name, np.float32, count=shape[0]*shape[1])
	d.shape = shape

	return d

def tile(cols, files):
	"""Place images on a tiling grid."""
	count = len(files)
	if count <= 1:
		return readraw(files[0])

	if not cols:
		cols = sqrt(count)
		if not cols.is_integer():
			cols = int(cols) + 1

	rows = count / cols
	if count % cols != 0:
		rows += 1

	d = np.empty((120*rows, 160*cols))
	average = None
	for r in range(rows):
		for c in range(cols):
			posr = 120*r
			posc = 160*c
			if files:
				i = readraw(files.pop(0))
				d[posr:posr+i.shape[0],posc:posc+i.shape[1]] = i
			else:
				if not average:
					average = d[0:60,0:80].mean()
				d[posr:posr+i.shape[0],posc:posc+i.shape[1]] = average

	return d

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Display raw temperature file for exploring interactively')
	parser.add_argument('--cmap', dest='cmap', default='coolwarm')
	parser.add_argument('--title', '-t', dest='t')
	parser.add_argument('--columns', '-c', dest='c')
	parser.add_argument('filenames', nargs='+')
	args = parser.parse_args()
	plt.imshow(tile(args.c, args.filenames))
	plt.axis('off')
	plt.colorbar()
	if args.t:
		plt.title(args.t)
	plt.set_cmap(args.cmap)
	plt.show()
