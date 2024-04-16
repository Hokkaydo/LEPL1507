import numpy as np
import math

def spher2cart(X) :
    r, phi, theta = X
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return (x, y, z)

def gps2cart(X) :
    r, longs, lats = X
    x_coords = []; y_coords = []; z_coords = []
    for lat, long in zip(lats, longs):
        lat_rad = math.radians(lat)
        lon_rad = math.radians(long)
        x = math.sin(lon_rad) * math.cos(lat_rad)*r
        y = math.sin(lon_rad) * math.sin(lat_rad)*r
        z = math.cos(lon_rad)*r
        x_coords.append(x) ; y_coords.append(y) ; z_coords.append(z)
    return x_coords, y_coords, z_coords


def cart2spher(X) :
    x, y, z = X
    r = (x**2 + y**2 + z**2)**0.5
        
    theta = []
    
    for i in range(len(r)):
        if z[i] > 0: theta.append(np.arctan((x[i]**2 + y[i]**2)**0.5 / z[i]))
        elif z[i] < 0: theta.append(np.pi + np.arctan((x[i]**2 + y[i]**2)**0.5 / z[i]))
        else: theta.append(np.pi / 2)
    theta = np.array(theta)
    
    phi = []
    
    for i in range(len(r)):
        if x[i] > 0: phi.append(np.arctan(y[i] / x[i]))
        elif x[i] < 0 and y[i] >= 0: phi.append(np.pi + np.arctan(y[i] / x[i]))
        elif x[i] < 0 and y[i] < 0: phi.append(-np.pi + np.arctan(y[i] / x[i]))
        elif x[i] == 0 and y[i] > 0: phi.append(np.pi / 2)
        elif x[i] == 0 and y[i] < 0: phi.append(-np.pi / 2)
        else: phi.append(0)
    phi = np.array(phi)    
    return np.array((r, phi, theta))

def spherical_to_lat_long(data):
    print(data, "to spherical", data * 180/np.pi)
    return data * 180/np.pi

def lat_long_to_spherical(data):
    print(data, "to long/lat", data/180*np.pi)
    return data/180 * np.pi