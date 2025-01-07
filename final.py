import random

num_pairs = 9
num_entity = 10
num_child = 5
num_generation = 10
tournament_size = 3  
mutation_rate = 0.1 

products = [
    {"name": "Product 1", "id": 1, "expiration": 3, "value": 15, "count": 4, "conflict": [1, 10]},
    {"name": "Product 2", "id": 2, "expiration": 6, "value": 10, "count": 2, "conflict": [5, 4]},
    {"name": "Product 3", "id": 3, "expiration": 5, "value": 30, "count": 10, "conflict": []},
    {"name": "Product 4", "id": 4, "expiration": 4, "value": 25, "count": 4, "conflict": [7]},
    {"name": "Product 5", "id": 5, "expiration": 9, "value": 20, "count": 3, "conflict": [6]},
    {"name": "Product 6", "id": 6, "expiration": 1, "value": 50, "count": 4, "conflict": [1]},
    {"name": "Product 7", "id": 7, "expiration": 7, "value": 35, "count": 5, "conflict": [10, 5]},
    {"name": "Product 8", "id": 8, "expiration": 8, "value": 25, "count": 1, "conflict": [8, 1]},
    {"name": "Product 9", "id": 9, "expiration": 5, "value": 50, "count": 3, "conflict": [3, 2]},
    {"name": "Product 10", "id": 10, "expiration": 5, "value": 20, "count": 3, "conflict": [1, 5]},
]

def has_conflict(pair):
    frs_product = products[pair[0] - 1]
    sec_product = products[pair[1] - 1]
    return sec_product["id"] in frs_product["conflict"] or frs_product["id"] in sec_product["conflict"]




def check_constraints(p1, p2, product_counts, product_expirations): 
    return (not has_conflict((p1, p2)) and 
            product_counts[p1] > 0 and product_counts[p2] > 0 and
            product_expirations[p1] > 0 and product_expirations[p2] > 0) 



def generate_entity(num_pairs): 
    valid_pairs = [] 
    product_counts = {product['id']: product['count'] for product in products}
    product_expirations = {product['id']: product['expiration'] for product in products}
    for _ in range(num_pairs): 
        valid = False
        while not valid:
            pair = random.sample(products, 2) 
            p1, p2 = pair[0]['id'], pair[1]['id'] 
            if check_constraints(p1, p2, product_counts, product_expirations):
                valid_pairs.append((p1, p2)) 
                product_counts[p1] -= 1 
                product_counts[p2] -= 1 
                product_expirations[p1] -= 1 
                product_expirations[p2] -= 1 
                valid = True
    return  valid_pairs




def generate_primary_population(num_entity, num_pairs):
    population = []
    for _ in range(num_entity):
        population.append(generate_entity(num_pairs))
    return population

def fitness(individual):
    profit = 0
    time_elapsed = 0
    s = []
    for trip in individual:
        if time_elapsed >= max(products, key=lambda x: x["expiration"])["expiration"]:
            break
        for prod_num in trip:
            s.append(prod_num)
            product = products[prod_num - 1]
            if time_elapsed < product["expiration"]:
                profit += product["value"]
            else:
                profit -= product["value"]
        time_elapsed += 1
    return profit

def tournament_selection(population, tournament_size):
    tournament = random.sample(population, tournament_size)
    winner = max(tournament, key=lambda x: fitness(x))
    return winner


def reproduction(parents):
    crossover_point = random.randint(2, 7)
    while True:
        parent1 = tournament_selection(parents, tournament_size)
        parent2 = tournament_selection(parents, tournament_size)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        
        product_counts = {product['id']: product['count'] for product in products}
        product_expirations = {product['id']: product['expiration'] for product in products}
        
        valid = True
        for p1, p2 in child:
            if not check_constraints(p1, p2, product_counts, product_expirations):
                valid = False
                break
            product_counts[p1] -= 1
            product_counts[p2] -= 1
            product_expirations[p1] -= 1
            product_expirations[p2] -= 1

        if valid:
            return child




def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            while True:
                pair = [random.randint(1, 10), random.randint(1, 10)]
                if not has_conflict(pair):
                    individual[i] = pair
                    break
    return individual

def select_survivors(population, n):
    sorted_population = sorted(population, key=lambda x: fitness(x), reverse=True)
    survivors = sorted_population[:n]
    return survivors

population = generate_primary_population(num_entity, num_pairs)

for generation in range(num_generation):
    children = []
    for _ in range(num_child):
        child = reproduction(population)
        child = mutate(child, mutation_rate)
        children.append(child)
    population.extend(children)
    population = select_survivors(population, num_entity)

   
    # print(f"Generation {generation + 1}:")
    # for individual in population:
    #     print(individual, fitness(individual))

  
print("____________________________________")
for i in  range(len(population)):
    print(population[i] , fitness(population[i])) 


print("\n")
best_individual = max(population, key=lambda x: fitness(x))
print("\nBest Answer in all generation:", best_individual ,fitness(best_individual) )
# print(fitness(best_individual))
