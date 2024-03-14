import numpy as np

print("Bonjour et bienvenue dans Euler-opti, une application permettant d'optimiser la position de satellites afin d'offrir une couverture internet.")
print("Nous sommes cinq jeunes ingénieurs civils en mathématiques appliquées.")
print("Concepteurs : Bertrand Laura, Doat Matthieu, Orékhoff Alexandre, Tavier Aloïs et Van Hees Charles.")

while (True) :
    print("Pour commencer, tapez start. Si vous désirez plus d'informations, tapez help. Pour terminer la session, tapez exit.")
    instruction = input()
    if   (instruction == "exit")  : break
    elif (instruction == "help")  :
        ...
    elif (instruction == "start") :
        while (True) :
            cities_file = input("Chemin vers le fichier avec les coordonnées et poids des villes : ")
            n_cit = 0
            cities_coord   = np.array()
            cities_weights = np.array()
            try :
                with open(cities_file, 'r') as file :
                    for city in file :
                        n_cit += 1
                        ...
                break
            except :
                print("Le fichier que vous avez entré n'existe pas...")
    else : print("La commande que vous avez entrée n'existe pas encore...")

print("Merci pour votre visite. Nous vous souhaitons une agréable journée.")