from satellites_problem import *
from math import floor

class Kmeans :
    """
    ...

    Attributs :
        problem  (SatellitesProblem) : problème sur lequel va être réalisé l'algorithme de Kmeans.
        max_iter (int)               : nombre d'itérations maximal qui vont être réalisées dans l'algorithme de Kmeans
    
    Méthodes :
        solve
    """

    def __init__(self, problem:SatellitesProblem, max_iter = 300) :
        self.problem = problem
        self.max_iter = max_iter
    
    def __kmeans2D(self) :
        n = self.problem.N_satellites

        cities_coordinates = self.problem.cities_coordinates
        weights = self.problem.cities_weights
        
        centroids = np.zeros((self.problem.N_satellites, 2))
        for i in range(self.problem.N_satellites):
            centroids[i] = cities_coordinates[i%len(cities_coordinates)]

        iteration = 0
        prev_centroids = None
        while prev_centroids is None or (iteration < self.max_iter and not np.allclose(prev_centroids, centroids)):
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
                     
        self.problem.sat_coordinates = centroids
        return iteration
    
    def __kmeans3D(self) :
        ### ATTENTION DEFINIR UNE VALEUR  de seuil###
        
        cities_coordinates = gps2cart(self.problem.cities_coordinates)

        for i in range(len(cities_coordinates)):
            cities_coordinates[i] /= np.linalg.norm(cities_coordinates[i])
        
        n = len(cities_coordinates)
        centroids = np.zeros((self.problem.N_satellites, 3))
        for i in range(self.problem.N_satellites):
            centroids[i] = cities_coordinates[i%len(cities_coordinates)]

        old_centroids = None
        iteration = 0
        while old_centroids is None or (iteration < self.max_iter and not np.allclose(old_centroids, centroids)):
            old_centroids = centroids
            clusters = [[] for _ in range(self.problem.N_satellites)]
            
            for i in range(n):
                nearest_clusters = np.argsort(cities_coordinates[i]@centroids.T, axis=0)        
                j = 0
                while j < self.problem.N_satellites and np.linalg.norm(cities_coordinates[i] - centroids[nearest_clusters[j]]) > 8300.65:
                    j+=1
                if j == self.problem.N_satellites:
                    print("Warning: A city is not covered by any satellite.")
                    continue

                clusters[nearest_clusters[j]].append(i)
                
            for k in range(self.problem.N_satellites):
                if len(clusters[k]) == 0: 
                    centroids[k] = cities_coordinates[np.random.randint(n)]
                    continue
                spherical_coords = cart2gps(cities_coordinates[clusters[k]]*self.problem.H)
                gps_centroid = np.average(spherical_coords, axis=0, weights=self.problem.cities_weights[clusters[k]])
                centroids[k] = gps2cart(gps_centroid)/self.problem.H

            iteration+=1
        self.problem.sat_coordinates = cart2gps(centroids*self.problem.H)
        print(self.problem.sat_coordinates)
        return iteration
    
    def solve(self, verbose = False) :
        if verbose :
            print("Lancement de l'algorithme de Kmeans.")
        if   self.problem.dimension == 2 : self.__kmeans2D()
        elif self.problem.dimension == 3 : iteration = self.__kmeans3D()
        self.problem.value = self.problem.cost()
        if verbose :
            print("Fin de l'algorithme.")
            if iteration == self.max_iter : print("Le nombre d'itérations maximal a été atteint.")
            else                          : print("L'algorithme s'est déroulé avec succès.")
            new_cost = self.problem.value
            print(f"La puissance totale reçue est de {new_cost * 1e6 :.2f}µW. La couverture est de {self.problem.coverage() * 100 :.2f}%.\n")
