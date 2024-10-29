import json
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import numpy as np
from collections import defaultdict

# Load the passes data
with open('corner_pass_events.json', 'r') as f:
    passes = json.load(f)

# Load the match data
with open('all_matches.json', 'r') as f:
    all_matches = json.load(f)

# Initialize dictionaries to count pass heights by season
pass_heights_by_season = defaultdict(lambda: defaultdict(int))
pass_heights_by_period = defaultdict(lambda: defaultdict(int))
season_total_passes = defaultdict(int)
corners_per_season = defaultdict(int)

def get_period(season):
    if season < "2009/2010":
        return "Before 2009/2010"
    elif "2010/2011" <= season <= "2014/2015":
        return "2010/2011 to 2014/2015"
    else:
        return "After 2014/2015"

# Loop through passes and match each pass with its corresponding season
for event in passes:
    match_id = event['match_id']  # Assuming match_id exists in the pass data
    if match_id in all_matches:
        season = all_matches[match_id]['season_name']
        period = get_period(season)
        if 'pass' in event and 'height' in event['pass']:
            height_name = event['pass']['height']['name']
            pass_heights_by_season[season][height_name] += 1
            pass_heights_by_period[period][height_name] += 1
            season_total_passes[season] += 1
            corners_per_season[season] += 1

# Prepare data for plotting (calculate percentage for each height by season)
sorted_seasons = sorted(pass_heights_by_season.keys())
corner_counts = [corners_per_season[season] for season in sorted_seasons]
heights = set(height for season in pass_heights_by_season for height in pass_heights_by_season[season])

# Convert counts to percentages
percentage_by_height_season = {height: [] for height in heights}
for season in sorted_seasons:
    total_passes = season_total_passes[season]
    for height in heights:
        count = pass_heights_by_season[season].get(height, 0)
        percentage = (count / total_passes) * 100 if total_passes > 0 else 0
        percentage_by_height_season[height].append(percentage)

# Prepare data for stackplot
stack_data = [percentage_by_height_season[height] for height in heights]
height_labels = list(heights)

# Plot using stackplot
plt.figure(figsize=(10, 6))
plt.stackplot(sorted_seasons, stack_data, labels=height_labels)

# Configure the plot
plt.xlabel('Season')
plt.ylabel('Percentage of Passes')
plt.title('Percentage of Pass Heights by Season (Stacked)')
plt.xticks(rotation=45, ha='right')
plt.legend(title="Pass Height", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

plt.figure(figsize=(10, 6))
bars = plt.bar(sorted_seasons, corner_counts, color='skyblue')

# Add numbers above the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center')

# Configure the plot
plt.xlabel('Season')
plt.ylabel('Number of Corners')
plt.title('Number of Corners per Season')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

periods = sorted(pass_heights_by_period.keys())
heights = sorted({height for period_data in pass_heights_by_period.values() for height in period_data})

# Construct the contingency table
contingency_table = np.array([[pass_heights_by_period[period].get(height, 0) for height in heights] for period in periods])

# Perform the Chi-Square test
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

# Output the results
print(f"Chi-Square Statistic: {chi2}")
print(f"P-Value: {p_value}")

# Interpretation of the p-value
alpha = 0.05
if p_value < alpha:
    print("Reject the null hypothesis: The distribution of pass heights changes across periods.")
else:
    print("Fail to reject the null hypothesis: No significant change in the distribution of pass heights across periods.")
# Show the plot
plt.show()