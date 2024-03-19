import numpy as np

class Nelder_Mead :
    def __init__(self, cities, weights, nsat, minmax = 'min', cout = None) :
        self.cities = cities
        self.weights = weights
        self.nsat = nsat
        self.minmax = minmax
        self.cout = cout
        if minmax == 'max' : self.cout *= -1
    
    def update_cout(self, minmax, cout) :
        self.minmax = minmax
        self.cout = cout
        if minmax == 'max' : self.cout *= -1
    
    def change_nsat(self, nsat) :
        self.nsat = nsat
    
    def __place(self, points, point) :
        points = points[:self.nsat]
        current = self.nsat
        f_point = self.cout(point)
        lo = 0; hi = self.nsat-1
        while (lo <= hi) :
            mid = (lo + hi)//2
            f_mid = self.cout(points[mid])
            if (f_mid < f_point) : lo = mid + 1
            elif (f_mid == f_point) :
                np.insert(points, mid, point); return
            else : hi = mid - 1
        np.insert(points, lo, point)

    def __iterations(self, points) :
        # critère d'arrêt :
        max = np.inf
        for i in range (self.nsat) :
            for j in range (i+1, self.nsat+1) :
                max = np.max(max, np.linalg.norm(points[i] - points[j]))
        if (max < 1e-5) : return

        barycentre = np.sum(points[:self.nsat])/self.nsat
        d = barycentre - points[-1]
        reflexion = barycentre + d
        f_reflexion = self.cout(reflexion)
        f_0 = self.cout(points[0])
        f_n_1 = self.cout(points[-2])
        f_n = self.cout(points[-1])
        if (f_reflexion < f_0) :
            expansion = reflexion + d
            f_expansion = self.cout(expansion)
            if (f_expansion < f_reflexion) : self.__place(points, expansion)
            else : self.__place(points, reflexion)
        elif (f_0 < f_reflexion < f_n_1) :
            self.__place(points, reflexion)
        elif (f_n_1 < f_reflexion < f_n) :
            extern_contraction = barycentre + d/2
            f_extern = self.cout(extern_contraction)
            if (f_extern < f_reflexion) :
                self.__place(points, extern_contraction)
            else : self.__place(points,reflexion)
        elif (f_n < f_reflexion) :
            intern_contraction = barycentre - d/2
            f_intern = self.cout(intern_contraction)
            if (f_intern < f_n) : self.__place(points, intern_contraction)
            else :
                for i in range (1, self.nsat+1) :
                    points[i] = (points[i] + points[0]) / 2
        self.__iterations(points)

    
    def Nelder_Mead(self, initial, coord = 'euclidian') :
        if (coord == 'euclidian') : initial = spherical(initial)
        else : initial = np.copy(initial)
        points = np.array([initial])
        for i in range (self.nsat) :
            phi = np.random.rand(self.nsat)*2*np.pi # polaire
            theta = np.random.rand(self.nsat)*np.pi # azimutal
            np.append(points, [(phi[j], theta[j]) for j in range (self.nsat)]) # initial positions of points
        
        points = np.sort(points)
        self.__iterations(points)
        return points[0]


# Initialization of cities
cities = []
for i in range (n_cit) :
    phi = np.random.rand() * 2*np.pi
    theta = np.random.rand() * np.pi
    cities.append([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])
cities = r * np.array(cities)
cities_weights = np.random.randint(1, 100, n_cit)

print(f"Maximal intensity required is {np.sum(cities_weights)*I_ok}")

satellites = []
for i in range (n_sat) :
    phi = np.random.rand() * 2*np.pi
    theta = np.random.rand() * np.pi
    satellites.append([phi, theta])
satellites = np.array(satellites)
satellites = np.reshape(satellites, 2*len(satellites))

def cost_satellite(satellite) :
    # satellite is in spherical coordinates (only phi, theta ; r is known)
    phi = satellite[0]; theta = satellite[1]
    x = R*np.sin(theta)*np.cos(phi)
    y = R*np.sin(theta)*np.sin(phi)
    z = R*np.cos(theta)
    coord = np.array([x, y, z])

    for i, city in enumerate(cities) :
        dist = np.linalg.norm(city - coord)
        if (dist < max_dist) :
            cities_cost[i] += Pt/(2*np.pi*dist**2*(1-cos_theta))

def cost_function(x) :
    """
    input
    x = [phi1, eta1, phi2, eta2, ...]
    """
    n_sat = len(x)//2
    satellites = np.reshape(x, (n_sat, 2))
    

def euclidean_satellites_repartition(N_satellites, cities_coordinates, cities_weights) :
    Nelder_Mead(cities_coordinates, cities_weights, N_satellites)