import json

ELO_START_VALUE = 100
# Load the JSON data from file
with open('data/matches/9/27.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Initialize a dictionary to hold team IDs and their names
team_elos = {}

# Loop through each match in the data
for match in data:
    # Check and add home team if not already in dictionary
    home_team_id = match['home_team']['home_team_id']
    if home_team_id not in team_elos:
        team_elos[home_team_id] = {
            'team_name': match['home_team']['home_team_name'],
            'elo': 100  # Starting Elo rating
        }

    # Check and add away team if not already in dictionary
    away_team_id = match['away_team']['away_team_id']
    if away_team_id not in team_elos:
        team_elos[away_team_id] = {
            'team_name': match['away_team']['away_team_name'],
            'elo': 100  # Starting Elo rating
        }

print(team_elos)
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

print(matches_by_week[0])
