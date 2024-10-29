from elo_functional import elo_adjustment
import json
import matplotlib.pyplot as plt

ELO_START_VALUE = 100
K = 15
S = 15

# Load the JSON data from file
with open('data/matches/9/27.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

team_elos = {}

# Populate initial team data and set Elo ratings to 100
for match in data:
    home_team_id = match['home_team']['home_team_id']
    away_team_id = match['away_team']['away_team_id']
    if home_team_id not in team_elos:
        team_elos[home_team_id] = {
            'team_name': match['home_team']['home_team_name'],
            'elo': [ELO_START_VALUE]  # Start with initial Elo in a list
        }
    if away_team_id not in team_elos:
        team_elos[away_team_id] = {
            'team_name': match['away_team']['away_team_name'],
            'elo': [ELO_START_VALUE]  # Start with initial Elo in a list
        }

# Calculate Elo ratings for each match week
for week in range(1, 35):  # Assuming 34 weeks
    for match in data:
        if match['match_week'] == week:
            home_team_id = match['home_team']['home_team_id']
            away_team_id = match['away_team']['away_team_id']
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
            new_home_elo, new_away_elo = elo_adjustment(home_elo[-1], away_elo[-1], K, S, result)
            team_elos[home_team_id]['elo'].append(new_home_elo)
            team_elos[away_team_id]['elo'].append(new_away_elo)

# Output the updated Elo ratings after all matches
#sorted_team_elos = sorted(team_elos.items(), key=lambda x: x[1]['elo'], reverse=True)

# Print the sorted team Elo ratings
#for team_id, info in sorted_team_elos:
#    print(f"Team ID: {team_id}, Team Name: {info['team_name']}, Elo: {info['elo']}")
# Sort the teams by their final Elo ratings in descending order
sorted_team_elos = sorted(team_elos.items(), key=lambda x: x[1]['elo'][-1], reverse=True)
print("Final Elo Ratings in Descending Order:")
for team_id, info in sorted_team_elos:
    print(f"Team ID: {team_id}, Team Name: {info['team_name']}, Final Elo: {info['elo'][-1]}")

plt.figure(figsize=(10, 6))
for team_id, info in team_elos.items():
    plt.plot(info['elo'], label=info['team_name'])
plt.title('Elo Ratings Over the Season')
plt.xlabel('Match Week')
plt.ylabel('Elo Rating')
plt.legend(loc='upper left', bbox_to_anchor=(1,1))
plt.show()