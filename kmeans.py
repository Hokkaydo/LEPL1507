from satellites_problem import *

class Kmeans :
    """
    ...
    Classe pour résoudre  problème de maximisation en utilisant un algorithme de K-means
    
    Classe permettant de résoudre un problème de maximisation en utilisant l'algorithme des K-Means

    Attributs :
        problem  (SatellitesProblem) : problème sur lequel va être réalisé l'algorithme de Kmeans.
        max_iter (int)               : nombre d'itérations maximal qui vont être réalisées dans l'algorithme de Kmeans
    
    Méthodes :
        __init__(self, problem, max_iter = 300)
        __kmeans2D(self)
        __kmeans3D(self)
        solve(self, verbose = False)
    """

    def __init__(self, problem:SatellitesProblem, max_iter = 300) :
        self.problem = problem
        self.max_iter = max_iter
        
    def __kmeans2D(self) :
        """
            Effectue une minimisation de la fonction objectif sur un plan 2D en utilisant l'algorithme des K-Means
        """
        n = self.problem.N_satellites

        cities_coordinates = self.problem.cities_coordinates[:,:2]
        weights = self.problem.cities_weights
        
        centroids = np.zeros((self.problem.N_satellites, 2))
        for i in range(self.problem.N_satellites):
            centroids[i] = cities_coordinates[i%len(cities_coordinates)]                    # Initialisation des satellites aux positions des villes dans l'ordre de la liste
                                                                                            # Cette initialisation permet de s'assurer qu'il est impossible que 2 satellites soient intialement
                                                                                            # placés au même endroit, sauf s'il y a trop peu de villes pour le nombre de satellites
        iteration = 0
        prev_centroids = None
        while prev_centroids is None or (iteration < self.max_iter and not np.allclose(prev_centroids, centroids)):
            classif = {i:{} for i in range(n)}
            for i in range(len(cities_coordinates)):
                dist = [np.linalg.norm(cities_coordinates[i] - c) for c in centroids]       # Calcul de la distance entre chaque ville et chaque satellite

                closest_cluster = dist.index(min(dist))                                     # Attribution de la ville au satellite le plus proche
                classif[closest_cluster][i] = cities_coordinates[i]
                
            prev_centroids = centroids.copy()
            for cluster in range(len(classif)):
                if len(classif[cluster]) == 0:                                              # Si un satellite n'a pas de ville attribuée, on lui en attribue une aléatoirement  
                    centroids[cluster] = cities_coordinates[np.random.randint(0, n)]
                else:           
                    indexes = [i for i in classif[cluster].keys()]                          
                    centroids[cluster] = np.average(cities_coordinates[indexes], axis=0, weights=weights[indexes])  # Nouvelle position du satellite = moyenne pondérée des villes qui lui sont attribuées
            iteration += 1
                     
        self.problem.sat_coordinates = np.zeros((self.problem.N_satellites, 3))
        for i in range(self.problem.N_satellites) :
            self.problem.sat_coordinates[i,:2] = centroids[i]
            self.problem.sat_coordinates[i, 2] = self.problem.H
        return iteration
    
    def __kmeans3D(self) :      
        """
            Effectue une minimisation de la fonction objectif 
            en utilisant l'algorithme des K-Means sur une hypersphère unitaire de dimension 3 
            en coordonnées cartésiennes
            
            Args:
                self.problem : problème sur lequel va être réalisé l'algorithme de Kmeans.
            Returns:
                int : nombre d'itérations réalisées pour converger
                self.problem.sat_coordinates : coordonnées des satellites optimales
        """  
        cities_coordinates = gps2cart(self.problem.cities_coordinates)

        for i in range(len(cities_coordinates)):
            cities_coordinates[i] /= np.linalg.norm(cities_coordinates[i])
        
        n = len(cities_coordinates)
        centroids = np.zeros((self.problem.N_satellites, 3))
        for i in range(self.problem.N_satellites):
            centroids[i] = cities_coordinates[i%len(cities_coordinates)]

        old_centroids = None
        max_covered = 1.3029769341972 # Distance maximum de couverture d'un satellite une fois les villes et satellites normalisés
        iteration = 0
        while old_centroids is None or (iteration < self.max_iter and not np.allclose(old_centroids, centroids)):
            old_centroids = centroids
            clusters = [[] for _ in range(self.problem.N_satellites)]
            
            cities_not_covered = 0
            for i in range(n):
                nearest_cluster = np.argmax(cities_coordinates[i]@centroids.T, axis=0)                          # Satellite maximisant le produit scalaire entre la ville i et chaque satellite
                
                if np.linalg.norm(cities_coordinates[i] - centroids[nearest_cluster]) > max_covered:            # Vérifier si le satellite le plus proche est à une distance supérieure à la distance maximale de couverture
                    cities_not_covered+=1
                    continue
                clusters[nearest_cluster].append(i)
                
            for k in range(self.problem.N_satellites):
                if len(clusters[k]) == 0:                                                                       # Si un satellite n'a pas de ville attribuée, on lui en attribue une aléatoirement
                    centroids[k] = cities_coordinates[np.random.randint(n)]
                    continue
                spherical_coords = cart2gps(cities_coordinates[clusters[k]]*self.problem.H)                                 # Le K-Means sur une hypersphère est effectué en coordonnées cartésiennes
                gps_centroid = np.average(spherical_coords, axis=0, weights=self.problem.cities_weights[clusters[k]])       # or si la moyenne est effectuée en coordonnées cartésiennes, le rayon n'est pas conservé.
                centroids[k] = gps2cart(gps_centroid)/self.problem.H                                                        # On effectue donc la moyenne en coordonnées sphériques avant de reconvertir en coordonnées cartésiennes.

            iteration+=1
        self.problem.sat_coordinates = cart2gps(centroids*self.problem.H)                                       # On reconvertit les coordonnées cartésiennes des satellites en coordonnées sphériques pour respecter la convention du Problem
        print("Number of cities not covered : ", cities_not_covered)
        return iteration
    
    def solve(self, verbose = False) :
        """
            Résoud un problème de maximisation en utilisant la méthode des K-Means

            Argument :
                verbose (bool) : booléen indiquant si les détails de l'optimisation doivent être imprimés dans la sortie standard

            Résultat :
                self.problem.sat_coordinates contient la position optimale des satellites trouvée et self.problem.cost contient le profit associé à cette solution.
            
            Complexité : O(|S||V|)
        """

        if verbose :
            print("Lancement de l'algorithme de Kmeans.")
        if   self.problem.dimension == 2 : iteration = self.__kmeans2D()
        elif self.problem.dimension == 3 : iteration = self.__kmeans3D()
        self.problem.value = self.problem.cost()
        if verbose :
            print("Fin de l'algorithme.")
            if iteration == self.max_iter : print("Le nombre d'itérations maximal a été atteint.")
            else                          : print("L'algorithme s'est déroulé avec succès.")
            new_cost = self.problem.value
            print(f"La puissance totale reçue est de {new_cost * 1e6 :.2f}µW. La couverture est de {self.problem.coverage() * 100 :.2f}%.\n")
