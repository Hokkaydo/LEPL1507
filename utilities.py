import numpy as np

def spher2cart(r, phi, theta) :
    """
    Transform spherical coordinates into cartesian coordinates
    Input :
    - 0 <= r             (float)
    - 0 <= phi   <= 2pi  (float)
    - 0 <= theta <=  pi  (float)

    Output :
    - x = r*sin(theta)*cos(phi)  (float)
    - y = r*sin(theta)*sin(phi)  (float)
    - z = r*cos(theta)           (float)
    """
    return r*np.sin(theta)*np.cos(phi), r*np.sin(theta)*np.sin(phi), r*np.cos(theta)

def cart2spher(x, y, z) :
    """
    Transform cartesian coordinates into spherical coordinates
    Input :
    - x  (float)
    - y  (float)
    - z  (float)

    Output :
    - r     = sqrt(x**2 + y**2 + z**2)  (float)
    - phi   = arctan(y/x) (+ pi if x < 0)
    - theta = arccos(z/r)
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    if x == 0 : phi = np.pi/2 + np.pi * (y < 0)
    else : phi = np.arctan(y/x) + np.pi * (x < 0)
    theta = np.arccos(z/r)
    return r, phi, theta