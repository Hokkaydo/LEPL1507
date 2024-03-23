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

if __name__ == '__main__' :
    assert cart2spher(0, 0, 4)  == (4, np.pi/2, 0)
    assert cart2spher(4, 0, 0)  == (4, 0, np.pi/2)
    assert cart2spher(0, 4, 0)  == (4, np.pi/2, np.pi/2)
    assert cart2spher(0, -4, 0) == (4, 3*np.pi/2, np.pi/2)
    assert cart2spher(-4, 0, 0) == (4, np.pi, np.pi/2)
    assert cart2spher(0, 0, -4) == (4, np.pi/2, np.pi)

    assert spher2cart(3, 0, 0) == (0, 0, 3)
    assert np.linalg.norm(np.array(spher2cart(3, np.pi/2, np.pi/2)) - np.array((0, 3, 0))) < 1e-15