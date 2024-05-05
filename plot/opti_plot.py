import numpy as np
import matplotlib.pyplot as plt

cities = np.geomspace(300, 3000, 10, dtype=int, endpoint=True)
time = np.array([0.29793263762026967, 0.41579046199125436, 0.613207666901085, 0.6783901230999358, 0.9237121247539807, 1.1918031609777733, 1.5380198989630218, 1.9945893670466845, 2.363046839537424, 3.0503406438742156])

plt.loglog(cities, time, 'o', label="Mesures")
plt.loglog(cities, 1e-3*cities, label="$\mathcal{O}(|V|)$")
plt.xlabel("Nombre de villes")
plt.ylabel("Temps d'exécution [s]")
plt.grid()
plt.title("Temps d'exécution d'une itération de la méthode du gradient \npour un nombre de satellites fixes (2) et un nombre de villes variable")
plt.legend()
plt.savefig("opti_complexity_cities.pdf")

