from math import sqrt, acos, sin, cos
def polar(x, y, z):
    r = sqrt(x**2 + y**2 + z**2)
    phi = acos(z/r)
    theta = y/abs(y)*x/sqrt(x**2 + y**2)
    return r, phi, theta

def cartesian(r, phi, theta):
    x = r*sin(phi) * cos(theta)
    y = r*sin(phi) * sin(theta)
    z = r*cos(phi)
    return x, y, z
