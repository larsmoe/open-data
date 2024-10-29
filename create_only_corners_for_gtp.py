import json

file_path = 'only_corner_events.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(len(data))
    corner_events = []

    # Loop through each event in the file
    for i, event in enumerate(data):
        # Check if the event is related to a corner based on pass, shot, or play_pattern
        corner_events.append(event)
        if i == 1000:
            break

# Save the corner events to a new JSON file
with open('only_corner_events_gpt.json', 'w') as outfile:
    json.dump(corner_events, outfile, indent=4)