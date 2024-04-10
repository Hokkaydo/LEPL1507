import numpy as np
from sphericalProblem import *
import matplotlib.pyplot as plt
from gradientConstant import *

cities_coordinates = []
cities_weights = []
height = 2
power = 0.2
radius = 1
N_satellites = 1
cities_coordinates.append([0, np.pi/2])
satellites_position = np.array([[np.pi/16, np.pi/2]])
cities_weights.append(1)

problem = SphericalProblem(N_satellites, cities_coordinates, cities_weights, height, radius, power)
problem.satellites_position = satellites_position
print(problem)
gradient_descent_satellites_repartition(problem, alpha=1e-4, eps=1e-3, max_iter=100000)
print(problem)
print(problem.satellites_position)