# thermocam tools

This set of tools serves for post processing thermal imaging raw data.
Currently supported are:

* calibrating and converting an entire set (one measurement campaign) of
  raw data files to temperature files
* exploring and plotting temperature files
* post processing using [gmic](https://gmic.eu) 


## File formats and filename convention
### raw data

Raw data is currently expected to be in
[DIY-Thermocam](https://github.com/maxritter/DIY-Thermocam) `*.DAT` format.
Only the raw image data is actually read and all metadata discarded. It
should be easy to support other raw data formats in the future.


### temperature data

Temperature data is currently stored as 32-bit float values in native
byte order without any header or meta data. Surely there exists already
an established file format for this kind of data - please tell me if
you know something about this! Temperature data files use the filename
extension `.raw`, if they are just converted and calibrated data without
further enhancements like noise removal.


### filenames

are expected to be in the format `YYYYMMDDhhmmss_object.ext` where
`_object` is optional and describes the primary object of the scene. This
is mostly used to automatically detect images of reference bodies for
calibration.


## Tools available

Programs with the `.py` filename extension are intended to be used from the
shell, but are also loadable as module from other python programs or the
python interpreter.


### dat2temp.py - convert and calibrate

Call it with `--help` to get an overview of options available. However
since the program currently only performs offset calibration, you need to
at least specify the `--slope` parameter.


### tempplot.py - explore and plot a temperature files

Plots the specified temperature files with matplotlib.pyplot for interactive
exploration. You can save the plot as `*.png` file from the plot window.
If you specify more then one file, all will be shown in the same plot with
one common color map.

Command line options:

* `--cmap`: specify a color map (whatever matplotlib supports)
* `--columns`: the number of files to show in one row
* `--title`: a plot title.


### tempviewer - explore and post process temperature files with gmic

Any command line argument is expected to be a temperature file. All
temperature files are shown as thumbnails. Selecting (clicking) one
allows to explore the temperature values interactively.

After closing the window you are prompted for [gmic](https://gmic.eu)
commands to operate on the set of open images. This allows for further
post processing like noise filtering or saving to different image formats.

To quit the interpreter loop, press CTRL+D (end of file).


## Suggested workflow

I have the thermocam configured to show the current time on the display.
Whenever I take an image of a reference body (usually wet ice), I note down
the time after that on paper. After moving the images from the thermocam
to my computer, I use the list on paper to locate all images of a
reference body in the file manager and rename them from `YYYYMMDDhhmmss.DAT`
to `YYYYMMDDhhmmss_ice.DAT`. Then I run
```
dat2temp.py -s 0.047 --ref ice -t 0.0 *.DAT
```
