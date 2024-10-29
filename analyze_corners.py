import json
import matplotlib.pyplot as plt
from collections import defaultdict


# Load the data from the provided file
with open('corner_pass_events.json', 'r') as f:
    corner_events = json.load(f)

# Initialize counters for passes and shots
pass_count = 0
shot_count = 0

# Loop through each event to count passes and shots
pass_heights = defaultdict(int)

# Loop through the passes to extract the height information
for event in corner_events:
    if 'pass' in event and 'height' in event['pass']:
        height_name = event['pass']['height']['name']
        pass_heights[height_name] += 1

# Prepare data for plotting
heights = list(pass_heights.keys())
counts = list(pass_heights.values())

# Plot the results as a bar plot
plt.figure(figsize=(10, 6))
plt.bar(heights, counts, color='blue', alpha=0.7)
plt.xlabel('Pass Height')
plt.ylabel('Number of Passes')
plt.title('Distribution of Pass Heights in Corner Events')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Display the plot
plt.show()