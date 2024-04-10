import numpy as np

def spher2cart(r, phi, theta) :
    """
    Transform spherical coordinates into cartesian coordinates
    Input :
    - 0 <= r             (numpy array of float)
    - 0 <= phi   <= 2pi  (numpy array of float)
    - 0 <= theta <=  pi  (numpy array of float)

    Output :
    - x = r*sin(theta)*cos(phi)  (numpy array of float)
    - y = r*sin(theta)*sin(phi)  (numpy array of float)
    - z = r*cos(theta)           (numpy array of float)
    """
    return r*np.sin(theta)*np.cos(phi), r*np.sin(theta)*np.sin(phi), r*np.cos(theta)

def cart2spher(x, y, z) :
    """
    Transform cartesian coordinates into spherical coordinates
    Input :
    - x  (numpy array of float)
    - y  (numpy array of float)
    - z  (numpy array of float)

    Output :
    - r     = sqrt(x**2 + y**2 + z**2)     (numpy array of float)
    - phi   = arctan(y/x) (+ pi if x < 0)  (numpy array of float)
    - theta = arccos(z/r)                  (numpy array of float)
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    phi = np.array([np.pi/2 + np.pi * (y[i] < 0) if x[i] == 0 else np.arctan(y[i]/x[i]) + np.pi * (x[i] < 0) for i in range(len(x))])
    theta = np.arccos(z/r)
    return r, phi, theta

if __name__ == '__main__' :
    r, phi, theta = cart2spher(np.array([0, 4, 0, 0, -4, 0]), np.array([0, 0, 4, -4, 0, 0]), np.array([4, 0, 0, 0, 0, -4]))
    R, PHI, THETA = np.array([4, 4, 4, 4, 4, 4]), np.array([np.pi/2, 0, np.pi/2, 3*np.pi/2, np.pi, np.pi/2]), np.array([0, np.pi/2, np.pi/2, np.pi/2, np.pi/2, np.pi])
    for i in range (len(r)) :
        assert abs(r[i] - R[i]) < 1e-15
        assert abs(phi[i] - PHI[i]) < 1e-15
        assert abs(theta[i] - THETA[i]) < 1e-15

    x, y, z = spher2cart(np.array([3, 3]), np.array([0, np.pi/2]), np.array([0, np.pi/2]))
    X, Y, Z = np.array([0, 0]), np.array([0, 3]), np.array([3, 0])
    for i in range (len(x)) :
        assert abs(x[i] - X[i]) < 1e-15
        assert abs(y[i] - Y[i]) < 1e-15
        assert abs(z[i] - Z[i]) < 1e-15