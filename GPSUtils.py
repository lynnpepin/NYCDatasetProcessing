''' Utilities related to location stuff.
'''

from math import sin, cos, floor, radians, atan2, sqrt
import numpy as np

origin_longitude        = -74.038971
origin_latitude         =  40.709279
top_left_longitude      = -73.96834326
top_left_latitude       =  40.81703286
bottom_right_longitude  = -73.996317
bottom_right_latitude   =  40.68132125
# Top-right lat/lon 40.78907511 -73.92568926


def gps_to_xy( lon, lat,
                   xbuckets = 1,
                   ybuckets = 1,
                   orlon = origin_longitude,
                   orlat = origin_latitude,
                   tllon = top_left_longitude,
                   tllat = top_left_latitude,
                   brlon = bottom_right_longitude,
                   brlat = bottom_right_latitude,
                   toint = False ):
    ''' gps_to_xy: Given a pair of GPS coordinates representing a
        location and 4 pairs of GPS coordinates defining a grid,
        get the GPS coordinates relative to that grid.
        (See: https://en.wikipedia.org/wiki/Change_of_basis) 
    # Arguments:
        lon, lat: Floating points representing GPS coordinates
        xbuckets, ybuckets: Integers represnting the grid size.
        orlon, orlat, ... brlat: Floating point values representing
            the GPS coordinates of the four corners defining the grid.
        toint: If true, return the x, y coordinates in the grid
            as integers rather than floats
    # Returns:
        x, y coordinates in the grid (as floats, unless toint==True).
            (E.g. gps_to_xy(lon=orlon, lat=orlat) = (0,0))
            (E.g. gps_to_xy(lon=brlon, lat=brlat) = (1,0))
    '''
    origin = np.array((orlon, orlat))
    # Basis vectors and basis matrix
    b1 = np.array([brlon, brlat]) - origin
    b2 = np.array([tllon, tllat]) - origin
    B = np.array([b1, b2])
    # Location in R2
    x = np.array([lon, lat]) - origin
    # Coordinates in terms of basis vectors
    c = np.matmul(x,np.linalg.inv(B))
    
    if not toint:
        return c[0]*xbuckets, c[1]*ybuckets
    return floor(c[0]*xbuckets), floor(c[1]*ybuckets)


# Values for the prebaked function below:
origin_array = np.array([origin_longitude, origin_latitude])
inv_basis = np.array([[ 16.39908019,   4.25489522],
                      [-10.74884902,   6.49152027]])

def pgps_to_xy(lon, lat):
    ''' gps_to_xy, using prebaked values to increase performance.'''
    x = (lon, lat) - origin_array
    c = np.matmul(x, inv_basis)
    return c[0], c[1]


def gps_distance(origin, destination):
    # https://stackoverflow.com/questions/19412462/
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_m : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), -2)
    504200
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (sin(dlat / 2) * sin(dlat / 2) +
         cos(radians(lat1)) * cos(radians(lat2)) *
         sin(dlon / 2) * sin(dlon / 2))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = radius * c
    
    return d*1000
