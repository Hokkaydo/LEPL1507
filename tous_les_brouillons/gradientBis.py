import matplotlib.pyplot as plt
import numpy as np
from cost_function import Satellites_problem

def pas(f, grad, x, y, px, py, alpha=1*10**11, c1=0.1, c2 = 0.9, arret=1e-10): #Recherche d'un pas vérifiant les conditions de Goldstein
    cost = f(x, y)
    grad_cost = grad(x, y)
    new_cost = f(x + alpha*px, y + alpha*py)
    while (not cost + c2 * np.dot(grad_cost, ))

        if np.linalg.norm(p) < arret:
            return alpha
        X2 = X + alpha * p
        if f(X2) < f(X) + c1 * alpha * np.dot(p, p):
            return alpha
        alpha *= c2

def tir(f, grad, X, arret=1e-1): #X=estimation initiale
    x = X[:,0] ; y = X[:,1]
    initial_cost = f(x, y)
    print(f"Coût initial : {initial_cost}")
    while True:
        grad_X, grad_Y = grad(X[0], X[1])
        alpha = pas(f, grad, x, y, grad_X, grad_Y)
        x2 = x + alpha * grad_X
        y2 = y + alpha * grad_Y
        print(f"Nouveau coût : {f(x,y)}")
        if np.linalg.norm(x2 - x) + np.linalg.norm(y2 - y) < arret:
            print("great")
            break 
        x = x2 ; y = y2
    return np.transpose([x, y])

if __name__ == '__main__' :
    X = np.array([100, 150, 300, 300, 700, 750, 800, 800, 800, 950, 1000, 1200, 1400, 1413, 1500])*10
    Y = np.array([30, 450, 200, 300, 50, 50, 400, 250, 300, 10, 420, 350, 270, 200, 430])*10
    cities = np.transpose([X, Y])
    weights = np.ones(15)

    Problem = Satellites_problem(cities, weights, 2, 2)
    satellites = np.array([[5991.27125287, 3339.79379483],[8874.46812281, 2547.49928173]])

    plt.figure()
    plt.scatter(cities[:, 0], cities[:, 1], color='b', label='Villes')
    plt.scatter(satellites[:,0], satellites[:,1], color='g', label='Satellites initiaux')
    plt.show()

    satellites = tir(Problem.profit2D, Problem.gradient_profit2D, satellites)
    print("Positions des satellites optimisées :")
    print(satellites)
    print("Nouveau cout optimisé :"+str(Problem.profit(satellites[0], satellites[1])))
    plt.figure()
    plt.scatter(cities[:, 0], cities[:, 1], color='b')
    plt.scatter(satellites[:, 0], satellites[:, 1], color='r')
    plt.show()