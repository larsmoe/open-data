import json

# Load the data from the provided file
with open('only_corner_events.json', 'r') as f:
    corner_events = json.load(f)

# Filter only the shot events
shot_events = [event for event in corner_events if event['type']['name'] == 'Shot']
pass_events = [event for event in corner_events if event['type']['name'] == 'Pass']

# Save the shot events to a new JSON file
with open('corner_shot_events.json', 'w') as outfile:
    json.dump(shot_events, outfile, indent=4)
with open('corner_pass_events.json', 'w') as outfile:
    json.dump(pass_events, outfile, indent=4)

print(f"Total number of corner shots: {len(shot_events)}")
print("All corner shot events have been saved to 'corner_shot_events.json'")