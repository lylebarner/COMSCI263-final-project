from flask import Flask, request, jsonify

app = Flask(__name__)

# Example database records
records = [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25},
    {"id": 3, "name": "Charlie", "age": 35}
]

def filter_records(filters):
    filtered = records
    for key, value in filters.items():
        filtered = [record for record in filtered if record.get(key) == value]
    return filtered

@app.route('/query', methods=['POST'])
def query_records():
    filters = request.json
    results = filter_records(filters)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)