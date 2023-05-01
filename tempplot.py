#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
from math import sqrt, ceil

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
		else:
			cols = int(cols)

	rows = ceil(count / cols)

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

def merge_cmaps(boundaries, maps):
	from matplotlib.colors import LinearSegmentedColormap

	def create_data(l, h, m):
		r = []
		for v in range(m.N):
			v = float(v) / (m.N-1)
			r.append(((1-v)*l + v*h, m(v)))
		return r

	low = 0.0
	result = []
	for m in maps:
		if boundaries:
			high = boundaries.pop(0)
		else:
			high = 1.0
		result += create_data(low, high, m)
		low = high

	return LinearSegmentedColormap.from_list("merged", result, N=len(result))


def colorspec(str, data):
	from matplotlib import cm
	from matplotlib.colors import Normalize
	boundaries = []
	cmaps = []
	vmin = None
	vmax = None
	xs = str.split(' ')
	try:
		vmin = float(xs[0])
		xs.pop(0)
	except:
		pass
	while len(xs) > 1:
		cmaps.append(cm.get_cmap(xs.pop(0)))
		boundaries.append(float(xs.pop(0)))

	if xs:
		cmaps.append(cm.get_cmap(xs[0]))
	else:
		vmax = boundaries.pop()

	norm = Normalize(vmin=vmin, vmax=vmax)
	norm.autoscale_None(data)

	return norm, merge_cmaps(list(map(norm, boundaries)), cmaps)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description='Display raw temperature files for exploring interactively',
		epilog='Example:\ntempplot.py --cmap "cool 12.6 coolwarm" test.raw')
	parser.add_argument('--cmap', dest='cmap', default='coolwarm',
		metavar='[min] cmap [temp cmap [...]] [max]')
	parser.add_argument('--title', '-t', dest='t')
	parser.add_argument('--columns', '-c', dest='c', type=int, help='number of images in per row')
	parser.add_argument('filenames', nargs='+')
	args = parser.parse_args()

	data = tile(args.c, args.filenames)
	norm, cmap = colorspec(args.cmap, data)
	plt.imshow(data, norm=norm, cmap=cmap)
	plt.axis('off')
	plt.colorbar()
	if args.t:
		plt.title(args.t)
	plt.show()
