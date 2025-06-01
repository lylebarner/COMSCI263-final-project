from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/get-file', methods=['POST'])
def get_file_contents():
    data = request.json
    filename = data.get('filename')
    if filename and os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                contents = file.read()
                return jsonify({
                    "status": "success",
                    "filename": filename,
                    "contents": contents
                })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "File does not exist or filename not provided"}), 404

if __name__ == '__main__':
    app.run(debug=True)