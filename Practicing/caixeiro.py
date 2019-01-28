import numpy
import copy

vertices = ['a', 'b', 'c', 'd']
edges = ['ab', 'ac', 'ad', 'ba', 'bc', 'bd', 'ca', 'cb', 'cd', 'da', 'db', 'dc']
costs = numpy.random.randint(0, 101, 12)

population_size = 100
max_generations = 1000
crossing_chance = 100
mutation_chance = 10


class Chromosome:
    def __init__(self, config, score=None, is_monster=True):
        self.config = config
        self.score = score
        self.is_monster = is_monster

    def __str__(self):
        path = ""

        for idx, e in enumerate(self.config):
            if e:
                path += edges[idx] + " "
        return "Path: [{}], Score: {}".format(path, self.score)


def evaluate(chromosome):
    score = 0
    is_monster = False
    count_income = {}
    count_outcome = {}

    for v in vertices:
        count_income[v] = 0
        count_outcome[v] = 0

    sub_edges = []
    for idx, e in enumerate(chromosome.config):
        if e:
            sub_edges += [edges[idx]]
            score -= costs[idx]

            count_income[edges[idx][0]] += 1
            count_outcome[edges[idx][1]] += 1

    # looking for monsters
    for v in vertices:
        if count_income[v] != 1 or count_outcome != 1:  # monster found
            score -= (0 if count_income[v] == 1 else 999) + (0 if count_outcome[v] == 1 else 999)  # penalty
            is_monster = True

    # ToDo identifying cycles

    return score, is_monster


def main():
    population = []
    # generating initial population
    for i in range(population_size):
        population.append(Chromosome([(True if numpy.random.randint(0, 2) == 1 else False) for j in range(len(edges))]))
        population[i].score, population[i].is_monster = evaluate(population[i])

    # generations
    for t in range(max_generations):

        # looking for solution
        for c in population:
            if not c.is_monster:
                print('Solution found!', c)
                return

        # selection
        population.sort(key=lambda c: c.score, reverse=True)
        top_pop = population[:int(population_size / 2)]
        bot_pop = population[int(population_size / 2):]

        # crossing
        descendants = []
        for i in range(len(top_pop)):
            for j in range(len(bot_pop)):
                if numpy.random.randint(0, 100) < crossing_chance:
                    cp = numpy.random.randint(0, len(edges))

                    new_path = copy.deepcopy(top_pop[i].config[:cp]) + copy.deepcopy(bot_pop[i].config[cp:])
                    descendants.append(Chromosome(new_path))

        # mutation (and evaluation)
        for i in range(len(descendants)):
            if numpy.random.randint(0, 100) < mutation_chance:
                mp = numpy.random.randint(0, len(edges))
                descendants[i].config[mp] = not descendants[i].config[mp]

            descendants[i].score, descendants[i].is_monster = evaluate(descendants[i])
            # print(descendants[i])

        # selection
        population = top_pop + descendants
        population.sort(key=lambda c: c.score, reverse=True)
        population = population[:population_size]
    else:
        print('No solution found...')
        print(population[0], population[population_size - 1])


main()
