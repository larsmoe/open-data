import json
from collections import defaultdict

# Load the corner events data
with open('corner_pass_events.json', 'r') as f:
    corners = json.load(f)

# Initialize counters for left and right corners based on foot preference
corner_foot_stats = {
    'left': {'right_foot': 0, 'left_foot': 0, 'unknown': 0},
    'right': {'right_foot': 0, 'left_foot': 0, 'unknown': 0}
}

# Loop through each corner pass and determine the player's foot and corner side
for event in corners:
    # Get the starting location of the corner
    start_x, start_y = event['location']

    # Identify the foot used
    try:
        foot_used = event['pass']['body_part']['name'].lower() if 'body_part' in event['pass'] else 'unknown'
    except KeyError:
        print(event)

    # Corners from the left (either from 0,0 or 120,80)
    if (start_x < 1 and start_y < 1) or (start_x > 119 and start_y > 79):
        if foot_used == 'right foot':
            corner_foot_stats['left']['right_foot'] += 1
        elif foot_used == 'left foot':
            corner_foot_stats['left']['left_foot'] += 1
        else:
            corner_foot_stats['left']['unknown'] += 1

    # Corners from the right (either from 0,80 or 120,0)
    elif (start_x < 1 and start_y > 79) or (start_x > 119 and start_y < 1):
        if foot_used == 'right foot':
            corner_foot_stats['right']['right_foot'] += 1
        elif foot_used == 'left foot':
            corner_foot_stats['right']['left_foot'] += 1
        else:
            corner_foot_stats['right']['unknown'] += 1

# Calculate total corners from left and right
total_left_corners = sum(corner_foot_stats['left'].values())
total_right_corners = sum(corner_foot_stats['right'].values())

# Calculate the percentage of corners for each foot preference
left_right_foot_percent = (corner_foot_stats['left'][
                               'right_foot'] / total_left_corners) * 100 if total_left_corners > 0 else 0
left_left_foot_percent = (corner_foot_stats['left'][
                              'left_foot'] / total_left_corners) * 100 if total_left_corners > 0 else 0

right_right_foot_percent = (corner_foot_stats['right'][
                                'right_foot'] / total_right_corners) * 100 if total_right_corners > 0 else 0
right_left_foot_percent = (corner_foot_stats['right'][
                               'left_foot'] / total_right_corners) * 100 if total_right_corners > 0 else 0

# Output the results
print(f"Total corners from the left: {total_left_corners}")
print(f"Right-footed corners from the left: {left_right_foot_percent:.2f}%")
print(f"Left-footed corners from the left: {left_left_foot_percent:.2f}%")

print(f"\nTotal corners from the right: {total_right_corners}")
print(f"Right-footed corners from the right: {right_right_foot_percent:.2f}%")
print(f"Left-footed corners from the right: {right_left_foot_percent:.2f}%")