import matplotlib.pyplot as plt
import numpy as np

from kmeans import euclidean_satellites_repartition, test_compare

l = 12742 # [km] largeur  approximative de la terre
L = 40030 # [km] longueur approximative de la terre

# 1 Génération de points aléatoires
X = np.random.rand(20)*L
Y = np.random.rand(20)*l
cost = np.random.randint(1, 50, 20)
N_satellites = 5

def test(func, i=-1, title="None"):
    if i >= 0:
        Xs, Ys = func(N_satellites, np.vstack((X,Y)).T, cost, return_after=i)
    else:
        Xs, Ys = func(N_satellites, np.vstack((X, Y).T), cost)
    a = str(i)
    plt.figure()
    for x,y,c in zip(X,Y,cost) :
        plt.scatter(x, y, c, 'b')
    for i in range(len(Xs)) :
        plt.plot(Xs[i], Ys[i], 'or')
        for r in range(100, 5001, 700) :
            circle = plt.Circle((Xs[i], Ys[i]), r, color='r', fill=False)
            plt.gca().add_patch(circle)
    plt.axis('equal')

    plt.title(title + " " + a)
    plt.show()

#test(euclidean_satellites_repartition, 20, "Kmeans")
for i in range(len(X), N_satellites-1, -1):
    test(test_compare, i, "Pas Kmeans")

