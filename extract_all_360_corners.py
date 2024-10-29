import json
import os

# File paths and directories
corners_file = 'corner_pass_events.json'
matches_dir = 'data/three-sixty'
output_file = 'all_360_corners.json'

# Load the corners data
with open(corners_file, 'r') as file:
    corners_data = json.load(file)

# Create a mapping of corner event IDs to their locations
corner_locations = {corner_event['id']: corner_event['location'] for corner_event in corners_data}
corner_pass_info = {corner_event['id']: corner_event['pass'] for corner_event in corners_data}

# Initialize a list to store all corner events with match IDs
all_corner_events = [] # To store the number of corners per match
corner_count = 0

# Loop through all match files in the directory
for filename in os.listdir(matches_dir):
    print(corner_count)
    if filename.endswith('.json'):
        match_id = filename.replace('.json', '')  # Extract match_id from filename
        match_file_path = os.path.join(matches_dir, filename)

        with open(match_file_path, 'r', encoding='utf-8') as match_file:
            try:
                events_data = json.load(match_file)
            except json.decoder.JSONDecodeError:
                print('Error')
                print(match_file_path)
                continue

            # Loop through events to find matches with corner events
            for event in events_data:
                event_id = event['event_uuid']
                if event_id in corner_locations:
                    # Increment the corner count for this match
                    corner_count += 1

                    # If it's a corner, append the event data with the match ID and corner location
                    corner_event_data = {
                        'match_id': match_id,
                        'event_id': event_id,
                        'freeze_frame': event.get('freeze_frame', []),
                        'location': corner_locations[event_id],  # Get the location from corners_data
                        'pass': corner_pass_info[event_id]
                    }
                    all_corner_events.append(corner_event_data)

# Write all corner events and corner counts to a new file

with open(output_file, 'w') as outfile:
    json.dump(all_corner_events, outfile, indent=4)

print(f"All corner events have been successfully extracted and saved to {output_file}.")
print(f"Corners total: {corner_count}.")