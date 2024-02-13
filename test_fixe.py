import matplotlib.pyplot as plt
import numpy as np

from euclidean_satellites_repartition import euclidean_satellites_repartition

X = np.array([100, 150, 300, 300, 700, 750, 800, 800, 800, 950, 1000, 1200, 1400, 1413, 1500])*10
Y = np.array([30, 450, 200, 300, 50, 50, 400, 250, 300, 10, 420, 350, 270, 200, 430])*10
cost = np.array([1, 4, 2, 10, 5, 3, 8, 1, 9, 2, 5, 8, 3, 1, 6])
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