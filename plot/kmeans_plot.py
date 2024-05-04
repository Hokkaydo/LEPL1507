import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter as clock

def kmeans_iteration(N_satellites, cities_coordinates, weights, max_iter = 300) :
        ### ATTENTION DEFINIR UNE VALEUR  de seuil###
        
        for i in range(len(cities_coordinates)):
            cities_coordinates[i] /= np.linalg.norm(cities_coordinates[i])
        
        n = len(cities_coordinates)
        centroids = np.zeros((N_satellites, 3))
        for i in range(N_satellites):
            centroids[i] = cities_coordinates[i%len(cities_coordinates)]

        clusters = [[] for _ in range(N_satellites)]
            
        for i in range(n):
            distances = np.array([np.linalg.norm(centroids[j] - cities_coordinates[i]) for j in range(N_satellites)])
            nearest_clusters = np.argsort(distances)
            clusters[nearest_clusters[0]].append(i)
                
        for k in range(N_satellites):
            if len(clusters[k]) == 0: 
                centroids[k] = cities_coordinates[np.random.randint(n)]
                continue
                
            centroids[k] = np.average(cities_coordinates[clusters[k]], axis=0, weights=weights[clusters[k]])

    
    

def test_N_fixed(N, iterations, average_iteration):
    results1 = np.zeros((iterations + 1, 2))
    for i in range(1, iterations + 1):
        time = 0
        for _ in range(average_iteration):
            n = i*50
            cities_coordinates = np.random.rand(n, 3)*20
            weights = np.random.rand(n)
            s = clock()
            kmeans_iteration(N, cities_coordinates, weights)
            time += clock() - s
            print(f"{_}/{average_iteration} | {i}")
        results1[i, :] = [n, time/average_iteration]
        print(i)
    return results1

def test_n_fixed(n, iterations, average_iteration):
    results2 = np.zeros((iterations + 1, 2))
    for i in range(1, iterations + 1):
        time = 0
        for _ in range(average_iteration):
            N = 10*i
            cities_coordinates = np.random.rand(n, 3)*20
            weights = np.random.rand(n)
            s = clock()
            kmeans_iteration(N, cities_coordinates, weights)
            time += clock() - s
            print(f"{_}/{average_iteration} | {i}")
        results2[i, :] = [N, time/average_iteration]
        print(i)
    return results2

    
iterations = 50
average_iteration = 10

results1 = test_N_fixed(50, iterations, average_iteration)
results2 = test_n_fixed(1000, iterations, average_iteration)
    

plt.plot(results1[1:, 0], results1[1:, 1], label = r"$N = 50$")
plt.plot(results1[1:, 0], 5e-3*results1[1:, 0], label = r"O(n)")
plt.title("Temps d'exécution de l'algorithme K-means \npour un nombre de clusters fixes et un nombre de points variable")
plt.xlabel("Nombre de points")
plt.ylabel("Temps d'exécution (s)")
plt.legend()
plt.savefig("kmeans_plot_N_50.png")

plt.clf()

plt.plot(results2[:, 0], results2[:, 1], label = r"$n = 1000$")
plt.plot(results2[:, 0], 2e-3*results2[:, 0], label = r"O(n)")
plt.title("Temps d'exécution de l'algorithme K-means \npour un nombre de points fixes et un nombre de clusters variable")
plt.xlabel("Nombre de clusters")
plt.ylabel("Temps d'exécution (s)")
plt.legend()
plt.savefig("kmeans_plot_n_1000.png")