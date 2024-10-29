import json
from collections import defaultdict

YARDS_TO_METER = 0.9144

with open('corner_pass_events.json', 'r') as f:
    passes = json.load(f)

total_length = 0
total_passes = 0
length_by_type = defaultdict(lambda: {'total_length': 0, 'count': 0})

# Loop through passes and calculate lengths
for event in passes:
    if 'pass' in event and 'length' in event['pass']:
        pass_length = event['pass']['length']
        total_length += pass_length
        total_passes += 1

        # Check pass type and store the length in corresponding type group
        if 'height' in event['pass']:
            pass_type = event['pass']['height']['name']
            length_by_type[pass_type]['total_length'] += pass_length
            length_by_type[pass_type]['count'] += 1

# Calculate overall average length
overall_average_length = total_length / total_passes if total_passes > 0 else 0

# Calculate average length by pass type
average_length_by_type = {pass_type: (data['total_length'] / data['count']) if data['count'] > 0 else 0
                          for pass_type, data in length_by_type.items()}

# Output the results
print(f"Overall average pass length: {YARDS_TO_METER*overall_average_length:.2f} meters")

print("\nAverage pass length by type:")
for pass_type, avg_length in average_length_by_type.items():
    print(f"{pass_type}: {YARDS_TO_METER*avg_length:.2f} meters")