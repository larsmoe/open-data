import os
import json


# Function to process a single JSON file and extract relevant corner events
def process_json_file(file_path, match_id):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        corner_events = []

        # Loop through each event in the file
        for event in data:
            # Check if the event is related to a corner based on pass, shot, or play_pattern
            if 'pass' in event and 'type' in event['pass'] and event['pass']['type']['id'] == 61:  # Corner Pass
                event['match_id'] = match_id
                corner_events.append(event)
            elif 'shot' in event and 'type' in event['shot'] and event['shot']['type']['id'] == 61:  # Corner Shot
                event['match_id'] = match_id
                corner_events.append(event)
            elif 'play_pattern' in event and event['play_pattern']['id'] == 2:  # Play Pattern from Corner
                event['match_id'] = match_id
                corner_events.append(event)

        return corner_events


# Main function to loop through all files and collect corner events
def process_event_files(folder_path):
    all_corner_events = []

    # Loop through each file in the directory
    for subdir, _, files in os.walk(folder_path):
        for i, file in enumerate(files):
            if file.endswith('.json'):
                if i%100 == 0:
                    print(i, 100*(i/3434))
                match_id = os.path.splitext(file)[0]  # Extract match ID from filename
                file_path = os.path.join(subdir, file)
                corner_events = process_json_file(file_path, match_id)
                all_corner_events.extend(corner_events)  # Collect all corner events

    return all_corner_events


# Specify the path to the folder containing the event JSON files
folder_path = 'data/events'

# Process all files and get corner events
all_corner_events = process_event_files(folder_path)

# Save the corner events to a new JSON file
with open('corner_events.json', 'w') as outfile:
    json.dump(all_corner_events, outfile, indent=4)

total_events = len(all_corner_events)
print(f"Total number of corner-related events saved: {total_events}")

print(f"All corner-related events saved to 'corner_events.json'")