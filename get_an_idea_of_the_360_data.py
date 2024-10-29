import json
import mplsoccer
import matplotlib.pyplot as plt

# Load the files
file_path_events = 'data/three-sixty/3788741.json'
file_path_corners = 'corner_pass_events.json'

with open(file_path_events, 'r') as file:
    events_data = json.load(file)

with open(file_path_corners, 'r') as file:
    corners_data = json.load(file)

# Let's create a mapping of corner events by id for faster lookup
corner_ids = {corner_event['id'] for corner_event in corners_data}

# Find the first matching event in events_data
matched_event = None
for event in events_data:
    if event['event_uuid'] in corner_ids:
        matched_event = event
        break

# If a match was found, let's extract player positions and plot them
if matched_event:
    freeze_frame = matched_event['freeze_frame']

    # Initialize the pitch
    pitch = mplsoccer.Pitch(pitch_type='statsbomb', half=True)
    fig, ax = pitch.draw(figsize=(10, 8))

    # Plot each player based on their location
    for player in freeze_frame:
        x, y = player['location']
        print(x, y)
        color = 'blue' if player['teammate'] else 'red'
        marker = 'o' if not player['keeper'] else 's'
        size = 100 if player['actor'] else 50
        ax.scatter(x, y, color=color, marker=marker, s=size)

    plt.title(f"Player positions during the first matched corner (ID: {matched_event['event_uuid']})")
    plt.show()
else:
    print("No matching corner events found.")