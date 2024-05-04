from kmeans import *
from optimization import *
from satellites_problem import *
from utilities import *

problem = None

def spherical_satellites_repartition (N_satellites, file_name, R = 6371, H = 35786 + 6371, P = 100e3, I_necessary = (10**((-67-30)/10)), verbose = False, optimisation_decided=False, optimize=False) :
    """
    Cette fonction trouve les positions de N_satellites satellites de façon à couvrir le mieux possible les villes indiquées pour une terre sphérique.

    Arguments :
    Obligatoires :
        N_satellites            (int) : nombre de satellites fournis.
        file_name               (str) : nom du fichier contenant les données sur les villes (poids et coordonnées)
    Optionnels :
        R                       (float) : rayon de la terre (en km). Par défaut, le rayon de la planète Terre de 6371 km est utilisé.
        H                       (float) : rayon de l'orbite géostationnaire des satellites (en km). Par défaut, une valeur de 35786 + 6371 a été choisie, correspondant à la somme de l'altitude géostationnaire et du rayon de la Terre.
        P                       (float) : puissance de l'onde qu'un satellite peut émettre (en W). Par défaut, une valeur de 100kW a été choisie.
        I_necessary             (float) : intensité nécessaire pour satisfaire une personne (en W). Par défaut, une valeur de -67dBm a été choisie.
        verbose                 (bool)  : booléen indiquant si les détails de l'optimisation doivent être imprimés dans la sortie standard
        optimisation_decided    (bool) : booléen indiquant si l'utilisateur a déjà décidé de lancer l'optimisation locale (interface graphique)
        optimize                (bool)  : booléen indiquant si l'optimisation locale doit être lancée après le clustering

    Retourne :
        satellites_coordinates (ndarray((N_satellites, 3))) : liste contenant les coordonnées des satellites sur la terre après optimisation. Les coordonnées sont renvoyées au format géographique (rayon, latitude, longitude).
        cost                   (float)                      : coût de la fonction objectif avec cette répartition des satellites.
    """
    global problem
    problem = SatellitesProblem(dimension=3, R=R, H=H, P=P, I_necessary=I_necessary)
    problem.input_from_file(file_name, N_satellites)
    kmeans = Kmeans(problem)
    kmeans.solve(verbose=verbose)
    problem.cost()
    cover = problem.coverage()
    if np.isclose(cover, 1) : return problem.sat_coordinates, problem.cost
    if not optimisation_decided:
        print(f"La couverture actuelle est de {cover * 100 :.2f}%.")
        print("Désirez-vous lancer l'algorithme d'optimisation locale (méthode du gradient) pour obtenir des résultats plus précis ?")
        answer = input("[oui/non] ")
        print()
        if answer == "oui" :
            optimization = Optimization(problem)
            optimization.solve(verbose=verbose)
    elif optimize:
        optimization = Optimization(problem)
        optimization.solve(verbose=verbose)
    return problem.sat_coordinates, problem.cost

def spherical_satellites_repartition_gps(N_satellites, cities_coordinates, cities_weights, R = 6371, H = 35786, P = 100e3, I_necessary = (10**((-67-30)/10))*1e4, verbose = False, optimize=False) :
    """
    Cette fonction trouve les positions de N_satellites satellites de façon à couvrir le mieux possible les villes indiquées pour une terre sphérique.

    Input :
    Obligatoire :
        N_satellites       (int)                                                                     : nombre de satellites fournis.
        cities_coordinates (nparray(nparray(float, float)) ou nparray(nparray(float, float, float))) : liste contenant les coordonnées latitude, longitude des villes.
        cities_weights     (nparray(float))                                                          : liste de même taille que cities_coordinates contenant les poids des villes.
    Optionnel :
        R           (float) : rayon de la terre (en km). Par défaut, le rayon de la planète Terre de 6371 km est utilisé.
        H           (float) : hauteur des satellites par rapport à la terre (en km). Par défaut, la hauteur géostationnaire de 35 786 km a été choisie.
        P           (float) : puissance de l'onde qu'un satellite peut émettre (en W). Par défaut, une valeur de 50 a été choisie.
        I_necessary (float) : intensité nécessaire pour satisfaire entièrement une ville ayant un poids de 1 (en W). Par défaut, une valeur de 2e-6 a été choisie. Cela correspond à une intensité de -67dBm pour 10000 appareils.
        verbose     (bool)  : booléen indiquant si les détails de l'optimisation doivent être imprimés dans la sortie standard
        optimize    (bool)  : booléen indiquant si l'optimisation locale doit être lancée après le clustering

    Return :
        satellites_coordinates (nparray(nparray(float, float))) : liste contenant les coordonnées des satellites sur la terre après optimisation sous le même format que celui avec lequel les coordonnées des villes avaient été fournies.
        cost                   (float)                          : coût de la fonction objectif avec cette répartition des satellites.
    """
    global problem
    problem = SatellitesProblem(dimension=3, R=R, H=H, P=P, I_necessary=I_necessary)
    problem.N_satellites = N_satellites
    problem.cities_coordinates = cities_coordinates
    problem.cities_weights = cities_weights
    kmeans = Kmeans(problem)
    kmeans.solve(verbose=verbose)
    if optimize:
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
    if answer == "stdout" : print(sat)
    else                  : sat.to_csv(answer)
    print("\nBonne journée :)")