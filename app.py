from flask import Flask, request, jsonify
from flask_cors import CORS
from suggestion_engine import generate_suggestions
from auto_report import auto_generate_and_get_reports_from_token
import os


 
app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "server is healthy"}), 200


@app.route('/suggestions', methods=['POST'])
def suggest():
    data = request.json
    # print(f"[INFO] Received data for suggestions: {data}")

    if not data or 'expenses' not in data:
        return jsonify({"error": "Invalid input, 'expenses' key is required"}), 400

    expenses = data.get('expenses', [])
    suggestions = generate_suggestions(expenses)
    print(f"[INFO] Generated suggestions: {suggestions}")
    
    return jsonify(suggestions)



@app.route('/reports', methods=['GET'])
def get_reports():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.replace("Bearer ", "")
    express_url = os.getenv("EXPRESS_API", "http://localhost:5000")

    reports, status = auto_generate_and_get_reports_from_token(token, express_url)
    return jsonify(reports), status


if __name__ == '__main__':
    app.run(port=5001)
