import json

# File path for the consolidated corner data
corners_file = 'all_360_corners.json'


# Helper function to check if a player is inside a given rectangular area
def is_inside_box(location, box_corners):
    x, y = location
    (x1, y1), (x2, y2) = box_corners
    return x1 <= x <= x2 and y1 <= y <= y2


# Define the boxes and goal areas
box_right = [(102, 18), (120, 62)]
box_left = [(0, 18), (18, 62)]
goal_area_right = [(114, 30), (120, 50)]
goal_area_left = [(0, 30), (6, 50)]

# Load the consolidated corner events data
with open(corners_file, 'r') as file:
    corners_data = json.load(file)


# Initialize counters
total_corners = 0
total_defensive_in_frame = 0
total_offensive_in_frame = 0
total_defensive_in_box = 0
total_offensive_in_box = 0
total_defensive_in_goal_area = 0
total_offensive_in_goal_area = 0

# Iterate over all the corner events in the consolidated file
for event in corners_data:
    total_corners += 1
    freeze_frame = event.get('freeze_frame', [])
    corner_location = event.get('location', [])

    # Determine which side the corner was taken from
    if corner_location == [120, 80]:  # Right corner
        offensive_box = box_left
        defensive_box = box_right
        offensive_goal_area = goal_area_left
        defensive_goal_area = goal_area_right
    elif corner_location == [120, 0.1]:  # Left corner
        offensive_box = box_right
        defensive_box = box_left
        offensive_goal_area = goal_area_right
        defensive_goal_area = goal_area_left
    else:
        continue  # Skip if it's not a corner event we can analyze

    # Initialize counters for the current event
    defensive_in_frame = 0
    offensive_in_frame = 0
    defensive_in_box = 0
    offensive_in_box = 0
    defensive_in_goal_area = 0
    offensive_in_goal_area = 0

    # Count players in various regions
    for player in freeze_frame:
        location = player['location']
        teammate = player['teammate']

        # Count offensive and defensive players in the frame
        if teammate:
            offensive_in_frame += 1
        else:
            defensive_in_frame += 1

        # Check if players are inside the dynamically defined boxes
        if is_inside_box(location, offensive_box):
            offensive_in_box += 1
        elif is_inside_box(location, defensive_box):
            defensive_in_box += 1

        # Check if players are inside the dynamically defined goal areas
        if is_inside_box(location, offensive_goal_area):
            offensive_in_goal_area += 1
        elif is_inside_box(location, defensive_goal_area):
            defensive_in_goal_area += 1

    # Accumulate totals
    total_defensive_in_frame += defensive_in_frame
    total_offensive_in_frame += offensive_in_frame
    total_defensive_in_box += defensive_in_box
    total_offensive_in_box += offensive_in_box
    total_defensive_in_goal_area += defensive_in_goal_area
    total_offensive_in_goal_area += offensive_in_goal_area

avg_defensive_in_frame = total_defensive_in_frame / total_corners
avg_offensive_in_frame = total_offensive_in_frame / total_corners
avg_defensive_in_box = total_defensive_in_box / total_corners
avg_offensive_in_box = total_offensive_in_box / total_corners
avg_defensive_in_goal_area = total_defensive_in_goal_area / total_corners
avg_offensive_in_goal_area = total_offensive_in_goal_area / total_corners

print(f'Total number of corners: {total_corners}')

print(f"Average Defensive Players in Frame: {avg_defensive_in_frame}")
print(f"Average Offensive Players in Frame: {avg_offensive_in_frame}")
print(f"Average Defensive Players in Box: {avg_defensive_in_box}")
print(f"Average Offensive Players in Box: {avg_offensive_in_box}")
print(f"Average Defensive Players in Goal Area: {avg_defensive_in_goal_area}")
print(f"Average Offensive Players in Goal Area: {avg_offensive_in_goal_area}")
