import json
import yaml
import argparse
import sys

def parse_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def perform_action(data):
    # Example action: print values
    for key, value in data.items():
        print(f"{key}: {value}")

def main():
    parser = argparse.ArgumentParser(description="Parse JSON or YAML input files and perform actions.")
    parser.add_argument('file', type=str, help='Path to the input JSON or YAML file')

    args = parser.parse_args()

    file_path = args.file
    if not file_path.endswith(('.json', '.yaml', '.yml')):
        print("Error: The file must be a JSON or YAML format.")
        sys.exit(1)

    try:
        if file_path.endswith('.json'):
            data = parse_json(file_path)
        else:
            data = parse_yaml(file_path)

        perform_action(data)
    except Exception as e:
        print(f"Error reading the file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()