# DIY-Thermocam absolute temperature accuracy

I'm using using the thermocam for thermal analysis of residential buildings.
My application requires an overall accuracy of absolute temperature of
about 1K. I found it difficult to achieve this with the builtin automatic
calibration procedure. This article documents my experiments and the
workflow I came up with.

The basic setup I'm working with is indoor measurement with wet ice as
reference body. IE most objects are in the range 0°C - 25°C and the
ambient temperature (both air and radiation) is about 20°C. At the
start, end and several times in between I take a thermal image of the
reference body. Such a campaign typically take about 20-30 minutes.

## Automatic calibration performance
While working with the built-in calibration procedure, I noticed several
issues:

* The resulting calibration data is not very reproducible.
* The slope of the calibration curve generally seems too low: Most of the
  time I get values around 30mK while the data sheet specifies <50mK.
  (Of course 30mK < 50mK actually is true, but it seems a bit off to me.)
* The spot sensor, supposed to help calibration, drifts a lot over half
  an hour. Probably due to warming up.

The following table shows repeated measurement results for a bowl of
wet snow:

```
Time	  mean raw value	temperature [°C]	spot sensor [°C]
------------------------------------------------------------------------
5:57:41	   7556,28		 4,03			 1,16
6:01:22	   7279,84		-3,95			-3,24
6:02:53	   7469,17		 0,97			-4,14
6:04:10	   7441,50		 4,36			-4,30
6:05:19	   7421,88		 2,86			-4,86
6:08:15	   7409,88		-1,21			-5,28
6:11:54	   7397,90		 5,38			-5,62
6:15:53	   7371,48		-6,23			-8,60
6:20:37	   7349,74		 0,81			-9,50
				===============
			average: 0,78 °C
```

While the average value of temperatures is quite close to the real value
of 0°C, the individual temperatures derived from the thermal images are
quite a bit off. The spot sensor gives a fairly decent temperature at
the beginning, after switching the camera on. But then the values start
running away.

## Manual calibration
The most simple conversation formula from raw values to temperatures is
```
temperature = reference_temperature + (value - offset) * slope
```
To calculate `slope` two reference bodies are used: The bowl of wet
ice (`reference_temperature = 0°C`) and an object in thermal equilibrium
with the air in the room. A piece of dry cloth hanging on a hook from the
ceiling is a good candidate.

The following image shows the average raw values of two reference bodies
in such an experiment. The colder object is wet ice and then other is at
21.6°C. As you can see, the offset has quite some drift, while the
difference between reference bodies (related to slope) is quite constant:

<img src="https://raw.githubusercontent.com/haraldg/thermocam-tools/master/images/calibration_raw_values.svg" />

The data was extracted using the following [gmic](https://gmic.eu) command
line in a semi-manual way. For each image on the command line, the user
is prompted to draw a rectangle of which gmic prints the average value
to stdout:
```
gmic *_object_raw.pgm -crop -repeat '$!' '-l[$>]' -echo_stdout '{0,b}':'{is#0/wh#0}' -endl -done
```

Actually using linear interpolation the slope can be calculated at each
measurement of either reference body. The next plot shows these values for
slope together with a linear regression fit. As you can see, there is some
trend for slope to become higher over time, but it is mostly within noise
level.

<img src="https://raw.githubusercontent.com/haraldg/thermocam-tools/master/images/calibration_slope.svg" />

Most slope values are within 5% of the mean. Thus when the
reference temperature is 0°C, the error at 20°C is about 1K. It is
possible to meet the requirements for my application without accounting for
the drift in slope. I still take measurements of warm reference bodies at
regularly, but only for monitoring measurement performance, not for
calibration.

Also slope values around 47mK are very compatible with the data sheet
specification of <50mK - so this method of calibration seems quite reasonable.
