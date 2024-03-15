import numpy as np
from utilities import *

Pt = 50                                                             # Transmission power of a satellite []
beta = np.deg2rad(5)                                                # angle of covering of a satellite [rad]
r = 6371                                                            # mean radius of Earth [km]
R = r + 35786                                                       # geostationary radius [km]
max_dist = R*np.cos(beta) - np.sqrt(r**2 - R**2 * np.sin(beta)**2)  # maximal distance at which a satellite has an impact
I_min = (10**((-67-30)/10))*1e4                                     # Intensity required to satisfy perfectly 10 000 residents

h = 1e-6 # for finite differences

class Satellites_problem :
    def __init__(self, cities, weights, n_sat) :
        """
        cities  (list of tuples of float) : cartesian coordinates of the cities
        weights (list of float)           : weights of each cities
        n_sat   (int)                     : number of satellites
        """
        self.cities  = cities
        self.weights = weights
        self.n_sat   = n_sat
    
    def city_profit(self, sat, i) :
        local_profit = 0
        for j in range (self.n_sat) :
            Rij = np.linalg.norm(sat[j] - self.cities[i])
            if (Rij <= max_dist) :
                local_profit += Pt/(2*np.pi*Rij**2*(1-np.cos(beta)))
        return local_profit
    
    def profit(self, phi, theta) :
        """
        Compute the profit of a given position of the satellites

        Input :
        phi   (numpy array of size n_sat) : the azimut      of the satellites (in [0, 2*pi])
        theta (numpy array of size n_sat) : the polar angle of the satellites (in [0,   pi])

        Output :
        a float representing the score of this position of satellites
        """
        profit = 0
        cartesian = spher2cart(R, phi, theta)
        for i in range (len(self.cities)) :
            local_profit = self.city_profit(cartesian, i)
            profit += np.minimum(local_profit, I_min * self.weights[i])
        return profit
    
    def gradient_profit(self, phi, theta) :
        """
        Compute the gradient of the profit of a given position of the satellites

        Input :
        phi   (numpy array of size n_sat) : the azimut      of the satellites (in [0, 2*pi])
        theta (numpy array of size n_sat) : the polar angle of the satellites (in [0,   pi])

        Output :
        a numpy array of floats of size 2*n_sat giving the gradient of the profit function with this position of satellites ([d/dphi_1 d/dtheta_1 d/dphi_2 ...] . f)
        """
        gradient = np.zeros(2*self.n_sat)
        cartesian = spher2cart(R, phi, theta)
        for i in range (len(self.cities)) :
            local_proft = self.city_profit(cartesian, i)
            if (local_proft < I_min * self.weights[i]) :
                for j in range (self.n_sat) :
                    gradient[2*j]   += (self.profit(phi[j] + h, theta[j]) - self.profit(phi[j] - h, theta[j])) / (2*h)
                    gradient[2*j+1] += (self.profit(phi[j], theta[j] + h) - self.profit(phi[j], theta[j] - h)) / (2*h)
        return gradient

test = Satellites_problem([(1, 2, 3)], [1], 1)
print(test.profit([1], [1]))
print(test.gradient_profit([1], [1]))