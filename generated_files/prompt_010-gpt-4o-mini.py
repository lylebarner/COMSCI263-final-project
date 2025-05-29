from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = SQLAlchemy(app)

# Example model
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'email': self.email
        }

db.create_all()

@app.route('/records', methods=['POST'])
def get_records():
    filter_criteria = request.json
    query = Record.query

    if 'name' in filter_criteria:
        query = query.filter(Record.name.like(f"%{filter_criteria['name']}%"))
    if 'age' in filter_criteria:
        query = query.filter(Record.age == filter_criteria['age'])
    if 'email' in filter_criteria:
        query = query.filter(Record.email.like(f"%{filter_criteria['email']}%"))

    results = query.all()
    return jsonify([record.serialize() for record in results])

if __name__ == '__main__':
    app.run(debug=True)