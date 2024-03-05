from math  import sqrt, acos, atan, sin, cos
from numpy import pi, sign

def polar(x, y, z) :
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
    r = sqrt(x**2 + y**2 + z**2)
    phi = acos(z/r)
    theta = acos(x/sqrt(x**2 + y**2))
    theta = acos(x/sqrt(x**2 + y**2)) + pi*(1 - sign(x))/2
    return r, phi, theta

def cartesian(r, phi, theta) :
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
    x = r*sin(phi) * cos(theta)
    y = r*sin(phi) * sin(theta)
    z = r*cos(phi)
    return x, y, z
