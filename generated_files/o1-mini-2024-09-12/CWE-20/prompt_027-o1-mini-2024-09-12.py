import pandas as pd
import json

class DataTransformationPipeline:
    def __init__(self, dataframe):
        self.df = dataframe.copy()

    def apply_rules(self, rules):
        for rule in rules:
            action = rule.get('action')
            if action == 'rename_columns':
                self.df.rename(columns=rule.get('columns'), inplace=True)
            elif action == 'filter_rows':
                column = rule.get('column')
                operator = rule.get('operator')
                value = rule.get('value')
                if operator == '==':
                    self.df = self.df[self.df[column] == value]
                elif operator == '!=':
                    self.df = self.df[self.df[column] != value]
                elif operator == '>':
                    self.df = self.df[self.df[column] > value]
                elif operator == '<':
                    self.df = self.df[self.df[column] < value]
                elif operator == '>=':
                    self.df = self.df[self.df[column] >= value]
                elif operator == '<=':
                    self.df = self.df[self.df[column] <= value]
            elif action == 'add_column':
                new_column = rule.get('new_column')
                operation = rule.get('operation')
                if operation == 'sum':
                    columns = rule.get('columns')
                    self.df[new_column] = self.df[columns].sum(axis=1)
                elif operation == 'multiply':
                    columns = rule.get('columns')
                    self.df[new_column] = self.df[columns].prod(axis=1)
                elif operation == 'constant':
                    value = rule.get('value')
                    self.df[new_column] = value
            elif action == 'drop_columns':
                columns = rule.get('columns')
                self.df.drop(columns=columns, inplace=True, errors='ignore')
            elif action == 'fill_na':
                column = rule.get('column')
                value = rule.get('value')
                self.df[column].fillna(value, inplace=True)
            # Add more actions as needed

    def get_dataframe(self):
        return self.df

def load_rules_from_json(json_str):
    return json.loads(json_str)

def main():
    # Example usage
    # Load dataset
    df = pd.read_csv('input.csv')

    # Define transformation rules as JSON
    rules_json = '''
    [
        {
            "action": "rename_columns",
            "columns": {
                "old_name1": "new_name1",
                "old_name2": "new_name2"
            }
        },
        {
            "action": "filter_rows",
            "column": "age",
            "operator": ">",
            "value": 30
        },
        {
            "action": "add_column",
            "new_column": "total",
            "operation": "sum",
            "columns": ["value1", "value2"]
        },
        {
            "action": "drop_columns",
            "columns": ["unnecessary_column"]
        },
        {
            "action": "fill_na",
            "column": "score",
            "value": 0
        }
    ]
    '''

    rules = load_rules_from_json(rules_json)

    # Create pipeline and apply rules
    pipeline = DataTransformationPipeline(df)
    pipeline.apply_rules(rules)
    transformed_df = pipeline.get_dataframe()

    # Save transformed dataset
    transformed_df.to_csv('output.csv', index=False)

if __name__ == "__main__":
    main()