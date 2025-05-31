#!/usr/bin/env python3

import argparse
import json
import yaml
import os
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process JSON or YAML input files and perform actions based on their contents.')
    parser.add_argument('input_file', help='Path to the JSON or YAML input file')
    return parser.parse_args()

def load_file(file_path):
    _, ext = os.path.splitext(file_path)
    try:
        with open(file_path, 'r') as f:
            if ext.lower() in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            elif ext.lower() == '.json':
                return json.load(f)
            else:
                # Try JSON first, then YAML
                try:
                    f.seek(0)
                    return json.load(f)
                except json.JSONDecodeError:
                    f.seek(0)
                    return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

def perform_actions(data):
    if isinstance(data, dict):
        for key, value in data.items():
            action = ACTIONS.get(key)
            if action:
                action(value)
            else:
                print(f"No action defined for key: {key}")
    else:
        print("Input data is not a dictionary.")

# Define actions based on keys
def action_print(value):
    print(f"Print action: {value}")

def action_sum(value):
    if isinstance(value, list):
        total = sum(value)
        print(f"Sum action: {total}")
    else:
        print("Sum action expects a list of numbers.")

def action_echo(value):
    print(f"Echo action: {value}")

ACTIONS = {
    'print': action_print,
    'sum': action_sum,
    'echo': action_echo,
}

def main():
    args = parse_arguments()
    data = load_file(args.input_file)
    perform_actions(data)

if __name__ == '__main__':
    main()