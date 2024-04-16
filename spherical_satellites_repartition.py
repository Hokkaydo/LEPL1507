import numpy as np

from kmeans import *
from optimization import *
from satellites_problem import *
from utilities import *

def spherical_satellites_repartition (N_satellites, cities_coordinates, cities_weights, format = "spherical", R = 6371, H = 35786, P = 50, I_necessary = (10**((-67-30)/10))*1e4, alpha = np.pi, verbose = False) :
    """
    Cette fonction trouve les positions de N_satellites satellites de façon à couvrir le mieux possible les villes indiquées pour une terre sphérique.

    Input :
    Obligatoire :
        N_satellites       (int)                                                                     : nombre de satellites fournis.
        cities_coordinates (nparray(nparray(float, float)) ou nparray(nparray(float, float, float))) : liste contenant les coordonnées sphérique 0 <= phi <= 2pi et 0 <= theta <= pi en radian (le rayon n'est pas nécessaire ici) ou cartésiennes x,y,z en km des villes sur la terre. Dans le second cas, la position (0,0,0) correspond au coin inférieur gauche de la terre.
        cities_weights     (nparray(float))                                                          : liste de même taille que cities_coordinates contenant les poids des villes.
    Optionnel :
        format      (str)   : valeur parmi {"cartesian", "spherical"}. Indique si les coordonnées des villes ont été fournies au format cartésien ou sphérique. Les coordonnées des satellites seront renvoyées sous le même format. Par défaut, des coordonnées sphériques sont attendues.
        R           (float) : rayon de la terre (en km). Par défaut, le rayon de la planète Terre de 6371 km est utilisé.
        H           (float) : hauteur des satellites par rapport à la terre (en km). Par défaut, la hauteur géostationnaire de 35 786 km a été choisie.
        P           (float) : puissance de l'onde qu'un satellite peut émettre (en W). Par défaut, une valeur de 50 a été choisie.
        I_necessary (float) : intensité nécessaire pour satisfaire entièrement une ville ayant un poids de 1 (en W). Par défaut, une valeur de 2e-6 a été choisie. Cela correspond à une intensité de -67dBm pour 10000 appareils.
        alpha       (float) : angle de focalisation de l'onde émise par le satellite en radian. Sa valeur doit être comprise entre 0 et pi. Par défaut, l'onde est supposée non focalisée et une valeur de pi est prise.
        verbose     (bool)  : booléen indiquant si les détails de l'optimisation doivent être imprimés dans la sortie standard

    Return :
        satellites_coordinates (nparray(nparray(float, float))) : liste contenant les coordonnées des satellites sur la terre après optimisation sous le même format que celui avec lequel les coordonnées des villes avaient été fournies.
        cost                   (float)                          : coût de la fonction objectif avec cette répartition des satellites.
    """
    if format == "cartesian" : cities_coordinates = [cart2spher(cities_coordinates[i])[1:] for i in range(len(cities_coordinates))]
    problem = SatellitesProblem(3, N_satellites, cities_coordinates, cities_weights, R=R, H=H, P=P, I_necessary=I_necessary, alpha=alpha)
    kmeans = Kmeans(problem)
    kmeans.solve(verbose=verbose)
    print(problem.sat_coordinates)
    optimization = Optimization(problem)
    optimization.solve(verbose=verbose)
    print(problem.sat_coordinates)
    return problem.sat_coordinates, problem.cost

if __name__ == '__main__' :
    N_satellites = 15
    N_cities = 30
    cities_coordinates = np.vstack((np.random.uniform(0, 2*np.pi, N_cities), np.random.uniform(0, np.pi, N_cities))).T
    cities_weights = np.random.uniform(0, 1, N_cities)

    sat_coordinates, cost = spherical_satellites_repartition(N_satellites, cities_coordinates, cities_weights, alpha=np.deg2rad(5), verbose=True)