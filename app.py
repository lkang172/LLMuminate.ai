from flask import Flask, request, jsonify
from extract_keywords import extract_k
from extract_quotes import extract_q
import json

app = Flask(__name__)
llm_message = ""

@app.route('/api/message', methods=['POST'])
def get_data():
    llm_message = request.get_json()
    
    if not llm_message or 'message' not in llm_message:
        return jsonify({"error": "No message provided!"}), 400
    
    llm_message = llm_message['message']
    
    keywords = extract_k(llm_message)
    fact_check = extract_q(keywords, llm_message)

    if isinstance(fact_check, str):
        fact_check = json.loads(fact_check)

    return jsonify(fact_check), 201

if __name__ == '__main__':
    app.run(debug=True)
