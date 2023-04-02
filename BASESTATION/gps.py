import os 
from math import asin, atan2, cos, degrees, radians, sin
from decimal import *

def get_point_at_distance(lat1, lon1, d, bearing, R=6371):
    """
    lat: initial latitude, in degrees
    lon: initial longitude, in degrees
    d: target distance from initial
    bearing: (true) heading in degrees
    R: optional radius of sphere, defaults to mean radius of earth

    Returns new lat/lon coordinate {d}km from initial, in degrees
    """
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    a = radians(bearing)
    lat2 = asin(sin(lat1) * cos(d/R) + cos(lat1) * sin(d/R) * cos(a))
    lon2 = lon1 + atan2(
        sin(a) * sin(d/R) * cos(lat1),
        cos(d/R) - sin(lat1) * sin(lat2)
    )
    return (degrees(lat2), degrees(lon2),)

lat,lon = os.popen('curl ipinfo.io/loc').read().split(',')
lat = Decimal(lat)
lon = Decimal(lon)
print(lat, lon)

distance = 1000 # in cm
distance = distance/10000
bearing = 90
lat2, lon2 = get_point_at_distance(lat, lon, distance, bearing)
lat2 = round(lat2, 4)
lon2 = round(lon2, 4)

print(lat2, lon2)
