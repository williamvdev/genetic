from random import randint, random
import json

POPULATION_SIZE = 100
GENERATIONS = 100
KNAPSACK_MAX_WEIGHT = 15000
TREASURE_FILE = 'python/treasures.json'
INHERITANCE_FACTOR = 0.5 # What fraction of bits are copied from parent A
MUTATION_FACTOR = 0.01 # What fraction of bits are flipped in a child.

def treasure_generator(item_count, max_weight, max_value):
    """
    Generates a list of treasure items
    """
    treasures = []
    for i in range(item_count):
        item = { "id": i, "weight": randint(0, max_weight), "value": randint(0, max_value)}
        treasures.append(item)
    return treasures

def generate_treasure_file(item_count, max_weight, max_value):
    with open(TREASURE_FILE, 'w') as output_file:
        json.dump(treasure_generator(item_count, max_weight, max_value), output_file)

def read_treasures():
    treasure_list = []
    with open(TREASURE_FILE, 'r') as input_file:
        treasure_list = json.load(input_file)
    return treasure_list

def select_by_tournament(candidates, treasures):
    """ 
    Randomly selects two candidates from the list and returns the one 
    with the best fitness score
    """
    candidate_a = candidates[randint(0, len(candidates) - 1)]
    candidate_b = candidates[randint(0, len(candidates) - 1)]
    return candidate_a if solution_fitness(treasures, candidate_a) > solution_fitness(treasures, candidate_b) else candidate_b

def solution_fitness(treasures, solution):
    """
    Determines the fitness score for a given solution
    """
    total_value = 0
    total_weight = 0
    for i in range(len(solution)):
        if solution[i] == True :
            total_value += treasures[i]['value']
            total_weight += treasures[i]['weight']
        if (total_weight > KNAPSACK_MAX_WEIGHT):
            return 0
    return total_value

def get_child(parent_a, parent_b):
    child = []
    for i in range(len(parent_a)):
        child_bit = parent_a[i] if random() < INHERITANCE_FACTOR else parent_b[i]
        child_bit = not child_bit if random() < MUTATION_FACTOR else child_bit
        child.append(child_bit)
    return child

def generate_random_solution(size):
    solution = []
    for i in range(size):
        solution.append(True if randint(0,1) == 1 else False)
    return solution


def get_generation(treasures, parent_generation, population_size):
    new_gen = []
    while len(new_gen) < population_size:
        if(len(parent_generation) == 0):
            new_gen.append(generate_random_solution(len(treasures)))
        else:
            parent_a = select_by_tournament(parent_generation, treasures)
            parent_b = select_by_tournament(parent_generation, treasures)
            new_gen.append(get_child(parent_a, parent_b))
    return new_gen

def get_generation_stats(treasures, generation):
    stats = {}
    total_score = 0
    for solution in generation:
        score = solution_fitness(treasures, solution)
        total_score += score
        if 'min' not in stats: stats['min'] = score
        if 'max' not in stats: stats['max'] = score
        if score < stats['min']: stats['min'] = score
        if score > stats['max']: stats['max'] = score
    stats['avg'] = total_score / len(generation)
    return stats

def main():
    print("Starting Genetic Search...")
    generation_stats = []
    treasure_list = read_treasures()
    current_generation = []

    for gen_no in range(GENERATIONS):
        current_generation = get_generation(treasure_list, current_generation, POPULATION_SIZE)
        current_gen_stats = get_generation_stats(treasure_list, current_generation)
        print('Generation {} stats: Lowest Fitness: {}, Highest Fitness: {}, Average Fitness: {}'.format(gen_no, current_gen_stats['min'], current_gen_stats['max'], current_gen_stats['avg']))
        generation_stats.append(current_gen_stats)

    print("Done!")

if __name__ == "__main__":
    main()