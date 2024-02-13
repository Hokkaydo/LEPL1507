import numpy as np
from math import *
from scipy.optimize import *
import matplotlib.pyplot as plt

def euclidean_satellites_repartition(N_satellites, cities_coordinates, cities_weights, puissance = 100000, I_acceptable = 1) :
    """
    N_satellites (int)                               : nombre de satellites disponibles pour couvrir la terre
    cities_coordinates (tableau de tuples d'entiers) : coordonnées des villes qu'on cherche à couvrir
    cities_weights (tableau d'entiers)               : poids d'une ville (importance relative par rapport aux autres)
    puissance (float)                                : puissance [W] d'un satellite (identique pour tous)
    I_acceptable (float)                             : intensité [W/m²] considérée comme acceptable pour 10 000 personnes

    Retourne :
    satellites_coordinates (tableau de tuples d'entiers) : coodonnées des N_satellites permettant d'offrir une couverture optimale
    """

    l = 500; L = 1500
    def obj(x) :
        cost = 0
        for j in range (len(cities_coordinates)) :
            local = 0
            for i in range (N_satellites) :
                local += 1/((np.linalg.norm(np.array([x[i],x[i+N_satellites]]) - cities_coordinates[j]))**2)
            local *= puissance/(4*np.pi)
            cost += np.minimum(local, I_acceptable*cities_weights[j])
        return -cost
    
    bounds = np.concatenate((np.array([(0, L) for i in range (N_satellites)]), 
                            np.array([(0,l) for i in range (N_satellites)])))
    
    return differential_evolution(obj, bounds).x


if (__name__ == '__main__') :
    N_satellites = 2
    cities_coordinates = np.array([[1, 1], [100, 300], [1000, 200], [700, 50]])
    cities_weights = [1, 1, 1, 1]
    result = euclidean_satellites_repartition(N_satellites, cities_coordinates, cities_weights)

    plt.figure()
    for city in cities_coordinates :
        plt.plot(city[0], city[1], 'ob')
    for i in range(N_satellites) :
        plt.plot(result[i], result[N_satellites+i], 'or')
    plt.show()