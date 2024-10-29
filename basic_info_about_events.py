import os
import json
from collections import defaultdict

# Initialize dictionary to store event types and their occurrences
event_types = defaultdict(lambda: {'name': '', 'count': 0})

# Function to process a single JSON file and update the event types count
def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        print(file_path)
        data = json.load(f)
        for event in data:
            event_id = event['type']['id']
            if event['id'] == "ccc1ea05-ddf4-4e70-8e4e-86ce6077b916":
                print(event.keys())
                print(event)
                print(json.dumps(event, indent=4, sort_keys=True))
                break
            event_name = event['type']['name']
            event_types[event_id]['name'] = event_name
            event_types[event_id]['count'] += 1
            #print(event_name)

# Main function to loop through all files in the folder
def process_event_files(folder_path):
    for subdir, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(subdir, file)
                process_json_file(file_path)
            break

# Specify the path to the folder containing the event JSON files
folder_path = 'data/events'
process_event_files(folder_path)

# Print the resulting dictionary with event types and their counts
for event_id, info in event_types.items():
    print(f"Event ID: {event_id}, Name: {info['name']}, Count: {info['count']}")

# If you want to save the result as a JSON file
with open('event_types_summary.json', 'w') as outfile:
    json.dump(event_types, outfile, indent=4)

print(f"\nSummary saved to 'event_types_summary.json'")