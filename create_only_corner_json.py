import os
import json

file_path = 'corner_events.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    corner_events = []

    # Loop through each event in the file
    for i, event in enumerate(data):
        # Check if the event is related to a corner based on pass, shot, or play_pattern
        if 'pass' in event and 'type' in event['pass'] and event['pass']['type']['id'] == 61:  # Corner Pass
            corner_events.append(event)
        elif 'shot' in event and 'type' in event['shot'] and event['shot']['type']['id'] == 61:  # Corner Shot
            corner_events.append(event)

# Save the corner events to a new JSON file
with open('only_corner_events.json', 'w') as outfile:
    json.dump(corner_events, outfile, indent=4)