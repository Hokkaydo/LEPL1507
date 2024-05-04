import pandas as pd
import numpy as np

def write_file(file_name, weights, x, y) :
    """Fonction pour écrire les coordonnées et poids de villes dans un fichier csv
    
    Input :
    file_name (str)              : nom du fichier dans lequel les données doivent être écrites
    weights   (nparray de float) : poids des villes
    x         (nparray de float) : premier vecteur de coordonnées. Ceci correspond à la coordonnée horizontale pour un problème euclidien et à la latitude pour un problème sphérique
    y         (nparray de float) : second vecteur de coordonnées. Ceci correspond à la coordonnée verticale pour un problème euclidien et à la longitude pour un problème sphérique
    
    Result :
    Les données ont été écrites dans le fichier file_name au format csv avec quatre colonnes : les indices, les poids et les deux coordonnées des villes. Il n'y a pas de ligne de titre dans le fichier.
    """
    database = pd.DataFrame({"name":np.zeros(len(weights)), "weights": weights, "x": x, "y": y})
    database.to_csv(file_name)

if __name__ == '__main__' :
    n = int(input("Nombre de villes : "))
    file_name = input("Nom du fichier : ")
    weights = np.random.randint(0, 100000, n)
    x = 180*np.random.rand(n) - 90 # lat
    y = 360*np.random.rand(n) - 180 # long
    write_file(file_name, weights, x, y)