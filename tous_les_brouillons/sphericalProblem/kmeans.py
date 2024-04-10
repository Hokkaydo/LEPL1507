import numpy as np

def spherical_kmeans_satellites_repartition(problem, max_iter=300):
    for i in range(len(problem.cities_coordinates)):
        problem.cities_coordinates[i] /= np.linalg.norm(problem.cities_coordinates[i])
    
    n = len(problem.cities_coordinates)
    centroids = np.zeros((problem.N_satellites, problem.cities_coordinates.shape[1]))
    for i in range(problem.N_satellites):
        centroids[i] = problem.cities_coordinates[np.random.randint(n)]
    old_centroids = None
    iteration = 0
    while old_centroids is None or iteration < max_iter:
        old_centroids = centroids
        y = np.argmin(centroids@problem.cities_coordinates.T, axis=0)
        for k in range(problem.N_satellites):
            Xk = problem.cities_coordinates[[y[i] == k for i in range(n)]]
            s = np.sum(Xk, axis=0)
            
            norm = np.linalg.norm(s)
            if len(s) == 0 or norm == 0:
                centroids[k] = problem.cities_coordinates[np.random.randint(n)]
                continue
            centroids[k] = s/norm
        iteration+=1
    problem.satellites_position = centroids
    problem.method = "kmeans"