import json

class RecordService:
    def __init__(self, records):
        self.records = records

    def query_records(self, filters):
        results = []
        for record in self.records:
            is_match = True
            for key, value in filters.items():
                if key not in record or record[key] != value:
                    is_match = False
                    break
            if is_match:
                results.append(record)
        return results

# Example usage
records = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Alice"}
]

service = RecordService(records)

filters = {"name": "Alice"}
result = service.query_records(filters)
print(result)