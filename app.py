from flask import Flask, request, jsonify

app = Flask(__name__)
llm_message = ""

@app.route('/api/message', methods=['POST'])
def get_data():
    llm_message = request.get_json()
    
    if not llm_message or 'message' not in llm_message:
        return jsonify({"error": "No message provided!"}), 400
        
    return jsonify({"status": "Message received!"}), 201


if __name__ == '__main__':
    app.run(debug=True)
