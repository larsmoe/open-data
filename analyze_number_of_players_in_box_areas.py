import json
import numpy as np

# File path for the consolidated corner data
corners_file = 'all_360_corners.json'


# Helper function to check if a player is inside a given rectangular area
def is_inside_box(location, box_corners):
    x, y = location
    (x1, y1), (x2, y2) = box_corners
    return x1 <= x <= x2 and y1 <= y <= y2


# Define the zones
zones = {
    'right_goal_area': [(114, 30), (120, 36)],
    'middle_goal_area': [(114, 36), (120, 44)],
    'left_goal_area': [(114, 44), (120, 50)],
    'right_box_area': [(102, 18), (120, 30)],
    'right_penalty_zone': [(102, 30), (114, 40)],
    'left_penalty_zone': [(102, 40), (114, 50)],
    'left_box_area': [(102, 50), (120, 62)]
}

# Load the consolidated corner events data
with open(corners_file, 'r') as file:
    corners_data = json.load(file)

# Initialize counters
defensive_counts_left = {zone: 0 for zone in zones}  # For left corners
defensive_counts_right = {zone: 0 for zone in zones}  # For right corners
left_corner_count = 0
right_corner_count = 0

# Loop through the corner events and count defensive players in each zone
for event in corners_data:
    freeze_frame = event.get('freeze_frame', [])
    corner_location = event.get('location', [])

    # Check if it's a left or right corner
    if corner_location == [120, 0.1]:  # Right corner
        right_corner_count += 1
        for player in freeze_frame:
            if not player['teammate']:  # Defensive player
                player_location = player['location']

                # Check if the player is inside any of the defined zones
                for zone_name, (bottom_left, top_right) in zones.items():
                    if is_inside_box(player_location, (bottom_left, top_right)):
                        defensive_counts_right[zone_name] += 1

    elif corner_location == [120, 80]:  # Left corner
        left_corner_count += 1
        for player in freeze_frame:
            if not player['teammate']:  # Defensive player
                player_location = player['location']

                # Check if the player is inside any of the defined zones
                for zone_name, (bottom_left, top_right) in zones.items():
                    if is_inside_box(player_location, (bottom_left, top_right)):
                        defensive_counts_left[zone_name] += 1


# Calculate averages
def calculate_average(counts, total_corners):
    if total_corners == 0:
        return {zone: 0 for zone in counts}  # Avoid division by zero
    return {zone: counts[zone] / total_corners for zone in counts}


average_defensive_left = calculate_average(defensive_counts_left, left_corner_count)
average_defensive_right = calculate_average(defensive_counts_right, right_corner_count)

# Print the results
print(f"Total left corners: {left_corner_count}")
print("Average Number of Defensive Players in Each Zone During Left Corners:")
for zone, avg in average_defensive_left.items():
    print(f"{zone}: {avg:.2f}")

print(f"\nTotal right corners: {right_corner_count}")
print("Average Number of Defensive Players in Each Zone During Right Corners:")
for zone, avg in average_defensive_right.items():
    print(f"{zone}: {avg:.2f}")