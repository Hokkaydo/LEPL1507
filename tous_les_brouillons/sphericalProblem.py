import numpy as np
import matplotlib.pyplot as plt
from plot_map import *





class SphericalProblem:
    """Class to represent the problem of finding the best position for N satellites
        in a 3D space to cover a set of cities with different weights.

        Attributes:
        N_satellites (int): The number of satellites to position.
        cities_coordinates (list): A list of spherical coordinates for each city.
        cities_weights (list): A list of weights for each city.
        height (float): The height of the satellites from the center of the sphere.
        radius (float): The radius of the sphere.
        satellites_position (list): A list of spherical coordinates for each satellite.
        power (float): The power of the satellites.

        Methods:
        __init__(self, N_satellites, cities_coordinates, cities_weights, height, radius, power): Constructor for the class.
    """
    def __init__(self, N_satellites, cities_coordinates, cities_weights, height, radius, power):
        self.N_satellites = N_satellites
        self.cities_coordinates = cities_coordinates
        self.cities_weights = cities_weights
        self.height = height
        self.radius = radius
        self.power = power
        self.method = None
        self.satellites_position = np.zeros((N_satellites, 2))
        self.max_distance = (self.radius**2 + self.height**2)**0.5

    def spherical_to_cartesian(self, r, phi, theta):
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        return x, y, z
    
    def cartesian_to_spherical(self, x, y, z):
        r = (x**2 + y**2 + z**2)**0.5
        if z > 0:
            theta = np.arctan((x**2 + y**2)**0.5 / z)
        elif z < 0:
            theta = np.pi + np.arctan((x**2 + y**2)**0.5 / z)
        else:
            theta = np.pi / 2
        if x > 0:
            phi = np.arctan(y / x)
        elif x < 0 and y >= 0:
            phi = np.pi + np.arctan(y / x)
        elif x < 0 and y < 0:
            phi = -np.pi + np.arctan(y / x)
        elif x == 0 and y > 0:
            phi = np.pi / 2
        elif x == 0 and y < 0:
            phi = -np.pi / 2
        else:
            phi = 0
        return r, phi, theta
    
    def distance(self, city_position, satellite_position):
        x1, y1, z1 = self.spherical_to_cartesian(self.radius, city_position[0], city_position[1])
        x2, y2, z2 = self.spherical_to_cartesian(self.height, satellite_position[0], satellite_position[1])
        distance = ((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)**0.5
        if distance > self.max_distance:
            return float('inf')
        else:
            return distance
        
    def city_received_power(self, city_position, city_weight):
        p = 0
        for i in range(self.N_satellites):
            p += self.power / self.distance(city_position, self.satellites_position[i])**2
        return min(city_weight, p)
    
    def total_received_power(self):
        power = 0
        for i in range(len(self.cities_coordinates)):
            power += self.city_received_power(self.cities_coordinates[i], self.cities_weights[i])
        return power
    
    def coverage(self):
        return self.total_received_power() / np.sum(self.cities_weights)
    
    def __str__(self):
        if self.method:
            return "Problem with {} satellites, {} cities, a power of {}, a height of {} and a radius of {}.\nSolved with {} method. The total received power is {}, the coverage is {}.\n".format(self.N_satellites, len(self.cities_coordinates), self.power, self.height, self.radius, self.method, self.total_received_power(), self.coverage())
        else:
            return "Problem with {} satellites, {} cities, a power of {} and a height of {} and a radius of {}.\nNot solved yet. The total received power is {}, the coverage is {}.\n".format(self.N_satellites, len(self.cities_coordinates), self.power, self.height, self.radius, self.total_received_power(), self.coverage())

    def plot(self):
        latitudes = []
        longitudes = []
        pol = []
        azi = []
        for i in range(len(self.cities_coordinates)):
            latitudes.append(self.cities_coordinates[i][1]*180/np.pi)
            longitudes.append(self.cities_coordinates[i][0]*180/np.pi)
        for i in range(self.N_satellites):
            pol.append(self.satellites_position[i][1])
            azi.append(self.satellites_position[i][0])
        create_fig()
        plot_satellite(pol, azi, 0.1)
        plot_cities(longitudes, latitudes)
        plot_fig()

def stupid_spherical_satellites_repartition(problem):    
    """A stupid algorithm to solve the problem of finding the best position for N satellites"""
    for i in range(problem.N_satellites):
        problem.satellites_position[i] = [np.random.uniform(0, 2*np.pi), np.random.uniform(0, np.pi)]
    problem.method = "stupid"
    return problem

# Example of use
cities_coordinates = []
cities_weights = []
height = 2
power = 0.01
radius = 1
N_satellites = 3
for i in range(10):
    cities_coordinates.append([np.random.uniform(0, 2*np.pi), np.random.uniform(0, np.pi)])
    cities_weights.append(np.random.uniform(0, 1))
problem = SphericalProblem(N_satellites, cities_coordinates, cities_weights, height, radius, power)
print(problem)
stupid_spherical_satellites_repartition(problem)
print(problem)
problem.plot()





        



