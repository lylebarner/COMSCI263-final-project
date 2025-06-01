from flask import Flask, request, jsonify

app = Flask(__name__)

# Example in-memory data store
RECORDS = [
    {"id": 1, "name": "Alice", "age": 30, "location": "NY"},
    {"id": 2, "name": "Bob", "age": 25, "location": "CA"},
    {"id": 3, "name": "Carol", "age": 27, "location": "NY"},
    {"id": 4, "name": "Dave", "age": 22, "location": "TX"}
]

def match_filter(record, filter_criteria):
    for key, value in filter_criteria.items():
        if isinstance(value, dict):  # Advanced filtering
            for op, v in value.items():
                if op == "$gt" and record.get(key, None) <= v:
                    return False
                if op == "$lt" and record.get(key, None) >= v:
                    return False
                if op == "$eq" and record.get(key, None) != v:
                    return False
                if op == "$ne" and record.get(key, None) == v:
                    return False
        else:
            if record.get(key, None) != value:
                return False
    return True

@app.route("/query", methods=["POST"])
def query_records():
    filter_criteria = request.get_json(force=True)
    result = [record for record in RECORDS if match_filter(record, filter_criteria)]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)