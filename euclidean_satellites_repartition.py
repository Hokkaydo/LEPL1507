import numpy as np
from math import *
from scipy.optimize import *
import matplotlib.pyplot as plt

def euclidean_satellites_repartition(N_satellites, cities_coordinates, cities_weights, puissance = 260*10**9, I_acceptable = 233*10**3) :
    """
    N_satellites (int)                               : nombre de satellites disponibles pour couvrir la terre
    cities_coordinates (tableau de tuples d'entiers) : coordonnées des villes qu'on cherche à couvrir
    cities_weights (tableau d'entiers)               : poids d'une ville (importance relative par rapport aux autres)
    puissance (float)                                : puissance [W] d'un satellite (identique pour tous)
    I_acceptable (float)                             : intensité [W/m²] considérée comme acceptable pour 10 000 personnes

    Retourne :
    satellites_coordinates (tableau de tuples d'entiers) : coodonnées des N_satellites permettant d'offrir une couverture optimale
    
    233kbits par seconde par utilisateur
    260Gbits par seconde par satellite
    """
    weight_sum = sum(cities_weights)
    cities_weights = [w/weight_sum for w in cities_weights]
    l = 12742 # [km] largeur  approximative de la terre
    L = 40030 # [km] longueur approximative de la terre
    c = 3 * 10**8 # [m/s] vitesse de la lumière dans le vide
    frequence = 10**9 # [Hz] fréquence des satellites !! rechercher une valeur de reference !!

    def interf_destr(satellite_coord, city_coord, dist) :
        phase_difference = dist*2*np.pi/(c/frequence)
        if phase_difference%np.pi == np.pi/2: #vérification multiple impair de pi
            return True
        return False
    
    def obj(x) :
        cost = 0
        for j in range (len(cities_coordinates)) :
            local = 0
            for i in range (N_satellites) :
                dist = np.linalg.norm(np.array([x[i],x[i+N_satellites]]) - cities_coordinates[j])
                local += 1/(dist**2)
            local *= puissance/(4*np.pi)
            if not interf_destr(x, cities_coordinates[j],dist):
                cost += np.minimum(local, I_acceptable*cities_weights[j])
        return -cost
    
    bounds = np.concatenate((np.array([(0, L) for i in range (N_satellites)]), 
                            np.array([(0,l) for i in range (N_satellites)])))
    
    result = differential_evolution(obj, bounds).x
    return result[:N_satellites], result[N_satellites:]


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
