import plot_map
import kmeans
import numpy as np
import conversion


n_cities = 50
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
satellites_cart = kmeans.spherical_kmeans(cities, [], n_sat)

def spherical_to_lat_long(data):
    return 180/np.pi * r * data

satellites_polar = np.array(conversion.polar(*satellites_cart.T))[1:]
cities_polar = np.array(conversion.polar(*cities.T))[1:]

satellites_lat, satellites_long = spherical_to_lat_long(satellites_polar)
cities_lat, cities_long = spherical_to_lat_long(cities_polar)

plot_map.plot_cities(cities_long, cities_lat)
print(satellites_lat, satellites_long)
plot_map.plot_satellite(satellites_lat, satellites_long, 2000)
plot_map.plot_fig()
