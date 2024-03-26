import numpy as np
import random as rnd

def spherical_kmeans(cities_coordinates, cities_weights, N_satellites=2, max_iter=15):

    cities_coordinates = cities_coordinates/np.tile(np.linalg.norm(cities_coordinates, axis=1), (3, 1)).T
    
    n = len(cities_coordinates)
    centroids = np.zeros((N_satellites, cities_coordinates.shape[1]))
    for i in range(N_satellites):
        centroids[i] = cities_coordinates[rnd.randrange(n)]
    old_centroids = None
    iteration = 0
    while old_centroids is None or iteration < max_iter:
        old_centroids = centroids
        y = np.argmin(centroids@cities_coordinates.T, axis=0)
        for k in range(N_satellites):
            indexes = [y[i] == k for i in range(n)]
            if True not in indexes:
                centroids[k] = cities_coordinates[rnd.randrange(n)]
                continue
            centroids[k] = np.average(cities_coordinates[indexes], axis=0, weights=cities_weights[indexes])
        iteration+=1
    return centroids
