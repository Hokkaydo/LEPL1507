
import numpy as np
import matplotlib.pyplot as plt
from math import *
from scipy.optimize import *
import random as rnd

"""A package to make a comparison between different algorithms to solve the problem of finding the best position for N satellites
in a 2D space and in a spherical space to cover a set of cities with different weights.
"""

class EuclidianProblem:
    """Class to represent the problem of finding the best position for N satellites
      in a 2D space to cover a set of cities with different weights.
      
      Attributes:
      N_satellites (int): The number of satellites to position.
      cities_coordinates (list): A list of 2D coordinates for each city. 
      cities_weights (list): A list of weights for each city.
      height (float): The height of the satellites.
      satellites_position (list): A list of 2D coordinates for each satellite.
      
      Methods:
      __init__(self, N_satellites, cities_coordinates, cities_weights, height): Constructor for the class.
    """
    def __init__(self,  N_satellites, cities_coordinates, cities_weights, height, power):
        self.N_satellites = N_satellites
        self.cities_coordinates = cities_coordinates
        self.cities_weights = cities_weights
        self.height = height
        self.power = power
        self.width = 1
        self.length = 1
        self.method = None
        self.satellites_position = np.zeros((N_satellites, 2))

    def distance(self, city_position, satellite_position):
        squared_ground_distance = (city_position[0] - satellite_position[0])**2 + (city_position[1] - satellite_position[1])**2
        return (squared_ground_distance + self.height**2)**0.5
    
    def received_power(self, distance):
        return self.power / distance**2
    
    def city_received_power(self, city_position, city_weight):
        p = 0
        for i in range(self.N_satellites):
            p += self.received_power(self.distance(city_position, self.satellites_position[i]))
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
            return "Problem with {} satellites, {} cities, a power of {} and a height of {}.\nSolved with {} method. The total received power is {}, the coverage is {}.\n".format(self.N_satellites, len(self.cities_coordinates), self.power, self.height, self.method, self.total_received_power(), self.coverage())
        else:
            return "Problem with {} satellites, {} cities, a power of {} and a height of {}.\nNot solved yet. The total received power is {}, the coverage is {}.\n".format(self.N_satellites, len(self.cities_coordinates), self.power, self.height, self.total_received_power(), self.coverage())
    
    def plot(self):
        plt.scatter(self.cities_coordinates[:, 0], self.cities_coordinates[:, 1], s=self.cities_weights*100)
        plt.scatter(self.satellites_position[:, 0], self.satellites_position[:, 1], c='r')
        plt.show()



def stupid_euclidean_satellites_repartition(problem):
    """A stupid algorithm to solve the problem of finding the best position for N satellites"""
    for i in range(problem.N_satellites):
        problem.satellites_position[i] = [np.random.uniform(0, 1), np.random.uniform(0, 1)]
    problem.method = "stupid"

def kmeans_euclidean_satellites_repartition(problem):
    """A kmeans algorithm to solve the problem of finding the best position for N satellites"""
    def KMeans(data, weights, n=2, tol=0.001, max_iter=300):
        centroids = np.zeros((n, 2))
        
        for j in range(n):
            centroids[j] = np.array(data[floor(rnd.random()*len(data))])

        for _ in range(max_iter):
            classif = {i:{} for i in range(n)}

            for i in range(len(data)):
                dist = [np.linalg.norm(data[i] - c) for c in centroids]

                closest_cluster = dist.index(min(dist))
                classif[closest_cluster][i] = data[i]
                
            prev_centroids = centroids.copy()
            for cluster in range(len(classif)):
                if len(classif[cluster]) == 0:
                    centroids[cluster] = data[np.random.randint(0, n)]
                else:
                    indexes = [i for i in classif[cluster].keys()]
                    centroids[cluster] = np.average(data[indexes], axis=0, weights=weights[indexes])
            
            optimized = True
            
            for c in range(len(centroids)):
                old_c = prev_centroids[c]
                new_c = centroids[c]
                if np.sum(new_c - old_c) > tol:
                    optimized = False
            if optimized:
                break            
        return centroids
    centroids = KMeans(problem.cities_coordinates, problem.cities_weights, n=problem.N_satellites)
    problem.satellites_position = centroids
    problem.method = "kmeans"



# Example of use
cities_coordinates = np.random.rand(10, 2)
cities_weights = np.random.rand(10)
height = 0.01
power = 0.01
N_satellites = 2
problem1 = EuclidianProblem(N_satellites, cities_coordinates, cities_weights, height, power)
print(problem1)
problem1.plot()
stupid_euclidean_satellites_repartition(problem1)
print(problem1)
problem1.plot()
kmeans_euclidean_satellites_repartition(problem1)
print(problem1)
problem1.plot()

sumStupid = 0
sumKmeans = 0
for i in range(2):
    sumStupid = 0
    sumKmeans = 0
    for j in range(10):
        cities_coordinates = np.random.rand(10, 2)
        cities_weights = np.random.rand(10)
        height = 0.01
        power = 0.01
        problem1 = EuclidianProblem(i, cities_coordinates, cities_weights, height, power)
        stupid_euclidean_satellites_repartition(problem1)
        sumStupid += problem1.coverage()
        kmeans_euclidean_satellites_repartition(problem1)
        sumKmeans += problem1.coverage()
    print("N = ", i, "Stupid: ", sumStupid/10, "Kmeans: ", sumKmeans/10) 


    

