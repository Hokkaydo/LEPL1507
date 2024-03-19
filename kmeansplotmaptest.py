import plot_map
from spherical_kmeans import *
import numpy as np
from utilities import *


n_cities = 5
n_sat = 5

r = 6371

# Initialization of cities
cities = []
for i in range (n_cities) :
    phi = np.random.rand() * 2*np.pi
    theta = np.random.rand() * np.pi
    #cities.append((phi, theta))
    cities.append([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])
cities = r * np.array(cities)
cities_weights = np.random.randint(1, 100, n_cities)

# shape (n, 3)
satellites_cart = spherical_kmeans(cities, [], n_sat)

def spherical_to_lat_long(data):
    return 180/np.pi * data

satellites_polar = np.array(cart2spher(*satellites_cart.T))[1:]
cities_polar = np.array(cart2spher(*cities.T))[1:]

satellites_lat, satellites_long = spherical_to_lat_long(satellites_polar)
cities_lat, cities_long = spherical_to_lat_long(cities_polar)

plot_map.create_fig()
plot_map.plot_cities(cities_long, cities_lat)
plot_map.plot_satellite(satellites_polar[1], satellites_cart[0], 2000)
plot_map.plot_fig()
