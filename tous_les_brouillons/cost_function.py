import numpy as np
from utilities import *

Pt = 50                                                             # Transmission power of a satellite []
beta = np.deg2rad(5)                                                # angle of covering of a satellite [rad]
r = 6371                                                            # mean radius of Earth [km]
R = r + 35786                                                       # geostationary radius [km]
I_min = (10**((-67-30)/10))*1e4                                     # Intensity required to satisfy perfectly 10 000 residents

h = 1e-6 # for finite differences

class Satellites_problem :
    def __init__(self, cities, weights, n_sat, dim) :
        """
        cities  (np array of np array of float) : cartesian coordinates of the cities (in 2D or 3D)
        weights (np array of float)             : weights of each cities
        n_sat   (int)                           : number of satellites
        dim     (int in {2, 3})                 : eulerian problem in 2D or spherical problem in 3D
        """
        self.cities  = cities
        self.weights = weights
        self.n_sat   = n_sat
        self.dim     = dim
        # maximal distance at which a satellite has an impact
        if   dim == 2 : self.max_dist = (R-r)/np.cos(beta)
        elif dim == 3 : self.max_dist = R*np.cos(beta) - np.sqrt(r**2 - R**2 * np.sin(beta)**2)

    def profit2D(self, x, y) :
        if self.dim == 3 :
            print("Error, you can't use a function for a 2D problem in a 3D problem")
            return None
        profit = 0
        for i in range (len(self.cities)) :
            local_profit = 0
            for j in range (self.n_sat) :
                Rij = np.sqrt((x[j] - self.cities[i][0])**2 + (y[j] - self.cities[i][1])**2 + (R-r)**2)
                if (Rij <= self.max_dist) :
                    local_profit += Pt/(2*np.pi*Rij**2*(1-np.cos(beta)))
            profit += np.minimum(local_profit, I_min * self.weights[i])
        return profit
    
    def profit3D(self, phi, theta) :
        """
        Compute the profit of a given position of the satellites

        Input :
        phi   (numpy array of size n_sat) : the azimut      of the satellites (in [0, 2*pi])
        theta (numpy array of size n_sat) : the polar angle of the satellites (in [0,   pi])

        Output :
        a float representing the score of this position of satellites
        """
        if self.dim == 2 :
            print("Error, you can't use a function for a 3D problem in a 2D problem")
            return None
        x, y, z = spher2cart(R, phi, theta)
        profit = 0
        for i in range (len(self.cities)) :
            local_profit = 0
            for j in range (self.n_sat) :
                Rij = np.sqrt((x[j] - self.cities[i][0])**2 + (y[j] - self.cities[i][1])**2 + (z[j] - self.cities[i][2])**2)
                if (Rij <= self.max_dist) :
                    local_profit += Pt/(2*np.pi*Rij**2*(1-np.cos(beta)))
            profit += np.minimum(local_profit, I_min * self.weights[i])
        return profit
    
    def profit(self, X) :
        """
        Input:
        X is a numpy array of length n_sat containing the cartesian coordinates of all satellites in the form of numpy array of floats
        
        Examples:
        If self.dim == 2 and self.n_sat == 3, X could be equal to [[1, 2], [2, 5], [3,1]]
        If self.dim == 3 and self.n_sat == 1, X could be equal to [[1, 2, 1]]
        """
        if self.dim == 2 : return self.profit2D(X[:,0], X[:,1])
        elif self.dim == 3 :
            _, phi, theta = cart2spher(X[:,0], X[:,1], X[:,2])
            return self.profit3D(phi, theta)
    
    def gradient_profit2D(self, x, y) :
        """
        Compute the gradient of the profit of a given position of the satellites

        Input :
        phi   (numpy array of size n_sat) : the azimut      of the satellites (in [0, 2*pi])
        theta (numpy array of size n_sat) : the polar angle of the satellites (in [0,   pi])

        Output :
        a numpy array of floats of size 2*n_sat giving the gradient of the profit function with this position of satellites ([d/dphi_1 d/dtheta_1 d/dphi_2 ...] . f)
        """
        if self.dim == 3 :
            print("Error, you can't use a function for a 2D problem in a 3D problem")
            return None
        gradientX = np.zeros(self.n_sat)
        gradientY = np.zeros(self.n_sat)
        for i in range (len(self.cities)) :
            local_profit = 0
            for j in range (self.n_sat) :
                Rij = np.sqrt((x[j] - self.cities[i][0])**2 + (y[j] - self.cities[i][1])**2 + (R-r)**2)
                if (Rij <= self.max_dist) :
                    local_profit += Pt/(2*np.pi*Rij**2*(1-np.cos(beta)))

            if (local_profit < I_min * self.weights[i]) :
                for j in range (self.n_sat) :
                    gradientX[j] += (self.profit2D(x + h*np.identity(len(x))[j,:], y) - self.profit2D(x - h*np.identity(len(x))[j,:], y)) / (2*h)
                    gradientY[j] += (self.profit2D(x, y + h*np.identity(len(y))[j,:]) - self.profit2D(x, y - h*np.identity(len(y))[j,:])) / (2*h)
        return gradientX, gradientY
    
    def gradient_profit3D(self, phi, theta) :
        """
        Compute the gradient of the profit of a given position of the satellites

        Input :
        phi   (numpy array of size n_sat) : the azimut      of the satellites (in [0, 2*pi])
        theta (numpy array of size n_sat) : the polar angle of the satellites (in [0,   pi])

        Output :
        a numpy array of floats of size 2*n_sat giving the gradient of the profit function with this position of satellites ([d/dphi_1 d/dtheta_1 d/dphi_2 ...] . f)
        """
        if self.dim == 2 :
            print("Error, you can't use a function for a 3D problem in a 2D problem")
            return None
        x, y, z = spher2cart(R, phi, theta)
        gradientPHI   = np.zeros(self.n_sat)
        gradientTHETA = np.zeros(self.n_sat)
        for i in range (len(self.cities)) :
            local_profit = 0
            for j in range (self.n_sat) :
                Rij = np.sqrt((x[j] - self.cities[i][0])**2 + (y[j] - self.cities[i][1])**2 + (z[j] - self.cities[i][2])**2)
                if (Rij <= self.max_dist) :
                    local_profit += Pt/(2*np.pi*Rij**2*(1-np.cos(beta)))

            if (local_profit < I_min * self.weights[i]) :
                for j in range (self.n_sat) :
                    gradientPHI[j]   += (self.profit3D(phi + h*np.identity(len(phi))[j,:], theta) - self.profit3D(phi - h*np.identity(len(phi))[j,:], theta)) / (2*h)
                    gradientTHETA[j] += (self.profit3D(phi, theta + h*np.identity(len(theta))[j,:]) - self.profit3D(phi, theta - h*np.identity(len(theta))[j,:])) / (2*h)
        return gradientPHI, gradientTHETA
    
    def gradient_profit(self, X) :
        """
        Input:
        X is a numpy array of length n_sat containing the cartesian coordinates of all satellites in the form of numpy array of floats
        
        Examples:
        If self.dim == 2 and self.n_sat == 3, X could be equal to [[1, 2], [2, 5], [3,1]]
        If self.dim == 3 and self.n_sat == 1, X could be equal to [[1, 2, 1]]
        """
        if self.dim == 2 : return self.gradient_profit2D(X[:,0], X[:,1])
        elif self.dim == 3 :
            r, phi, theta = cart2spher(X[:,0], X[:,1], X[:,2])
            return self.gradient_profit3D(phi, theta)

if __name__ == '__main__' :
    cities2D = np.array([(1, 2)])
    weights2D = np.array([1])
    sat2D = np.array([(1, 1)])
    test2D = Satellites_problem(cities2D, weights2D, 1, 2)
    print(test2D.profit(sat2D))
    print(test2D.gradient_profit(sat2D))

    cities3D = np.transpose(spher2cart(np.array([r]), np.array([1]), np.array([1])))
    weights3D = np.array([1])
    sat3D = np.transpose(spher2cart(np.array([R]), np.array([1]), np.array([1])))
    test = Satellites_problem(cities3D, weights3D, 1, 3)
    print(test.profit(sat3D))
    print(test.gradient_profit(sat3D))