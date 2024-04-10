import numpy as np

from kmeans import *
from optimization import *
from satellites_problem import *

def euclidean_satellites_repartition(N_satellites, cities_coordinates, cities_weights, H = 35786, P = 50, I_necessary = (10**((-67-30)/10))*1e4, alpha = np.pi, verbose=False) :
    """
    Cette fonction trouve les positions de N_satellites satellites de façon à couvrir le mieux possible les villes indiquées pour une terre rectangulaire.

    Input :
    Obligatoire :
        N_satellites       (int)                       : nombre de satellites fournis.
        cities_coordinates (list(tuple(float, float))) : liste contenant les coordonnées cartésiennes x,y (en km) des villes sur la terre. La position (0,0) correspond au coin inférieur gauche de la terre.
        cities_weights     (list(float))               : liste de même taille que cities_coordinates contenant les poids des villes.
    Optionnel :
        H           (float) : hauteur des satellites par rapport à la terre (en km). Par défaut, la hauteur géostationnaire de 35 786 km a été choisie.
        P           (float) : puissance de l'onde qu'un satellite peut émettre (en W). Par défaut, une valeur de 50 a été choisie.
        I_necessary (float) : intensité nécessaire pour satisfaire entièrement une ville ayant un poids de 1 (en W). Par défaut, une valeur de 2e-6 a été choisie. Cela correspond à une intensité de -67dBm pour 10000 appareils.
        alpha       (float) : angle de focalisation de l'onde émise par le satellite en radian. Sa valeur doit être comprise entre 0 et pi. Par défaut, l'onde est supposée non focalisée et une valeur de pi est prise.
        verbose     (bool)  : booléen indiquant si les détails de l'optimisation doivent être imprimés dans la sortie standard
    
    Return :
        satellites_coordinates (list(tuple(float, float))) : liste contenant les coordonnées cartésiennes x,y (en km) des satellites sur la terre après optimisation.
        cost                   (float)                     : valeur de la fonction objectif avec cette répartition des satellites.
    """

    problem = SatellitesProblem(2, N_satellites, cities_coordinates, cities_weights, H=H, P=P, I_necessary=I_necessary, alpha=alpha)
    kmeans = Kmeans(problem)
    kmeans.solve(verbose=verbose)
    optimization = Optimization(problem)
    optimization.solve(verbose=verbose)
    return problem.sat_coordinates, problem.cost

if __name__ == '__main__' :
    N_satellites = 15
    N_cities = 30
    cities_coordinates = np.vstack((np.random.uniform(0, 2000, N_cities), np.random.uniform(0, 1000, N_cities))).T
    cities_weights = np.random.uniform(0, 1, N_cities)

    sat_coordinates, cost = euclidean_satellites_repartition(N_satellites, cities_coordinates, cities_weights, verbose=True)