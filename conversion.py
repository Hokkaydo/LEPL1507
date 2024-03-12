from numpy import arcsin, pi, sign, sqrt, arccos, sin, cos

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
    phi = arcsin(z/r)
    theta = arccos(x/(cos(phi)*r))
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
