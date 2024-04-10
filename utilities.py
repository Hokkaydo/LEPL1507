import numpy as np

def spher2cart(X) :
    r, phi, theta = X
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return (x, y, z)

def cart2spher(X) :
    x, y, z = X
    r = (x**2 + y**2 + z**2)**0.5
        
    if z > 0: theta = np.arctan((x**2 + y**2)**0.5 / z)
    elif z < 0: theta = np.pi + np.arctan((x**2 + y**2)**0.5 / z)
    else: theta = np.pi / 2
    
    if x > 0: phi = np.arctan(y / x)
    elif x < 0 and y >= 0: phi = np.pi + np.arctan(y / x)
    elif x < 0 and y < 0: phi = -np.pi + np.arctan(y / x)
    elif x == 0 and y > 0: phi = np.pi / 2
    elif x == 0 and y < 0: phi = -np.pi / 2
    else: phi = 0
    
    return (r, phi, theta)