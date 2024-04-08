import numpy as np
from sphericalProblem import *
from gradientShoot import *
from kmeans import *

cities_coordinates = []
cities_weights = []
height = 2  # height of the satellites from the center of the sphere
power = 0.05 # power of the satellites
radius = 1 # radius of the sphere
N_satellites = 15
for i in range(30):
    cities_coordinates.append([np.random.uniform(0, 2*np.pi), np.random.uniform(0, np.pi)])
    cities_weights.append(np.random.uniform(0, 1))
cities_coordinates = np.array(cities_coordinates)
cities_weights = np.array(cities_weights)
problem = SphericalProblem(N_satellites, cities_coordinates, cities_weights, height, radius, power)
print(problem)
spherical_kmeans_satellites_repartition(problem)
print(problem)
gradient_descent_satellites_repartition(problem, eps=1e-5, max_iter=100, verbose=True)
print(problem)