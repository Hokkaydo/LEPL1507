import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter as clock

def kmeans2D(n, cities_coordinates, weights, max_iter = 300) :
        centroids = np.zeros((n, 2))
        for i in range(n):
            centroids[i] = cities_coordinates[i%len(cities_coordinates)]

        iteration = 0
        prev_centroids = None
        while prev_centroids is None or (iteration < max_iter and not np.allclose(prev_centroids, centroids)):
            classif = {i:{} for i in range(n)}
            for i in range(len(cities_coordinates)):
                dist = [np.linalg.norm(cities_coordinates[i] - c) for c in centroids]

                closest_cluster = dist.index(min(dist))
                classif[closest_cluster][i] = cities_coordinates[i]
                
            prev_centroids = centroids.copy()
            for cluster in range(len(classif)):
                if len(classif[cluster]) == 0:
                    centroids[cluster] = cities_coordinates[np.random.randint(0, n)]
                else:
                    indexes = [i for i in classif[cluster].keys()]
                    centroids[cluster] = np.average(cities_coordinates[indexes], axis=0, weights=weights[indexes])
            iteration += 1
        return iteration
    

def test_N_fixed(N, iterations):
    results1 = np.zeros((iterations + 1, 2))
    for i in range(1, iterations + 1):
        n = i*50
        cities_coordinates = np.random.rand(n, 2)*20
        weights = np.random.rand(n)
        s = clock()
        kmeans2D(N, cities_coordinates, weights)
        results1[i, :] = [n, clock() - s]
        print(i)
    return results1

def test_n_fixed(n, iterations):
    results2 = np.zeros((iterations + 1, 2))
    for i in range(1, iterations + 1):
        N = 10*i
        cities_coordinates = np.random.rand(n, 2)*20
        weights = np.random.rand(n)
        s = clock()
        kmeans2D(N, cities_coordinates, weights)
        results2[i, :] = [N, clock() - s]
        print(i)
    return results2

    
iterations = 100
# results1 = test_N_fixed(50, iterations)
results2 = test_n_fixed(1000, iterations)
    

# plt.plot(results1[1:, 0], results1[1:, 1], label = r"$N = 50$")
# plt.plot(results1[1:, 0], 5e-3*results1[1:, 0], label = r"O(n)")
# plt.title("Temps d'exécution de l'algorithme K-means \npour un nombre de clusters fixes et un nombre de points variable")
# plt.xlabel("Nombre de points")
# plt.ylabel("Temps d'exécution (s)")
# plt.legend()
# plt.savefig("kmeans_plot_N_50.png")

# plt.clf()

plt.plot(results2[:, 0], results2[:, 1], label = r"$n = 1000$")
plt.plot(results2[:, 0], 1e-2*results2[:, 0], label = r"O(n)")
plt.title("Temps d'exécution de l'algorithme K-means \npour un nombre de points fixes et un nombre de clusters variable")
plt.xlabel("Nombre de clusters")
plt.ylabel("Temps d'exécution (s)")
plt.legend()
plt.savefig("kmeans_plot_n_1000.png")