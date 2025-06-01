import argparse
import sys
import json

try:
    import yaml
except ImportError:
    yaml = None

def parse_input(file_path):
    with open(file_path, 'r') as f:
        first_line = f.readline()
        f.seek(0)
        if file_path.endswith('.json') or first_line.strip().startswith('{'):
            try:
                return json.load(f)
            except Exception as e:
                sys.exit(f"Error parsing JSON: {e}")
        elif file_path.endswith(('.yml', '.yaml')) or first_line.strip().startswith(('---', '-')):
            if not yaml:
                sys.exit("PyYAML not installed. Please install it to process YAML files.")
            try:
                return yaml.safe_load(f)
            except Exception as e:
                sys.exit(f"Error parsing YAML: {e}")
        else:
            sys.exit("Unknown file type or file content does not look like JSON or YAML.")

def perform_actions(data):
    # Example action: Just demonstrate how data is handled
    # Replace, extend, or map this logic as needed
    if isinstance(data, dict):
        if 'action' in data:
            if data['action'] == 'greet' and 'name' in data:
                print(f"Hello, {data['name']}!")
            elif data['action'] == 'sum' and 'numbers' in data and isinstance(data['numbers'], list):
                print(f"Sum: {sum(data['numbers'])}")
            else:
                print(f"Unknown action or missing parameters: {data}")
        else:
            print(f"Data received (no 'action' key): {data}")
    elif isinstance(data, list):
        print("List of items in data:")
        for item in data:
            print(f"- {item}")
    else:
        print(f"Unknown data format: {data}")

def main():
    parser = argparse.ArgumentParser(
        description="Command-line tool to process JSON or YAML input files."
    )
    parser.add_argument('input_file', help='Path to the JSON or YAML input file')
    args = parser.parse_args()

    data = parse_input(args.input_file)
    perform_actions(data)

if __name__ == '__main__':
    main()
