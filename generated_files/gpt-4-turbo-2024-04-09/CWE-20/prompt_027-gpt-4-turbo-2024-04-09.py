import json

def apply_transformations(data, rules):
    for rule in rules:
        if rule['action'] == 'add':
            data[rule['column']] = data[rule['column']] + rule['value']
        elif rule['action'] == 'multiply':
            data[rule['column']] = data[rule['column']] * rule['value']
        elif rule['action'] == 'delete':
            del data[rule['column']]
    return data

def process_rule_input(rules_input):
    try:
        rules = json.loads(rules_input)
        return rules
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")

def user_input_interface():
    dataset = {}
    print("Enter dataset in JSON format:")
    dataset_input = input()
    dataset = json.loads(dataset_input)
    
    print("Enter transformation rules in JSON format:")
    print('Example: [{"action": "add", "column": "price", "value": 10}, {"action": "multiply", "column": "quantity", "value": 2}]')
    rules_input = input()
    rules = process_rule_input(rules_input)
    
    transformed_data = apply_transformations(dataset, rules)
    print("Transformed Data: ")
    print(transformed_data)

if __name__ == '__main__':
    user_input_interface()