from satellites_problem import *

class Optimization :
    """
    
    Attributs :
        problem (SatellitesProblem) : problème sur lequel va être appliqué l'algorithme d'optimisation
    
    Méthodes :
        solve
    """

    def __init__(self, problem, max_iter = 100, epsilon=1e-13) :
        self.problem = problem
        self.max_iter = max_iter
        self.epsilon = epsilon
        if   self.problem.dimension == 2 : self.increment = 10
        elif self.problem.dimension == 3 : self.increment = 1
    
    def __find_alpha(self, gradient, direction, alpha=1, c1 = 0.001, c2 = 0.9) :
        L = 0; U = np.inf
        gradient_vector = np.reshape(gradient, 3*len(gradient))
        direction_vector = np.reshape(direction, 3*len(direction))
        current_position = np.copy(self.problem.sat_coordinates)
        current_value = self.problem.value
        scalar_product_grad = np.dot(gradient_vector, direction_vector)
        while (True) :
            self.problem.sat_coordinates = current_position + alpha*direction
            new_value = self.problem.cost()
            if (new_value < current_value + c1*alpha*scalar_product_grad) : U = alpha; alpha = (U+L)/2; continue
            new_gradient = np.reshape(self.problem.grad(), 3*len(gradient))
            if (np.dot(new_gradient, direction_vector) > c2*scalar_product_grad) :
                L = alpha
                if U == np.inf : alpha = 2*L
                else : alpha = (U+L)/2
                continue
            break
        self.problem.sat_coordinates = current_position; self.problem.value = self.problem.cost()
        return alpha
    
    def solve(self, verbose = False) :
        if verbose :
            print("Lancement de l'algorithme d'optimisation locale.")
            old_cost = self.problem.value
            print(f"La puissance totale reçue actuellement est de {old_cost * 1e6 :.2f}µW, ce qui représente une couverture de {self.problem.coverage() * 100 :.2f}%.")

        iteration = 0
        while iteration < self.max_iter :
            iteration += 1
            old_value = self.problem.value
            grad = self.problem.grad()
            direction = grad/np.linalg.norm(np.reshape(grad, 3*len(grad)))
            alpha = self.__find_alpha(grad, direction)
            if (alpha == -1) : break
            self.problem.sat_coordinates += alpha * direction
            print(alpha)
            self.problem.value = self.problem.cost()
            print(f"Après {iteration} itérations, la puissance totale reçue est de {self.problem.value * 1e6 :.2f}µW")
            print(abs(self.problem.value - old_value))
            if abs(self.problem.value - old_value) < self.epsilon : break
        
        if verbose :
            print("Fin de l'algorithme.")
            if iteration == self.max_iter : print("Le nombre d'itérations maximal a été atteint.")
            else                          : print("L'algorithme s'est déroulé avec succès.")
            new_cost = self.problem.value
            print(f"La nouvelle puissance totale reçue est de {new_cost * 1e6 :.2f}µW, ce qui représente une amélioration de {100 * (new_cost - old_cost)/old_cost :.2f}%. La couverture est maintenant de {self.problem.coverage() * 100 :.2f}%.\n")