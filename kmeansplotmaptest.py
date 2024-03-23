import plot_map
from spherical_kmeans import *
import numpy as np
from utilities import *
import plotly.graph_objects as go
from plotly.offline import plot

n_cities = 6
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
satellites_cart = spherical_kmeans(cities, [], n_sat)*r

def spherical_to_lat_long(data):
    return 180/np.pi * data

satellites_polar = np.array(cart2spher(*satellites_cart.T))[1:]
cities_polar = np.array(cart2spher(*cities.T))[1:]

satellites_lat, satellites_long = spherical_to_lat_long(satellites_polar)
cities_lat, cities_long = spherical_to_lat_long(cities_polar)

plot_map.create_fig()
plot_map.plot_cities(cities_long, cities_lat)
print("sat polar\n", satellites_polar)
print("sat cart\n", satellites_cart)
print("cities polar\n", cities_polar)
print("cities cart\n", cities)
plot_map.plot_satellite(satellites_polar[0], satellites_polar[1], 2000)
#plot_map.plot_fig()

t = go.Figure()

t.add_trace(go.Scatter3d(x=satellites_cart.T[0], y=satellites_cart.T[1],z=satellites_cart.T[2], mode="markers", line=dict(color="blue")))
t.add_trace(go.Scatter3d(x=cities.T[0], y=cities.T[1], z=cities.T[2], mode="markers", line=dict(color="red")))

print("Rad sats", np.linalg.norm(satellites_cart, axis=1))
print("Rad cities", np.linalg.norm(cities, axis=1))
t.update_layout(
        scene = dict (
        xaxis = dict(nticks=4, range=[-6371, 6371],),
        yaxis = dict(nticks=4, range=[-6371, 6371],),
        zaxis = dict(nticks=4, range=[-6371, 6371],),
        )
    )
plot(t)

import time
time.sleep(10)
plot_map.plot_fig()
