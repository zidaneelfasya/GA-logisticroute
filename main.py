import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Parameters for Genetic Algorithm
population_size = 100  # Number of individuals in the population
generations = 500  # Number of generations to evolve
mutation_rate = 0.1  # Probability of mutation
elitism_count = 2  # Number of best individuals to carry forward

# Data jarak dari tabel (dalam km)
file_path = "data_route.csv"
data = pd.read_csv(file_path, header=None)  # header=None karena file hanya berisi angka

# Mengonversi DataFrame menjadi matriks numpy
distance_matrix = data.values
num_locations = distance_matrix.shape[0]

# Initialize population
def initialize_population(size, num_locations):
    population = []
    for _ in range(size):
        route = list(range(1, num_locations))  # Exclude the depot (index 0)
        random.shuffle(route)
        route = [0] + route + [0]  # Start and end at the depot
        population.append(route)
    return population

# Calculate route distance
def calculate_route_distance(route, distance_matrix):
    distance = 0
    for i in range(len(route) - 1):
        distance += distance_matrix[route[i]][route[i + 1]]
    return distance

# Evaluate population fitness
def evaluate_population(population, distance_matrix):
    fitness = []
    for route in population:
        distance = calculate_route_distance(route, distance_matrix)
        fitness.append(1 / distance)  # Fitness is inversely proportional to distance
    return fitness

# Select parents using tournament selection
def select_parents(population, fitness, tournament_size=5):
    parents = []
    for _ in range(2):  # Select two parents
        tournament = random.sample(list(zip(population, fitness)), tournament_size)
        winner = max(tournament, key=lambda x: x[1])  # Higher fitness wins
        parents.append(winner[0])
    return parents

# Order Crossover
def order_crossover(parent1, parent2):
    start, end = sorted(random.sample(range(1, len(parent1) - 1), 2))
    offspring = [-1] * len(parent1)
    offspring[start:end] = parent1[start:end]
    
    pos = end
    for gene in parent2[1:-1]:
        if gene not in offspring:
            if pos >= len(parent1) - 1:
                pos = 1
            offspring[pos] = gene
            pos += 1
    offspring[0], offspring[-1] = 0, 0  # Ensure depot at start and end
    return offspring

# Mutate a route
def mutate(route, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(1, len(route) - 1), 2)  # Exclude depot
        route[i], route[j] = route[j], route[i]
    return route

# Main Genetic Algorithm
def genetic_algorithm(distance_matrix, population_size, generations, mutation_rate, elitism_count):
    population = initialize_population(population_size, num_locations)
    for generation in range(generations):
        fitness = evaluate_population(population, distance_matrix)
        next_population = []
        
        # Elitism: Carry forward the best individuals
        elite_indices = sorted(range(len(fitness)), key=lambda x: fitness[x], reverse=True)[:elitism_count]
        for idx in elite_indices:
            next_population.append(population[idx])
        
        # Generate new offspring
        while len(next_population) < population_size:
            parents = select_parents(population, fitness)
            offspring = order_crossover(parents[0], parents[1])
            offspring = mutate(offspring, mutation_rate)
            next_population.append(offspring)
        
        population = next_population
    
    # Return the best route in the final population
    final_fitness = evaluate_population(population, distance_matrix)
    best_index = final_fitness.index(max(final_fitness))
    best_route = population[best_index]
    best_distance = calculate_route_distance(best_route, distance_matrix)
    return best_route, best_distance

# Jalankan algoritma dan buat kesimpulan
if __name__ == "__main__":
    best_route, best_distance = genetic_algorithm(
        distance_matrix,
        population_size,
        generations,
        mutation_rate,
        elitism_count
    )

    # Output kesimpulan
    print("=== Hasil Algoritma Genetika untuk Rute Logistik ===")
    print(f"Rute Terbaik     : {best_route}")
    print(f"Jarak Total (km) : {best_distance:.2f}")
    print("\nKesimpulan:")
    print(f"Rute terbaik ditemukan dengan total jarak {best_distance:.2f} km.")
    print(f"Ini menunjukkan efisiensi rute logistik untuk mengunjungi {num_locations - 1} lokasi.")
coordinates = [
    (0, 0), (2, 3), (4, 1), (6, 5), (3, 4), (5, 2), (1, 5),
    (7, 6), (8, 3), (9, 5), (10, 2)
]

# Visualisasi rute terbaik
def visualize_route(route, coordinates):
    x = [coordinates[loc][0] for loc in route]
    y = [coordinates[loc][1] for loc in route]
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, '-o', label='Route')
    plt.title('Optimal Logistics Route')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    for i, loc in enumerate(route):
        plt.text(x[i], y[i], str(loc), fontsize=12, ha='right')
    plt.legend()
    plt.grid()
    plt.show()

visualize_route(best_route, coordinates)