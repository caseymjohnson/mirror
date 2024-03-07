from hx711 import HX711
import RPi.GPIO as GPIO


'''
Casey Johnson 3.1.24

This script is used to parse load cell data.
The HX711 module was used.
This data is saved to an output file.

'''

outputFile = 'parsedLoads.txt'

# initialize load 0
cell0 = HX711(
    dout_pin=5,
    pd_sck_pin=6,
    channel='A',
    gain=64
)

# initialize load cell 1
cell1 = HX711(
    dout_pin=5,
    pd_sck_pin=6,
    channel='A',
    gain=64
)

# reset cells prior to reading
cell0.reset()   
cell1.reset()   

# read each channel
d0 = cell0.get_raw_data(num_measures=5)
d1 = cell0.get_raw_data(num_measures=5)

# write to file
with open(outputFile, 'a') as f:
    f.write(f'{d0} {d1}')
