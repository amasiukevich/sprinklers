import csv
import json
import numpy as np

import argparse

import matplotlib.pyplot as plt
from evolutionary.population import Population


"""
Parsing command line arguments part
"""
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description='''\
Placing sprinklers task
------------------------------------------------------------------------''')

parser.add_argument('-wd', '--width', type=int, default=10, help='the width of the area to cover')
parser.add_argument('-ht', '--height', type=int, default=10, help='the height of the area to cover')
parser.add_argument('-ra', '--radius', type=int, default=2, help='the radius for every sprinkler')
parser.add_argument('-cov', '--coverage', type=int, default=75, help='a percent of the area to be covered')
parser.add_argument('-mu', '--mu', type=int, default=70, help='a size of the population')
parser.add_argument('-ld', '--llambda', type=int, default=20, help='a number of the offspring at every generation')
parser.add_argument('-mtp', '--mutation_prob', type=float, help='mutation probability')

args = parser.parse_args()

# WIDTH = args.width
# HEIGHT = args.height
# RADIUS = args.radius
# MUTATION_PROB = args.mutation_prob
# MU = args.mu
# LAMBDA = args.llambda
# COVERAGE_PERCENT = args.coverage




def estimate_lower_bound(width, height, radius, coverage_percent):

    """

    :param height:
    :param weight:
    :param radius:
    :param coverage_percent:
    :return:
    """
    theory_min_sprinklers = np.inf

    i = 0
    while True:
        i += 1
        theory_covered_percent = round(100 * i * np.pi * (radius ** 2) / (height * width), 3)
        print(f'Can cover {theory_covered_percent} % of the area.')

        if theory_covered_percent >= coverage_percent:
            print(f"Minimal i: {i}")
            theory_min_sprinklers = i
            break

    return theory_min_sprinklers


def optimize(weight, height, radius, mutation_prob, lambda_, mu, coverage_percent):

    """
    A final method for testing our algorithm
    :param height:
    :param weight:
    :param radius:
    :param mutation_prob:
    :param lambda_:
    :param mu:
    :param coverage_percent:
    :return:
    """
    theory_min_sprinklers = estimate_lower_bound(height, weight, radius, coverage_percent)

    start_n_sprinklers = int(1.5 * theory_min_sprinklers)

    population = Population(
            width=weight,
            height=height,
            radius=radius,
            mutation_prob=mutation_prob,
            lambda_=lambda_,
            mu=mu
    )

    best_solutions = {}

    for j in range(start_n_sprinklers, theory_min_sprinklers - 1, -1):

        print(f"Changing n_sprinklers to {j}")
        population.n_sprinklers = j
        population.generate_init_population()

        # perform optimization
        best_score = 0
        best_individual = None

        best_prev_score = 0
        outter_break = False

        generation = 0

        gens_without_improvement = 0
        while best_score < coverage_percent:

            best_individual, second_best_individual, worst_individual = population.perform_optimization(generation)
            if generation % 10 == 0:
                print(f"Generation: {generation},\t"
                      f"Best: {best_individual.fitness},\t"
                      f"Second best: {second_best_individual.fitness},\t"
                      f"Worst: {worst_individual.fitness}")

            best_score = best_individual.fitness

            if best_individual.fitness == best_prev_score:
                gens_without_improvement += 1
            else:
                best_prev_score = best_individual.fitness
                gens_without_improvement = 0

            if (gens_without_improvement > 60 or generation > 100):
                outter_break = True
                break
            generation += 1

        try:
            if outter_break:
                break
            else:
                print(best_score)
                best_solutions[j] = best_individual
        except:
            breakpoint()
    try:
        best_solutions = [(key, value) for key, value in sorted(best_solutions.items())]
        best_ever = best_solutions[0]
    except:
        best_ever = None

    return best_ever


def visualize(best_solution, width, height, radius):

    spr_coords = [pair for pair in zip(best_solution[1].sprinklers1, best_solution[1].sprinklers2)]

    fig, ax = plt.subplots()
    ax.set(xlim=(0, width), ylim=(0, height))

    for pair in spr_coords:
        a_circle = plt.Circle((pair), radius)
        ax.add_artist(a_circle)

    fig.show()


def save_results(csv_file, params):
    with open(csv_file, 'w') as results_file:
        field_names = ['width', 'height', 'radius', 'mutation_prob', 'theoretical_lowest', 'lowest_n_sprinklers', 'placement']
        writer = csv.DictWriter(results_file, fieldnames=field_names)
        for i in range(25):
            theoretical_best = estimate_lower_bound(params['width'], params['height'], params['radius'], params['coverage'])
            best_solution = optimize(params['width'], params['height'], params['radius'], params['mutation_prob'],
                                     params['lambda'], params['mu'], params['coverage'])

            if best_solution:
                placement = json.dumps(
                    [list(pair) for pair in zip(best_solution[1].sprinklers1, best_solution[1].sprinklers2)]
                )

                writer.writerow(dict(zip(field_names, [params['width'], params['height'], params['radius'], params['mutation_prob'],
                                                   best_solution[0], theoretical_best, placement])))

            else:
                writer.writerow(dict(zip(field_names, [
                    params['width'],
                    params['height'],
                    params['radius'],
                    params['mutation_prob'],
                    0,
                    theoretical_best,
                    placement
                ])))


best_solution = optimize(args.width, args.height, args.radius, args.mutation_prob,
                                     args.llambda, args.mu, args.coverage)

if best_solution:
    print(best_solution[0],[elem for elem in zip(best_solution[1].sprinklers1, best_solution[1].sprinklers2)])

print("Finished")