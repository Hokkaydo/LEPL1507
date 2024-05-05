from satellites_problem import *

class Optimization :
    """
    Classe pour résoudre un problème de maximisation en utilisant la méthode du gradient

    Attributs :
        problem  (SatellitesProblem) : problème sur lequel va être appliqué l'algorithme d'optimisation
        max_iter (int)               : nombre d'itérations maximal pour la méthode du gradient
        epsilon  (float)             : taux définissant le critère d'arrêt
    
    Méthodes :
        __init__(self, problem, max_iter = 100, epsilon = 1e-13)
        __find_alpha(self, gradient, direction, alpha = 1, c1 = 1e-3, c2 = 0.9)
        solve(self, verbose = False)
    """

    def __init__(self, problem, max_iter = 100, epsilon=1e-13) :
        self.problem = problem
        self.max_iter = max_iter
        self.epsilon = epsilon
    
    def __find_alpha(self, gradient, direction, alpha=1, c1 = 1e-7, c2 = 1e-3) :
        """
        Trouve une valeur d'un pas satisfaisant aux conditions de Wolfe pour le problème donné dans la diection de recherche et avec le gradient indiqués.

        Arguments :
            gradient  (ndarray((self.problem.N_satellites, 3))) : gradient de la fonction objectif continue à la position des satellites actuelle
            direction (ndarray((self.problem.N_satellites, 3))) : direction de recherche
            alpha     (float)                                   : estimation initiale de la longueur de pas pour démarrer un algorithme itératif permettant de trouver sa valeur. Par défaut, une valeur de 1 est choisie.
            c1        (float)                                   : paramètre pour la première condition de Wolfe (condition de croissance suffisante). 0 < c1 < 1. Par défaut, une valeur de 1e-3 est choisie.
            c2        (float)                                   : paramètre pour la seconde condition de Wolfe (condition de courbure). c1 < c2 < 1. Par défaut, une valeur de 0.9 est choisie.
        
        Retourne :
            alpha (float) : valeur d'une longueur de pas vérifiant les conditions de Wolfe
        
        Complexité : O()
        """
        L = 0; U = np.inf # bornes sur la longueur de pas

        gradient_vector = np.reshape(gradient, 3*len(gradient))
        direction_vector = np.reshape(direction, 3*len(direction))
        current_position = np.copy(self.problem.sat_coordinates)
        current_value = self.problem.value
        scalar_product_grad = np.dot(gradient_vector, direction_vector)

        while (True) : # Une méthode de bissection est utilisée
            if np.isclose(L,U) : alpha = -1; break
            self.problem.sat_coordinates = current_position + alpha*direction
            new_value = self.problem.cost()
            if (new_value < current_value + c1*alpha*scalar_product_grad) : U = alpha; alpha = (U+L)/2; continue # Si la première condition de Wolfe n'est pas respectée, l'intervalle de recherche est réduit à [L; alpha] (on est allé trop loin)

            new_gradient = np.reshape(self.problem.grad(), 3*len(gradient))
            if (np.dot(new_gradient, direction_vector) > c2*scalar_product_grad) : # Si la seconde condition de Wolfe n'est pas respectée, l'intervalle de recherche est réduit à [alpha;U] (on n'est pas suffisament loin pour que le gradient ait changé)
                L = alpha
                if U == np.inf : alpha = 2*L
                else : alpha = (U+L)/2
                continue
            break

        self.problem.sat_coordinates = current_position
        self.problem.cost()
        return alpha
    
    def solve(self, verbose = False) :
        """
        Résoud un problème de maximisation en utilisant la méthode du gradient

        Argument :
            verbose (bool) : booléen indiquant si les détails de l'optimisation doivent être imprimés dans la sortie standard

        Résultat :
            self.problem.sat_coordinates contient la position optimale des satellites trouvée et self.problem.cost contient le profit associé à cette solution.
        
        Complexité : O()
        """
        if verbose :
            print("Lancement de l'algorithme d'optimisation locale.")
            old_cost = self.problem.value
            print(f"La puissance totale reçue actuellement est de {old_cost * 1e6 :.2f}µW, ce qui représente une couverture de {self.problem.coverage() * 100 :.2f}%.")

        iteration = 0
        while iteration < self.max_iter :
            iteration += 1
            
            old_value = self.problem.value
            grad = self.problem.grad()
            norm_grad = np.linalg.norm(np.reshape(grad, 3*len(grad)))
            if norm_grad == 0 : break # La position des satellites correspond à un optimum
            direction = grad/norm_grad
            
            alpha = self.__find_alpha(grad, direction)
            if alpha == -1 : break
            self.problem.sat_coordinates += alpha * direction
            self.problem.cost()
            
            if abs(self.problem.value - old_value) < self.epsilon : break # Critère d'arrêt portant sur la variation du profit
        
        if verbose :
            print("Fin de l'algorithme.")
            if iteration == self.max_iter : print("Le nombre d'itérations maximal a été atteint.")
            else                          : print("L'algorithme s'est déroulé avec succès.")
            new_cost = self.problem.value
            if old_cost != 0 : print(f"La nouvelle puissance totale reçue est de {new_cost * 1e6 :.2f}µW, ce qui représente une amélioration de {100 * (new_cost - old_cost)/old_cost :.2f}%. La couverture est maintenant de {self.problem.coverage() * 100 :.2f}%.\n")
            else : print(f"La nouvelle puissance totale reçue est de {new_cost * 1e6 :.2f}µW. La couverture est maintenant de {self.problem.coverage() * 100 :.2f}%.\n")