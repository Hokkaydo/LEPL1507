import numpy as np
import pandas as pd

from utilities import *

class SatellitesProblem :
    """
    Classe pour représenter le problème de trouver la meilleure position possible de N_satellites satellites pour couvrir au mieux un ensemble de villes en Internet.

    Attributs :
        dimension    (int)   : valeur parmi {2, 3}. Représente la dimension du problème. Si dimension == 2, le problème est réalisé sur une terre rectangulaire. Si dimension == 3, il est réalisé sur une terre sphérique.
        R            (float) : rayon de la terre (en km). Par défaut, le rayon de la planète Terre de 6371 km est utilisé. Cette variable ne sera utilisée que pour un problème sphérique.
        H            (float) : dans le cas d'un problème euclidien, hauteur des satellites par rapport à la terre (en km). Dans le cas d'un problème sphérique, rayon de l'orbite géostationnaire. Par défaut, une valeur de 35786 + 6371 a été choisie, correspondant à la somme de l'altitude géostationnaire et du rayon de la Terre.
        P            (float) : puissance de l'onde qu'un satellite peut émettre (en W). Par défaut, une valeur de 100kW a été choisie.
        I_necessary  (float) : intensité nécessaire pour satisfaire entièrement une ville ayant un poids de 1 (en W). Par défaut, une valeur de -67dBm a été choisie (poids de 1 = 1 habitant dans la ville).
        max_distance (float) : distance maximale entre une ville et un satellite pour que l'onde émise par le satellite n'ait pas à traverser la terre pour atteindre la ville. Cette variable n'est utilisée que pour un problème sphérique et vaut sqrt(H² - R²)
        
        cities_coordinates (ndarray((N_cities, 3)))               : liste contenant les coordonnées des villes sur la terre. Si dimension == 2, des coordonnées cartésiennes (x,y,0) (en km) sont attendues. Si dimension == 3, les coordonnées géographiques (R,phi,lambda) avec -90° <= phi <= 90° (latitude) et -180° <= lambda <= 180° (longitude) sont attendues.
        cities_weights     (ndarray(N_cities))                    : liste de même taille que cities_coordinates contenant les poids des villes. Par défaut, nous supposons que ce poids correspond au nombre d'habitants de la ville (sinon, I_necessary doit être modifié).
        N_satellites       (int)                           : nombre de satellites fournis.
        sat_coordinates    (ndarray((N_satellites, 3)))    : liste contenant les coordonnées des satellites sur la terre. Si dimension == 2, des coordonnées cartésiennes (x,y,H) (en km) sont utilisées. Si dimension == 3, les coordonnées géographiques sont utilisées.
        value              (float)                         : valeur de la fonction objectif avec cette répartition des satellites.

        alpha (float) : paramètre pour rendre continue la fonction objectif. 0 < alpha < 1
        gamma (float) : paramètre pour rendre continue la fonction objectif. gamma > 1

    Méthodes :
        __init__(self, dimension, R, H, P, I_necessary)
        input_from_file(self, file_name, N_satellites)
        __square_distance(self, index_city, index_sat)
        __cost_city(self, index_city, continuous=False)
        cost(self, continuous=False)
        __grad_2D(self)
        __grad_3D(self)
        grad(self)
        coverage(self)
    """

    def __init__(self, dimension = 3, R = 6371, H = 35786 + 6371, P = 100e3, I_necessary = (10**((-67-30)/10))) :
        self.dimension    = dimension
        self.R            = R
        self.H            = H
        self.P            = P
        self.I_necessary  = I_necessary
        self.max_square_distance = H**2 - R**2

        self.cities_coordinates = None
        self.cities_weights     = None
        self.N_satellites       = 0
        self.sat_coordinates    = None
        self.value              = None

        self.alpha = 0.999
        self.gamma = 5
    
    def input_from_file(self, file_name, N_satellites) :
        """
        Fonction permettant de compléter les poids et coordonnées des villes à partir d'un fichier csv de nom file_name contenant cinq colonnes : les indices, les noms, les poids et les deux coordonnées des villes. Dans le cas d'un problème en deux dimensions, les deux coordonnées sont les coordonnées x et y de chaque ville. Pour un problème sphérique, elles correspondent à la latitude ([-90°, 90°]) et à la longitude de chaque ville ([-180°, 180°]). Cette fonction permet également de donner le nombre de satellites du problème.

        Arguments :
        file_name    (str) : le nom du fichier dans lequel se trouvent les données des villes
        N_satellites (int) : nombre de satellites fournis

        Résultat :
        self.cities_weights et self.cities_coordinates ont été complétés avec les informations dans le fichier. Les poids des villes ont été remis entre 0 et 1 en les divisant par la norme infinie. Notons que chaque ville est représentée par trois coordonnées dans self.cities_coordinates : (x,y,0) dans le cas d'un problème bidimensionnel et (R,lat,long) dans le cas d'un problème sphérique. self.N_satellites contient le nombre de satellites indiqués.
        self.I_necessary a été modifié pour correspondre au nombre d'habitants d'une ville ayant un poids de 1 (ce nombre d'habitants correspond à la norme infinie du vecteur self.cities_weights initial).
        """
        database = pd.read_csv(file_name)
        self.cities_weights = np.array(database[database.columns[2]], dtype=float)
        maximum_person = np.max(self.cities_weights)
        self.cities_weights /= maximum_person
        self.I_necessary *= maximum_person

        x, y = np.array(database[database.columns[3]], dtype=float), np.array(database[database.columns[4]], dtype=float) # x,y ou lat,long
        if   self.dimension == 2 : self.cities_coordinates = np.array([x, y, np.zeros(len(x))]).T
        elif self.dimension == 3 : self.cities_coordinates = np.array([self.R * np.ones(len(x)), x, y]).T
        
        self.N_satellites = N_satellites

    def __square_distance(self, index_city, index_sat) :
        """
        Calcule la distance euclidienne entre la ville index_city et le satellite index_sat
        
        Arguments :
        index_city (int) : indice de la ville dans self.cities_coordinates
        index_sat  (int) : indice du satellite dans self.sat_coordinates
        
        Retourne :
        float : la distance euclidienne entre la ville et le satellite

        Complexité : O(1)
        """
        if   self.dimension == 2 : return np.linalg.norm(self.cities_coordinates[index_city] - self.sat_coordinates[index_sat])**2
        elif self.dimension == 3 :
            X1 = gps2cart(self.cities_coordinates[index_city])
            X2 = gps2cart(self.sat_coordinates[index_sat])
            return np.linalg.norm(X1 - X2)**2
    
    def __cost_city(self, index_city, continuous=False) :
        """
        Calcule l'intensité (en W/km²) reçue dans la ville index_city.
        
        Arguments :
            index_city (int)  : indice de la ville pour laquelle il faut calculer l'intensité reçue
            continuous (bool) : booléen indiquant s'il faut utiliser une version continue ou non de la fonction objectif (dans le cas sphérique)
        
        Retourne :
            float : l'intensité reçue dans la ville. Si l'intensité reçue dépasse l'intensité nécessaire pour satisfaire 100% de la population de la ville, uniquement l'intensité nécessaire est renvoyée (tout le surplus est "jeté")
        
        Complexité : O(N_satellites)
        """
        local_received = 0
        for j in range (self.N_satellites) :
            square_distance = self.__square_distance(index_city, j)
            if self.dimension == 3 and not continuous and square_distance > self.max_square_distance : square_distance = np.inf
            elif self.dimension == 3 and continuous and square_distance > self.alpha*self.max_square_distance : square_distance += (square_distance - self.alpha*self.max_square_distance)**self.gamma
            local_received += self.P / (4*np.pi*square_distance)
        return min(local_received, self.cities_weights[index_city] * self.I_necessary)
    
    def cost(self, continuous=False) :
        """
        Calcule le profit (valeur de la fonction objectif) avec la position des satellites actuelle

        Arguments :
            continuous (bool) : booléen indiquant s'il faut utiliser une version continue ou non de la fonction objectif (dans le cas sphérique)

        Retourne :
            float : valeur de la fonction objectif avec la position des satellites actuelles. Celle-ci correspond à la somme des intensités reçues dans chaque ville.
        
        Résultat :
            Si la valeur de la "vraie" fonction objectif (non continue dans le cas sphérique) est calculée, self.value est actualisé.
        
        Complexité : O(N_cities * N_satellites)
        """
        total_received = 0
        for i in range (len(self.cities_coordinates)) :
            total_received += self.__cost_city(i, continuous=continuous)
        if not continuous : self.value = total_received
        return total_received
    
    def __grad_2D(self) :
        """
        Calcule le gradient de la fonction objectif à la position des satellites actuelles (pour un problème 2D)

        Retourne :
            ndarray((N_satellites, 3)) : gradient de la fonction objectif à la position des satellites considérées. La coordonnée z des satellites étant constante, la troisième colonne est une colonne de zéros.
        
        Complexité : O(N_cities * N_satellites)
        """
        grad = np.zeros((self.N_satellites, 3)) # 3 car coordonnées x,y,z avec z = H toujours
        for i in range (len(self.cities_coordinates)) :
            if (self.__cost_city(i) == self.cities_weights[i]*self.I_necessary) : continue # La pente est nulle

            for j in range(self.N_satellites) :
                coef = -2*self.P/(4*np.pi*(self.__square_distance(i, j))**2)
                grad[j,0] += coef*(self.sat_coordinates[j,0] - self.cities_coordinates[i,0])
                grad[j,1] += coef*(self.sat_coordinates[j,1] - self.cities_coordinates[i,1])
        return grad

    def __grad_3D(self) :
        """
        Calcule le gradient de la version continue de la fonction objectif à la position des satellites actuelles (pour un problème 3D)

        Retourne :
            ndarray((N_satellites, 3)) : gradient de la fonction objectif à la position des satellites considérées. Le rayon des satellites étant constant, la première colonne est une colonne de zéros.
        
        Complexité : O(N_cities * N_satellites)
        """
        grad = np.zeros((self.N_satellites, 3)) # 3 coordonnées r,phi,lambda
        for i in range(len(self.cities_coordinates)) :
            if (self.__cost_city(i, continuous=True) == self.cities_weights[i]*self.I_necessary) : continue # La pente est nulle

            x,y,z = gps2cart(self.cities_coordinates[i])
            for j in range(self.N_satellites) :
                R, lat, long = self.sat_coordinates[j]
                lat = np.deg2rad(lat); long = np.deg2rad(long)

                square_dist = self.__square_distance(i,j)

                dfdlat  = 2*R* (np.cos(lat)*(R*np.sin(lat)-z) - np.sin(lat)*np.cos(long)*(R*np.cos(lat)*np.cos(long) - x) - np.sin(lat)*np.sin(long)*(R*np.cos(lat)*np.sin(long)-y))
                dfdlong = 2*R* (np.cos(lat)*np.cos(long)*(R*np.cos(lat)*np.sin(long) - y) - np.cos(lat)*np.sin(long)*(R*np.cos(lat)*np.cos(long) - x))

                if square_dist < self.alpha*self.max_square_distance : 
                    grad[j,1:] -= self.P/(4*np.pi*square_dist**2) * np.array([dfdlat, dfdlong])
                else :
                    grad[j,1:] -= self.P * (1+self.gamma*(square_dist-self.alpha*self.max_square_distance)**(self.gamma-1)) / (4*np.pi * (square_dist + (square_dist-self.alpha*self.max_square_distance)**self.gamma)**2) * np.array([dfdlat, dfdlong])
        return grad
    
    def grad(self) :
        """
        Calcule le gradient de la version continue de la fonction objectif à la position des satellites actuelle.

        Retourne :
            ndarray((N_satellites, 3)) : gradient de la fonction objectif continue à la position des satellites actuelle
        
        Complexité : O(N_cities * N_satellites)
        """
        if   self.dimension == 2 : return self.__grad_2D()
        elif self.dimension == 3 : return self.__grad_3D()
    
    def coverage(self) :
        """
        Calcule la couverture Internet fournie par la position actuelle des satellites.
        
        Retourne :
            float : valeur comprise entre 0 et 1 correspondant à la couverture
        
        Complexité : O(N_cities)
        """
        return self.value / (np.sum(self.cities_weights) * self.I_necessary)
    
    def uncovered_cities(self) :
        nb_uncovered = 0
        for i in range (len(self.cities_coordinates)) :
            if self.__cost_city(i) == 0 : nb_uncovered += 1
        return nb_uncovered