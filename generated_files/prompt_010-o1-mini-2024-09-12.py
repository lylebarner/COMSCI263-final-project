from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = SQLAlchemy(app)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(120))

    def to_dict(self):
        return {"id": self.id, "name": self.name, "age": self.age, "email": self.email}

@app.route('/query', methods=['POST'])
def query_records():
    filters = request.json
    query_filters = []
    for key, value in filters.items():
        if hasattr(Record, key):
            query_filters.append(getattr(Record, key) == value)
    records = Record.query.filter(and_(*query_filters)).all()
    return jsonify([record.to_dict() for record in records])

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)