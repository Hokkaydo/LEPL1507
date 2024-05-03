import numpy as np

from kmeans import *
from optimization import *
from satellites_problem import *
from utilities import *

def spherical_satellites_repartition (N_satellites, file_name, R = 6371, H = 35786 + 6371, P = 100e3, I_necessary = (10**((-67-30)/10)), verbose = False) :
    """
    Cette fonction trouve les positions de N_satellites satellites de façon à couvrir le mieux possible les villes indiquées pour une terre sphérique.

    Arguments :
    Obligatoires :
        N_satellites (int) : nombre de satellites fournis.
        file_name    (str) : nom du fichier contenant les données sur les villes (poids et coordonnées)
    Optionnels :
        R           (float) : rayon de la terre (en km). Par défaut, le rayon de la planète Terre de 6371 km est utilisé.
        H           (float) : rayon de l'orbite géostationnaire des satellites (en km). Par défaut, une valeur de 35786 + 6371 a été choisie, correspondant à la somme de l'altitude géostationnaire et du rayon de la Terre.
        P           (float) : puissance de l'onde qu'un satellite peut émettre (en W). Par défaut, une valeur de 100kW a été choisie.
        I_necessary (float) : intensité nécessaire pour satisfaire une personne (en W). Par défaut, une valeur de -67dBm a été choisie.
        verbose     (bool)  : booléen indiquant si les détails de l'optimisation doivent être imprimés dans la sortie standard

    Return :
        satellites_coordinates (nparray(nparray(float, float))) : liste contenant les coordonnées des satellites sur la terre après optimisation. Les coordonnées sont renvoyées au format géographique (altitude, latitude, longitude).
        cost                   (float)                          : coût de la fonction objectif avec cette répartition des satellites.
    """

    problem = SatellitesProblem(dimension=3, R=R, H=H, P=P, I_necessary=I_necessary)
    problem.input_from_file(file_name, N_satellites)
    kmeans = Kmeans(problem)
    kmeans.solve(verbose=verbose)
    problem.value = problem.cost()
    cover = problem.coverage()
    if cover >= 1 : return problem.sat_coordinates, problem.cost
    print(f"La couverture actuelle est de {cover * 100 :.2f}%.")
    print("Désirez-vous lancer l'algorithme d'optimisation locale (méthode du gradient) pour obtenir des résultats plus précis ?")
    answer = input("[oui/non] ")
    print()
    if answer == "oui" :
        optimization = Optimization(problem)
        optimization.solve(verbose=verbose)
    return problem.sat_coordinates, problem.cost

if __name__ == '__main__' :
    file_name = input("Nom du fichier avec les données : ")
    N_satellites = int(input("Nombre de satellites : "))
    print()

    sat_coordinates, cost = spherical_satellites_repartition(N_satellites, file_name, verbose=True)
    sat = pd.DataFrame()
    sat["Rayon"]     = sat_coordinates[:,0]
    sat["Latitude"]  = sat_coordinates[:,1]
    sat["Longitude"] = sat_coordinates[:,2]
    print("Merci d'avoir utilisé notre application pour trouver la position de vos satellites.")
    print("Où souhaitez-vous que nous imprimions les coordonnées finales des satellites ?")
    answer = input("[stdout/<filename>] ")
    if answer == "stdout" :
        print(sat)
    else :
        sat.to_csv(answer)
    print("\nBonne journée :)")