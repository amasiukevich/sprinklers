import numpy as np

# from collections import Counter
from .solution import Solution
from .area import Area

class Population():

    """
    Author: Anton Masiukevich
    github: https://github.com/amasiukevich
    """

    def __init__(self, width, height, radius, lambda_=15, mu=25, mutation_prob=0.001, n_sprinklers=5):

        """
        :param lambda_: the number of offsprings
        :param mu: the number of parent population
        """

        self.lambda_ = lambda_
        self.mu = mu

        self.n_sprinklers = n_sprinklers
        self.width = width
        self.height = height
        self.radius = radius

        self.t_competitors = self.mu + 5
        self.tour_competitors = 2 * self.lambda_ + 5

        # using mutation probability (CAN BE BETTER)
        self.mutation_pool = np.zeros(1000)

        chosen_places = []
        i = 0
        while i < int(mutation_prob * 1000):
            random_place = int(np.random.uniform(low=0, high=len(self.mutation_pool)))
            if random_place not in chosen_places:
                chosen_places.append(random_place)
                self.mutation_pool[random_place] = 1
            else:
                continue
            i += 1

        # For 2-point crossover
        self.breakers = [
            np.random.randint(low=0, high=self.n_sprinklers // 2),
            np.random.randint(low=self.n_sprinklers // 2, high=self.n_sprinklers)
        ]


    def generate_init_population(self):

        """
        Generates the initial population of possible solutions
        :return: a list of all specimen (len = mu)
        """

        specimen = []
        for i in range(self.mu):
            new_speciman = Solution(self.n_sprinklers, self.width, self.height)
            new_speciman.fitness = self.evaluate_one(new_speciman)

            specimen.append(new_speciman)

        self.individuals = specimen
        self.pool = specimen


    def tournament_selection_for_crossover(self):

        """
        Performs a tournament selection
        :return: selected pairs (monogamy)
        """
        # Faster to use set
        chosen_specimen = list(np.random.choice(self.pool, self.tour_competitors))
        # Faster to use set
        chosen_to_reproduct = []

        for i in range(2 * self.lambda_):

            fighter1 = np.random.choice(chosen_specimen)
            chosen_specimen.remove(fighter1)
            fighter2 = np.random.choice(chosen_specimen)
            chosen_specimen.remove(fighter2)

            if fighter1.fitness < fighter2.fitness:
                winner = fighter2
                chosen_specimen.append(fighter2)
            else:
                winner = fighter1
                chosen_specimen.append(fighter2)

            chosen_to_reproduct.append(winner)


        # Actual pairs
        pairs = []

        for i in range(self.lambda_):

            parent1 = np.random.choice(chosen_to_reproduct)
            chosen_to_reproduct.remove(parent1)
            parent2 = np.random.choice(chosen_to_reproduct)
            chosen_to_reproduct.remove(parent2)

            pairs.append((parent1, parent2))

        return pairs


    def simple_selection(self):

        """
        Performs a simple random selection
        :return: selected pairs (polygamy)
        """
        pairs = []

        for i in range(self.lambda_):

            parent = np.random.choice(self.pool)
            partner = np.random.choice(self.pool)

            while partner == parent:
                partner = np.random.choice(self.pool)
            pairs.append((parent, partner))

        return pairs


    def perform_optimization(self, generation):

        """
        A function where the whole process of optimization is performed
        :return:
        """

        current_generation = self.individuals
        self.pool = current_generation

        parents_pairs = self.tournament_selection_for_crossover()
        offsprings = []

        # product LAMBDA offsprings
        for i in range(len(parents_pairs)):

            # get parents to crossover
            parent1, parent2 = parents_pairs[i]
            genes = self.crossover(parent1, parent2)

            # when to use mutation
            mutation_ticket = np.random.choice(self.mutation_pool)

            if mutation_ticket == 1:
                genes = self.mutation(genes)

            offspring = Solution(self.n_sprinklers, self.width, self.height)

            offspring.sprinklers1 = genes[0]
            offspring.sprinklers2 = genes[1]

            # evaluating offspring's fitness
            offspring.fitness = self.evaluate_one(offspring)
            offsprings.append(offspring)

        self.pool += offsprings

        ### Making it better
        best = self.get_best()

        second_best = self.get_second_best(best)
        worst = self.get_worst()

        ### Selecting who lives and who dies
        self.individuals = self.tournament_selection()
        self.pool = []

        return best, second_best, worst


    def evaluate_one(self, solution):

        """
        Evaluation of the given solution
        :param solution: possible solution
        :return: fitness of the solution
        """

        self.area = Area(width=self.width, height=self.height, sprinkler_rad=self.radius)

        # Just in case
        self.area.clear_area()

        # Inserting sprinklers
        for coord_pair in zip(solution.sprinklers1, solution.sprinklers2):
            self.area.add_sprinkle(coord_pair)

        # Evaluating itself
        fitness = round(self.area.calc_sprinkled_ratio(), 3)
        return fitness


    def crossover(self, parent1: Solution, parent2: Solution):

        """
        :param parent1: first parent to reproduct
        :param parent2: second parent to reproduct
        :return:
        """

        is_first = np.random.choice([parent1, parent2])

        if is_first == parent1:

            child_genes1 = list(parent1.sprinklers1[:self.breakers[0]]) + \
                           list(parent2.sprinklers1[self.breakers[0]: self.breakers[1]]) + \
                           list(parent1.sprinklers1[self.breakers[1]:])

            child_genes2 = list(parent1.sprinklers2[:self.breakers[0]]) + \
                           list(parent2.sprinklers2[self.breakers[0]: self.breakers[1]]) + \
                           list(parent1.sprinklers2[self.breakers[1]:])

        elif is_first == parent2:

            child_genes1 = list(parent2.sprinklers1[:self.breakers[0]]) + \
                           list(parent1.sprinklers1[self.breakers[0]: self.breakers[1]]) + \
                           list(parent2.sprinklers1[self.breakers[1]:])

            child_genes2 = list(parent2.sprinklers2[:self.breakers[0]]) + \
                           list(parent1.sprinklers2[self.breakers[0]: self.breakers[1]]) + \
                           list(parent2.sprinklers2[self.breakers[1]:])

        return [child_genes1, child_genes2]


    def mutation(self, genes: list):

        """
        :param genes: genes to mutate
        :return:
        """

        choice = np.random.choice([0, 1])

        np.random.shuffle(genes[choice])

        bit_choice = np.random.randint(len(genes[int(not choice)]))
        new_gene_part = self.mutate_unit(genes[int(not choice)], pos=bit_choice, part=int(not choice))

        genes[int(not choice)] = new_gene_part

        return genes


    def mutate_unit(self, gene_parts, pos, part):

        min = 0
        max = self.width - 1

        if part == 1:
            max = self.height - 1

        if pos == min:
            gene_parts[pos] += 1
        elif pos == max:
            gene_parts[pos] -= 1
        else:
            gene_parts[pos] = max - gene_parts[pos]

        return gene_parts


    def tournament_selection(self):

        """
        A tournament selection to the next generation
        :return:
        """

        selected = []

        # Prioritizing the best offspring in the pool
        best_spec = self.get_best()
        selected.append(best_spec)
        self.pool.remove(best_spec)

        # 2 - fighters tournament
        for i in range(self.mu - 1):
            fighter1 = np.random.choice(self.pool)
            self.pool.remove(fighter1)
            fighter2 = np.random.choice(self.pool)
            self.pool.remove(fighter2)

            winner = None
            if fighter1.fitness < fighter2.fitness:
                winner = fighter2
                self.pool.append(fighter1)
            else:
                winner = fighter1
                self.pool.append(fighter2)

            selected.append(winner)

        return selected


    def get_worst(self):

        """
        A method to get the worst solution in pool
        :return:
        """

        worst = None
        worst_score = np.inf
        for el in self.pool:
            if el.fitness < worst_score:
                worst_score = el.fitness
                worst = el

        return worst

    def get_second_best(self, best):

        """
        A method to get the second best solution in pool
        :param best:
        :return:
        """

        second_best = None
        second_best_score = 0
        for el in self.pool:
            if el.fitness > second_best_score and el != best:
                second_best_score = el.fitness
                second_best = el


        assert len(self.pool) == self.mu + self.lambda_
        return second_best


    def get_best(self):

        """
        A method to get the best solution in pool
        :param fitnesses:
        :return:
        """

        best = None
        best_score = 0
        for el in self.pool:
            if el.fitness > best_score:
                best = el
                best_score = el.fitness

        return best