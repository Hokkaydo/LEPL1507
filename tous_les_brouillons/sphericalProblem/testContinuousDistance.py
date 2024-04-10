import numpy as np
from sphericalProblem import *
import matplotlib.pyplot as plt

cities_coordinates = []
cities_weights = []
height = 2
power = 0.2
radius = 1
N_satellites = 1
cities_coordinates.append([0, np.pi/2])
cities_weights.append(1)

cities_coordinates = np.array(cities_coordinates)
cities_weights = np.array(cities_weights)
problem = SphericalProblem(N_satellites, cities_coordinates, cities_weights, height, radius, power)

n = 10000
d = np.zeros(n)
d_continuous = np.zeros(n)
phi = np.linspace(0, 2*np.pi, n)
for i in range(n):
    d[i] = problem.distance([0, np.pi/2], [phi[i], np.pi/2])
    d_continuous[i] = problem.continuous_distance([0, np.pi/2], [phi[i], np.pi/2])
print(problem.max_distance)
plt.plot(phi, d_continuous)
plt.xlabel("phi")
plt.ylabel("continuous distance")
plt.show()

plt.plot(phi, d)
plt.show()

plt.plot(phi, d_continuous)
plt.show()
          