import numpy as np

from kmeans import *
from optimization import *
from satellites_problem import *
from utilities import *

def spherical_satellites_repartition (N_satellites, file_name, R = 6371, H = 35786 + 6371, P = 100e3, I_necessary = (10**((-67-30)/10)), verbose = False) :
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

    problem = SatellitesProblem(dimension=3, R=R, H=H, P=P, I_necessary=I_necessary)
    problem.input_from_file(file_name, N_satellites)
    kmeans = Kmeans(problem)
    kmeans.solve(verbose=verbose)
    problem.value = problem.cost()
    cover = problem.coverage()
    if cover >= 1 : return problem.sat_coordinates, problem.cost
    print(f"La couverture actuelle est de {problem.coverage()}.")
    print("Désirez-vous lancer l'algorithme d'optimisation locale (méthode du gradient) pour obtenir des résultats plus précis ? Cela peut prendre un peu de temps.")
    answer = input("[oui/non] ")
    if answer == "oui" :
        optimization = Optimization(problem)
        optimization.solve(verbose=verbose)
    return problem.sat_coordinates, problem.cost

if __name__ == '__main__' :
    file_name = input("Nom du fichier avec les données : ")
    N_satellites = int(input("Nombre de satellites : "))

    sat_coordinates, cost = spherical_satellites_repartition(N_satellites, file_name, verbose=True)
    print(sat_coordinates)