import matplotlib.pyplot as plt
import numpy as np

from euclidean_satellites_repartition import euclidean_satellites_repartition

l = 12742 # [km] largeur  approximative de la terre
L = 40030 # [km] longueur approximative de la terre

# 1 Génération de points aléatoires
X = np.random.rand(20)*L
Y = np.random.rand(20)*l
cost = np.random.randint(1, 50, 20)
N_satellites = 5

Xs, Ys = euclidean_satellites_repartition(N_satellites, np.vstack((X,Y)).T, cost)

plt.figure()
for x,y,c in zip(X,Y,cost) :
    plt.scatter(x, y, c, 'b')
for i in range(N_satellites) :
    plt.plot(Xs[i], Ys[i], 'or')
    for r in range(100, 5001, 700) :
        circle = plt.Circle((Xs[i], Ys[i]), r, color='r', fill=False)
        plt.gca().add_patch(circle)
plt.axis('equal')
plt.show()