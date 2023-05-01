#!/usr/bin/env python3

from datinfo import readdat
from scipy.interpolate import interp1d
import numpy as np
import scipy.ndimage as ndimage
import argparse
import time

def getcoldvalue(img):
	"""Return the average value of the coldes areas of an image."""
	blur = ndimage.gaussian_filter(img.astype(np.float32), 1.5)
	mask = blur < (blur.min() + 10)
	mask_count = mask.sum()
	if mask_count < 500:
		raise RuntimeError("found less then 500 cold pixels")

	return (blur*mask).sum()/mask_count

def timestamp(name):
	"""Return the timestamp part of a filename as seconds since epoch."""
	try:
		return time.mktime(time.strptime(name[:14], '%Y%m%d%H%M%S'))
	except:
		return 0

def get_offset(raw_value, temp_value, slope, temperature=0.0):
	return raw_value - (temp_value - temperature) / slope

def calibrate(names, selector):
	times = []
	values = []
	for name in names:
		print(name)
		times.append(timestamp(name))
		values.append(selector(readdat(name)))

	return interp1d(times, values, fill_value="extrapolate")

def convert(name, temperature, offset, slope):
	src = readdat(name)
	dest = (temperature + (src - offset) * slope).astype(np.float32)
	dest.tofile(name[:-3]+"raw")
	print(name, "using raw value", offset, "for temperature", temperature)

	return dest

def process_files(names, slope, ref="ice", temperature=0.0, offset=None):
	if offset == None:
		refs = []
		suffix = "_" + ref + ".DAT"
		for name in names:
			if name.endswith(suffix):
				refs.append(name)

		o = calibrate(refs, getcoldvalue)
	elif isinstance(offset, (int, float)):
		o = lambda t: offset
	else:
		o = offset

	for name in names:
		convert(name, temperature, o(timestamp(name)), slope)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert Lepton raw values to actual temperatures.')
	parser.add_argument('--slope', '-s', dest='s', type=float, required=True)
	parser.add_argument('--ref', dest='ref', default='ice')
	parser.add_argument('--temperature', '-t', dest='t',  type=float, default=0.0)
	parser.add_argument('--offset', '-o', dest='o', type=float)
	parser.add_argument('filenames', metavar='file', nargs='+')

	args = parser.parse_args()
	process_files(args.filenames, args.s, ref=args.ref, temperature=args.t, offset=args.o)
