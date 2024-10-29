import json
from elo_functional import calculate_elo_for_season
import numpy as np
from scipy.stats import kendalltau
import random
from deap import base, creator, tools, algorithms

ELO_START_VALUE = 100
ACTUAL_STANDINGS_AT_SEASON_END = [169, 180, 904, 185, 181, 177, 173, 179, 186, 171, 189, 172, 176, 872, 175, 184, 174, 178]

with open('data/matches/9/27.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

matches_by_week = [{} for _ in range(34)]
for match in data:
    week = match['match_week'] - 1  # Adjusting match_week to be zero-indexed for list access
    if week in range(34):  # Ensure valid match week
        # Initialize a list for this week in the matches_by_week list if not already present
        if not matches_by_week[week]:
            matches_by_week[week] = []

        # Determine the winner of the match
        if match['home_score'] > match['away_score']:
            winner = 1  # Home team wins
        elif match['home_score'] == match['away_score']:
            winner = 0.5  # Draw
        else:
            winner = 0  # Away team wins

        # Append current match details to the appropriate week
        matches_by_week[week].append({
            'match_id': match['match_id'],
            'home_team_id': match['home_team']['home_team_id'],
            'home_team_name': match['home_team']['home_team_name'],
            'away_team_id': match['away_team']['away_team_id'],
            'away_team_name': match['away_team']['away_team_name'],
            'winner': winner,
            'home_score': match['home_score'],
            'away_score': match['away_score']
        })

def create_team_elos():
    team_elos = {}

    for match in data:
        home_team_id = match['home_team']['home_team_id']
        away_team_id = match['away_team']['away_team_id']
        if home_team_id not in team_elos:
            team_elos[home_team_id] = {
                'team_name': match['home_team']['home_team_name'],
                'elo': ELO_START_VALUE  # Start with initial Elo in a list
            }
        if away_team_id not in team_elos:
            team_elos[away_team_id] = {
                'team_name': match['away_team']['away_team_name'],
                'elo': ELO_START_VALUE  # Start with initial Elo in a list
            }
    return team_elos

# Define the problem object as maximizing the fitness (Kendall's tau)
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Initialize the population
toolbox = base.Toolbox()
toolbox.register("attr_k", random.uniform, 1, 50)
toolbox.register("attr_s", random.uniform, 1, 50)
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_k, toolbox.attr_s), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define the evaluation function
def evalElo(individual):
    k, s = individual
    team_elos = calculate_elo_for_season(create_team_elos(), matches_by_week, k, s)  # Implement this function
    predicted_standings = sorted(team_elos.keys(), key=lambda x: team_elos[x]['elo'], reverse=True)
    tau, _ = kendalltau(predicted_standings, ACTUAL_STANDINGS_AT_SEASON_END)
    return (tau,)

toolbox.register("evaluate", evalElo)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Genetic Algorithm
population = toolbox.population(n=50)
ngen = 40
for gen in range(ngen):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(offspring, k=len(population))
sorted_population = sorted(population, key=lambda ind: ind.fitness.values[0], reverse=True)

# Print the sorted population
print("Sorted population based on fitness values:")
for ind in sorted_population:
    print(ind, ind.fitness.values)