import numpy as np

from kmeans import *
from optimization import *
from satellites_problem import *

def euclidean_satellites_repartition(N_satellites, file_name, H = 35786, P = 100e3, I_necessary = (10**((-67-30)/10)), verbose=False) :
    """
    Cette fonction trouve les positions de N_satellites satellites de façon à couvrir le mieux possible les villes indiquées pour une terre rectangulaire.

    Input :
    Obligatoire :
        N_satellites (int) : nombre de satellites fournis.
        file_name    (str) : nom du fichier contenant les données sur les villes
    Optionnel :
        H           (float) : hauteur des satellites par rapport à la terre (en km). Par défaut, la hauteur géostationnaire de 35 786 km a été choisie.
        P           (float) : puissance de l'onde qu'un satellite peut émettre (en W). Par défaut, une valeur de 100kW a été choisie.
        I_necessary (float) : intensité nécessaire pour satisfaire entièrement une ville ayant un poids de 1 (en W/km²). Par défaut, une valeur de -67dBm/km² a été choisie. Cela correspond à une intensité acceptable pour une personne, en considérant donc qu'un poids de un correspond à une personne.
        verbose     (bool)  : booléen indiquant si les détails de l'optimisation doivent être imprimés dans la sortie standard
    
    Return :
        satellites_coordinates (nparray(tuple(float, float, H))) : liste contenant les coordonnées cartésiennes (x,y,H) (en km) des satellites sur la terre après optimisation.
        cost                   (float)                           : valeur de la fonction objectif avec cette répartition des satellites.
    """
    
    problem = SatellitesProblem(dimension=2, H=H, P=P, I_necessary=I_necessary)
    problem.input_from_file(file_name, N_satellites)
    kmeans = Kmeans(problem)
    kmeans.solve(verbose=verbose)
    problem.value = problem.cost()
    cover = problem.coverage()
    if cover >= 1 : return problem.sat_coordinates, problem.cost
    print(f"La couverture actuelle est de {problem.coverage()}.")
    print("Désirez-vous lancer l'algorithme d'optimisation locale (méthode du gradient) pour obtenir des résultats plus précis ? Attention, cela risque de prendre un peu de temps.")
    answer = input("[oui/non] ")
    if answer == "oui" :
        optimization = Optimization(problem)
        optimization.solve(verbose=verbose)
    return problem.sat_coordinates, problem.cost

if __name__ == '__main__' :
    file_name = input("Nom du fichier avec les données : ")
    N_satellites = int(input("Nombre de satellites : "))

    sat_coordinates, cost = euclidean_satellites_repartition(N_satellites, file_name, verbose=True)
    sat = pd.DataFrame()
    sat["X"] = sat_coordinates[:,0]
    sat["Y"] = sat_coordinates[:,1]
    sat["Z"] = sat_coordinates[:,2]
    print("Merci d'avoir utilisé notre application pour trouver la position de vos satellites.")
    print("Où souhaitez-vous que nous imprimions les coordonnées finales des satellites ?")
    answer = input("[stdout/<filename>] ")
    if answer == "stdout" :
        print(sat)
    else :
        sat.to_csv(answer)
    print("Bonne journée :)")