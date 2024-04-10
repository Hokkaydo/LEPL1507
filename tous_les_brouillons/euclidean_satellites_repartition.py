import matplotlib.pyplot as plt
import numpy as np

Pt = 50                                                             # Transmission power of a satellite []
beta = np.deg2rad(5)                                                # angle of covering of a satellite [rad]
r = 6371                                                            # mean radius of Earth [km]
R = r + 35786                                                       # geostationary radius [km]
I_min = (10**((-67-30)/10))*1e4                                     # Intensity required to satisfy perfectly 10 000 residents

h = 1e-6 # for finite differences

X = np.array([100, 150, 300, 300, 700, 750, 800, 800, 800, 950, 1000, 1200, 1400, 1413, 1500])*10
Y = np.array([30, 450, 200, 300, 50, 50, 400, 250, 300, 10, 420, 350, 270, 200, 430])*10
#X = np.array([5000])
#Y = np.array([750])
cities = np.transpose([X, Y])
weights = np.ones(15)
n_sat   = 2
# maximal distance at which a satellite has an impact
max_dist = (R-r)/np.cos(beta)

def profit(X) :
    """
    Input :
    X is a numpy array of floats of size 2*n_sat containing the cartesian coordinates of all satellites

    Example :
    X = [x_sat1, y_sat1, x_sat2, y_sat2, ...]
    """
    x = [] ; y = []
    for i in range (n_sat) :
        x.append(X[2*i]) ; y.append(X[2*i+1])
    x = np.array(x) ; y = np.array(y)

    profit = 0
    for i in range (len(cities)) :
        local_profit = 0
        for j in range (n_sat) :
            Rij = np.sqrt((x[j] - cities[i][0])**2 + (y[j] - cities[i][1])**2 + (R-r)**2)
            if (Rij <= max_dist) :
                local_profit += Pt/(2*np.pi*Rij**2*(1-np.cos(beta)))
        profit += np.minimum(local_profit, I_min * weights[i])
    return -profit

def grad(X) :
    """
    Input :
    X is a numpy array of floats of size 2*n_sat containing the cartesian coordinates of all satellites

    Example :
    X = [x_sat1, y_sat1, x_sat2, y_sat2, ...]
    """
    x = [] ; y = []
    for i in range (n_sat) :
        x.append(X[2*i]) ; y.append(X[2*i+1])
    x = np.array(x) ; y = np.array(y)

    gradient = np.zeros(2 * n_sat)
    for i in range (len(cities)) :
        local_profit = 0
        for j in range (n_sat) :
            Rij = np.sqrt((x[j] - cities[i][0])**2 + (y[j] - cities[i][1])**2 + (R-r)**2)
            if (Rij <= max_dist) :
                local_profit += Pt/(2*np.pi*Rij**2*(1-np.cos(beta)))

        if (local_profit < I_min * weights[i]) :
            for j in range (2*n_sat) :
                gradient[j] += (profit(X + h*np.identity(len(X))[j,:]) - profit(X - h*np.identity(len(X))[j,:])) / (2*h)
    return gradient

def pas(X, gradient, c1 = 0.0001, c2 = 0.9, alpha = 100000000) :
    L = 0 ; U = np.inf
    cost = profit(X)
    while True :
        print(alpha)
        new_cost = profit(X - alpha*gradient)
        if new_cost > cost + c1*alpha*np.dot(gradient, -gradient) :
            U = alpha
            alpha = (L + U)/2
        elif np.dot(grad(X - alpha*gradient), -gradient) < c2 * np.dot(gradient, -gradient)  :#new_cost < cost + c2*alpha*np.dot(gradient, -gradient) :
            L = alpha
            if U == np.inf : alpha = 2*L
            else : alpha = (L+U)/2
        else : return alpha

def line_research(X, arret = 1e-5) :
    alpha = 1
    while True :
        gradient = grad(X)
        print(gradient)
        alpha = pas(X, gradient, alpha)
        print(alpha)
        X2 = X - alpha * gradient
        if np.linalg.norm(X - X2) < arret : break
        X = X2
        print(f"Current cost : {-profit(X)}")
    return X

if __name__ == '__main__' :
    """plt.figure()
    x = np.arange(0, 10000, 1)
    y = np.zeros(len(x))
    gaus = np.zeros(len(x))
    for i in range (len(x)) :
        satellites = np.array([x[i], 750])
        y[i] = profit(satellites)
        gaus[i] = (1/3000*np.sqrt(2*np.pi)) * np.exp(-(x[i]-5000)**2 / (2*3000**2))*1e-3*3
    plt.plot(x, -y)
    plt.plot(x, gaus)
    plt.plot([5000], [I_min], 'og')
    plt.show()
"""



    satellites = np.array([[1500, 4501],[500, 500]])

    plt.figure()
    plt.scatter(cities[:, 0], cities[:, 1], color='b', label='Villes')
    plt.scatter(satellites[:,0], satellites[:,1], color='g', label='Satellites initiaux')
    plt.show()

    satellites = np.reshape(satellites, 2*n_sat)
    print(f"Initial cost : {-profit(satellites)}")

    satellites = line_research(satellites)
    print(f"Cost after optimization : {-profit(satellites)}")
    satellites = np.reshape(satellites, (n_sat, 2))
    print(f"Positions of the satellites : {satellites}")
    plt.figure()
    plt.scatter(cities[:, 0], cities[:, 1], color='b')
    plt.scatter(satellites[:, 0], satellites[:, 1], color='r')
    plt.show()