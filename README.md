# LEPL1507
Projet 4 en mathématiques appliquées - Développement d'une couverture satellitaire optimale
-

Le projet se présente sous forme de 2 modules : `euclidean_satellites_repartition` et `spherical_satellites_repartition`.

Le premier permet de résoudre le problème sur une surface plane 2D tandis que le second permet de résoudre le problème sur un volume sphérique en 3D. 

Le package nécessite Python2.7+ ainsi que l'installation des packages listés dans le fichier `requirements.txt` via la commande `pip install -r requirements.txt`

Le fichier `main.py` présente un exemple d'utilisation de ces 2 modules. Il peut être exécuté via la commande
```sh
    python3 main.py <euclidean|spherical>
```