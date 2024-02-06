def euclidean_satellites_repartition(N_satellites, cities_coordinates, cities_weights, portee) :
    """
    N_satellites (int)                               : nombre de satellites disponibles pour couvrir la terre
    cities_coordinates (tableau de tuples d'entiers) : coordonnées des villes qu'on cherche à couvrir
    cities_weights (tableau d'entiers)               : poids d'une ville (importance relative par rapport aux autres)
    portee                                           : ...

    Retourne :
    satellites_coordinates (tableau de tuples d'entiers) : coodonnées des N_satellites permettant d'offrir une couverture optimale
    """
    (...)