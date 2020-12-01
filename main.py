import numpy as np
import matplotlib.pyplot as plt
from evolutionary.population import Population

HEIGHT = 20
WIDTH = 20
RADIUS = 2
MUTATION_PROB = 0.01

LAMBDA = 20
MU = 70

COVERAGE_PERCENT = 75

theory_min_sprinklers = np.inf

i = 0
while True:
    theory_covered_percent = round(100 * i * np.pi * (RADIUS ** 2) / (HEIGHT * WIDTH), 3)
    print(f'Can cover {theory_covered_percent} % of the area.')

    if theory_covered_percent >= COVERAGE_PERCENT:
        print(f"Minimal i: {i}")
        theory_min_sprinklers = i
        break

    i += 1

start_n_sprinklers = int(1.5 * theory_min_sprinklers)

population = Population(
        width=WIDTH,
        height=HEIGHT,
        radius=RADIUS,
        mutation_prob=MUTATION_PROB,
        lambda_=20,
        mu=70
    )

best_solutions = {}

for j in range(start_n_sprinklers, theory_min_sprinklers - 1, -1):

    print(f"Changing n_sprinklers to {j - 1}")
    population.n_sprinklers = j
    population.generate_init_population()

    # perform optimization
    best_score = 0
    best_individual = None

    outter_break = False

    generation = 0
    while best_score < COVERAGE_PERCENT:

        best_individual, second_best_individual, worst_individual = population.perform_optimization(generation)
        print(f"Generation: {generation},\t"
              f"Best: {best_individual.fitness},\t"
              f"Second best: {second_best_individual.fitness},\t"
              f"Worst: {worst_individual.fitness}")
        generation += 1

        if generation > 100:
            outter_break = True
            break
        best_score = best_individual.fitness

    if outter_break:
        break
    print(best_score)

    best_solutions[j] = best_individual

best_solutions = [(key, value) for key, value in sorted(best_solutions.items())]

print(best_solutions[0][0], best_solutions[0][1].fitness, [pair for pair in zip(best_solutions[0][1].sprinklers1,
                                                                                best_solutions[0][1].sprinklers2)])

spr_coords = [pair for pair in zip(best_solutions[0][1].sprinklers1, best_solutions[0][1].sprinklers2)]
best_fitness = best_solutions[0][1].fitness

fig, ax = plt.subplots()
ax.set(xlim=(0, WIDTH), ylim = (0, HEIGHT))

for pair in spr_coords:
    a_circle = plt.Circle((pair), RADIUS)
    ax.add_artist(a_circle)

fig.show()
print("Percentage: ", best_fitness)