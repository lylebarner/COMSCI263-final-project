import json
import pandas as pd

def apply_rule(df, rule):
    action = rule.get('action')
    column = rule.get('column')
    if action == "rename_column":
        df = df.rename(columns={column: rule['new_name']})
    elif action == "drop_column":
        df = df.drop(columns=[column])
    elif action == "fillna":
        df[column] = df[column].fillna(rule.get('value'))
    elif action == "apply_map":
        df[column] = df[column].map(rule['mapping'])
    elif action == "filter_rows":
        expr = rule['expression']  # Example: 'age > 30'
        df = df.query(expr)
    elif action == "convert_dtype":
        df[column] = df[column].astype(rule['dtype'])
    elif action == "add_column":
        df[rule['new_column']] = eval(rule['expression'], {}, {'df': df})
    # Add more actions as needed
    return df

def transform_dataset(df, rules):
    for rule in rules:
        df = apply_rule(df, rule)
    return df

def main():
    # 1. Load user dataset
    file_path = input("Enter path to your CSV dataset: ")
    df = pd.read_csv(file_path)

    # 2. Get transformation rules from user
    print("Enter your transformation rules as JSON (one line):")
    rules_json = input()
    rules = json.loads(rules_json)

    # 3. Apply rules
    df_transformed = transform_dataset(df, rules)

    # 4. Save or preview results
    out_path = input("Enter path for output CSV (or leave blank to preview): ")
    if out_path.strip():
        df_transformed.to_csv(out_path, index=False)
        print(f"Transformed dataset saved to {out_path}")
    else:
        print("Preview of transformed data:")
        print(df_transformed.head())

if __name__ == "__main__":
    main()
