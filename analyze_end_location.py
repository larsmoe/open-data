import json
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# Load the passes data (assuming passes represent corner events)
with open('corner_pass_events.json', 'r') as f:
    passes = json.load(f)

# Initialize lists to hold normalized end locations of the corners
end_locations_x = []
end_locations_y = []
left_end_locations_x = []
left_end_locations_y = []
right_end_locations_x = []
right_end_locations_y = []

# Loop through each corner pass and normalize the end location based on the corner side
counter_left = 0
counter_right = 0
for event in passes:
    # Get the starting location of the corner
    start_x, start_y = event['location']

    # Identify if it's a left or right corner and normalize
    if (start_x < 1 and start_y < 1) or (start_x > 119 and start_y > 79):
        # Corner from the left (either from 0,0 or 120,80)
        counter_left +=1
        if start_x > 119 and start_y > 79:
            # Transform for corners taken from 120,80
            end_x = 120 - event['pass']['end_location'][0]
            end_y = 80 - event['pass']['end_location'][1]
        else:
            # No transformation needed for corners taken from 0,0
            end_x = event['pass']['end_location'][0]
            end_y = event['pass']['end_location'][1]
        left_end_locations_x.append(end_x)
        left_end_locations_y.append(end_y)
    elif (start_x < 1 and start_y > 79) or (start_x > 119 and start_y < 1):
        # Corner from the right (either from 0,80 or 120,0)
        counter_right +=1
        if (start_x < 1 and start_y > 79):
            end_x = 120 - event['pass']['end_location'][0]
            end_y = 80 - event['pass']['end_location'][1]
            print(end_x, end_y)
            break
        else:
            # No transformation needed for corners taken from 0,0
            end_x = event['pass']['end_location'][0]
            end_y = event['pass']['end_location'][1]
        right_end_locations_x.append(end_x)
        right_end_locations_y.append(end_y)

    # Add the normalized end location to the lists
    end_locations_x.append(end_x)
    end_locations_y.append(end_y)

print(len(end_locations_x))
print(np.max(end_locations_x))
print(counter_left, counter_right)

# Create the heatmap data using numpy's 2D histogram
heatmap_data, xedges, yedges = np.histogram2d(end_locations_x, end_locations_y, bins=[120, 80], range=[[0, 120], [0, 80]])
# Create heatmap data using numpy's 2D histogram for left corners
left_heatmap_data, xedges_left, yedges_left = np.histogram2d(left_end_locations_x, left_end_locations_y, bins=[120, 80], range=[[0, 120], [0, 80]])

# Create heatmap data using numpy's 2D histogram for right corners
right_heatmap_data, xedges_right, yedges_right = np.histogram2d(right_end_locations_x, right_end_locations_y, bins=[120, 80], range=[[0, 120], [0, 80]])

# Plot using mplsoccer
pitch = Pitch(pitch_type='statsbomb', pitch_length=120, pitch_width=80)  # Create the soccer field
fig, ax = pitch.draw(figsize=(10, 6))  # Create the figure and axis for the pitch

# Plot the heatmap on top of the field
pos = ax.imshow(heatmap_data.T, extent=[0, 120, 0, 80], origin='lower', cmap='bwr', alpha=0.6)

# Add color bar
cbar = fig.colorbar(pos, ax=ax)
cbar.set_label('Corner End Frequency')

plt.title('Heatmap of Corner End Locations')
# Plot heatmap for left corners
fig_left, ax_left = pitch.draw(figsize=(10, 6))
pos_left = ax_left.imshow(left_heatmap_data.T, extent=[0, 120, 0, 80], origin='lower', cmap='bwr', alpha=0.6)
cbar_left = fig_left.colorbar(pos_left, ax=ax_left)
cbar_left.set_label('Corner End Frequency (Left Corners)')
plt.title('Heatmap of Corner End Locations (Left Corners)')

# Plot heatmap for right corners
fig_right, ax_right = pitch.draw(figsize=(10, 6))
pos_right = ax_right.imshow(right_heatmap_data.T, extent=[0, 120, 0, 80], origin='lower', cmap='bwr', alpha=0.6)
cbar_right = fig_right.colorbar(pos_right, ax=ax_right)
cbar_right.set_label('Corner End Frequency (Right Corners)')
plt.title('Heatmap of Corner End Locations (Right Corners)')
plt.show()