import numpy as np

from utilities import *

class SatellitesProblem :
    """
    Classe pour représenter le problème de trouver la meilleur position possible de N_satellites satellites pour couvrir au mieux un ensemble de villes en Internet.

    Attributs :
        dimension          (int)                       : valeur parmi {2, 3}. Représente la dimension du problème. Si dimension == 2, le problème est réalisé sur une terre rectangulaire. Si dimension == 3, il est réalisé sur une terre sphérique.
        N_satellites       (int)                       : nombre de satellites fournis.
        cities_coordinates (list(tuple(float, float))) : liste contenant les coordonnées des villes sur la terre. Si dimension == 2, des coordonnées cartésiennes x,y (en km) sont attendues. La position (0,0) correspond au coin inférieur gauche de la terre. Si dimension == 3, les coordonnées sphériques 0 <= phi <= 2pi et 0 <= theta <= pi (en radian) sont attendues.
        cities_weights     (list(float))               : liste de même taille que cities_coordinates contenant les poids des villes.
        R                  (float)                     : rayon de la terre (en km). Par défaut, le rayone de la planète Terre de 6371 km est utilisé. Cette variable ne sera utilisée que pour un problème sphérique.
        H                  (float)                     : hauteur des satellites par rapport à la terre (en km). Par défaut, la hauteur géostationnaire de 35 786 km a été choisie.
        P                  (float)                     : puissance de l'onde qu'un satellite peut émettre (en W). Par défaut, une valeur de 50 a été choisie.
        I_necessary        (float)                     : intensité nécessaire pour satisfaire entièrement une ville ayant un poids de 1 (en W). Par défaut, une valeur de 2e-6 a été choisie. Cela correspond à une intensité de -67dBm pour 10000 appareils.
        alpha              (float)                     : angle de focalisation de l'onde émise par le satellite en radian. Sa valeur doit être comprise entre 0 et pi. Par défaut, l'onde est supposée non focalisée et une valeur de pi est prise.
        sat_coordinates    (list(tuple(float, float))) : liste contenant les coordonnées des satellites sur la terre. Si dimension == 2, des coordonnées cartésiennes x,y (en km) sont attendues. Si dimension == 3, les coordonnées sphériques 0 <= phi <= 2pi et 0 <= theta <= pi (en radian) sont attendues. Initialement, les satellites sont tous placés en (0,0).
        value              (float)                     : valeur de la fonction objectif avec cette répartition des satellites.
        forbidden_cities   (liste(tuple(float, float))): liste contenant les coordonnées des villes interdites sur la terre (initialisée par défaut comme une liste vide).
        penality           (int)                       : valeur de pénalité rajouté aux couts lorsqu'on a une ville interdite
    
    Méthodes ;
    """

    def __init__(self, dimension, N_satellites, cities_coordinates, cities_weights, R = 6371, H = 35786, P = 50, I_necessary = (10**((-67-30)/10))*1e4, alpha = np.pi, forbidden_cities=[], penalty=1000) :
        self.dimension = dimension
        self.N_satellites = N_satellites
        self.cities_coordinates =  cities_coordinates
        self.cities_weights = cities_weights

        self.R = R
        self.H = H
        self.P = P
        self.I_necessary = I_necessary
        alpha = np.minimum(alpha, np.arcsin(R/(H+R)))
        self.alpha = alpha
        if   dimension == 2 : self.max_distance = H/np.cos(alpha)
        elif dimension == 3 : self.max_distance = (H+R)*np.cos(alpha) - np.sqrt(R**2 - ((H+R)*np.sin(alpha))**2)

        self.sat_coordinates = np.zeros((N_satellites, 2))
        self.forbidden_cities = forbidden_cities
        self.value = self.cost()
        self.penalty = penalty ### ATTENTION DEFINIR UNE VALEUR ###
    
    def __distance(self, index_city, index_sat) :
        if   self.dimension == 2 :
            X1 = np.append(np.array(self.cities_coordinates[index_city], 0))
            X2 = np.append(np.array(self.sat_coordinates   [index_sat],  self.H))
        elif self.dimension == 3 :
            X1 = np.array(spher2cart((self.R, self.cities_coordinates[index_city][0], self.cities_coordinates[index_city][1])))
            X2 = np.array(spher2cart((self.H, self.sat_coordinates   [index_sat] [0], self.sat_coordinates   [index_sat] [1])))
        return np.linalg.norm(X1 - X2)
    
    def __cost_city(self, index_city, continuous = False, alpha = 0.99, gamma = 10) :
        local_received = 0
        for j in range (self.N_satellites) :
            distance = self.__distance(index_city, j)

            if not continuous and distance > self.max_distance: den = float('inf')
            elif continuous and distance > alpha*self.max_distance: den = distance + (distance - self.alpha * self.max_distance)**gamma
            else: den = distance

            local_received += self.P / den**2
        return min(local_received, self.cities_weights[index_city] * self.I_necessary)
    
    def cost(self, continuous = False) :
        total_received = 0
        for i in range (len(self.cities_coordinates)) :
            city_coordinate_tuple = tuple(self.cities_coordinates[i])
            if city_coordinate_tuple in self.forbidden_cities:
                forbidden_city_reached = False
                for k in range(self.N_satellites):
                    if np.linalg.norm(np.array(city_coordinate_tuple) - self.sat_coordinates[k]) < threshold:
                        forbidden_city_reached = True
                        break
                if forbidden_city_reached:
                    total_received -= self.penalty_factor
            else:
                total_received += self.__cost_city(i, continuous=continuous)
        if not continuous : self.value = total_received
        return total_received
    
    def grad_sat(self, index_sat, alpha = 0.99, gamma = 10, h=1e-6) :
        grad = np.zeros(2)
        for i in range (len(self.cities_coordinates)) :
            if self.__cost_city(i, continuous=True, alpha=alpha, gamma=gamma) == self.cities_weights[i] * self.I_necessary : continue # La pente est nulle
            distance = self.__distance(i, index_sat)
            for j in range(2) :
                if   self.dimension == 2 : grad[j] += (self.sat_coordinates[index_sat][j] - self.cities_coordinates[i][j]) * (1 + gamma * (distance - alpha*self.max_distance) ** (gamma-1)) / distance
                elif self.dimension == 3 : # Différences finies
                    old_position = self.sat_coordinates[index_sat][j]
                    self.sat_coordinates[index_sat][j] += h
                    power_plus_h = self.cost(continuous=True)
                    self.sat_coordinates[index_sat][j] -= 2*h
                    power_moins_h = self.cost(continuous=True)
                    grad[j] = (power_plus_h - power_moins_h) / (2*h)
                    self.sat_coordinates[index_sat][j] = old_position
        return grad
    
    def coverage(self) : return self.value / (np.sum(self.cities_weights) * self.I_necessary)
