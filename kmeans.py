from satellites_problem import *

class Kmeans :
    """
    ...

    Attributs :
        problem  (SatellitesProblem) : problème sur lequel va être réalisé l'algorithme de Kmeans.
        max_iter (int)               : nombre d'itérations maximal qui vont être réalisées dans l'algorithme de Kmeans
    
    Méthodes :
        solve
    """

    def __init__(self, problem, max_iter = 300) :
        self.problem = problem
        self.max_iter = max_iter
    
    def __kmeans2D(self) :
        ...
    
    def __kmeans3D(self) :
        ### ATTENTION DEFINIR UNE VALEUR  de seuil###
        threshold = 1.0  # Définir la valeur de seuil = distance entre un kluster interdit et un centroid
        
        for i in range(len(self.problem.cities_coordinates)):
            self.problem.cities_coordinates[i] /= np.linalg.norm(self.problem.cities_coordinates[i])
        
        n = len(self.problem.cities_coordinates)
        centroids = np.zeros((self.problem.N_satellites, 2))
        for i in range(self.problem.N_satellites):
            centroids[i] = self.problem.cities_coordinates[np.random.randint(n)]
        
        # Vérifier si les positions des satellites générées sont trop proche des villes interdites
        for i in range(self.problem.N_satellites):
            for forbidden_city in self.problem.forbidden_cities:
                distance = np.linalg.norm(centroids[i] - forbidden_city)
                if distance < threshold:
                    # Choisir une autre position aléatoire pour ce satellite
                    valid_position_found = False
                    while not valid_position_found:
                        new_position = np.random.choice(self.problem.cities_coordinates)
                        if tuple(new_position) not in self.problem.forbidden_cities:
                            centroids[i] = new_position
                            valid_position_found = True
                        centroids[i] = self.problem.cities_coordinates[np.random.randint(n)]

        old_centroids = None
        iteration = 0
        while old_centroids is None or iteration < self.max_iter:
            old_centroids = centroids
            y = np.argmin(centroids@self.problem.cities_coordinates.T, axis=0)
            for k in range(self.problem.N_satellites):
                Xk = self.problem.cities_coordinates[[y[i] == k for i in range(n)]]
                s = np.sum(Xk, axis=0)
                
                norm = np.linalg.norm(s)
                if len(s) == 0 or norm == 0:
                    centroids[k] = self.problem.cities_coordinates[np.random.randint(n)]
                    continue
                centroids[k] = s/norm
            iteration+=1
        self.problem.sat_coordinates = centroids
        return iteration
    
    def solve(self, verbose = False) :
        if verbose :
            print("Lancement de l'algorithme de Kmeans.")
            old_cost = self.problem.value
            print(f"La puissance totale reçue actuellement est de {old_cost * 1e6 :.2f}µW, ce qui représente une couverture de {self.problem.coverage() * 100 : .2f}%.")
        if   self.problem.dimension == 2 : self.__kmeans2D()
        elif self.problem.dimension == 3 : iteration = self.__kmeans3D()
        self.problem.value = self.problem.cost()
        if verbose :
            print("Fin de l'algorithme.")
            if iteration == self.max_iter : print("Le nombre d'itérations maximal a été atteint.")
            else                          : print("L'algorithme s'est déroulé avec succès.")
            new_cost = self.problem.value
            print(f"La nouvelle puissance totale reçue est de {new_cost * 1e6 :.2f}µW, ce qui représente une amélioration de {100 * (new_cost - old_cost)/old_cost :.2f}%. La couverture est maintenant de {self.problem.coverage() * 100 :.2f}%.\n")
