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
=rr^(θ,ϕ), where
r^(θ,ϕ)=sinθcosϕx^+sinθsinϕy^+cosθz^.
Thus the components of the radius vector with respect to the "spherical basis" (r^(θ,ϕ),θ^(θ,ϕ),ϕ^(θ,ϕ)) AT THE POINT with spherical coordinates (r,θ,ϕ) (it is VERY important to realize that the spherical unit vectors are really vector fields, they vary from point to point!) are NOT (r,θ,ϕ). Instead, they are (r,0,0)! Indeed, θ and ϕ

, having no physical dimension, cannot be the components of a vector.

When r1,θ1,ϕ1
and r2,θ2,ϕ2 are known for two vectors p1,p2, we have
p1=r1r^(θ1,ϕ1)andp2=r2r^(θ2,ϕ2).
(With respect to the spherical basis, we are forced to use different unit vectors r^(θ1,ϕ1) and r^(θ2,ϕ2)! This is a striking difference between cartesian coordinates and spherical coordinates.) Hence:
p1⋅p2=[r1r^(θ1,ϕ1)]⋅[r2r^(θ2,ϕ2)]=r1r2r^(θ1,ϕ1)⋅r^(θ2,ϕ2)=r1r2(sinθ1cosϕ1x^+sinθ1sinϕ1y^+cosθ1z^)⋅(sinθ2cosϕ2x^+sinθ2sinϕ2y^+cosθ2z^)=r1r2(sinθ1sinθ2cosϕ1cosϕ2+sinθ1sinθ2sinϕ1sinϕ2+cosθ1cosθ2)=r1r2[sinθ1sinθ2cos(ϕ1−ϕ2)+cosθ1cosθ2].
This is the formula you have given in your post. When we put r1=r2=1 and call ω the angle between p1 and p2, we get a fairly established formula, namely
cosω=sinθ1sinθ2cos(ϕ1−ϕ2)+cosθ1cosθ2
since p1⋅p2=r1r2cosω=cosω

.

EDIT: never mind, your question ended up at the top of the list because someone recently edited your OP. My bad for not noticing the 2016 date in due time ...
Share
Cite
Improve this answer
Follow
edited Sep 3, 2020 at 14:13
answered Sep 3, 2020 at 13:55
Rindler98's user avatar
Rindler98
48244 silver badges1212 bronze badges
Add a comment
1

You can write the dot product of two vectors p,q
in the form ∑ijpiAijqj where the matrix A is a kind of "metric" that defines the inner product. In cartesian 3D coordinates this metric is a diagonal matrix, A=diag(1,1,1)

, but in the spherical coordinates it takes a different form (and depends on position).
Share
Cite
Improve this answer
Follow
answered Jun 25, 2020 at 6:06
physics's user avatar
physics
31411 silver badge44 bronze badges

    Should one transform the metric like a covariant tensor to end up with the formula? – 
    Emil
    Jun 25, 2020 at 6:58 

Precisely. And in the case of Euclidean metric in the Cartesian basis, the transformation is rather simple, given by JTJ

    of the basis transformation, see en.wikipedia.org/wiki/Metric_tensor#Euclidean_metric. The metric is useful since it also gives you immediately the volume element, if one needs to do integration. – 
    physics
    Jun 27, 2020 at 0:39

Add a comment
Your Answer

Sign up or log in
Post as a guest
Name
Email

Required, but never shown

By clicking “Post Your Answer”, you agree to our terms of service and acknowledge you have read our privacy policy.
Not the answer you're looking for? Browse other questions tagged

    coordinate-systemsvectors

or ask your own question.

    The Overflow Blog

    Defining socially responsible AI: How we select partners
    Featured on Meta
    Changing how community leadership works on Stack Exchange: a proposal and...
    Our partnership with Google and commitment to socially responsible AI

Related
85
What is the physical significance of dot & cross product of vectors? Why is division not defined for vectors?
0
Conversion of motion equation from Cartesian to Polar coordinates: Is covariant differentiation necessary?
0
Adding rotations onto a vector
1
Superposition at π/4
phase-offset of elliptically polarised light
0
Different results when using generalized coordinates?
4
Variables of an SO(3)-invariant function (hamiltonian)
2
How velocities transform from Cartesian to Polar coordinates
0
How do I write the gradient in angular coordinates (θ1
, θ2
, θ3
)?
Hot Network Questions

    Is using content from publicly available sources (without alteration) for my own course material academic dishonesty?
    first apartment ever need pet advice
    How to prevent GTK inspector from opening when opening an app from the terminal?
    What is the mountain lake in this photo?
    Can one get a liquidity premium as a retail investor?
    What are theistic responses to Graham Oppy's argument for atheism from naturalism?
    Can mountains form in rings?
    6 year old won't go to the bathroom by herself anymore, because of being scared. What to do?
    Search and replace regular expressions
    Reconstruct a list of strings from its prefixes
    PhD supervisor complaining about not getting paid for supervision
    Great battles in the history of mathematics
    A short story about a woman in a life-preservation capsule
    Slice knots in 3-manifolds
    How can I add a marker or meshpoint to the start and end of a ListLinePlot or DateListPlot
    Is the term "dumping tours" a generic English term?
    Conflict of interests of reviewing paper if I have talked to the author
    How to calculate the orientation of a point at another point in QGIS
    Could mountains form on anhydrous planets?
    Is it bad practice for audio inputs and outputs to share a common ground?
    (TAoE) JFET voltage reference derivation
    How to stop mapping on true results for large lists?
    Do 1.5% of lithium-ion batteries overheat, explode, or catch fire each year?
    Why doesn't Washington want to enact a law to punish all currency manipulators, including China?

Question feed

Physics

    Tour
    Help
    Chat
    Contact
    Feedback

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

def polar_cos(theta1, phi1, theta2, phi2):
    return sin(theta1)*sin(theta2)*cos(phi1 - phi2) + cos(theta1)*cos(theta2)

def spherical_kmeans(cities_coordinates, cities_weigths, N_satellites=2, max_iter=300):

    cities_coordinates/= np.linalg.norm(cities_coordinates)
    n = len(cities_coordinates)
    centroids = np.zeros((N_satellites, cities_coordinates.shape[1]))
    for i in range(N_satellites):
        centroids[i] = cities_coordinates[rnd.randrange(n)]
    old_centroids = None
    iteration = 0
    while old_centroids is None or iteration < max_iter:
        old_centroids = centroids
        y = np.argmin(centroids@cities_coordinates.T, axis=0)
        #print(y)
        for k in range(N_satellites):
            Xk = cities_coordinates[[y[i] == k for i in range(n)]]
            s = np.sum(Xk, axis=0)
            
            norm = np.linalg.norm(s)
            if len(s) == 0 or norm == 0:
                centroids[k] = cities_coordinates[rnd.randrange(n)]
                continue
            centroids[k] = s/norm
        #print("iter =", iteration)
        iteration+=1
    #print(centroids)
    return centroids
