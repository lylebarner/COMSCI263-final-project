import argparse
import json
import yaml

# Parse command-line arguments
parser = argparse.ArgumentParser(description='JSON/YAML parser tool')
parser.add_argument('file_path', type=str, help='Path to the input JSON/YAML file')
args = parser.parse_args()

# Read input file
with open(args.file_path, 'r') as file:
    file_content = file.read()

# Check if the input file is in JSON format
try:
    input_data = json.loads(file_content)
    print('Input file is in JSON format')
except json.JSONDecodeError:
    # Check if the input file is in YAML format
    try:
        input_data = yaml.safe_load(file_content)
        print('Input file is in YAML format')
    except yaml.YAMLError as e:
        print('Error: Input file is neither in JSON nor YAML format')
        raise e

# Perform actions based on the contents of the input data
# Add your code here to define actions based on the parsed input data.