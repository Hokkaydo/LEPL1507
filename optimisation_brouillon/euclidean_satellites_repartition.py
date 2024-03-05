import numpy as np
from math import *
from scipy.optimize import *
import matplotlib.pyplot as plt

# Dimensions
l = 12742    # [km] largeur  approximative de la Terre
L = 40075    # [km] longueur approximative de la Terre
h = 35786    # [km] altitude géostationnaire
lamb = 0.015*10**-3 # [km]  longueur d'onde (c = 3*10^8, f = 20*10^9)

def euclidean_satellites_repartition(N_satellites, cities_coordinates, cities_weights, P_tr = 20, P_re = (200*1e-12)*1e4) :
    """
    N_satellites (int)                               : nombre de satellites disponibles pour couvrir la terre
    cities_coordinates (tableau de tuples d'entiers) : coordonnées des villes qu'on cherche à couvrir
    cities_weights (tableau d'entiers)               : poids d'une ville (importance relative par rapport aux autres)
    P_tr (float)                                     : puissance [W] transmise par un satellite (identique pour tous)
    P_re (float)                                     : puissance [W] reçue considérée comme acceptable pour 10 000 personnes

    Retourne :
    satellites_coordinates (tableau de tuples d'entiers) : coodonnées des N_satellites permettant d'offrir une couverture optimale
    """

    # Normalisation des poids des villes
    # weight_sum = sum(cities_weights)
    # cities_weights = [w/weight_sum for w in cities_weights]

    def interf(satellite1_coord, satellite2_coord, city_coord):
        dist1 = np.linalg.norm(satellite1_coord-city_coord)
        dist2 = np.linalg.norm(satellite2_coord-city_coord)
        m1 = abs(dist1 - dist2)/(lamb)-1/2
        m2 = m1 % 1
        tolerance = 0.1 #correspond à 0.1 radian autour du point exact d'interférence destructive !! determiner une valeur de reference !! 
        if abs(m1 - m2)  <= tolerance: #interference destructive
            return True
        return False

    def obj(x) :
        inter = np.zeros((len(cities_coordinates), N_satellites), dtype=bool)
        cost = 0
        for j in range (len(cities_coordinates)) :
            sum = 0
            for i in range (N_satellites) :
                for k in range(i+1, N_satellites):
                    if interf(np.array([x[i], x[i + N_satellites]]), np.array([x[k], x[k + N_satellites]]),
                                    cities_coordinates[j]):
                        inter[j][i] = True
                        inter[j][k] = True
                if (inter[j][i]):
                    continue
                d = np.linalg.norm(h**2 + (cities_coordinates[j][0] - x[i][0])**2 + (cities_coordinates[j][1] - x[i][1])**2)
                sum += 1/d**2
            sum *= P_tr*lamb**2/(4*np.pi)**2
            cost += np.minimum(sum, P_re*cities_weights[j])
        return -cost
    
    bounds = np.concatenate((np.array([(0, L) for i in range (N_satellites)]), 
                            np.array([(0,l) for i in range (N_satellites)])))
    
    result = differential_evolution(obj, bounds)
    print(result.fun)
    print(np.sum(I_acceptable*cities_weights))
    return result.x[:N_satellites], result.x[N_satellites:]


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
