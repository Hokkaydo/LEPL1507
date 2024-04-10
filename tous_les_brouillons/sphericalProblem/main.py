import numpy as np
from sphericalProblem import *
from gradientShoot import *
from kmeans import *

height = 35786+6371  # height of the satellites from the center of the sphere
power = 50 # power of the satellites
radius = 6371 # radius of the sphere

N_cities = 30
cities_coordinates = np.vstack((np.random.uniform(0, 2*np.pi, N_cities), np.random.uniform(0, np.pi, N_cities))).T
cities_weights = np.random.uniform(0, 1, N_cities)

N_satellites = 15

problem = SphericalProblem(N_satellites, cities_coordinates, cities_weights, height, radius, power)
print(problem)
spherical_kmeans_satellites_repartition(problem)
print(problem)
gradient_descent_satellites_repartition(problem, eps=1e-10, max_iter=100, verbose=True)
print(problem)