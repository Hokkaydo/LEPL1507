import numpy as np
import cvxpy as cp
from pyomo.environ import *

def euclidean_satellites_repartition(N_satellites, cities_coordinates, cities_weights, puissance = 3.8, I_acceptable = 1) :
    """
    N_satellites (int)                               : nombre de satellites disponibles pour couvrir la terre
    cities_coordinates (tableau de tuples d'entiers) : coordonnées des villes qu'on cherche à couvrir
    cities_weights (tableau d'entiers)               : poids d'une ville (importance relative par rapport aux autres)
    puissance (float)                                : puissance [W] d'un satellite (identique pour tous)
    I_acceptable (float)                             : intensité [W/m²] considérée comme acceptable pour 10 000 personnes

    Retourne :
    satellites_coordinates (tableau de tuples d'entiers) : coodonnées des N_satellites permettant d'offrir une couverture optimale
    """

    def obj (model) :
        cost = 0
        for j in range (len(cities_coordinates)) :
            local = 0
            for i in range (N_satellites) :
                local += 1/((np.linalg.norm(np.array([model.x[i], model.y[i]]) - cities_coordinates[j]))**2)
            local *= puissance/(4*np.pi)
            cost += np.minimum(local, I_acceptable*cities_weights[j])
        return cost

    L = 1500; l = 500
    model = ConcreteModel()
    model.x = Var(np.arange(N_satellites), bounds=(0,L))
    model.y = Var(np.arange(N_satellites), bounds=(0,l))
    model.obj = Objective(rule = obj, sense = maximize)

    solver = SolverFactory('glpk')
    solver.solve(model)
    model.pprint()









"""
    X = cp.Variable((N_satellites, 2))
    cost = 0
    for j in range (len(cities_coordinates)) :
        local = 0
        for i in range (N_satellites) :
            local += 1/((cp.norm(X[i,:] - cities_coordinates[j]))**2)
        local *= puissance/(4*np.pi)
        cost += cp.minimum(local, I_acceptable*cities_weights[j])
    objective = cp.Maximize(cost)
    prob = cp.Problem(objective)
    print(prob.solve())"""


if (__name__ == '__main__') :
    N_satellites = 2
    cities_coordinates = np.array([[1, 1], [100, 300], [1000, 200], [700, 50]])
    cities_weights = [1, 1, 1, 1]
    euclidean_satellites_repartition(N_satellites, cities_coordinates, cities_weights)