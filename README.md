# Seis-Utils
Various utilities for seismology

1. station2hypo71.py
Convert a space-delimited station file to HYPO71 input format. Input format: Network, station, lat, long, elevation (m).
Usage: station2hypo71.py <infile> <outfile>

2. surface_wave_detect.py
Python script to download LDEO surface-wave detection events from last week from
https://www.ldeo.columbia.edu/~ekstrom/Research/SWD/current/RADB_SWD_grd.html
and cross-check with events in USGS-NEIC and ISC catalogues.
Prints out a list of surface wave detections not found in catalogues and plots map. 
Usage: python surface_wave_detect.py
