import numpy as np
from nelder_mead import *

# DATA
r = 6371 # [km] mean radius of Earth
R = r + 35786 # [km] geostationary height
theta = np.deg2rad(5) # Angle of covering of a satellite
cos_theta = np.cos(theta) # cosinus of this angle
max_dist = R*cos_theta - np.sqrt((R**2)*(cos_theta**2) - R**2 + r**2) # maximal distance at which a satellite has an impact

I_ok = (10**((-67-30)/10))*1e4 # Intensity required to satisfy perfectly 10 000 residents
Pt = 50 # Transmission power of a satellite

n_cit = 50 # Number of cities
n_sat = 10 # Number of satellites