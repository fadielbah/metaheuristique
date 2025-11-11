import random as r
import ville as v
def quality(chemin):
    distance=0
    n=chemin.__len__()

    for i in range(n-1):
        distance+=v.haversine(chemin[i],chemin[i+1])
    return distance
def Recherche_aléatoire(chemin=v.ville_list.copy(),n=3):
    global best
    best = chemin
    best_distance=quality(chemin)
    for i in range(n):
        r.shuffle(chemin)
        chemin_distance=quality(chemin)
        if chemin_distance<best_distance:
            best=chemin
            best_distance=chemin_distance
    return best
def Recherche_locale(chemin=v.ville_list.copy(), n=100):
    best = chemin.copy()
    best_distance = quality(best)
    for i in range(n):
        voisin = best.copy()
        i1, i2 = r.sample(range(len(voisin)), 2)
        voisin[i1], voisin[i2] = voisin[i2], voisin[i1]
        voisin_distance = quality(voisin)
        if voisin_distance < best_distance:
            best = voisin
            best_distance = voisin_distance

    return best
def Hill_climbing(chemin=v.ville_list.copy(), max_iterations=1000):
    current = chemin.copy()
    current_distance = quality(current)

    improved = True
    iteration = 0

    while improved and iteration < max_iterations:
        improved = False
        iteration += 1

        voisin = current.copy()
        i1, i2 = r.sample(range(len(voisin)), 2)
        voisin[i1], voisin[i2] = voisin[i2], voisin[i1]

        voisin_distance = quality(voisin)

        if voisin_distance < current_distance:
            current = voisin
            current_distance = voisin_distance
            improved = True

    return current


