import numpy as np
from math import *
from scipy.optimize import *
import random as rnd

l = 12742 # [km] largeur  approximative de la terre
L = 40030 # [km] longueur approximative de la terre

c = 3*10**8
f = 20*10**9

def euclidean_satellites_repartition(N_satellites, cities_coordinates, cities_weights, puissance = 100000, I_acceptable = 1):
    """
    N_satellites (int)                               : nombre de satellites disponibles pour couvrir la terre
    cities_coordinates (tableau de tuples d'entiers) : coordonnées des villes qu'on cherche à couvrir
    cities_weights (tableau d'entiers)               : poids d'une ville (importance relative par rapport aux autres)
    puissance (float)                                : puissance [W] d'un satellite (identique pour tous)
    I_acceptable (float)                             : intensité [W/m²] considérée comme acceptable pour 10 000 personnes

    Retourne :
    satellites_coordinates (tableau de tuples d'entiers) : coodonnées des N_satellites permettant d'offrir une couverture optimale
    """
    weight_sum = sum(cities_weights)
    cities_weights = np.array([w/weight_sum for w  in cities_weights])
    
    centroids = KMeans(cities_coordinates, cities_weights, n=N_satellites)
    
    centroids = np.array(centroids)
    #res = np.append(centroids[:, 0], centroids[:, 1])
    return centroids[:, 0], centroids[:, 1]

def euclidean_satellites_repartition2(N_satellites, cities_coordinates, cities_weights, puissance = 100000, I_acceptable = 1):
    """
    N_satellites (int)                               : nombre de satellites disponibles pour couvrir la terre
    cities_coordinates (tableau de tuples d'entiers) : coordonnées des villes qu'on cherche à couvrir
    cities_weights (tableau d'entiers)               : poids d'une ville (importance relative par rapport aux autres)
    puissance (float)                                : puissance [W] d'un satellite (identique pour tous)
    I_acceptable (float)                             : intensité [W/m²] considérée comme acceptable pour 10 000 personnes

    Retourne :
    satellites_coordinates (tableau de tuples d'entiers) : coodonnées des N_satellites permettant d'offrir une couverture optimale
    """
    weight_sum = sum(cities_weights)
    cities_weights = np.array([w/weight_sum for w  in cities_weights])
    
    #centroids = KMeans3(cities_coordinates, cities_weights, n=N_satellites)
    
    centroids = np.array(centroids)
    #res = np.append(centroids[:, 0], centroids[:, 1])
    return centroids[:, 0], centroids[:, 1]

def test_compare(N_satellites, cities_coordinates, cities_weights, puissance = 100000, I_acceptable = 1, return_after=99999):
    """
    N_satellites (int)                               : nombre de satellites disponibles pour couvrir la terre

    cities_coordinates (tableau de tuples d'entiers) : coordonnées des villes qu'on cherche à couvrir
    cities_weights (tableau d'entiers)               : poids d'une ville (importance relative par rapport aux autres)
    puissance (float)                                : puissance [W] d'un satellite (identique pour tous)
    I_acceptable (float)                             : intensité [W/m²] considérée comme acceptable pour 10 000 personnes

    Retourne :
    satellites_coordinates (tableau de tuples d'entiers) : coodonnées des N_satellites permettant d'offrir une couverture optimale
    """
    weight_sum = sum(cities_weights)
    cities_weights = np.array([w/weight_sum for w  in cities_weights])
    
    #centroids = KMeans2(cities_coordinates, cities_weights, return_after=return_after, n=N_satellites)
    
    centroids = np.array(centroids)
    #res = np.append(centroids[:, 0], centroids[:, 1])
    return centroids[:, 0], centroids[:, 1]


def KMeans(problem, centroids=None, n=-1, tol=0.001, max_iter=300):
    if n == -1:
        n = problem.N_satellites
    data = problem.cities_coordinates
    weights = problem.cities_weights
    
    
    if centroids is None:
        centroids = np.zeros((n, 2))
        for j in range(n):
            centroids[j] = data[floor(rnd.random()*len(data))][:2]
    

    for _ in range(max_iter):
        classif = {i:{} for i in range(n)}
        for i in range(len(data)):
            dist = [np.linalg.norm(data[i] - c) for c in centroids]

            closest_cluster = dist.index(min(dist))
            classif[closest_cluster][i] = data[i]
            
        prev_centroids = centroids.copy()
        for cluster in range(len(classif)):
            if len(classif[cluster]) == 0:
                centroids[cluster] = data[np.random.randint(0, n)]
            else:
                indexes = [i for i in classif[cluster].keys()]
                centroids[cluster] = np.average(data[indexes], axis=0, weights=weights[indexes])
        
        optimized = True
        
        for c in range(len(centroids)):
            old_c = prev_centroids[c]
            new_c = centroids[c]
            if np.sum(new_c - old_c) > tol:
                optimized = False
        if optimized:
            break            
    problem.satellites_position = centroids
    problem.method = "kmeans"
    return centroids

