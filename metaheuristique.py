import random as r
import math as m
import ville as v


def quality(chemin):
    distance = 0
    n = len(chemin)

    for i in range(n - 1):
        distance += v.haversine(chemin[i], chemin[i + 1])
    
    distance += v.haversine(chemin[-1], chemin[0])
    return distance


def Recherche_aléatoire(chemin=v.ville_list.copy(), n=3):
    global best
    best = chemin
    best_distance = quality(chemin)
    for _ in range(n):
        r.shuffle(chemin)
        chemin_distance = quality(chemin)
        if chemin_distance < best_distance:
            best = chemin.copy()
            best_distance = chemin_distance
    return best, best_distance


def Recherche_locale(chemin=v.ville_list.copy(), n=100):
    best = chemin.copy()
    best_distance = quality(best)
    for _ in range(n):
        voisin = best.copy()
        i1, i2 = r.sample(range(len(voisin)), 2)
        voisin[i1], voisin[i2] = voisin[i2], voisin[i1]
        voisin_distance = quality(voisin)
        if voisin_distance < best_distance:
            best = voisin
            best_distance = voisin_distance

    return best, best_distance


def Hill_climbing(chemin=v.ville_list.copy(), n=1000):
    current = chemin.copy()
    current_distance = quality(current)

    improved = True
    iteration = 0

    while improved and iteration < n:
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

    return current, current_distance  # current is the best


def generate_neighbor(chemin, i, j):#the 2 opt method   
    if i > j:
        i, j = j, i
    new_chemin = chemin[:i] + list(reversed(chemin[i:j+1])) + chemin[j+1:]
    return new_chemin


def Recuit_Simule(
    chemin=v.ville_list.copy(),
    T_init=10.0,
    T_min=0.1,
    alpha=0.995,# the cooling factor
    time_to_cool=50  # Reduced from 100 for faster execution
):
    
   
    current = chemin.copy()
    current_distance = quality(current)

    
    best = current.copy()
    best_distance = current_distance

    T = T_init

    while T > T_min:
        n = len(current)
        for c in range(time_to_cool):
            
            i, j = r.sample(range(n), 2)

            
            voisin = generate_neighbor(current, i, j)
            voisin_distance = quality(voisin)
            delta = voisin_distance - current_distance

            if delta < 0:# the new solution is better than the current one
                
                current = voisin
                current_distance = voisin_distance
            else:
                
                Metropolis = m.exp(-delta / T)#  we accept  with a probability
                if r.random() < Metropolis: 
                    current = voisin
                    current_distance = voisin_distance

            if current_distance < best_distance:
                best = current.copy()
                best_distance = current_distance

        
        T *= alpha

    return best, best_distance
def Tabu_Search(
    chemin=v.ville_list.copy(),
    tabu_tenure=15,
    iterations=500,
    candidate_size=50  # Only evaluate a sample of moves, not all
):
    n = len(chemin)

    
    current = chemin.copy()
    current_distance = quality(current)

    best = current.copy()
    best_distance = current_distance

    tabu_list = {}#the tabu list is a dictionary

    for itr in range(iterations):

        best_move = None
        best_m_distance = float("inf")  
        best_move_is_tabu = False

        # Sample candidate moves instead of evaluating all
        candidates = []
        for _ in range(min(candidate_size, n * (n - 1) // 2)):
            i, j = r.sample(range(n), 2)
            if i > j:
                i, j = j, i
            candidates.append((i, j))
        
        # Remove duplicates
        candidates = list(set(candidates))

        for move in candidates:
            i, j = move

            voisin = generate_neighbor(current, i, j)
            d = quality(voisin)

            is_tabu = move in tabu_list and tabu_list[move] > 0

            if is_tabu and d < best_distance:
                is_tabu = False  # Aspiration criterion

            if (not is_tabu) and d < best_m_distance:
                best_move = move
                best_m_distance = d
                best_move_is_tabu = False

            if is_tabu and best_move is None and d < best_m_distance:
                best_move = move
                best_m_distance = d
                best_move_is_tabu = True

        if best_move is None:
            # If all moves are tabu, pick a random one
            i, j = r.sample(range(n), 2)
            if i > j:
                i, j = j, i
            best_move = (i, j)
            current = generate_neighbor(current, i, j)
            current_distance = quality(current)
        else:
            i, j = best_move
            current = generate_neighbor(current, i, j)
            current_distance = best_m_distance

        if current_distance < best_distance:
            best = current.copy()
            best_distance = current_distance

        # Age tabu list
        for m in list(tabu_list.keys()):
            tabu_list[m] -= 1
            if tabu_list[m] <= 0:
                del tabu_list[m]

        # Add reverse move to tabu list
        tabu_list[(j, i)] = tabu_tenure

    return best, best_distance




def Genetic_Algorithm(
    population_size=100,
    generations=500,

    elite_size=15,
    path = v.ville_list.copy()

):
   

    


   
    def fitness(ind):
        d = quality(ind)
        return 1.0 / (1 + d)


    def selection(population, k=5):
        competitors = r.sample(population, k)
        competitors.sort(key=lambda ind: fitness(ind), reverse=True)
        return competitors[0]


    def crossover(parent1, parent2):
        size = len(parent1)
        a, b = sorted(r.sample(range(size), 2))

        child = [None] * size
        child[a:b+1] = parent1[a:b+1]

        pos = 0
        for city in parent2:
            if city not in child:
                while child[pos] is not None:
                    pos += 1
                child[pos] = city

        return child

    
    

    
    # Initialize population with random shuffles
    population = []
    for _ in range(population_size):
        ind = path.copy()
        r.shuffle(ind)
        population.append(ind)

   
    best_ind = min(population, key=lambda ind: quality(ind))
    best_dist = quality(best_ind)

    
    for gen in range(generations):

        
        population.sort(key=lambda ind: fitness(ind), reverse=True)

      
        new_population = population[:elite_size]

       
        while len(new_population) < population_size:
            parent1 = selection(population)
            parent2 = selection(population)
            child = crossover(parent1, parent2)
            
            new_population.append(child)

        population = new_population

        
        current_best = min(population, key=lambda ind: quality(ind))
        current_dist = quality(current_best)

        if current_dist < best_dist:
            best_dist = current_dist
            best_ind = current_best.copy()

    return best_ind, best_dist



