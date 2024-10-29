import json
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# Load the corner events data
with open('corner_pass_events.json', 'r') as f:
    corners = json.load(f)

# Initialize lists to hold normalized end locations for each group
end_locations = {
    'left_right_foot': {'x': [], 'y': []},
    'left_left_foot': {'x': [], 'y': []},
    'right_right_foot': {'x': [], 'y': []},
    'right_left_foot': {'x': [], 'y': []}
}

# Loop through each corner pass and separate them by foot and side
for event in corners:
    # Get the starting location of the corner
    start_x, start_y = event['location']

    # Identify the foot used
    foot_used = event['pass']['body_part']['name'].lower() if 'body_part' in event['pass'] else 'unknown'

    # Corners from the left (either from 0,0 or 120,80)
    if  (start_x > 119 and start_y > 79):
        # Normalize coordinates if from 120,80
        end_x = 120 - event['pass']['end_location'][0]
        end_y = 80 - event['pass']['end_location'][1]

        if foot_used == 'right foot':
            end_locations['left_right_foot']['x'].append(end_x)
            end_locations['left_right_foot']['y'].append(end_y)
        elif foot_used == 'left foot':
            end_locations['left_left_foot']['x'].append(end_x)
            end_locations['left_left_foot']['y'].append(end_y)

    # Corners from the right (either from 0,80 or 120,0)
    elif (start_x > 119 and start_y < 1):
        end_x = event['pass']['end_location'][0]
        end_y =  event['pass']['end_location'][1]
        if foot_used == 'right foot':
            end_locations['right_right_foot']['x'].append(end_x)
            end_locations['right_right_foot']['y'].append(end_y)
        elif foot_used == 'left foot':
            end_locations['right_left_foot']['x'].append(end_x)
            end_locations['right_left_foot']['y'].append(end_y)


# Helper function to create heatmaps
def plot_heatmap(end_x, end_y, title, ax):
    heatmap_data, xedges, yedges = np.histogram2d(end_x, end_y, bins=[120, 80], range=[[0, 120], [0, 80]])
    pos = ax.imshow(heatmap_data.T, extent=[0, 120, 0, 80], origin='lower', cmap='coolwarm', alpha=0.6)
    ax.set_title(title)
    return pos


# Create the pitch
pitch = Pitch(pitch_type='statsbomb', pitch_length=120, pitch_width=80)

# Set up the figure for 4 subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Heatmaps of Corner End Locations by Foot and Side')

# Plot heatmaps for each side and foot
pos1 = plot_heatmap(end_locations['left_right_foot']['x'], end_locations['left_right_foot']['y'], 'Left Corners (Right Foot)', axs[0, 0])
pos2 = plot_heatmap(end_locations['left_left_foot']['x'], end_locations['left_left_foot']['y'], 'Left Corners (Left Foot)', axs[0, 1])
pos3 = plot_heatmap(end_locations['right_right_foot']['x'], end_locations['right_right_foot']['y'], 'Right Corners (Right Foot)', axs[1, 0])
pos4 = plot_heatmap(end_locations['right_left_foot']['x'], end_locations['right_left_foot']['y'], 'Right Corners (Left Foot)', axs[1, 1])

# Adjust the layout to place the color bar outside the subplots
plt.subplots_adjust(right=0.85)
cbar_ax = fig.add_axes([0.88, 0.15, 0.03, 0.7])  # Color bar axis to the right of the plots
cbar = fig.colorbar(pos1, cax=cbar_ax)
cbar.set_label('Corner End Frequency')

# Draw the soccer field on each subplot
for ax in axs.flat:
    pitch.draw(ax=ax)

plt.tight_layout(rect=[0, 0, 0.85, 1])  # Adjust layout to leave space for the color bar
plt.show()