import matplotlib.pyplot as pl
import numpy as np

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

request = cimgt.OSM()


# helper function
def zoomlevel_from_deg(deg):
    "Calculate OSM zoom level from a span in degrees.  Adjust +/-1 as desired"
    from numpy import log2, clip, floor

    zoomlevel = int(clip(floor(log2(360) - log2(delta)), 0, 20))
    return zoomlevel


long_min = 2.233778
lat_min = 49.030821
long_max = 2.251614
lat_max = 49.038626

lon_i = long_min + (long_max - long_min) / 2
lat_i = lat_min + (lat_max - lat_min) / 2
delta = (lat_max - lat_min) * 1.1
zoom = zoomlevel_from_deg(delta) - 1  # 10 #  0-19
print(f"Zoom Level: {zoom}")

# Bounds: (lon_min, lon_max, lat_min, lat_max):
extent = [
    lon_i - delta / np.cos(lat_i * np.pi / 180),
    lon_i + delta / np.cos(lat_i * np.pi / 180),
    lat_i - delta,
    lat_i + delta,
]

ax = pl.axes(projection=request.crs)
ax.set_extent(extent)
ax.add_image(request, zoom)  # 6 = zoom level

# Just some random points/lines:
pl.scatter(lon_i, lat_i, transform=ccrs.PlateCarree())
pl.plot(
    [lon_i, lon_i + delta / 2], [lat_i, lat_i - delta / 2], transform=ccrs.PlateCarree()
)
pl.show()
