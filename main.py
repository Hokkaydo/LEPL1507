import pandas as pd
from spherical_satellites_repartition import spherical_satellites_repartition
from euclidean_satellites_repartition import euclidean_satellites_repartition
import sys


if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("Syntaxe: python main.py <euclidian|spherical>")
        sys.exit(1)
    if sys.argv[1] not in ["euclidian", "spherical"]:
        print("Syntaxe: python main.py <euclidian|spherical>")
        sys.exit(1)
        
    file_name = input("Nom du fichier avec les données : ")
    N_satellites = int(input("Nombre de satellites : "))
    print()
    
    if sys.argv[1] == "euclidean":
        sat_coordinates, cost = euclidean_satellites_repartition(N_satellites, file_name, verbose=True)
    elif sys.argv[1] == "spherical":
        sat_coordinates, cost = spherical_satellites_repartition(N_satellites, file_name, verbose=True)
        
    sat = pd.DataFrame()
    sat["Rayon"]     = sat_coordinates[:,0]
    sat["Latitude"]  = sat_coordinates[:,1]
    sat["Longitude"] = sat_coordinates[:,2]
    print("Merci d'avoir utilisé notre application pour trouver la position de vos satellites.")

    print("Où souhaitez-vous que nous imprimions les coordonnées finales des satellites ?")
    answer = input("[stdout/<filename>]: ")
    if answer == "stdout" : print(sat)
    else                  : sat.to_csv(answer)
    print("\nBonne journée :)")

    
    
