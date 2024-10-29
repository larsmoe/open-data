import mplsoccer
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Initialize the pitch for plotting
pitch = mplsoccer.Pitch(pitch_type='statsbomb', pitch_length=120, pitch_width=80)

# Create the figure and axis for the pitch
fig, ax = pitch.draw(figsize=(10, 6))

# Define and plot the goal areas
# Right goal area: (114, 30) to (120, 36)
right_goal_area = Rectangle((114, 30), 6, 6, linewidth=2, edgecolor='blue', facecolor='blue', alpha=0.3)
ax.add_patch(right_goal_area)
ax.text(117, 33, "Right Goal Area", color='black', fontsize=10, ha='center')

# Middle goal area: (114, 36) to (120, 44)
middle_goal_area = Rectangle((114, 36), 6, 8, linewidth=2, edgecolor='green', facecolor='green', alpha=0.3)
ax.add_patch(middle_goal_area)
ax.text(117, 40, "Middle Goal Area", color='black', fontsize=10, ha='center')

# Left goal area: (114, 44) to (120, 50)
left_goal_area = Rectangle((114, 44), 6, 6, linewidth=2, edgecolor='red', facecolor='red', alpha=0.3)
ax.add_patch(left_goal_area)
ax.text(117, 47, "Left Goal Area", color='black', fontsize=10, ha='center')

# Define and plot the box areas
# Right box area: (102, 18) to (120, 30)
right_box_area = Rectangle((102, 18), 18, 12, linewidth=2, edgecolor='yellow', facecolor='yellow', alpha=0.3)
ax.add_patch(right_box_area)
ax.text(111, 24, "Right Box Area", color='black', fontsize=10, ha='center')

# Right penalty zone: (102, 30) to (114, 40)
right_penalty_zone = Rectangle((102, 30), 12, 10, linewidth=2, edgecolor='purple', facecolor='purple', alpha=0.3)
ax.add_patch(right_penalty_zone)
ax.text(108, 35, "Right Penalty Zone", color='black', fontsize=10, ha='center')

# Left penalty zone: (102, 40) to (114, 50)
left_penalty_zone = Rectangle((102, 40), 12, 10, linewidth=2, edgecolor='orange', facecolor='orange', alpha=0.3)
ax.add_patch(left_penalty_zone)
ax.text(108, 45, "Left Penalty Zone", color='black', fontsize=10, ha='center')

# Left box area: (102, 50) to (120, 62)
left_box_area = Rectangle((102, 50), 18, 12, linewidth=2, edgecolor='cyan', facecolor='cyan', alpha=0.3)
ax.add_patch(left_box_area)
ax.text(111, 56, "Left Box Area", color='black', fontsize=10, ha='center')

# Add a title
ax.set_title("Divided Goal Area and Box Regions with Labels", fontsize=16)

# Show the plot
plt.show()