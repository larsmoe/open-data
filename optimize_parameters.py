import json
from elo_functional import calculate_elo_for_season
import numpy as np
from scipy.stats import kendalltau

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

k_values = range(1, 51, 1)
s_values = range(1, 51, 1)

best_k = None
best_s = None
best_tau = -1

for k in k_values:
    for s in s_values:
        team_elos = calculate_elo_for_season(team_elos, matches_by_week, k, s)  # You need to implement this function
        # Sort teams by Elo to get predicted standings
        predicted_standings = sorted(team_elos.keys(), key=lambda x: team_elos[x]['elo'], reverse=True)
        tau, _ = kendalltau(predicted_standings, ACTUAL_STANDINGS_AT_SEASON_END)
        if tau > best_tau:
            best_tau = tau
            best_k = k
            best_s = s

print(f"Best k: {best_k}, Best s: {best_s}, Kendall's tau: {best_tau}")