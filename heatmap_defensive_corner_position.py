import json
import numpy as np
import mplsoccer
import matplotlib.pyplot as plt

# File path for the consolidated corner data
corners_file = 'all_360_corners.json'

# Load the consolidated corner events data
with open(corners_file, 'r') as file:
    corners_data = json.load(file)

# Initialize lists to store defensive player positions
# Initialize lists to store defensive player positions
defensive_positions_left_x = []
defensive_positions_left_y = []
defensive_positions_right_x = []
defensive_positions_right_y = []

# Loop through the corner events and collect defensive player positions
for event in corners_data:
    freeze_frame = event.get('freeze_frame', [])
    corner_location = event.get('location', [])

    # Determine the side of the corner and collect defensive player positions
    if corner_location == [120, 0.1]:  # Right corner
        for player in freeze_frame:
            if not player['teammate']:  # Defensive player
                defensive_positions_right_x.append(player['location'][0])
                defensive_positions_right_y.append(player['location'][1])

    elif corner_location == [120, 80]:  # Left corner
        for player in freeze_frame:
            if not player['teammate']:  # Defensive player
                defensive_positions_left_x.append(player['location'][0])
                defensive_positions_left_y.append(player['location'][1])

# Create heatmap data using numpy's 2D histogram for left corners
print(len(defensive_positions_left_x))
left_heatmap_data, xedges_left, yedges_left = np.histogram2d(defensive_positions_left_x, defensive_positions_left_y,
                                                             bins=[120, 80], range=[[0, 120], [0, 80]])

# Create heatmap data using numpy's 2D histogram for right corners
right_heatmap_data, xedges_right, yedges_right = np.histogram2d(defensive_positions_right_x,
                                                                defensive_positions_right_y, bins=[120, 80],
                                                                range=[[0, 120], [0, 80]])

# Initialize the pitch for plotting
pitch = mplsoccer.Pitch(pitch_type='statsbomb', pitch_length=120, pitch_width=80)  # Create the soccer field

# Plot heatmap for corners taken from the left
fig_left, ax_left = pitch.draw(figsize=(10, 6))  # Create the figure and axis for the pitch
pos_left = ax_left.imshow(left_heatmap_data.T, extent=[0, 120, 0, 80], origin='lower', cmap='Reds', alpha=0.6)
ax_left.set_title("Heatmap of Defensive Player Positions\nCorners taken from the left", fontsize=16)
plt.colorbar(pos_left, ax=ax_left)

# Plot heatmap for corners taken from the right
fig_right, ax_right = pitch.draw(figsize=(10, 6))  # Create the figure and axis for the pitch
pos_right = ax_right.imshow(right_heatmap_data.T, extent=[0, 120, 0, 80], origin='lower', cmap='Reds', alpha=0.6)
ax_right.set_title("Heatmap of Defensive Player Positions\nCorners taken from the right", fontsize=16)
plt.colorbar(pos_right, ax=ax_right)
plt.show()