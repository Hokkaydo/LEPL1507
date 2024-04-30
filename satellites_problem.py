import numpy as np
import pandas as pd

from utilities import *

class SatellitesProblem :
    """
    Classe pour représenter le problème de trouver la meilleure position possible de N_satellites satellites pour couvrir au mieux un ensemble de villes en Internet.

    Attributs :
        dimension          (int)                                   : valeur parmi {2, 3}. Représente la dimension du problème. Si dimension == 2, le problème est réalisé sur une terre rectangulaire. Si dimension == 3, il est réalisé sur une terre sphérique.
        N_satellites       (int)                                   : nombre de satellites fournis.
        cities_coordinates (nparray(nparray(float, float, float))) : liste contenant les coordonnées des villes sur la terre. Si dimension == 2, des coordonnées cartésiennes (x,y,0) (en km) sont attendues. Si dimension == 3, les coordonnées géographiques (phi,lambda,R) avec -90° <= phi <= 90° (latitude) et -180° <= lambda <= 180° (longitude) sont attendues.
        cities_weights     (nparray(float))                        : liste de même taille que cities_coordinates contenant les poids des villes.
        R                  (float)                                 : rayon de la terre (en km). Par défaut, le rayon de la planète Terre de 6371 km est utilisé. Cette variable ne sera utilisée que pour un problème sphérique.
        H                  (float)                                 : hauteur des satellites par rapport à la terre (en km). Par défaut, l'altitude géostationnaire de 35 786 km a été choisie.
        P                  (float)                                 : puissance de l'onde qu'un satellite peut émettre (en W). Par défaut, une valeur de 100kW a été choisie.
        I_necessary        (float)                                 : intensité nécessaire pour satisfaire entièrement une ville ayant un poids de 1 (en W/km²). Par défaut, une valeur de -40dBm a été choisie. Cela correspond à une intensité de -67dBm pour 500 habitants par km².
        sat_coordinates    (nparray(tuple(float, float,float)))    : liste contenant les coordonnées des satellites sur la terre. Si dimension == 2, des coordonnées cartésiennes (x,y,H) (en km) sont utilisées. Si dimension == 3, les coordonnées géographiques sont utilisées.
        value              (float)                                 : valeur de la fonction objectif avec cette répartition des satellites.

    Méthodes :
        __init__(self, dimension, R, H, P, I_necessary)
        input_from_file(self, file_name)
        input_from_data(self, cities_weights, cities_coordinates)
        __distance(self, index_city, index_sat)
        __cost_city(self, index_city, continuous, alpha, gamma)
        cost(self, continuous)
        grad_sat(self, index_sat, alpha, gamma, h)
        coverage(self)
    """

    def __init__(self, dimension = 3, R = 6371, H = 35786 + 6371, P = 100e3, I_necessary = (10**((-67-30)/10))) :
        self.dimension    = dimension
        self.R            = R
        self.H            = H
        self.P            = P
        self.I_necessary  = I_necessary
        self.max_distance = np.sqrt(H**2 - R**2)

        self.N_satellites       = 0
        self.sat_coordinates    = None
        self.cities_coordinates = None
        self.cities_weights     = None
        self.value              = None

        self.alpha = 0.999
        self.gamma = 5
    
    def input_from_file(self, file_name, N_satellites) :
        """
        Fonction permettant de compléter les poids et coordonnées des villes à partir d'un fichier csv de nom file_name contenant quatre colonnes : les indices, les poids et les deux coordonnées des villes. Il ne peut pas y avoir de ligne titre ! Dans le cas d'un problème en deux dimensions, les deux coordonnées sont les coordonnées x et y de chaque ville. Pour un problème sphérique, elles correspondent à la latitude ([-90°, 90°]) et à la longitude de chaque ville ([-180°, 180°]). Cette fonction permet également de donner le nombre de satellites du problème.

        Input :
        file_name    (str) : le nom du fichier dans lequel se trouvent les données des villes
        N_satellites (int) : nombre de satellites fournis

        Result :
        self.cities_weights et self.cities_coordinates ont été complétés avec les informations dans le fichier. Notons que chaque ville est représentée par trois coordonnées dans self.cities_coordinates : (x,y,0) dans le cas d'un problème bidimensionnel et (R,lat,long) dans le cas d'un problème sphérique. self.N_satellites contient le nombre de satellites indiqués.
        """
        database = pd.read_csv(file_name)
        self.cities_weights = np.array(database[database.columns[2]], dtype=float)
        maximum_person = np.max(self.cities_weights)
        self.cities_weights /= maximum_person
        self.I_necessary *= maximum_person
        x, y = np.array(database[database.columns[3]]), np.array(database[database.columns[4]]) # x,y ou lat,long
        if   self.dimension == 2 : self.cities_coordinates = np.array([x, y, np.zeros(len(x))]).T
        elif self.dimension == 3 : self.cities_coordinates = np.array([self.R * np.ones(len(x)), x, y]).T
        self.N_satellites = N_satellites

    def __distance(self, index_city, index_sat, continuous=False) :
        """
        Calcule la distance euclidienne entre la ville index_city et le satellite index_sat
        
        Input :
        index_city (int) : indice de la ville dans self.cities_coordinates
        index_sat  (int) : indice du satellite dans self.sat_coordinates
        
        Return :
        (float) : la distance euclidienne entre la ville et le satellite
        """
        if   self.dimension == 2 : return np.linalg.norm(self.cities_coordinates[index_city] - self.sat_coordinates[index_sat])
        elif self.dimension == 3 :
            X1 = gps2cart(self.cities_coordinates[index_city])
            X2 = gps2cart(self.sat_coordinates[index_sat])
            distance = np.linalg.norm(X1 - X2)
            if   not continuous and distance > self.max_distance              : return np.inf
            elif     continuous and distance > self.alpha * self.max_distance : return distance + (distance - self.alpha * self.max_distance)**self.gamma
            else                                                              : return distance
    
    def __cost_city(self, index_city) :
        """
        Calcule l'intensité (en W/km²) reçue dans la ville index_city."""
        local_received = 0
        for j in range (self.N_satellites) :
            distance = self.__distance(index_city, j)
            local_received += self.P / (4*np.pi*distance**2)
        return min(local_received, self.cities_weights[index_city] * self.I_necessary)
    
    def cost(self) :
        total_received = 0
        for i in range (len(self.cities_coordinates)) :
            total_received += self.__cost_city(i)
        self.value = total_received
        return total_received
    
    def __grad_2D(self) :
        grad = np.zeros((self.N_satellites, 3)) # 3 car coordonnées x,y,z avec z = H toujours
        for i in range (len(self.cities_coordinates)) :
            if (self.__cost_city(i) == self.cities_weights[i]*self.I_necessary) : continue # La pente est nulle
            for j in range(self.N_satellites) :
                coef = -2*self.P/(4*np.pi*(self.__distance(i, j))**4)
                grad[j,0] += coef*(self.sat_coordinates[j,0] - self.cities_coordinates[i,0])
                grad[j,1] += coef*(self.sat_coordinates[j,1] - self.cities_coordinates[i,1])
        return grad

    def __grad_3D(self) :
        grad = np.zeros((self.N_satellites, 3)) # 3 coordonnées r,phi,lambda
        for i in range(len(self.cities_coordinates)) :
            if (self.__cost_city(i) == self.cities_weights[i]*self.I_necessary) : continue # La pente est nulle
            x,y,z = gps2cart(self.cities_coordinates[i])
            for j in range(self.N_satellites) :
                coef = -self.P/(4*np.pi*(self.__distance(i,j,continuous=True))**4) * 2*self.R*(1 + self.gamma*(self.__distance(i,j,continuous=True) - self.alpha*self.max_distance)**(self.gamma-1))
                grad[j,1] += coef*(-(self.R*np.sin(self.sat_coordinates[j,1]) - z)*np.cos(self.sat_coordinates[j,1]) + (self.R*np.sin(self.sat_coordinates[j,2])*np.cos(self.sat_coordinates[j,1]) - y)*np.sin(self.sat_coordinates[j,2])*np.sin(self.sat_coordinates[j,1]) + (self.R*np.cos(self.sat_coordinates[j,2])*np.cos(self.sat_coordinates[j,1]) - x)*np.sin(self.sat_coordinates[j,1])*np.cos(self.sat_coordinates[j,2]))
                grad[j,2] += coef*(-(self.R*np.sin(self.sat_coordinates[j,2])*np.cos(self.sat_coordinates[j,1]) - y)*np.cos(self.sat_coordinates[j,2])*np.cos(self.sat_coordinates[j,1]) + 2*self.R*(self.R*np.cos(self.sat_coordinates[j,2])*np.cos(self.sat_coordinates[j,1]) - x)*np.sin(self.sat_coordinates[j,2])*np.cos(self.sat_coordinates[j,1]))
        return grad
    
    def grad(self) :
        if   self.dimension == 2 : return self.__grad_2D()
        elif self.dimension == 3 : return self.__grad_3D()
    
    def coverage(self) : return self.value / (np.sum(self.cities_weights) * self.I_necessary)