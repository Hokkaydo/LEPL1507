import matplotlib.pyplot as plt
import numdifftools as nd
import numpy as np

h = 35786
#cities  = np.array([[1, 2, 0], [2, 1, 0], [1.5, 1.5, 0], [15,6, 0], [14, 6, 0]])
#weights = np.array([1, 1, 1, 1, 1])
#cities = np.array([[1,1,0]])
#weights = np.array([1])
X = np.array([100, 150, 300, 300, 700, 750, 800, 800, 800, 950, 1000, 1200, 1400, 1413, 1500])*10
Y = np.array([30, 450, 200, 300, 50, 50, 400, 250, 300, 10, 420, 350, 270, 200, 430])*10
#weights = np.array([1, 4, 2, 10, 5, 3, 8, 1, 9, 2, 5, 8, 3, 1, 6])
weights = np.ones(15)
cities = np.zeros((15,3))
for i in range(15) : cities[i][0] = X[i]; cities[i][1] = Y[i]

"""cities = np.random.rand(15, 3)*10000
weights = np.random.randint(0, 10, 15)
"""

Pt = 50 # [W]
I_ok = (10**((-67-30)/10))*1e4 # 10 000 habitants
#print(np.sum(weights)*I_ok) # Intensité max

def g_city(satellites, city, weight) :
    max = I_ok*weight
    n_satellites = len(satellites)//2
    cost = 0
    for i in range(n_satellites) :
        satellite = np.array([satellites[i], satellites[i+n_satellites], h])
        dist = np.linalg.norm(satellite - city)
        if (dist != 0) : cost += Pt/(dist**2)
    return np.minimum(cost, max)

def f(satellites) :
    cost = 0
    for i in range(len(cities)) :
        cost += g_city(satellites = satellites, city = cities[i], weight = weights[i])
    return cost

def pas(f, X, p, alpha=50, c1 = 1e-4, c2 = 1+1e-10, arret = 1e-10) :
    U, L = 1e17, 0
    while True :
        if (U - L < arret) : return 0
        X2 = X + alpha*p
        grad_X2 = nd.Gradient(f)(X2)
        if (f(X2) < f(X) + c1*alpha*np.dot(p, p)) :
            U = alpha
            alpha = (U+L)/2
        #elif (0 < np.dot(grad_X2, p) < c2*np.dot(p, p)) :
        #    L = alpha
        #    if U == np.inf : alpha = 2*L
        #    else : alpha = (U+L)/2
        else : return alpha


def tir(f, X, arret = 1e-7) :
    print(f(X))
    plt.figure()
    plt.scatter(cities[:,0], cities[:,1])
    #print(X[:len(X)//2])
    #print(X[len(X)//2:])
    plt.scatter(X[:len(X)//2], X[len(X)//2:])
    plt.show()
    grad_X = nd.Gradient(f)(X)
    print(grad_X)
    X2 = X + pas(f, X, grad_X)*grad_X
    #print(X2)
    if (np.linalg.norm(X2 - X) < arret) : return np.reshape(X2, (2, len(X)//2), order='F')
    else : return tir(f, X2, arret)
    """pa, cont = pas(f, X, grad_X)
    if cont :
        X2 = X + pa*grad_X
        return tir(f, X2)
    else : return np.reshape(X, (2, len(X)//2), order='F')"""
    
    #if (f(X) > f(X2)) : return X
    #else : return tir(f, X2)
    #if (alpha < 1e-10) : return np.reshape(X, (2, len(X)//2), order='F')

satellites = np.array([[4000, 1000], [12000, 2600]])

satellites = tir(f, np.reshape(satellites, 2*len(satellites), order='F'))

plt.figure()
plt.scatter(cities[:,0], cities[:,1], color='b')
plt.scatter(satellites[:,0], satellites[:,1], color='r')
plt.show()