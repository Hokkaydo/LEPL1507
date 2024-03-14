import numpy as np

def spher2cart(r, phi, theta) :
    """
    Transform spherical coordinates into cartesian coordinates
    Input :
    - 0 <= r             (float)
    - 0 <= phi   <= pi   (float)
    - 0 <= theta <= 2pi  (float)

    Output :
    - x = r*sin(phi)*cos(theta)  (float)
    - y = r*sin(phi)*sin(theta)  (float)
    - z = r*cos(phi)             (float)
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
    - phi   = arccos(z/r)
    - theta = 
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    return r, np.arccos(z/r), np.arctan(y/x)

