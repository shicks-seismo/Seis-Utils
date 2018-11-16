#!/usr/bin/env python

"""
Python script to download LDEO surface-wave detection events from last week from
https://www.ldeo.columbia.edu/~ekstrom/Research/SWD/current/RADB_SWD_grd.html
and cross-check with events in USGS-NEIC and ISC catalogues.
Prints out a list of surface wave detections not found in catalogues.
Python module prerequisites: ObsPy, BeautifulSoup, Basemap, Matplotlib
"""

import bs4
import urllib.request
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

# Start of parameters to define
dt = 180  # Number of seconds to search either side of SWD time
dl = 2.0  # Degrees lat/long to search either side of SWD detection loc
minmag = 3.0  # Minimum magnitude threshold to search catalogues
# End of parameters to define

# Set up FDSN client
client1 = Client("USGS")
client2 = Client("ISC")

# Download data from website and split into list of lines
link = ("https://www.ldeo.columbia.edu/~ekstrom/Research/SWD/current/"
        "RADB_SWD_grd.html")
webpage=str(urllib.request.urlopen(link).read())
soup = bs4.BeautifulSoup(webpage, features="lxml")
dat = soup.get_text().split("\\n")

lats = []
lons = []

# Loop over each line, select events, get location parameters
for l in dat:
    l = l.lstrip()
    if l[0:2] == "20" and l[4:5] != "-":
        SWD_date = UTCDateTime(
            year=int(l[0:4]), month=int(l[5:7]), day=int(l[8:10]),
            hour=int(l[11:13]), minute=int(l[14:16]), second=int(l[17:19]))
        SWD_lat = float(l[23:29])
        SWD_lon = float(l[30:37])
    
        # First try to get event from USGS catalogue. If nothing found, try ISC
        # catalogue
        try:
            cat = client1.get_events(
                starttime=SWD_date-dt, endtime=SWD_date+dt, minmagnitude=minmag,
                latitude=SWD_lat, longitude=SWD_lon, maxradius=dl)
        except:
            try:
                cat = client2.get_events(
                    starttime=SWD_date-dt, endtime=SWD_date+dt, minmagnitude=minmag,
                    latitude=SWD_lat, longitude=SWD_lon, maxradius=dl)
            except:

                # If not found print event and append location to list for plotting
                # later.
                print("No corresponding events found in ISC/NEIC catalogues:", l)
                lats.append(SWD_lat)
                lons.append(SWD_lon)

# Now make a map showing locations not found
eq_map = Basemap(projection='robin', lat_0=0, lon_0=-100,
                 resolution='l', area_thresh=1000.0)
eq_map.drawcoastlines()
eq_map.drawcountries()
eq_map.fillcontinents(color = 'gray')
eq_map.drawmapboundary()
eq_map.drawmeridians(np.arange(0, 360, 30))
eq_map.drawparallels(np.arange(-90, 90, 30))
x,y = eq_map(lons, lats)
eq_map.plot(x, y, 'ro', markersize=6)
plt.title("Surface wave detections from past 7 days not in ISC/USGS " 
          "catalogues")
plt.show()
