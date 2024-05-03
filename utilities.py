import numpy as np
import math

def spher2cart(X) :
    """
    Transforme des coordonnées sphériques en coordonnées cartésiennes

    Argument :
        X (ndarray((n, 3))) : Tableau de coordonnées sphériques (rayon, phi, theta)

    Retourne :
        ndarray((n, 3))     : Tableau de coordonnées cartésiennes (x,y,z) correspondant aux mêmes points que ceux de X

    Complexité : O(n) 
    """
    r, phi, theta = X.T
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return np.array((x, y, z)).T

def cart2spher(X):
    """
    Transforme des coordonnées cartésiennes en coordonnées sphériques

    Arguments :
        X (ndarray((n, 3))) : Tableau de coordonnées cartésiennes (x,y,z)

    Retourne :
        ndarray((n, 3))     : Tableay de coordonnées sphériques (rayon, phi, theta) correspondant aux mêmes points que ceux de X
    
    Complexité : O(n)
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

def gps2cart(X) :
    """
    Transforme des coordonnées géographiques en coordonnées cartésiennes

    Arguments : 
        X (ndarray((n, 3))) : Tableau de coordonnées géographiques (rayon, lat, long)

    Retourne :
        ndarray((n, 3))     : Tableau de coordonnées cartésiennes (x,y,z) correspondant aux mêmes points que ceux de X
    
    Complexité : O(n)
    """
    R, lats, lons = X.T
    
    lats = np.deg2rad(lats)
    lons = np.deg2rad(lons)
    
    x = R * np.cos(lats) * np.cos(lons)
    y = R * np.cos(lats) * np.sin(lons)
    z = R * np.sin(lats)
    return np.array([x, y, z]).T

def cart2gps(X):
    """
    Transforme des coordonnées cartésiennes et coordonnées géographiques

    Arguments : 
        X (ndarray((n, 3))) : Tableau de coordonnées cartésiennes (x,y,z)

    Retourne :
        ndarray((n, 3))     : Tableau de coordonnées géographiques (rayon, lat, long) correspondant aux mêmes points que ceux de X
    
    Complexité : O(n)
    """
    x, y, z = X.T
    R = (x**2 + y**2 + z**2)**0.5
    lats = np.arcsin(z / R)*180/np.pi
    lons = np.arctan2(y, x)*180/np.pi
    return np.array((R, lats, lons)).T


def spher2gps(X):
    """
    Transforme des coordonnées sphériques en coordonnées géographiques

    Arguments : 
        X (ndarray((n, 3))) : Tableau de coordonnées sphériques (rayon, phi, theta) 

    Retourne :
        ndarray((n, 3))     : Tableau de coordonnées géographiques (rayon, lat, long) correspondant aux mêmes points que ceux de X
    
    Complexité : O(n)
    """
    return cart2gps(spher2cart(X))
   
def gps2spher(X):
    """
    Transforme des coordonnées géographiques en coordonnées sphériques

    Arguments : 
        X (ndarray((n, 3))) : Tableau de coordonnées géographiques (rayon, lat, long) 

    Retourne :
        ndarray((n, 3))     : Tableau de coordonnées sphériques (rayon, phi, theta) correspondant aux mêmes points que ceux de X
    
    Complexité : O(n)
    """
    return cart2spher(gps2cart(X))
