#!/usr/bin/env python
"""
Convert a space-delimited station file to HYPO71 input format
Input format: Network, station, lat, long, elevation (m)
(allows 5-character station names for seisan hyp package)
Usage: station2hypo71.py <infile> <outfile>
"""

import sys
import math

try:
    infile = sys.argv[1]
    outfile = sys.argv[2]
except IndexError:
    sys.exit("Did not specify input and/or output file.\n"
             "Usage: station2hypo71.py <infile> <outfile>")

output = open(outfile, 'w')

# Read in input file
for line in open(infile, 'r'):
    sta = line.split()[1]
    lat = float(line.split()[2])
    lon = float(line.split()[3])
    ele = float(line.split()[4])

    # Determine hemispheres
    if lat < 0:
        lat_side = 'S'
    else:
        lat_side = 'N'
    if lon < 0:
        lon_side = 'W'
    else:
        lon_side = 'E'

    # Format and write to file
    output.write(" {:>5s}{:02g}{:05.2f}{:1s}{:03.0f}{:05.2f}{:1s}{:4.0f}\n"
                 .format(sta,
                         abs(math.modf(lat)[1]),
                         60*abs(math.modf(lat)[0]), lat_side,
                         abs(math.modf(lon)[1]),
                         60*abs(math.modf(lon)[0]), lon_side,
                         ele))
output.close()
