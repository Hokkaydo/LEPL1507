from satellites_problem import *

class Optimization :
    """
    
    Attributs :
        problem (SatellitesProblem) : problème sur lequel va être appliqué l'algorithme d'optimisation
    
    Méthodes :
        solve
    """

    def __init__(self, problem, max_iter = 100, epsilon=1e-10) :
        self.problem = problem
        self.max_iter = max_iter
        self.epsilon = epsilon
    
    def __first_derivative(self, index, alpha, h, grad):
            old_position = np.copy(self.problem.sat_coordinates[index])
            self.problem.sat_coordinates[index] += (alpha + h)* grad
            power_plus_h = self.problem.cost(continuous = True)
            self.problem.sat_coordinates[index] -= 2*h*grad
            power_minus_h = self.problem.cost(continuous = True)
            self.problem.sat_coordinates[index] = old_position
            return (power_plus_h - power_minus_h) / (2*h)
    
    def __find_alpha(self, index_sat, gradient, alpha=1, c1=1e-10, c2=0.9) :
        sign = np.sign(self.__first_derivative(index_sat, 0, 1e-6, gradient))
        alpha_a = 0
        alpha_b = 0
        while(sign == np.sign(self.__first_derivative(index_sat, alpha_b, 1e-6, gradient))):
            alpha_b += 0.1*sign
        if sign == -1:
            a = alpha_a
            alpha_a = alpha_b
            alpha_b = a
        while(True):
            alpha = (alpha_a + alpha_b) / 2
            if self.__first_derivative(index_sat, alpha, 1e-6, gradient) > 0:
                alpha_a = alpha
            else:
                alpha_b = alpha
            if abs(alpha_b - alpha_a) < 1e-8:
                break
        return alpha
    
    def solve(self, verbose = False) :
        if verbose :
            print("Lancement de l'algorithme d'optimisation locale.")
            old_cost = self.problem.value
            print(f"La puissance totale reçue actuellement est de {old_cost * 1e6 :.2f}µW, ce qui représente une couverture de {self.problem.coverage() * 100 : .2f}%.")

        iteration = 0
        while iteration < self.max_iter :
            old_value = self.problem.value
            for i in range(self.problem.N_satellites) :
                iter_sat = 0
                while iter_sat < self.max_iter :
                    grad = self.problem.grad_sat(i)
                    if np.linalg.norm(grad) < self.epsilon : break
                    grad /= np.linalg.norm(grad)

                    alpha = self.__find_alpha(i, grad)
                    self.problem.sat_coordinates[i] += alpha * grad

                    iter_sat += 1
                self.problem.value = self.problem.cost()
            new_value = self.problem.value
            iteration += 1
            if verbose :
                print(f"Après {iteration} itérations, la puissance totale reçue est de {new_value * 1e6 :.2f}µW")
            if abs(new_value - old_value) < self.epsilon : break
        
        if verbose :
            print("Fin de l'algorithme.")
            if iteration == self.max_iter : print("Le nombre d'itérations maximal a été atteint.")
            else                          : print("L'algorithme s'est déroulé avec succès.")
            new_cost = self.problem.value
            print(f"La nouvelle puissance totale reçue est de {new_cost * 1e6 :.2f}µW, ce qui représente une amélioration de {100 * (new_cost - old_cost)/old_cost :.2f}%. La couverture est maintenant de {self.problem.coverage() * 100 :.2f}%.\n")