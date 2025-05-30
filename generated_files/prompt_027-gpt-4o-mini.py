import pandas as pd
import json

class DataTransformer:
    def __init__(self, data):
        self.data = data

    def apply_rule(self, rule):
        if 'operation' in rule:
            if rule['operation'] == 'drop':
                self.data.drop(columns=rule['columns'], inplace=True, errors='ignore')
            elif rule['operation'] == 'rename':
                self.data.rename(columns=rule['mapping'], inplace=True)
            elif rule['operation'] == 'filter':
                condition = rule['condition']
                self.data = self.data.query(condition)
            elif rule['operation'] == 'add_column':
                new_col_name = rule['new_column']
                self.data[new_col_name] = eval(rule['expression'])
    
    def transform(self, rules):
        for rule in rules:
            self.apply_rule(rule)
        return self.data

def load_data(file_path):
    return pd.read_csv(file_path)

def main():
    # User uploads a dataset
    file_path = input("Enter the path to your CSV dataset: ")
    data = load_data(file_path)
    
    # User defines transformation rules
    rules_input = input("Enter transformation rules in JSON format: ")
    rules = json.loads(rules_input)
    
    transformer = DataTransformer(data)
    transformed_data = transformer.transform(rules)
    
    # Output the transformed dataset
    print("Transformed Dataset:")
    print(transformed_data)

if __name__ == "__main__":
    main()