# Idée : chaque point a son cluster initialement. A chaque itération, trier les distances entre chaque centroïde en ordre croissant.
# Joindre la première paire la plus proche qui respecte encore les >80% de couverture quand on fait la moyenne des 2 centroïdes

def dist(p1, p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1] - p2[1])**2)

def friss_ratio(R):
    return (c/f/(4*np.pi*R))**2

def score(p1, p2, z=0.0000000001):
    """
    Args:
        p1: first satellite position and weight (x1, y1, w1)
        p2: second satellite position and weight (x2, y2, w2)
        w1: first satelllite weight
        w2: second satellite weight
        z:  power ratio acceptability treshold
    """
    w1, w2 = p1[2], p2[2]
    p1, p2 = np.array(p1[:2]), np.array(p2[:2])
    distance = dist(p1, p2)
    new_satellite_position = weighted_mid(p1, p2, w1, w2)
    power_acceptability_p1 = friss_ratio(dist(p1, new_satellite_position))/(z*w1)
    power_acceptability_p2 = friss_ratio(dist(p2, new_satellite_position))/(z*w2)
    return distance#+ (1/power_acceptability_p1 + 1/power_acceptability_p2) * 1000

def weighted_mid(p1, p2, w1, w2):
    return p1*w1/(w1+w2) + p2*w2/(w1+w2)

# prendre en compte la hauteur du satellite
def KMeans2(problem, centroids=None, tol=0.001, max_iter=300, return_after=-1):
    n = problem.N_satellites
    data = problem.cities_coordinates
    weights = problem.cities_weights
    centroids = []
    for i in range(len(data)):
        centroids.append((*data[i], weights[i]))
    centroids = np.array(centroids)
    i = 0
    # ((score, 0, 0), (x1, y1, w1), (x2, y2, w2))
    # 0 are dummys

    scores = []
    for i1 in range(len(centroids) - 1):
        for i2 in range(i1+1, len(centroids)):
            scores.append(((score(centroids[i1], centroids[i2]), 0, 0), centroids[i1], centroids[i2]))
    scores = np.array(scores)
    
    while i < max_iter and len(centroids) > n:
        sorted_indices = np.argsort(scores[:, 0, 0])
        sorted_scores = scores[sorted_indices]
        best = sorted_scores[0]
        p1, p2, w1, w2 = best[1][:2], best[2][:2], best[1][2], best[2][2] 
        new_pos = weighted_mid(p1, p2, w1, w2)
        
        centroids = np.delete(centroids, [np.equal(c, best[1]).all() or np.equal(c, best[2]).all() for c in centroids], 0)
        scores = np.delete(scores, [np.equal(s[1], best[1]).all() or np.equal(s[2], best[1]).all() or np.equal(s[1], best[2]).all() or np.equal(s[2], best[2]).all() for s in scores], 0)
        tmp = []
        new_pos_w = (w1+w2)/2
        for centroid in centroids:
            tmp.append(((score(centroid, (*new_pos, new_pos_w)), 0, 0), centroid, (*new_pos, new_pos_w)))
        
        centroids = np.append(centroids, [(*new_pos, new_pos_w)], axis=0)
        scores = np.append(scores, tmp, axis=0)
        
        
        i+=1
        if len(centroids) <= return_after:
            print("--------")
            problem.satellites_position = centroids[:, :2]
            return 
    problem.satellites_position = centroids[:, :2]
    problem.method = "kmeans2"
    return centroids[:, :2]


# Idée: La couverture d'une ville est le min entre la somme des 1/R² pour chaque satellite et le seuil d'une ville

def score3(points, weights, centroids, excluded_centroid):
    """
    Args:
        point: tuple (x, y, w)
        params centroids: tableau de tuples (x, y)
    
    Returns:
        float: score
    """
    return sum([min(weights[ip], sum([1/H**2 if (H:=dist(points[ip], c)) else 1 for c in centroids if not np.equal(c, excluded_centroid).all()])) for ip in range(len(points))])

# Idée: Un satellite par ville initialement, retirer celui de moindre couverture et re-run KMeans 
# jusqu'à atteindre le nombre de satellite requis

def KMeans3(problem, centroids=None, tol=0.001, max_iter=300):
    n = problem.N_satellites
    data = problem.cities_coordinates
    weights = problem.cities_weights
    centroids = np.copy(data)

    i = 0
    # ((score, 0, 0), (x1, y1, w1), (x2, y2, w2))
    # 0 are dummys
    while i < max_iter and len(centroids) > n:
        scores = []
        for i1 in range(len(centroids)):
            print("Scoring", i1)
            scores.append(((score3(data, weights, centroids, centroids[i1]), 0), centroids[i1]))
        scores = np.array(scores)

        sorted_indices = np.argsort(scores[:, 0, 0])
        sorted_scores = scores[sorted_indices]

        worst = sorted_scores[-1]   

        centroids = np.delete(centroids, [np.equal(c, worst[1]).all() for c in centroids], 0)
        print("Kmeans", i)
        centroids = KMeans(problem, tol=tol, centroids=centroids, n=len(centroids), max_iter=max_iter)
        i+=1
    problem.satellites_position = centroids
    problem.method = "kmeans3"
