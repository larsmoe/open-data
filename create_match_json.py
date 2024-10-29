import os
import json


# Function to process each JSON file and extract the necessary data
def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        match_data = {}
        for match in data:
            match_id = match['match_id']
            match_info = {
                'match_date': match['match_date'],
                'season_id': match['season']['season_id'],
                'season_name': match['season']['season_name'],
                "competition_id": match['competition']['competition_id'],
                "country_name": match['competition']['country_name'],
                "competition_name": match['competition']['competition_name'],
                "gender": match['home_team']['home_team_gender']
            }
            match_data[match_id] = match_info
        return match_data


# Main function to iterate over folders and files
def process_matches_folder(folder_path):
    all_matches = {}

    # Walk through each subfolder and file in the main folder
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(subdir, file)
                match_data = process_json_file(file_path)
                all_matches.update(match_data)

    # Save all matches to a single JSON file
    output_file = 'all_matches.json'
    with open(output_file, 'w') as outfile:
        json.dump(all_matches, outfile, indent=4)
    print(f'All matches have been saved to {output_file}')


# Specify the path to the folder containing the subfolders and JSON files
folder_path = 'data/matches'
process_matches_folder(folder_path)