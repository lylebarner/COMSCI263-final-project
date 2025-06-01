import json
import yaml
import argparse

def parse_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def parse_yaml_file(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def process_data(data):
    if "action" in data:
        action = data["action"]
        if action == "print":
            print_data(data["content"])
        elif action == "calculate":
            calculate(data["expression"])

def print_data(content):
    print(content)

def calculate(expression):
    try:
        result = eval(expression)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error calculating expression: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Process JSON or YAML files.")
    parser.add_argument("file", help="The JSON or YAML file to be processed.")
    parser.add_argument("-t", "--type", choices=['json', 'yaml'], required=True, help="The type of file: json or yaml")
    
    args = parser.parse_args()
    file_type = args.type
    file_path = args.file

    try:
        if file_type == 'json':
            data = parse_json_file(file_path)
        elif file_type == 'yaml':
            data = parse_yaml_file(file_path)
        process_data(data)
    except FileNotFoundError:
        print(f"File {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()