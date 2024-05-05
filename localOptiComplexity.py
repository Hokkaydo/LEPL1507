from kmeans import *
from optimization import *
from satellites_problem import *
from utilities import *
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter

R = 6371
H = 35786 + 6371
P = 100e3
I_necessary = (10**((-67-30)/10))

global problem
problem = SatellitesProblem(dimension=3, R=R, H=H, P=P, I_necessary=I_necessary)


optimization = Optimization(problem)
optimization.max_iter = 1
N = np.geomspace(10, 1000, 10, dtype=int)
V = np.arange(1000, 1001, 200)
elapsed_times_total = np.zeros((len(N), len(V)))
for j in range(len(V)):
    print(f"Nombre de villes : {V[j]}")
    elapsed_times = np.zeros(len(N))
    for i in range(len(N)):
        print(f"Nombre de satellites : {N[i]}")
        x, y = (np.random.rand(V[j])-0.5)*180, (np.random.rand(V[j])-0.5)*360
        coordinates = np.array([R*np.ones(V[j]), x, y]).T
        weights = np.random.rand(V[j])
        x_sat = (np.random.rand(N[i])-0.5)*180
        y_sat = (np.random.rand(N[i])-0.5)*360
        sat_coordinates = np.array([H*np.ones(N[i]), x_sat, y_sat]).T
        problem.cities_coordinates = coordinates
        problem.cities_weights = weights
        problem.N_satellites = N[i]
        problem.sat_coordinates = sat_coordinates
        start = perf_counter()
        optimization.solve()
        end = perf_counter()
        elapsed_times[i] = end-start
        print(f"Temps écoulé : {elapsed_times[i]}")
    elapsed_times_total[:,j] = elapsed_times

for i in range(len(V)):
    plt.loglog(N, elapsed_times_total[:,i], 'o', label="Mesures")
    #plt.loglog(results2[:, 0], 2e-3*results2[:, 0], label = "$\mathcal{O}(|S|)$")
    plt.loglog(N, 2*1e-2*N, label = "$\mathcal{O}(|S|)$")

plt.title("Temps d'exécution d'une itération de la méthode du gradient\n pour un nombre de villes fixes (1000) et un nombre de satellites variable")
plt.xlabel("Nombre de satellites")
plt.ylabel("Temps d'exécution [s]")
plt.legend()
plt.grid()
plt.savefig("plot/opti_complexity_satellites.pdf")
plt.show()

