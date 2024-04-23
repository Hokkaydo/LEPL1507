import numpy as np
import math

def spher2cart(X) :
    """
    Args:
        ndarray((n, 3)) containing radius, phi and theta coordinates
    Returns:
        ndarray((n, 3)) containing x, y and z coordinates 
    """
    r, phi, theta = X.T
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return np.array((x, y, z)).T

def gps2cart(X) :
    """
    Args: 
        X: ndarray((n, 3)) containing radius, latitude and longitude coordinates
    Returns
        ndarray((n, 3)) containing x, y and z coordinates
    """
    R, lons, lats = X.T
    
    lons = lons * np.pi/180
    lats = lats * np.pi/180
    
    x = R * np.cos(lats) * np.cos(lons)
    y = R * np.cos(lats) * np.sin(lons)
    z = R * np.sin(lats)
    return np.array([x, y, z]).T

def cart2gps(X):
    """
    Args:
        X: ndarray((n, 3)) containing x, y and z coordinates
    Returns:
        ndarray((n, 3)) containing radius, latitude and longitude coordinates
    """
    x, y, z = X.T
    R = (x**2 + y**2 + z**2)**0.5
    lats = np.arcsin(z / R)*180/np.pi
    lons = np.arctan(y, x)*180/np.pi
    return np.array((R, lats, lons)).T


def cart2spher(X):
    """
    Args:
        X: ndarray((n, 3)) containing, x, y and z coordinates
    Args:
        ndarray((n, 3)) containing radius, phi and theta coordinates
    """
    x, y, z = X.T
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
        elif x[i] < 0 and y[i] < 0: phi.append(np.pi + np.arctan(y[i] / x[i]))
        elif x[i] == 0 and y[i] > 0: phi.append(np.pi / 2)
        elif x[i] == 0 and y[i] < 0: phi.append(3*np.pi / 2)
        else: phi.append(0)
    phi = np.array(phi)    
    return np.array((r, phi, theta)).T

def spher2gps(data):
    """
    Args:
        ndarray((n, 3)) containing phi and theta coordinates 
    Returns:
        ndarray((n, 3)) containing longitudes and latitude coordinates
    """
    return cart2gps(spher2cart(data))
   
def gps2spher(data):
    """
    Args:
        ndarray((n, 2)) containing radius, latitude and longitude coordinates
    Returns:
        ndarray((n, 2)) containing radius, phi and theta coordinates 
    """
    return cart2spher(gps2cart(data))
