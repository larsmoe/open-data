import numpy as np
import json

ELO_START_VALUE=100

def elo_adjustment(elo_home_team, elo_away_team, k, s, s_a):
    elo_difference = elo_home_team - elo_away_team
    sigma_team_1 = 1/(1+10 ** (-elo_difference/s))
    sigma_team_2 = 1 / (1 + 10 ** (elo_difference / s))
    expected_points_home_team = sigma_team_1
    expected_points_away_team = sigma_team_2
    elo_home_team_new = elo_home_team + k * (s_a - expected_points_home_team)
    elo_away_team_new = elo_away_team + k * ((1-s_a) - expected_points_away_team)
    return elo_home_team_new, elo_away_team_new

def elo_adjustment_mse(elo_home_team, elo_away_team, k, s, s_a,se):
    elo_difference = elo_home_team - elo_away_team
    sigma_team_1 = 1/(1+10 ** (-elo_difference/s))
    sigma_team_2 = 1 / (1 + 10 ** (elo_difference / s))
    expected_points_home_team = sigma_team_1
    expected_points_away_team = sigma_team_2
    elo_home_team_new = elo_home_team + k * (s_a - expected_points_home_team)
    elo_away_team_new = elo_away_team + k * ((1-s_a) - expected_points_away_team)
    se += (s_a - expected_points_home_team) ** 2
    return elo_home_team_new, elo_away_team_new, se

def calculate_elo_for_season(team_elos, matches_by_week, k, s):
    for week in matches_by_week:
        #print(week)
        for match in week:
            home_team_id = match['home_team_id']
            away_team_id = match['away_team_id']
            home_elo = team_elos[home_team_id]['elo']
            away_elo = team_elos[away_team_id]['elo']

            # Determine match result for Elo adjustment
            if match['home_score'] > match['away_score']:
                result = 1
            elif match['home_score'] == match['away_score']:
                result = 0.5
            else:
                result = 0

            # Update Elo ratings based on match result
            new_home_elo, new_away_elo = elo_adjustment(home_elo, away_elo, k, s, match['winner'])
            team_elos[home_team_id]['elo'] = new_home_elo
            team_elos[away_team_id]['elo'] = new_away_elo
    return team_elos

def calculate_elo_for_season_mse(team_elos, matches_by_week, k, s):
    mse = 0
    for week in matches_by_week:
        #print(week)
        for match in week:
            home_team_id = match['home_team_id']
            away_team_id = match['away_team_id']
            home_elo = team_elos[home_team_id]['elo']
            away_elo = team_elos[away_team_id]['elo']

            # Determine match result for Elo adjustment
            if match['home_score'] > match['away_score']:
                result = 1
            elif match['home_score'] == match['away_score']:
                result = 0.5
            else:
                result = 0

            # Update Elo ratings based on match result
            new_home_elo, new_away_elo, mse = elo_adjustment_mse(home_elo, away_elo, k, s, match['winner'], mse)
            team_elos[home_team_id]['elo'] = new_home_elo
            team_elos[away_team_id]['elo'] = new_away_elo
    return team_elos, mse