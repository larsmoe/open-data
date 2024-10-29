import json
import matplotlib.pyplot as plt
from collections import defaultdict

# Load data from the JSON file
with open('all_matches.json', 'r', encoding='utf-8') as f:
    all_matches = json.load(f)

matches_per_season = defaultdict(lambda: {'male': 0, 'female': 0})
matches_per_country = defaultdict(int)
matches_per_season_country = defaultdict(lambda: defaultdict(int))

# Count the matches by season, gender, and country
for match_id, match_info in all_matches.items():
    season = match_info['season_name']
    gender = match_info['gender']
    country = match_info['country_name']

    matches_per_season[season][gender] += 1
    matches_per_country[country] += 1
    matches_per_season_country[season][country] += 1

# Sort the matches by season
sorted_seasons = sorted(matches_per_season.keys())

# Print the total number of matches
total_matches = sum(sum(gender_data.values()) for gender_data in matches_per_season.values())
print(f'Total number of matches: {total_matches}')

# Print the number of matches per season, ordered by season
for season in sorted_seasons:
    counts = matches_per_season[season]
    print(f"Season: {season}, Male: {counts['male']}, Female: {counts['female']}")

all_countries = set()
for season in matches_per_season_country:
    all_countries.update(matches_per_season_country[season].keys())
sorted_countries = sorted(all_countries)
country_counts_per_season = {country: [matches_per_season_country[season][country] for season in sorted_seasons] for country in sorted_countries}

# Prepare data for the first plot (matches per season)
male_counts = [matches_per_season[season]['male'] for season in sorted_seasons]
female_counts = [matches_per_season[season]['female'] for season in sorted_seasons]

# Plot the number of matches per season
plt.figure(figsize=(10, 6))
plt.bar(sorted_seasons, male_counts, label='Male matches', color='blue', alpha=0.6)
plt.bar(sorted_seasons, female_counts, label='Female matches', color='pink', alpha=0.6, bottom=male_counts)
plt.xlabel('Season')
plt.ylabel('Number of Matches')
plt.title('Number of Matches per Season (Male vs Female)')
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.tight_layout()

# Prepare data for the second plot (matches per country)
sorted_countries = sorted(matches_per_country.keys(), key=lambda x: matches_per_country[x], reverse=True)
country_counts = [matches_per_country[country] for country in sorted_countries]

# Plot the number of matches per country
plt.figure(figsize=(10, 6))
plt.bar(sorted_countries, country_counts, color='green', alpha=0.7)
plt.xlabel('Country')
plt.ylabel('Number of Matches')
plt.title('Number of Matches per Country')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Plot the stacked bar chart for matches per season by country
plt.figure(figsize=(10, 6))

bottom_stack = [0] * len(sorted_seasons)  # Initialize the bottom stack for each season

# Add each country to the plot
for country in sorted_countries:
    counts = country_counts_per_season[country]
    plt.bar(sorted_seasons, counts, label=country, bottom=bottom_stack)
    bottom_stack = [i + j for i, j in zip(bottom_stack, counts)]  # Update bottom stack

# Configure the plot
plt.xlabel('Season')
plt.ylabel('Number of Matches')
plt.title('Number of Matches per Season (Stacked by Country)')
plt.xticks(rotation=45, ha='right')
plt.legend(title="Country", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Display the plot
plt.show()